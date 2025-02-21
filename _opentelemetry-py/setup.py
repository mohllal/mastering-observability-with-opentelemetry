from setuptools import setup, find_packages


def read_requirements(filename):
    with open(filename, encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]


setup(
    name="opentelemetry_py",
    version="1.0.0",
    packages=find_packages(),
    install_requires=read_requirements('requirements.txt'),
)
