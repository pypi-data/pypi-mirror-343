from setuptools import setup, find_packages

setup(
    name="impactmap",
    version="0.0.3",
    description="Official Python SDK for the ImpactMap API",
    author="ImpactMap.io",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1"
    ],
    python_requires=">=3.7",
    url="https://github.com/impactmap-io/impactmap-python",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
