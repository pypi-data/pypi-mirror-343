from setuptools import setup, find_packages

setup(
    name="Easify",  # Replace with your package name
    version="1.0.6",
    description="Prints preprocessing code for data engineering tasks",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Taksh Dhabalia",
    author_email="no@example.com",
    license="MIT",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "ass1=Easify.main:ass1",
            "ass2=Easify.main:ass2",
            "ass3=Easify.main:ass3",
            "ass4=Easify.main:ass4",
            "ass5=Easify.main:ass5",
            "ass6=Easify.main:ass6",
            "ass7=Easify.main:ass7",
            "info=Easify.main:info",


        ],
    },

    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "scikit-learn",
        "scipy"
    ],
    python_requires=">=3.6",
)
