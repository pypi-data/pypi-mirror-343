from setuptools import setup, find_packages

setup(
    name="hp7.1wp1",
    version="0.0.1",
    description="A very hp package",
    author="compinfun",
    author_email="compinfun@gmail.com",
    packages=find_packages(),
    package_data={
        "hp7.1wp1": ["data/*.wav"],
    },
    include_package_data=True,
)
