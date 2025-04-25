from setuptools import setup, find_packages

setup(
    name="color_ur_text",
    version="0.1.2.4",  # Increment this version number for each new release
    author="Basit Ahmad Ganie",
    author_email="basitahmed1412@gmail.com",
    description="A module for printing colored text to terminal/console in Python, Now with more methods and colors like printing animations.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/basitganie/colored_text",  # Replace with your actual repository URL
    packages=find_packages(where="src"),  # This will find the package in the 'src' directory
    package_dir={"": "src"},  # Tell setuptools that packages are under the 'src' directory
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
