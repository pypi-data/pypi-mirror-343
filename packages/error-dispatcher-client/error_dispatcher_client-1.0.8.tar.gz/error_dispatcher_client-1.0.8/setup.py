from setuptools import setup, find_packages

setup(
    name="error_dispatcher_client",
    version="1.0.8",
    description="A Python package for tracking and handling errors with support for multiple providers like Kafka and Email.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Willian Antunes",
    author_email="willian.antunes@solinftec.com",
    url="https://github.com/solinftec/error_dispatcher_client",
    packages=find_packages(),
    install_requires=[
        "flask",
        "fastapi>=0.108.0",
        "confluent-kafka",
        "discord-webhook"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
