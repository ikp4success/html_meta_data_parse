import pathlib

from setuptools import find_packages, setup

long_description = (pathlib.Path(__file__).parent.resolve() / "README.md").read_text(
    encoding="utf-8"
)
setup(
    name="html_meta_data_parse",
    version="0.0.5",
    python_requires=">=3.6",
    packages=find_packages(exclude=["tests"]),
    package_data={},
    install_requires=["beautifulsoup4>=4.10.0", "requests>=2.22.0", "parsel>=1.6.0"],
    setup_requires=["pytest-runner"],
    tests_require=[
        "pytest==3.3.0",
        "flake8==3.6.0",
        "requests-mock==1.5.2",
        "pyflakes==2.1.1",
        "pytest-flakes==4.0.0",
    ],
    entry_points="""""",
    url="https://github.com/ikp4success/html_meta_data_parse",
    author="Immanuel George",
    license="MIT",
    description="Collects meta data from url, or html content.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    project_urls={
        "Tracker": "https://github.com/ikp4success/html_meta_data_parse/issues",
    },
)
