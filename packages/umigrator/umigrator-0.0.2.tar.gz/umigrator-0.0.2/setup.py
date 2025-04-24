from setuptools import setup, find_packages

setup(
    name="umigrator",
    version="0.0.2",
    description="Custom Django migration and model manager for precise schema control.",
    author="umakaran",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=4.2",  # or Django>=5.0 if using db_default
    ],
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
