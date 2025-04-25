from setuptools import setup, find_packages

setup(
    name='okayletsgo',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'just_playback',
    ],
    package_data={
        'okayletsgo': ['sound.mp3'],
    },
    include_package_data=True,
    description="""A simple Python package to play 'Okaaaay let's go!' through your speakers with just one line of 
    code."""
)
