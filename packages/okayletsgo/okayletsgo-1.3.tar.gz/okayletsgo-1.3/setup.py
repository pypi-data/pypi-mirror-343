from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='okayletsgo',
    version='1.3',
    packages=find_packages(),
    install_requires=[
        'just_playback',
    ],
    package_data={
        'okayletsgo': ['sound.mp3'],
    },
    include_package_data=True,
    description="""A simple Python package to play 'Okaaaay let's go!' through your speakers with just one line of code.""",
    long_description=long_description,
    long_description_content_type='text/markdown'
)
