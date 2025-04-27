import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dispatchy",  # Changed to "dispatchy"
    version="0.0.1",
    author="PDX",
    author_email="valkdevice@gmail.com",
    description="A Python library for handling webhooks with ease.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.valkdevices.com",  # Keep the same URL or update as needed
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests >= 2.20.0",  #  Include requests, as Dispatchy uses it
    ],
)
