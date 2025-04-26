from setuptools import setup, find_packages
import pathlib

# Read the contents of your README file
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")
setup(
    name="blitzkit",
    author="Lenny Uwaeme",
    author_email="lenyeuwame@gmail.com",
    version= "0.0.10",
    description="BlitzKit is a command-line tool that helps student developers automate full-stack project setup. It generates a clean, organized folder structure with starter files to help you get started fast.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lennythecreator/BlitzKit/tree/main",
    packages=find_packages(),  # Find packages in the current directory
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    entry_points = {'console_scripts':['blitzkit=blitzkit.cli:main'] ,
    },
    install_requires=[
        'argparse',
        'pyfiglet',
    ],
)