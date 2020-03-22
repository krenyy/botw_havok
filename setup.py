from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

setup(
    name="botw_havok",
    version="0.2.3",
    author="kreny",
    author_email="kronerm9@gmail.com",
    description="A library for converting Breath of the Wild Havok packfiles to JSON and back",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/23kreny/botw_havok",
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["colorama", "numpy"],
    entry_points={
        "console_scripts": [
            "hk_to_json = botw_havok.cli.hk_to_json:main",
            "json_to_hk = botw_havok.cli.json_to_hk:main",
        ]
    },
)
