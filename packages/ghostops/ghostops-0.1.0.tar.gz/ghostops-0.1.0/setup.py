from setuptools import setup, find_packages
from pathlib import Path

here = Path(__file__).parent

long_description = (here / "README.md").read_text(encoding="utf-8")

requirements_path = here / "requirements.txt"
if requirements_path.exists():
    install_requires = requirements_path.read_text(encoding="utf-8").splitlines()
    install_requires = [line for line in install_requires if line and not line.startswith("#")]
else:
    install_requires = []

setup(
    name="ghostops",
    version="0.1.0",
    author="Awagat Dhungana",
    author_email="4w4647@gmail.com",
    description="A powerful Command and Control Framework for penetration testing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/4w4647/ghostops",
    packages=find_packages(exclude=["tests*", "docs*", "examples*"]),
    python_requires=">=3.6",
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "ghostops=ghostops.__main__:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Security",
    ],
    license="BSD-3-Clause",
)