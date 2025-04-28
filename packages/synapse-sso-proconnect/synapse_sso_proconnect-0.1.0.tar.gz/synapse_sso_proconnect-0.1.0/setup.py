from setuptools import setup, find_packages

setup(
    name="synapse-sso-proconnect",    # this must match the name on PyPI
    version="0.1.0",                   # your package version
    packages=find_packages(),
    install_requires=[                 # your dependencies
        # example: "requests", "flask", etc.
    ],
    author="JPD Tester",
    author_email="jpdtester04@email.com",
    description="A short description of what your package does",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jpd/synapse-sso-proconnect",  # if you have GitHub
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # or your license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
