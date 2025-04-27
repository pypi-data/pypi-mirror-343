from setuptools import setup

setup(
    name="dmrid_lookup",
    version="1.0.0",
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
)

