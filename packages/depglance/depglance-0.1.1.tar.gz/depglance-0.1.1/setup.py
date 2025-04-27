from setuptools import setup, find_packages

# Read the README file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="depglance",
    version="0.1.1",
    author="Prajeet Singh",
    author_email="dev.prajeet2016@gmail.com",
    description="Visualize and analyze Python project dependencies with vulnerability highlights.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/devprajeet/depglance",
    project_urls={
        "Bug Tracker": "https://github.com/devprajeet/depglance/issues",
        "Source Code": "https://github.com/devprajeet/depglance",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
    packages=find_packages(),
    # package_dir={"": "src"},
    python_requires=">=3.7",
    install_requires=[
        "pyvis",
        "requests",
        "networkx",
    ],
)
