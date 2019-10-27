from setuptools import setup, find_packages

with open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name="bumpit",
    version="0.0.2",
    description="A small command line tool to bump tracked versions in your repository.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/mobiusbyte/bumpit",
    project_urls={
        "Code": "https://github.com/mobiusbyte/bumpit",
        "Issue tracker": "https://github.com/mobiusbyte/bumpit/issues",
    },
    license="MIT",
    author="Jill San Luis",
    author_email="jill@mobiusbyte.com",
    packages=find_packages(),
    entry_points={"console_scripts": ["bumpit=bumpit.console.cli:main"]},
    include_package_data=True,
    install_requires=["click", "pyyaml"],
    extras_require={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    python_requires=">=3.7",
)
