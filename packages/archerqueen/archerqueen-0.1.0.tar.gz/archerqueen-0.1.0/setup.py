from setuptools import setup, find_packages

setup(
    name="archerqueen",
    version="0.1.0",
    author="Incineroar",
    description="Nooki ezhutikoo",
    packages=find_packages(),
    install_requires=[],  # Add dependencies here if needed
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "archerqueen=archerqueen.main:main",
        ],
    },
)