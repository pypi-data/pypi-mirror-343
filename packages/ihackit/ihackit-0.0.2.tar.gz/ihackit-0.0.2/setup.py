from setuptools import setup

setup(
    name="ihackit",
    version="0.0.2",
    packages=["ihackit"],
    install_requires=["requests","pycryptodomex"],
    author="Moh Iqbal Hidayat",
    author_email="iqbalmh18.dev@gmail.com",
    description="Instagram Automation, Device Customization & User-Agent Generator Library",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/ihackit",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["ihackit", "instagram", "instagram-api", "instagram-bot", "instagram-private-api"],
    python_requires=">=3.7",
)