from setuptools import setup, find_packages

# Read the long description from README.md
try:
    with open('README.md', 'r') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "A small package to list directory tree structures."

setup(
    name="folder_tree_lister",           # Package name
    version="0.0.5",                     # Initial version
    author="Dikshyant",                  # Your name
    author_email="dikshyant180@gmail.com",  # Your email
    description="/README.md",  # Short description
    long_description=long_description,   # Long description from README
    long_description_content_type="text/markdown",  # Set the format of the long description
    url="https://github.com/yourusername/folder_tree_lister",  # Add your repository URL here
    packages=find_packages(),            # Automatically discover packages
    classifiers=[                        # Metadata to help PyPI users discover the package
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",              # Minimum Python version required
)
