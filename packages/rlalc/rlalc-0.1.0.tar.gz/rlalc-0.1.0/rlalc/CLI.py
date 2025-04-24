import os.path

import questionary
import sys
import io
import shutil

import roboflow
import requests

from rlalc.ImageHandler import ImageHandler

from prompt_toolkit.styles import Style
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from enum import IntEnum
from ultralytics import YOLO

class Selections(IntEnum):
    LOGIN = 0,
    SELECT_PROJECT = 1,
    SET_TAG = 2,
    START_LABELING = 3,
    EXIT = 4

class CLI:
    def __init__(self):
        self._console = Console()

        self._menu_selections = [
            "- Login",
            "- Select Project",
            "- Set Tag",
            "- Start Labeling 🚀",
            "- Exit"
        ]

        self._style = Style.from_dict({
            'question': 'bold fg:#00ffff',
            'answer': 'bold fg:#00ff00',
            'pointer': 'fg:#ff00aa bold',
            'highlighted': 'fg:#80ef80 bold',
            'selected': 'fg:#00ee00 bold',
        })

        self._rf = roboflow.Roboflow()

        self._api_key = ""
        self._workspace = ""
        self._project = ""
        self._tag = ""

        self._source = ""

        self._greet()

    def _greet(self):
        title = "RlAlC - v0.1.0 🚀"
        text = "[yellow]Roboflow Local Auto labeling CLI[/yellow]\n\nType [green]'help'[/green] to see available commands."

        greeting = Panel(text, border_style="bright_blue", title=title)
        self._console.print(greeting)

        self._help_menu()

    def _help_menu(self):
        while True:
            choice = questionary.select(
                "🔧 Setup options",
                choices=self._menu_selections,
                style=self._style,
            ).ask()

            if choice not in self._menu_selections:
                self._console.print("[red]Invalid choice. Please try again.[/red]")
                continue

            if choice == self._menu_selections[Selections.EXIT]:
                self._console.print("[red]Exiting ...[/red]")
                break

            self._handle_command(choice)

    def _handle_command(self, choice):
        if choice == self._menu_selections[Selections.LOGIN]:
            self._login()
        elif choice == self._menu_selections[Selections.SELECT_PROJECT]:
            self._select_project()
        elif choice == self._menu_selections[Selections.SET_TAG]:
            self._set_tag()
        elif choice == self._menu_selections[Selections.START_LABELING]:
            self._start_labeling()


    def _login(self, force=False):
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            if force:
                roboflow.login(force=True)
            else:
                roboflow.login()
        except Exception as e:
            captured_output.write(f"Login failed: {str(e)}")
        finally:
            sys.stdout = sys.__stdout__

        login_message = captured_output.getvalue().strip()

        login_panel = Panel(login_message, border_style="cyan", title="Roboflow Login Status")
        self._console.print(login_panel)

        if "You are already logged into Roboflow" in login_message:
            choice = questionary.select(
                "Force a new login?",
                choices=["Yes", "No"],
                style=self._style,
            ).ask()

            if choice == "Yes":
                self._login(force=True)

        if "Login failed" not in login_message:
            self._api_key = self._rf.api_key
            self._workspace = self._rf.workspace().url

    def _select_project(self):
        panel = Panel("Select Project", border_style="cyan", title="Select Project")
        self._console.print(panel)

        if not self._workspace:
            self._console.print("[red]Please login first.[/red]")
            self._login()

        data = requests.get(f"https://api.roboflow.com/{self._workspace}?api_key={self._api_key}").json()
        projects = [project["id"] for project in data["workspace"]["projects"]]

        choice = questionary.select(
            "📽️ Select a project",
            choices=projects,
            style=self._style,
        ).ask()

        choice = str(choice)
        choice.replace(f"{self._workspace}/", "")

        self._project = choice

    def _set_tag(self):
        panel = Panel("Set Tag", border_style="cyan", title="Tag Setup")
        self._console.print(panel)

        self._tag = Prompt.ask("Enter the tag you want to use").strip()
        self._console.print(f"[green]Tag '{self._tag}' set successfully.[/green]")

    def _start_labeling(self):
        panel = Panel("Start Labeling", border_style="cyan", title="Start Labeling")
        self._console.print(panel)

        if not self._workspace:
            self._console.print("[red]Please login first.[/red]")
            self._login()

        if not self._project:
            self._console.print("[red]Please select a project first.[/red]")
            self._select_project()

        if not self._tag:
            self._console.print("[red]All images selected! Do you want to continue?[/red]")
            choice = questionary.select(
                "Continue with all images?",
                choices=["No", "Yes"],
                style=self._style,
            ).ask()

            if choice == "No":
                self._set_tag()

        self._console.print(f"[green]Starting labeling for project '{self._project}' with tag '{self._tag}'...[/green]")

        self._handler = ImageHandler(self._api_key, self._workspace, self._project)
        image_ids = self._handler.get_image_ids(self._tag)
        source_path = self._handler.download_images(image_ids)
        self._source = source_path
        self._dir_name = os.path.basename(source_path)

        inference = Panel("Running inference...", border_style="cyan", title="Inference")
        self._console.print(inference)

        choice = questionary.select(
            "Select inference method",
            choices=["Select Model", self._menu_selections[Selections.EXIT]],
            style=self._style,
        )

        if choice == self._menu_selections[Selections.EXIT]:
            self._handle_command(self._menu_selections[Selections.EXIT])

        self._set_model()

    def _set_model(self):
        path = Prompt.ask("Enter the path to the model: ").strip()

        try:
            model = YOLO(path)
            model.to('mps')
        except Exception as e:
            self._console.print(f"[red]Model loading failed: {str(e)}[/red]")
            return

        dir_name = self._dir_name
        dir_name = dir_name.replace('source_', '')

        model.predict(self._source, save_txt=True, device='mps', project=f'predictions_{dir_name}')

        self._console.print("[green]Inference completed successfully![/green]")
        self._console.print("[blue]Results saved to 'predictions' folder.[/blue]")

        output_dir = f'output_{dir_name}'
        os.makedirs(output_dir, exist_ok=True)

        shutil.move(self._source, os.path.join(output_dir, "images"))
        shutil.move(f'predictions_{dir_name}/predict/labels', os.path.join(output_dir, "labels"))

        self._handler.upload_images()