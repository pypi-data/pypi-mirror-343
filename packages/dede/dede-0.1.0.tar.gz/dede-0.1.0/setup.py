from setuptools import setup, find_packages

setup(
    name="dede",
    version="0.1.0",
    author="Zhiying Xu",
    author_email="xuzhiying9510@gmail.com",
    description="Decouple and Decompose: Scaling Resource Allocation through a Different Lens",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/harvard-cns/dede",
    packages=find_packages(),
    install_requires=[
        "cvxpy==1.4.0",
        "ray==2.10.0",
        "requests==2.32.3",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)