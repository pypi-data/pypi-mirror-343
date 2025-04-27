from setuptools import setup

setup(
    name="dmrid-lookup",
    version="1.0.4",
    py_modules=["dmrid_lookup"],
    install_requires=[
        "requests",
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "dmrid_lookup=dmrid_lookup:main",
        ],
    },
    author="Mark Cohen",
    author_email="k6ef@k6ef.net",
    description="A CLI tool to lookup DMR IDs by amateur radio callsign.",
    url="https://github.com/k6ef/dmrid_lookup",  # optional
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

