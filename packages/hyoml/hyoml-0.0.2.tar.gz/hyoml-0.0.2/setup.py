from setuptools import setup, find_packages

setup(
    name="hyoml",
    version="0.0.2",  # Match your latest version
    description="Hyoml - Intelligent Relaxed Data Parser and Formatter",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Ahmed Daif",
    author_email="prog.ahmeddaif@gmail.com",
    license="MIT",
    url="https://github.com/progdaif/hyoml",
    packages=find_packages(where="python"),
    package_dir={"": "python"},
    python_requires=">=3.8",
    install_requires=[
        "beautifulsoup4>=4.12.2",
        "rdflib>=6.3.2",
        "requests>=2.31.0"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",  # Until you reach stable
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
        "Topic :: Utilities",
    ],
    keywords="hyoml relaxed-json yaml parser formatter data-processing",
)
