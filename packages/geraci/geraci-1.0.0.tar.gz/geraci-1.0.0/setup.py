from setuptools import setup, find_packages

setup(
    name="geraci",
    version="1.0.0",
    author="Rpx",
    author_email="cubyc.ro@gmail.com",
    description="A library for managing files and directories easily and efficiently.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[],
    include_package_data=True,
    license="MIT",
    license_files=[],
)
