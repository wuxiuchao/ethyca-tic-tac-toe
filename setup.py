"""
Setup script for Tic-Tac-Toe package
"""
from setuptools import setup, find_packages

setup(
    name="tictactoe",
    version="1.0.0",
    description="Tic-Tac-Toe Web Service",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "Flask>=3.0.0",
        "flask-cors>=4.0.0",
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
        ]
    },
)

