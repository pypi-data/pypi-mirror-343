from setuptools import setup, find_packages
import os

# Read version from package
with open(os.path.join('mintlify_changelog', '__init__.py'), 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().strip('"\'')
            break
    else:
        version = '0.0.1'

# Read long description from README
with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name="mintlify-changelog",
    version=version,
    description="AI-powered, beautiful changelog generator for git repositories",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mintlify",
    author_email="careers@mintlify.com",
    url="https://github.com/mintlify/changelog",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "mintlify-changelog=mintlify_changelog.cli:main",
        ],
    },
    install_requires=[
        "requests>=2.25.0",
        "keyring>=23.0.0",
        "markdown>=3.3.0",  # For HTML conversion
    ],
    extras_require={
        "dev": [
            "black",
            "pytest",
            "pytest-cov",
            "twine",
            "build",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Version Control :: Git",
    ],
    python_requires=">=3.7",
    keywords="changelog, git, claude, ai, mintlify, documentation",
)