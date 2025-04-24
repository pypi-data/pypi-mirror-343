from setuptools import setup, find_packages

setup(
    name="djmigrator",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Django>=4.2"],
    author="Your Name",
    author_email="you@example.com",
    description="Smart Django migration manager.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/djmigrator",
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
)
