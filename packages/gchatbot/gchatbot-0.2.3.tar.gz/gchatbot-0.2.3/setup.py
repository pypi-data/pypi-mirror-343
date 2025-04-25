from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gchatbot",
    version="0.2.3",
    author="João Matheus & Guilherme Fialho",
    author_email="guilhermec.fialho@gmail.com",
    description="Biblioteca Python para criar bots para o Google Chat",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/guilhermecf10/gchatbot",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "flask>=2.0.0",
        "google-auth>=1.0.0",
        "google-api-python-client>=1.12.0",
        "google-apps-chat>=0.0.0",
        "protobuf>=3.0.0"
    ],
)
