from setuptools import setup, find_packages

setup(
    name="tria_hr_data_gatherer",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
)