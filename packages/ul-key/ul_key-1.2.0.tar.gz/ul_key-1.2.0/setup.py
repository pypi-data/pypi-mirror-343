from setuptools import setup, find_packages

setup(
    name="ul-key",
    version="1.2.0",
    author="starfal8k",
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'ulkey-encode = utils.cli:encode_cli',
            'ulkey-decode = utils.cli:decode_cli',
        ],
    },
    install_requires=[
        'click',
    ],
    description="UL-Key An indispensable assistant in data encryption.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://example.com/ulkey",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
