import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ruuvitag-mqtt-publisher",
    version="0.0.1",
    author="Jaakko Vuori",
    author_email="jaakko.vuori@gmail.com",
    description="RuuviTag MQTT Publisher",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jvuori/ruuvitag-mqtt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.5",
)
