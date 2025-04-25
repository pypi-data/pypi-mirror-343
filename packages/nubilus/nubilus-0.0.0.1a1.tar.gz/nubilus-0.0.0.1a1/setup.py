from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="nubilus",
    version="0.0.0.1a1",
    description="A UX-friendly AI learning framework with signal processing and multi-process support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="shyubi",
    author_email="sjslife97@gmail.com",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "numpy",
        "numba",
        "scipy",
        "wfdb",
        "matplotlib",
        "scikit-learn",
        "PyWavelets"
    ],
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License"
    ],
    keywords=["AI", "deep learning", "UX", "signal processing", "nubilus"],
)
