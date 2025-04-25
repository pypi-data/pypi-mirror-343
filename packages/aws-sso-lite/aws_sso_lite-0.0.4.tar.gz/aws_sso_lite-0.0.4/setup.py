from setuptools import setup, find_packages

setup(
    name="aws-sso-lite",
    version="0.0.4",
    author="Jun Ke",
    author_email="kejun91@gmail.com",
    description="A lightweight package to do aws sso without aws cli",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kejun91/aws-sso-lite",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)