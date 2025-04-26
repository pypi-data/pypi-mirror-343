r'''
# AWS IoT Core Thing with Certificate v3 construct

This is a CDK construct that creates an AWS IoT Core Thing with a certificate and policy using [aws-sdk-js-v3](https://github.com/aws/aws-sdk-js-v3).

![elements](./images/iot.png)

Cloudformation does not support creating a certificate for an IoT Thing, so this construct uses the AWS SDK to create a certificate and attach it to the Thing.

This construct is a modified version of this excellent [construct (cdk-iot-core-certificate)](https://github.com/devops-at-home/cdk-iot-core-certificates) to work with aws-sdk-js-v3.

[![View on Construct Hub](https://constructs.dev/badge?package=cdk-iot-core-certificates-v3)](https://constructs.dev/packages/cdk-iot-core-certificates-v3)
[![Open in Visual Studio Code](https://img.shields.io/static/v1?logo=visualstudiocode&label=&message=Open%20in%20Visual%20Studio%20Code&labelColor=2c2c32&color=007acc&logoColor=007acc)](https://open.vscode.dev/badmintoncryer/cdk-iot-core-certificates-v3)
[![npm version](https://badge.fury.io/js/cdk-iot-core-certificates-v3.svg)](https://badge.fury.io/js/cdk-iot-core-certificates-v3)
[![Build Status](https://github.com/badmintoncryer/cdk-iot-core-certificates-v3/actions/workflows/build.yml/badge.svg)](https://github.com/badmintoncryer/cdk-iot-core-certificates-v3/actions/workflows/build.yml)
[![Release Status](https://github.com/badmintoncryer/cdk-iot-core-certificates-v3/actions/workflows/release.yml/badge.svg)](https://github.com/badmintoncryer/cdk-iot-core-certificates-v3/actions/workflows/release.yml)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
![npm downloads](https://img.shields.io/npm/dt/cdk-iot-core-certificates-v3?label=npm&color=blueviolet)

## Installation

```bash
npm i cdk-iot-core-certificates-v3
```

## Usage

```python
import * as s3 from 'aws-cdk-lib/aws-s3';
import { ThingWithCert } from 'cdk-iot-core-certificates-v3';

declare const saveFileBucket: s3.IBucket;

const { thingArn, certId, certPem, privKey } = new ThingWithCert(this, 'MyThing', {
  // The name of the thing
  thingName: 'MyThing',
  // Whether to save the certificate and private key to the SSM Parameter Store
  saveToParamStore: true,
  // The prefix to use for the SSM Parameter Store parameters
  paramPrefix: 'test',
  // The bucket to save the certificate and private key to
  // Both files are saved at `{thingName}/{thingName}.private.key` and `{thingName}/{thingName}.cert.pem`
  // If not provided, the certificate and private key will not be saved
  saveFileBucket,
});
```

If you want to create multiple things and save certificates and private keys to the same bucket, you should not use `saveFileBucket` prop and save them at once by `BucketDeployment` construct.

This is because the each `saveFileBucket` prop will share a custom resource for each thing, which will cause the deployment to fail.

```python
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as s3deploy from 'aws-cdk-lib/aws-s3-deployment';
import { ThingWithCert } from 'cdk-iot-core-certificates-v3';

const thingNames = ['Thing1', 'Thing2', 'Thing3'];
const certBucket = new s3.Bucket(this, "CertBucket");
const sources: s3deploy.ISource[] = [];

thingNames.forEach((thingName, index) => {
  const { certPem, privKey } = new ThingWithCert(this, `Thing${index}`, {
    thingName,
    saveToParamStore: true,
  });
  sources.push(
    s3deploy.Source.data(`${thingName}/${thingName}.cert.pem`, certPem),
    s3deploy.Source.data(`${thingName}/${thingName}.private.key`, privKey)
  );
});

// Deploy the certificate and private key to the S3 bucket at once
new s3deploy.BucketDeployment(this, "DeployCerts", {
  sources,
  destinationBucket: certBucket,
});
```
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import constructs as _constructs_77d1e7e8


class ThingWithCert(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-iot-core-certificates-v3.ThingWithCert",
):
    '''A CDK Construct for creating an AWS IoT Core thing with a certificate.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        thing_name: builtins.str,
        param_prefix: typing.Optional[builtins.str] = None,
        save_file_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        save_to_param_store: typing.Optional[builtins.bool] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param thing_name: The name of the thing.
        :param param_prefix: The prefix for the parameter store path.
        :param save_file_bucket: The bucket to save the certificate and private key files. Default: - do not save the files
        :param save_to_param_store: Whether to save the certificate and private key to AWS Systems Manager Parameter Store.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a2892446dd7ea3ccfba34288bf29693eeeb61459a404c23794634d362a94189)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ThingWithCertProps(
            thing_name=thing_name,
            param_prefix=param_prefix,
            save_file_bucket=save_file_bucket,
            save_to_param_store=save_to_param_store,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="certId")
    def cert_id(self) -> builtins.str:
        '''The ID of the certificate.'''
        return typing.cast(builtins.str, jsii.get(self, "certId"))

    @builtins.property
    @jsii.member(jsii_name="certPem")
    def cert_pem(self) -> builtins.str:
        '''The certificate PEM.'''
        return typing.cast(builtins.str, jsii.get(self, "certPem"))

    @builtins.property
    @jsii.member(jsii_name="privKey")
    def priv_key(self) -> builtins.str:
        '''The private key.'''
        return typing.cast(builtins.str, jsii.get(self, "privKey"))

    @builtins.property
    @jsii.member(jsii_name="thingArn")
    def thing_arn(self) -> builtins.str:
        '''The ARN of the thing.'''
        return typing.cast(builtins.str, jsii.get(self, "thingArn"))


