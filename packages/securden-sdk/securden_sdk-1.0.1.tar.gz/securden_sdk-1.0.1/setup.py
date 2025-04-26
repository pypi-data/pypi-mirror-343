from setuptools import setup, find_packages  # noqa: H301

NAME = "securden_sdk"
VERSION = "1.0.1"
PYTHON_REQUIRES = ">= 3.8"
REQUIRES = [
    "urllib3==2.0.2",
    "python-dateutil==2.9.0",
    "pydantic==2.10.4",
    "typing-extensions==4.12.2",
]

setup(
    name=NAME,
    version=VERSION,
    description="Using functions which use Securden APIs, developers can retrieve credentials programmatically from Securden server.",
    readme = "README.md",
    author="Securden Dev",
    author_email="devops-support@securden.com",
    url="https://www.securden.com",
    keywords=["Securden", "Securden SDK", "Credential Retrieval APIs as functions"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={"securden_sdk": ["py.typed"]},
    license="MIT",
    license_files=("LICENSE",),
    python_requires=PYTHON_REQUIRES,
)
