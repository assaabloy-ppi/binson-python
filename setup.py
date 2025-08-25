import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="binson-python",
    version="0.0.1",
    author="Simon Johansson",
    author_email="simon.johansson@assaabloy.com",
    description="A python imlementation of Binson",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/assaabloy-ppi/binson-python",
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',
)
