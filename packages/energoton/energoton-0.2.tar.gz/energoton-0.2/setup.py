from distutils.core import setup

from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="energoton",
    version="0.2",
    description="Automated task planning package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="IlyaFaer",
    author_email="ilya.faer.gurov@gmail.com",
    url="https://github.com/IlyaFaer/energoton_py/",
    packages=[
        "energoton",
        "energoton.base",
        "energoton.energoton",
        "energoton.planner",
        "energoton.relation",
        "energoton.work",
    ],
)
