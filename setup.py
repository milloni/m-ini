from setuptools import setup

setup(
    name = "mini",
    version = "0.1.0",
    packages = ["mini", "tests"],
    entry_points = {
        "console_scripts": [
            "mini = mini.cli:main"
        ]
    }
)
