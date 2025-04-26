import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-iot-core-certificates-v3",
    "version": "0.1.0",
    "description": "CDK Construct for AWS IoT Core certificates and things",
    "license": "Apache-2.0",
    "url": "https://github.com/badmintoncryer/cdk-iot-core-certificates-v3.git",
    "long_description_content_type": "text/markdown",
    "author": "Kazuho CryerShinozuka<malaysia.cryer@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/badmintoncryer/cdk-iot-core-certificates-v3.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_iot_core_certificates_v3",
        "cdk_iot_core_certificates_v3._jsii"
    ],
    "package_data": {
        "cdk_iot_core_certificates_v3._jsii": [
            "cdk-iot-core-certificates-v3@0.1.0.jsii.tgz"
        ],
        "cdk_iot_core_certificates_v3": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.150.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.105.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard>=2.13.3,<4.3.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
