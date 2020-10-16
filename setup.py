import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="destiny-manifest-manager-HEROICOSHM",
    version="0.0.1",
    author="Heroicos_HM",
    author_email="houghtonawe@gmail.com",
    description="A wrapper for the Destiny 2 API manifests.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url="https://github.com/HeroicosHM/DestinyManifestManager",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires = '>=3.6'
)
