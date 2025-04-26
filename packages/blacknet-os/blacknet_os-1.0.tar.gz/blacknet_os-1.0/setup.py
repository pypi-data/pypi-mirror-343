from setuptools import setup, find_packages

setup(
    name="blacknet-os",
    version="1.0",
    author="Xscripts Inc.",
    author_email="sunnyplaysyt9@gmail.com",
    description="A hacker OS terminal-based toolset with web browsing, port scanning, reverse shells, and more",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-repo",  # Replace with your GitHub repo or package page
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

