from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='logview_core',
    version='1.3.0',
    packages=find_packages(),
    description="A modern Python web framework designed to simplify your development process.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Utsavch189/LogView-Main",
    author="Utsav Chatterjee",
    author_email="utsavchatterjee71@gmail.com",
    license="MIT",
    include_package_data=True,  # Ensure this is set to True
    package_data={
        "": ["*.py"],  # Adjust the pattern to match your HTML files
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests"
    ],
    entry_points={
    },
    python_requires=">=3.10",
)