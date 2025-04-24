from setuptools import setup, find_packages

setup(
    name="Easify",  # Replace with your package name
    version="1.0.4",
    description="Prints preprocessing code for data engineering tasks",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Sardar Khan",
    author_email="no@example.com",
    license="MIT",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "print_preprocessing=Easify.main:ass1",
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
