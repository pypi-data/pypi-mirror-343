import os
from setuptools import setup, find_packages

# Read the contents of README.md
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="django-dashboard-boilerplate",
    version="0.1.0",
    author="dttsi",
    author_email="dttsi@example.com",
    description="A reusable dashboard boilerplate for Django applications with modern UI and authentication",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dttsi/django-dashboard-boilerplate",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Framework :: Django :: 4.2",
    ],
    python_requires=">=3.6",
    install_requires=[
        "django>=3.2",
        "pillow>=8.0.0",  # For ImageField
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-django>=4.5.0",
            "coverage>=6.0.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "flake8>=4.0.0",
        ],
    },
)
