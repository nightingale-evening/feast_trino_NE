from setuptools import setup

NAME = "feast-trino"
VERSION = "1.0.0"
DESCRIPTION = "Trino support for Feast offline store"
with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

INSTALL_REQUIRE = [
    "feast>=0.15.0,<1.0.0",
    "trino>=0.305.0,<0.400.0",
]

CI_REQUIRE = [
    "pytest==6.0.0",
    "flake8",
    "black==19.10b0",
    "isort>=5",
    "mypy==0.790",
]

setup(
    name="feast-trino",
    version=VERSION,
    author="Shopify",
    author_email="developers@shopify.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    python_requires=">=3.7.0",
    url="https://github.com/Shopify/feast-trino",
    project_urls={
        "Bug Tracker": "https://github.com/Shopify/feast-trino/issues",
    },
    license="MIT License",
    packages=["feast_trino"],
    install_requires=INSTALL_REQUIRE,
    extras_require={
        "ci": CI_REQUIRE,
    },
    keywords=("feast featurestore trino offlinestore"),
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)