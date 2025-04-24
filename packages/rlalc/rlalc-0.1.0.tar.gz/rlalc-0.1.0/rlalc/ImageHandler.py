import os
import glob
import requests
import roboflow

from datetime import datetime
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn


class ImageHandler:
    def __init__(self, api_key, workspace, project):
        self._api_key = api_key
        self._workspace = workspace
        self._project_name = project
        self._timestamp = ""

        self._rf = roboflow.Roboflow(api_key=self._api_key)
        self._project = self._rf.project(self._project_name)

    def _get_safe_timestamp(self):
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    def get_image_ids(self, tag=None):
        records = []

        if tag:
            for page in self._project.search_all(in_dataset=False, tag=tag, fields=["id"]):
                records.extend(page)
        else:
            for page in self._project.search_all(in_dataset=False, fields=["id"]):
                records.extend(page)

        return [record["id"] for record in records]

    def download_images(self, image_ids):
        self._timestamp = self._get_safe_timestamp()
        date_folder = f"source_{self._timestamp}"
        os.makedirs(date_folder, exist_ok=True)

        with Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.1f}%",
            TimeRemainingColumn(),
        ) as progress:
            task = progress.add_task("Downloading images...", total=len(image_ids))

            for image_id in image_ids:
                image = self._project.image(image_id)
                image_url = image.get('urls')['original']

                response = requests.get(image_url)
                if response.status_code == 200:
                    image_path = os.path.join(date_folder, f"{image_id}.jpg")
                    with open(image_path, "wb") as f:
                        f.write(response.content)

                progress.update(task, advance=1)

        return os.path.abspath(date_folder)

    def upload_images(self):
        if not self._timestamp:
            raise RuntimeError("No timestamp set. Make sure to call download_images() first.")

        image_dir = f"output_{self._timestamp}/images"
        label_dir = f"output_{self._timestamp}/labels"
        label_paths = glob.glob(os.path.join(label_dir, "*.txt"))

        total_labels = len(label_paths)
        batch_name = self._timestamp

        with Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.1f}%",
            TimeRemainingColumn(),
        ) as progress:
            task = progress.add_task("Uploading images...", total=total_labels)

            for label_path in label_paths:
                base_name = os.path.splitext(os.path.basename(label_path))[0]
                image_path = os.path.join(image_dir, base_name + '.jpg')

                if os.path.exists(image_path):
                    try:
                        self._project.single_upload(
                            image_path=image_path,
                            annotation_path=label_path,
                            batch_name=batch_name
                        )
                        progress.update(task, advance=1)
                    except Exception as e:
                        print(f"Failed to upload {base_name}: {e}")

        print("Upload complete!")
