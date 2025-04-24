from setuptools import setup, find_packages

setup(
    name="barkcli",
    version="1.0.1",
    packages=find_packages(),
    py_modules=["barkcli"],
    install_requires=[
        "requests",
        "barknotificator>=1.0.0"
    ],
    entry_points={
        "console_scripts": [
            "bark=barkcli:main"
        ]
    },
    author="FalconChen",
    author_email="falcon_chen@qq.com",
    description="CLI tool for sending notifications to Bark",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
