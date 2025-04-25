from pathlib import Path
from setuptools import setup, find_packages

# Helper: read the long description from README.md
this_dir = Path(__file__).parent
long_description = (this_dir / "README.md").read_text(encoding="utf-8")

setup(
    name="rankest",                  # must be unique on PyPI
    version="0.1.0",
    description="A package for Rank Set Sampling using sum‑based ranking",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="T. Vaishnavi",
    author_email="tvaishu13@gmail.com",
    maintainer="Neha Singh",         # optional: second contributor
    # maintainer_email="neha@example.com",

    packages=find_packages(),        # automatically find rankest/ etc.
    install_requires=["pandas"],     # runtime dependencies

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
