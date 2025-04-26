from setuptools import setup, find_packages

setup(
    name="friendly-web-face",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "googletrans==4.0.0-rc1"
    ],
    author="Максим",
    description="Библиотека для перевода создания дружественного интерфейса",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MaXikme/friendly_web_face",
)
