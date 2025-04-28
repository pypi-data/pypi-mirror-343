from setuptools import setup

VERSION = "0.1.0"

setup(
    name="datasette-google-analytics",
    description="Datasette plugin that adds Google Analytics tracking code to your Datasette instance",
    author="Jerry Ng",
    url="https://github.com/ngshiheng/datasette-google-analytics",
    packages=["datasette_google_analytics"],
    license="MIT",
    version=VERSION,
    py_modules=["datasette_google_analytics"],
    entry_points={"datasette": ["google_analytics = datasette_google_analytics"]},
    install_requires=["datasette>=0.54"],
    extras_require={
        "test": [
            "beautifulsoup4",
            "pytest-asyncio",
            "pytest",
            "python-semantic-release",
        ],
        "build": [
            "build",
            "twine",
        ],
    },
    python_requires=">=3.9",
)
