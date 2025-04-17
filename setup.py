from setuptools import setup, find_packages
from pathlib import Path

# Read long description from README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="customer_analytics",
    version="0.1.0",
    packages=find_packages(include=["glue_etl_pipeline", "glue_etl_pipeline.*"]),
    install_requires=[
        "boto3>=1.34.0",
        "pyspark>=3.3.0",
        "awswrangler>=3.0.0"
    ],
    author="Dipak Vaidya",
    author_email="your.email@example.com",
    description="AWS Glue ETL pipeline for customer analytics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/03dipak/glue_etl_pipeline",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    include_package_data=True,
    zip_safe=False,
)
