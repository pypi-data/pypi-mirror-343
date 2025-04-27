from setuptools import setup, find_packages

setup(
    name="project-mjolnir",
    version="2.0.0",
    author="DaveTmire85",
    description="Modular D&D 3.5e Parser and Database Builder",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "python-docx>=0.8.11",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
