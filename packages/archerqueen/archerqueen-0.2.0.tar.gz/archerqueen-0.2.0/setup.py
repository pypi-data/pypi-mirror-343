from setuptools import setup, find_packages

setup(
    name="archerqueen",
    version="0.2.0",
    author="Incineroar",
    description="Advanced data analysis toolkit",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "matplotlib",
        "scikit-learn",
        "nltk",
        "wordcloud",
        "seaborn",
        "textblob",
        "networkx",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "archerqueen=archerqueen.main:main",
            "archerqueen-nlp=archerqueen.experiment5:run",
            "archerqueen-tree=archerqueen.experiment6:run",
            "archerqueen-graph=archerqueen.experiment7:run",
            "archerqueen-cluster=archerqueen.experiment8:run",
        ],
    },
)