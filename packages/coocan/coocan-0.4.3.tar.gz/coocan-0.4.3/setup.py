from setuptools import setup, find_packages

setup(
    name="coocan",
    version="0.4.3",
    author="wauo",
    author_email="markadc@126.com",
    description="Air Spider Framework",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        'click>=8.0.0',
    ],
    entry_points={
        'console_scripts': [
            'cc=coocan.cmd.cli:main',
        ],
    }
)
