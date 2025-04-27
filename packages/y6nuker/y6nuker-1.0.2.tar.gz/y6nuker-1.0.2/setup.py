from setuptools import setup, find_packages

setup(
    name="y6nuker",
    version="1.0.2",  
    author="y6locc",
    description="A Python Tool to Nuke Discord Servers",
    packages=find_packages(),
    install_requires=[
        "discord.py",
        "colorama",
        "requests",
    ],
)