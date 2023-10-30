from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="WorkoutRoutineGenerator",
    version="0.9.7",
    author="Nimble Capricorn",
    author_email="nimble.capricorn@gmail.com",
    description="this package creates a workout routine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NimbleCapricorn/WorkoutRoutineGenerator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        #exact versions in the requirements.txt file
        "numpy",
        "pandas",
        "python-dateutil",
        "pytz",
        "PyYAML",
        "six",
        "tablib",
        "tzdata",
        "wcwidth",
        "XlsxWriter",

    ],
    python_requires='>=3.10',
)