from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="linkedin-games-solver",
    version="0.1.2",
    author="Zane Bookbinder",
    url="https://github.com/zanebookbinder/LinkedIn-Games-Solver",
    description="A solver for LinkedIn's puzzle games using Selenium",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "attrs",
        "certifi",
        "charset-normalizer",
        "h11",
        "idna",
        "outcome",
        "PySocks",
        "readchar",
        "rich",
        "selenium",
        "sniffio",
        "sortedcontainers",
        "trio",
        "trio-websocket",
        "typing_extensions",
        "urllib3",
        "websocket-client",
        "websockets",
        "wsproto",
    ],
    entry_points={
        "console_scripts": [
            "linkedin-solver=linkedin_games_solver.solver:main",  # CLI command
            "linkedin_games_solver=linkedin_games_solver.solver:main",  # CLI command
            "linkedin-games-solver=linkedin_games_solver.solver:main",  # CLI command
            "linkedin_solver=linkedin_games_solver.solver:main",  # CLI command
            "solver=linkedin_games_solver.solver:main",  # CLI command
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
