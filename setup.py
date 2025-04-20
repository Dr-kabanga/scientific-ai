from setuptools import setup, find_packages

# Read the content of the README file
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="scientific-Ai",
    version="1.0.0",
    author="Dr Kabanga",
    author_email="allankabanga@yahoo.com",  # Replace with your email
    description="A scientific AI project for data analysis and machine learning.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dr-kabanga/scientific-Ai",  # Replace with your repo URL
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy==1.24.3",
        "pandas==1.5.3",
        "scipy==1.10.1",
        "scikit-learn==1.2.0",
        "tensorflow==2.12.0",
        "torch==2.0.1",
        "matplotlib==3.7.1",
        "seaborn==0.12.2",
        "flask==2.3.2",
        "django==4.2.1",
        "requests==2.31.0",
        "beautifulsoup4==4.12.2",
        "pytest==7.4.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    entry_points={
        "console_scripts": [
            "scientific-ai=scientific_ai.cli:main",  # Replace with your CLI entry point
        ],
    },
)