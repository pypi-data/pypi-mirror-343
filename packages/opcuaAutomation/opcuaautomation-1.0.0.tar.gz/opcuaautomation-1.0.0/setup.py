from setuptools import setup, find_packages

setup(
    name="opcuaAutomation",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "opcua==0.98.13",
        "python-dateutil==2.9.0.post0",
        "pytz==2025.2",
        "lxml==5.3.2",
        "numpy==2.2.4",
        "matplotlib==3.10.1",
        "pillow==11.2.1",
        "six==1.17.0",
        "packaging==24.2",
        "kiwisolver==1.4.8",
        "cycler==0.12.1",
        "fonttools==4.57.0",
        "contourpy==1.3.1"
    ],
    entry_points={
        "console_scripts": [
        ],
    },
    description="An OPC UA client for automation engineers",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Raphaël Hecker",
    url="https://github.com/Raph-67/Py_Client_OPCUA_for_Automation.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
