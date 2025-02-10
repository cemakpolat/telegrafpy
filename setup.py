from setuptools import setup, find_packages

setup(
    name="telegrafpy",
    version="0.1.0",
    description="A Telegraf-like tool for collecting and processing metrics.",
    author="Cem Akpolat",
    author_email="akpolatcem@gmail.com",
    packages=find_packages(),
    install_requires=[
        "paho-mqtt",  # MQTT dependency
        "toml",       # TOML configuration parsing
    ],
    entry_points={
        "console_scripts": [
            "telegrafpy=telegrafpy:main",  # Makes `telegrafpy` command available
        ],
    },
    python_requires=">=3.6",
)