@jsii.data_type(
    jsii_type="cdk-iot-core-certificates-v3.ThingWithCertProps",
    jsii_struct_bases=[_aws_cdk_ceddda9d.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "thing_name": "thingName",
        "param_prefix": "paramPrefix",
        "save_file_bucket": "saveFileBucket",
        "save_to_param_store": "saveToParamStore",
    },
)
class ThingWithCertProps(_aws_cdk_ceddda9d.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        thing_name: builtins.str,
        param_prefix: typing.Optional[builtins.str] = None,
        save_file_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        save_to_param_store: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Properties of ThingWithCert construct.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param thing_name: The name of the thing.
        :param param_prefix: The prefix for the parameter store path.
        :param save_file_bucket: The bucket to save the certificate and private key files. Default: - do not save the files
        :param save_to_param_store: Whether to save the certificate and private key to AWS Systems Manager Parameter Store.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85446f1b57787250078dc42ab739c5a41dc29c3d08150dd7f39d1f27f991a883)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument thing_name", value=thing_name, expected_type=type_hints["thing_name"])
            check_type(argname="argument param_prefix", value=param_prefix, expected_type=type_hints["param_prefix"])
            check_type(argname="argument save_file_bucket", value=save_file_bucket, expected_type=type_hints["save_file_bucket"])
            check_type(argname="argument save_to_param_store", value=save_to_param_store, expected_type=type_hints["save_to_param_store"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "thing_name": thing_name,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if param_prefix is not None:
            self._values["param_prefix"] = param_prefix
        if save_file_bucket is not None:
            self._values["save_file_bucket"] = save_file_bucket
        if save_to_param_store is not None:
            self._values["save_to_param_store"] = save_to_param_store

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def thing_name(self) -> builtins.str:
        '''The name of the thing.'''
        result = self._values.get("thing_name")
        assert result is not None, "Required property 'thing_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def param_prefix(self) -> typing.Optional[builtins.str]:
        '''The prefix for the parameter store path.'''
        result = self._values.get("param_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def save_file_bucket(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket]:
        '''The bucket to save the certificate and private key files.

        :default: - do not save the files
        '''
        result = self._values.get("save_file_bucket")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket], result)

    @builtins.property
    def save_to_param_store(self) -> typing.Optional[builtins.bool]:
        '''Whether to save the certificate and private key to AWS Systems Manager Parameter Store.'''
        result = self._values.get("save_to_param_store")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ThingWithCertProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ThingWithCert",
    "ThingWithCertProps",
]

publication.publish()

def _typecheckingstub__8a2892446dd7ea3ccfba34288bf29693eeeb61459a404c23794634d362a94189(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    thing_name: builtins.str,
    param_prefix: typing.Optional[builtins.str] = None,
    save_file_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    save_to_param_store: typing.Optional[builtins.bool] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85446f1b57787250078dc42ab739c5a41dc29c3d08150dd7f39d1f27f991a883(
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    thing_name: builtins.str,
    param_prefix: typing.Optional[builtins.str] = None,
    save_file_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    save_to_param_store: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass
