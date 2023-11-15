from setuptools import setup

setup(
    name = "mini",
    version = "0.1.0",
    package_data = {
        "mini": ["py.typed"]
    },
    packages = ["mini", "tests"],
    entry_points = {
        "console_scripts": [
            "mini = mini.cli:main"
        ]
    }
)
