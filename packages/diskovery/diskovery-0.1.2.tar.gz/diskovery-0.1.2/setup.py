from setuptools import setup, find_packages
import pathlib

setup(
    name="diskovery",
    version="0.1.2",
    author="Simmi Thapad, Vrinda Abrol",
    description="DISKOVERY: Disk Forensics Tool for Data Categorization & Keyword Filtering",
    long_description=(pathlib.Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/simmithapad/DISKOVERY",
    packages=find_packages(include=["diskovery", "diskovery.*"]),
    install_requires=pathlib.Path("requirements.txt").read_text().splitlines(),
    entry_points={
        "console_scripts": [
            "diskovery = diskovery.main:main"
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    
    license="MIT",
    python_requires='>=3.7',
    include_package_data=True,
)

# from setuptools import setup, find_packages

# setup(
#     name="disko",
#     version="1.0.0",
#     packages=find_packages(include=["stages", "utils"]),  # include your folders as packages
#     py_modules=["main"],  # since main.py is a standalone module
#     install_requires=open("requirements.txt").read().splitlines(),
#     entry_points={
#         "console_scripts": [
#             "disko = main:main",  # refers to main() in main.py
#         ],
#     },
#     author="Simmi Thapad, Vrinda Abrol",
#     description="DISKO - Disk Operation Tool for Data Categorization and Keyword Filtering",
#     license="MIT",
# )
