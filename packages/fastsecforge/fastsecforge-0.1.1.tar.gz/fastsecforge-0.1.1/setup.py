from setuptools import setup, find_packages
from pathlib import Path

# Read README.md for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="fastsecforge",
    version="0.1.1",
    packages=find_packages(),
    package_data={
        'fastsecforge': [
            'templates/project_template/**/*',
            'templates/project_template/**/.*'
        ]
    },
    include_package_data=True,
    install_requires=[
        "fastapi",
        "uvicorn",
        "python-dotenv",
        "sqlalchemy",
        "pydantic>=2.0.0",
        "pydantic-settings>=2.0.0",
        "passlib[bcrypt]",
        "python-jose[cryptography]",
        "motor",
        "typer",
        "python-multipart"
    ],
    entry_points={
        "console_scripts": [
            "fastsecforge=fastsecforge.cli:app",
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
)
