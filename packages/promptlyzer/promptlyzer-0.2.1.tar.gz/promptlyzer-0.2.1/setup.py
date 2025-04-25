from setuptools import setup, find_packages
setup(
    name="promptlyzer",
    version="0.2.1",
    description="A client library for the Promptlyzer API with automated prompt updates",
    author="Promptlyzer Team",
    author_email="info@promptlyzer.com",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    entry_points={
        "console_scripts": [
            "promptlyzer=promptlyzer.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
) 