from setuptools import setup, find_packages

setup(
    name='rlalc',
    version='0.1.0',
    description='Roboflow Local Auto Labeling CLI',
    author='Jan Schlegel',
    python_requires='>=3.12',
    packages=find_packages(),
    install_requires=[
        'questionary>=2.1.0',
        'rich==14.0.0',
        'roboflow==1.1.61',
        'ultralytics>=8.3.113',
    ],
    entry_points={
        'console_scripts': [
            'rlalc = rlalc.main:main',  # assumes rlalc/CLI.py has a main() function
        ],
    },
)
