from setuptools import setup, find_packages

setup(
    name="axios-py",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],
    python_requires=">=3.7",
    author="Avijit Sen",
    author_email="avijitsen@example.com",
    description="A Python implementation of the Axios HTTP client with custom HTTP client",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/avijitsen/axios-py",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 