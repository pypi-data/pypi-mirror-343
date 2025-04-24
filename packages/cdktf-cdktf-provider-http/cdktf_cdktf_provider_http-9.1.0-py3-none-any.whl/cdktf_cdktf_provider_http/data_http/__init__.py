r'''
# `data_http`

Refer to the Terraform Registry for docs: [`data_http`](https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http).
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

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class DataHttp(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-http.dataHttp.DataHttp",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http http}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        url: builtins.str,
        ca_cert_pem: typing.Optional[builtins.str] = None,
        client_cert_pem: typing.Optional[builtins.str] = None,
        client_key_pem: typing.Optional[builtins.str] = None,
        insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        method: typing.Optional[builtins.str] = None,
        request_body: typing.Optional[builtins.str] = None,
        request_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        request_timeout_ms: typing.Optional[jsii.Number] = None,
        retry: typing.Optional[typing.Union["DataHttpRetry", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http http} Data Source.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param url: The URL for the request. Supported schemes are ``http`` and ``https``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#url DataHttp#url}
        :param ca_cert_pem: Certificate Authority (CA) in `PEM (RFC 1421) <https://datatracker.ietf.org/doc/html/rfc1421>`_ format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#ca_cert_pem DataHttp#ca_cert_pem}
        :param client_cert_pem: Client certificate in `PEM (RFC 1421) <https://datatracker.ietf.org/doc/html/rfc1421>`_ format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#client_cert_pem DataHttp#client_cert_pem}
        :param client_key_pem: Client key in `PEM (RFC 1421) <https://datatracker.ietf.org/doc/html/rfc1421>`_ format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#client_key_pem DataHttp#client_key_pem}
        :param insecure: Disables verification of the server's certificate chain and hostname. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#insecure DataHttp#insecure}
        :param method: The HTTP Method for the request. Allowed methods are a subset of methods defined in `RFC7231 <https://datatracker.ietf.org/doc/html/rfc7231#section-4.3>`_ namely, ``GET``, ``HEAD``, and ``POST``. ``POST`` support is only intended for read-only URLs, such as submitting a search. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#method DataHttp#method}
        :param request_body: The request body as a string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#request_body DataHttp#request_body}
        :param request_headers: A map of request header field names and values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#request_headers DataHttp#request_headers}
        :param request_timeout_ms: The request timeout in milliseconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#request_timeout_ms DataHttp#request_timeout_ms}
        :param retry: retry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#retry DataHttp#retry}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6cd955bd349cdf3bff4e55c988ca69502aeda8b1ad29c58e5fc66c185056a1f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DataHttpConfig(
            url=url,
            ca_cert_pem=ca_cert_pem,
            client_cert_pem=client_cert_pem,
            client_key_pem=client_key_pem,
            insecure=insecure,
            method=method,
            request_body=request_body,
            request_headers=request_headers,
            request_timeout_ms=request_timeout_ms,
            retry=retry,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a DataHttp resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataHttp to import.
        :param import_from_id: The id of the existing DataHttp that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataHttp to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61a149b03a57fdba51f40235c91954dba6a70c08100210b3f6415f2a72abd1a1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRetry")
    def put_retry(
        self,
        *,
        attempts: typing.Optional[jsii.Number] = None,
        max_delay_ms: typing.Optional[jsii.Number] = None,
        min_delay_ms: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param attempts: The number of times the request is to be retried. For example, if 2 is specified, the request will be tried a maximum of 3 times. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#attempts DataHttp#attempts}
        :param max_delay_ms: The maximum delay between retry requests in milliseconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#max_delay_ms DataHttp#max_delay_ms}
        :param min_delay_ms: The minimum delay between retry requests in milliseconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#min_delay_ms DataHttp#min_delay_ms}
        '''
        value = DataHttpRetry(
            attempts=attempts, max_delay_ms=max_delay_ms, min_delay_ms=min_delay_ms
        )

        return typing.cast(None, jsii.invoke(self, "putRetry", [value]))

    @jsii.member(jsii_name="resetCaCertPem")
    def reset_ca_cert_pem(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaCertPem", []))

    @jsii.member(jsii_name="resetClientCertPem")
    def reset_client_cert_pem(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertPem", []))

    @jsii.member(jsii_name="resetClientKeyPem")
    def reset_client_key_pem(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientKeyPem", []))

    @jsii.member(jsii_name="resetInsecure")
    def reset_insecure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsecure", []))

    @jsii.member(jsii_name="resetMethod")
    def reset_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethod", []))

    @jsii.member(jsii_name="resetRequestBody")
    def reset_request_body(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestBody", []))

    @jsii.member(jsii_name="resetRequestHeaders")
    def reset_request_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestHeaders", []))

    @jsii.member(jsii_name="resetRequestTimeoutMs")
    def reset_request_timeout_ms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestTimeoutMs", []))

    @jsii.member(jsii_name="resetRetry")
    def reset_retry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetry", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="body")
    def body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "body"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="responseBody")
    def response_body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseBody"))

    @builtins.property
    @jsii.member(jsii_name="responseBodyBase64")
    def response_body_base64(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseBodyBase64"))

    @builtins.property
    @jsii.member(jsii_name="responseHeaders")
    def response_headers(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "responseHeaders"))

    @builtins.property
    @jsii.member(jsii_name="retry")
    def retry(self) -> "DataHttpRetryOutputReference":
        return typing.cast("DataHttpRetryOutputReference", jsii.get(self, "retry"))

    @builtins.property
    @jsii.member(jsii_name="statusCode")
    def status_code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "statusCode"))

    @builtins.property
    @jsii.member(jsii_name="caCertPemInput")
    def ca_cert_pem_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "caCertPemInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertPemInput")
    def client_cert_pem_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertPemInput"))

    @builtins.property
    @jsii.member(jsii_name="clientKeyPemInput")
    def client_key_pem_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientKeyPemInput"))

    @builtins.property
    @jsii.member(jsii_name="insecureInput")
    def insecure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "insecureInput"))

    @builtins.property
    @jsii.member(jsii_name="methodInput")
    def method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "methodInput"))

    @builtins.property
    @jsii.member(jsii_name="requestBodyInput")
    def request_body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestBodyInput"))

    @builtins.property
    @jsii.member(jsii_name="requestHeadersInput")
    def request_headers_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "requestHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="requestTimeoutMsInput")
    def request_timeout_ms_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "requestTimeoutMsInput"))

    @builtins.property
    @jsii.member(jsii_name="retryInput")
    def retry_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataHttpRetry"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataHttpRetry"]], jsii.get(self, "retryInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="caCertPem")
    def ca_cert_pem(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "caCertPem"))

    @ca_cert_pem.setter
    def ca_cert_pem(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a9976926007362727ba46d39d34cc37325fb0abf65b12fa7408881586c95e41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caCertPem", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCertPem")
    def client_cert_pem(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertPem"))

    @client_cert_pem.setter
    def client_cert_pem(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d19afdc64ff831a5029bd1d31f9e5d74134eb61d20a6b84d20f24c08bce16e8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertPem", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientKeyPem")
    def client_key_pem(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientKeyPem"))

    @client_key_pem.setter
    def client_key_pem(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9597d6e2e2c8828af78c93d228daf35b79cca01a09bedad65ee76cbe7b4dc5a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientKeyPem", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="insecure")
    def insecure(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "insecure"))

    @insecure.setter
    def insecure(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b102819c1c00055ec6c4e6009490d1ea76febc24ba3788f0dccbe68472caa22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "method"))

    @method.setter
    def method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb75bbe2280973db0e399bbcb80f72879e613a8852dd8816be6e56ee4d97707f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestBody")
    def request_body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestBody"))

    @request_body.setter
    def request_body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d01263d0beceb77a3aaa9f3dc2f952559e4dc223f6412bdd77cc04338609870)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestBody", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestHeaders")
    def request_headers(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "requestHeaders"))

    @request_headers.setter
    def request_headers(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a74bd45d9b8a30578befabcf666ca96bd1f9bef3b6e84638b0934128d782b51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestTimeoutMs")
    def request_timeout_ms(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "requestTimeoutMs"))

    @request_timeout_ms.setter
    def request_timeout_ms(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56342ca3a5f8a383c7aa7363c40000689eb017e1d4a08f440bf27cac06150376)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestTimeoutMs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63c7570b908cd9916d86ef50e54da516dfc1d30d4f00a51c428bab8efd6bef04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-http.dataHttp.DataHttpConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "url": "url",
        "ca_cert_pem": "caCertPem",
        "client_cert_pem": "clientCertPem",
        "client_key_pem": "clientKeyPem",
        "insecure": "insecure",
        "method": "method",
        "request_body": "requestBody",
        "request_headers": "requestHeaders",
        "request_timeout_ms": "requestTimeoutMs",
        "retry": "retry",
    },
)
class DataHttpConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        url: builtins.str,
        ca_cert_pem: typing.Optional[builtins.str] = None,
        client_cert_pem: typing.Optional[builtins.str] = None,
        client_key_pem: typing.Optional[builtins.str] = None,
        insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        method: typing.Optional[builtins.str] = None,
        request_body: typing.Optional[builtins.str] = None,
        request_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        request_timeout_ms: typing.Optional[jsii.Number] = None,
        retry: typing.Optional[typing.Union["DataHttpRetry", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param url: The URL for the request. Supported schemes are ``http`` and ``https``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#url DataHttp#url}
        :param ca_cert_pem: Certificate Authority (CA) in `PEM (RFC 1421) <https://datatracker.ietf.org/doc/html/rfc1421>`_ format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#ca_cert_pem DataHttp#ca_cert_pem}
        :param client_cert_pem: Client certificate in `PEM (RFC 1421) <https://datatracker.ietf.org/doc/html/rfc1421>`_ format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#client_cert_pem DataHttp#client_cert_pem}
        :param client_key_pem: Client key in `PEM (RFC 1421) <https://datatracker.ietf.org/doc/html/rfc1421>`_ format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#client_key_pem DataHttp#client_key_pem}
        :param insecure: Disables verification of the server's certificate chain and hostname. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#insecure DataHttp#insecure}
        :param method: The HTTP Method for the request. Allowed methods are a subset of methods defined in `RFC7231 <https://datatracker.ietf.org/doc/html/rfc7231#section-4.3>`_ namely, ``GET``, ``HEAD``, and ``POST``. ``POST`` support is only intended for read-only URLs, such as submitting a search. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#method DataHttp#method}
        :param request_body: The request body as a string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#request_body DataHttp#request_body}
        :param request_headers: A map of request header field names and values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#request_headers DataHttp#request_headers}
        :param request_timeout_ms: The request timeout in milliseconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#request_timeout_ms DataHttp#request_timeout_ms}
        :param retry: retry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#retry DataHttp#retry}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(retry, dict):
            retry = DataHttpRetry(**retry)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee2b6a3664a80e642a2ef1d255302a3f3dc3d391999cb8f3d6103cac8420d573)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument ca_cert_pem", value=ca_cert_pem, expected_type=type_hints["ca_cert_pem"])
            check_type(argname="argument client_cert_pem", value=client_cert_pem, expected_type=type_hints["client_cert_pem"])
            check_type(argname="argument client_key_pem", value=client_key_pem, expected_type=type_hints["client_key_pem"])
            check_type(argname="argument insecure", value=insecure, expected_type=type_hints["insecure"])
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument request_body", value=request_body, expected_type=type_hints["request_body"])
            check_type(argname="argument request_headers", value=request_headers, expected_type=type_hints["request_headers"])
            check_type(argname="argument request_timeout_ms", value=request_timeout_ms, expected_type=type_hints["request_timeout_ms"])
            check_type(argname="argument retry", value=retry, expected_type=type_hints["retry"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if ca_cert_pem is not None:
            self._values["ca_cert_pem"] = ca_cert_pem
        if client_cert_pem is not None:
            self._values["client_cert_pem"] = client_cert_pem
        if client_key_pem is not None:
            self._values["client_key_pem"] = client_key_pem
        if insecure is not None:
            self._values["insecure"] = insecure
        if method is not None:
            self._values["method"] = method
        if request_body is not None:
            self._values["request_body"] = request_body
        if request_headers is not None:
            self._values["request_headers"] = request_headers
        if request_timeout_ms is not None:
            self._values["request_timeout_ms"] = request_timeout_ms
        if retry is not None:
            self._values["retry"] = retry

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def url(self) -> builtins.str:
        '''The URL for the request. Supported schemes are ``http`` and ``https``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#url DataHttp#url}
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ca_cert_pem(self) -> typing.Optional[builtins.str]:
        '''Certificate Authority (CA) in `PEM (RFC 1421) <https://datatracker.ietf.org/doc/html/rfc1421>`_ format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#ca_cert_pem DataHttp#ca_cert_pem}
        '''
        result = self._values.get("ca_cert_pem")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_cert_pem(self) -> typing.Optional[builtins.str]:
        '''Client certificate in `PEM (RFC 1421) <https://datatracker.ietf.org/doc/html/rfc1421>`_ format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#client_cert_pem DataHttp#client_cert_pem}
        '''
        result = self._values.get("client_cert_pem")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_key_pem(self) -> typing.Optional[builtins.str]:
        '''Client key in `PEM (RFC 1421) <https://datatracker.ietf.org/doc/html/rfc1421>`_ format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#client_key_pem DataHttp#client_key_pem}
        '''
        result = self._values.get("client_key_pem")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insecure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disables verification of the server's certificate chain and hostname. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#insecure DataHttp#insecure}
        '''
        result = self._values.get("insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def method(self) -> typing.Optional[builtins.str]:
        '''The HTTP Method for the request.

        Allowed methods are a subset of methods defined in `RFC7231 <https://datatracker.ietf.org/doc/html/rfc7231#section-4.3>`_ namely, ``GET``, ``HEAD``, and ``POST``. ``POST`` support is only intended for read-only URLs, such as submitting a search.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#method DataHttp#method}
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_body(self) -> typing.Optional[builtins.str]:
        '''The request body as a string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#request_body DataHttp#request_body}
        '''
        result = self._values.get("request_body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_headers(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of request header field names and values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#request_headers DataHttp#request_headers}
        '''
        result = self._values.get("request_headers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def request_timeout_ms(self) -> typing.Optional[jsii.Number]:
        '''The request timeout in milliseconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#request_timeout_ms DataHttp#request_timeout_ms}
        '''
        result = self._values.get("request_timeout_ms")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retry(self) -> typing.Optional["DataHttpRetry"]:
        '''retry block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#retry DataHttp#retry}
        '''
        result = self._values.get("retry")
        return typing.cast(typing.Optional["DataHttpRetry"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataHttpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-http.dataHttp.DataHttpRetry",
    jsii_struct_bases=[],
    name_mapping={
        "attempts": "attempts",
        "max_delay_ms": "maxDelayMs",
        "min_delay_ms": "minDelayMs",
    },
)
class DataHttpRetry:
    def __init__(
        self,
        *,
        attempts: typing.Optional[jsii.Number] = None,
        max_delay_ms: typing.Optional[jsii.Number] = None,
        min_delay_ms: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param attempts: The number of times the request is to be retried. For example, if 2 is specified, the request will be tried a maximum of 3 times. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#attempts DataHttp#attempts}
        :param max_delay_ms: The maximum delay between retry requests in milliseconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#max_delay_ms DataHttp#max_delay_ms}
        :param min_delay_ms: The minimum delay between retry requests in milliseconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#min_delay_ms DataHttp#min_delay_ms}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5db3ea948028eba5857abc78a333d807c1e084b83b50b80801b01c9a63f2d524)
            check_type(argname="argument attempts", value=attempts, expected_type=type_hints["attempts"])
            check_type(argname="argument max_delay_ms", value=max_delay_ms, expected_type=type_hints["max_delay_ms"])
            check_type(argname="argument min_delay_ms", value=min_delay_ms, expected_type=type_hints["min_delay_ms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attempts is not None:
            self._values["attempts"] = attempts
        if max_delay_ms is not None:
            self._values["max_delay_ms"] = max_delay_ms
        if min_delay_ms is not None:
            self._values["min_delay_ms"] = min_delay_ms

    @builtins.property
    def attempts(self) -> typing.Optional[jsii.Number]:
        '''The number of times the request is to be retried.

        For example, if 2 is specified, the request will be tried a maximum of 3 times.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#attempts DataHttp#attempts}
        '''
        result = self._values.get("attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_delay_ms(self) -> typing.Optional[jsii.Number]:
        '''The maximum delay between retry requests in milliseconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#max_delay_ms DataHttp#max_delay_ms}
        '''
        result = self._values.get("max_delay_ms")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_delay_ms(self) -> typing.Optional[jsii.Number]:
        '''The minimum delay between retry requests in milliseconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.5.0/docs/data-sources/http#min_delay_ms DataHttp#min_delay_ms}
        '''
        result = self._values.get("min_delay_ms")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataHttpRetry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataHttpRetryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-http.dataHttp.DataHttpRetryOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cf266833e9dd8e06f847ea44a4e068fb0ee801803b7ebef25f70a7de5dfcd02)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAttempts")
    def reset_attempts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttempts", []))

    @jsii.member(jsii_name="resetMaxDelayMs")
    def reset_max_delay_ms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxDelayMs", []))

    @jsii.member(jsii_name="resetMinDelayMs")
    def reset_min_delay_ms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinDelayMs", []))

    @builtins.property
    @jsii.member(jsii_name="attemptsInput")
    def attempts_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "attemptsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxDelayMsInput")
    def max_delay_ms_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxDelayMsInput"))

    @builtins.property
    @jsii.member(jsii_name="minDelayMsInput")
    def min_delay_ms_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minDelayMsInput"))

    @builtins.property
    @jsii.member(jsii_name="attempts")
    def attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "attempts"))

    @attempts.setter
    def attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba6ceaf9624235fec7754791a324617747f68d6b3bc1dcfb74de6d279a0aa7ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxDelayMs")
    def max_delay_ms(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDelayMs"))

    @max_delay_ms.setter
    def max_delay_ms(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5f294fe63a7fd316b6ec5164799a68a0d8639c0e2fc23d8bd552231c0f7d60a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxDelayMs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minDelayMs")
    def min_delay_ms(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minDelayMs"))

    @min_delay_ms.setter
    def min_delay_ms(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d59f2427a3deeb5b67ceab4f858492ff5754a45bc2792465bae30603cbe442f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minDelayMs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataHttpRetry]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataHttpRetry]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataHttpRetry]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a2d49cc40232891cff2e743c36c379a77b753843ddef54acaa1aa0c95341d88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataHttp",
    "DataHttpConfig",
    "DataHttpRetry",
    "DataHttpRetryOutputReference",
]

publication.publish()

def _typecheckingstub__d6cd955bd349cdf3bff4e55c988ca69502aeda8b1ad29c58e5fc66c185056a1f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    url: builtins.str,
    ca_cert_pem: typing.Optional[builtins.str] = None,
    client_cert_pem: typing.Optional[builtins.str] = None,
    client_key_pem: typing.Optional[builtins.str] = None,
    insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    method: typing.Optional[builtins.str] = None,
    request_body: typing.Optional[builtins.str] = None,
    request_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    request_timeout_ms: typing.Optional[jsii.Number] = None,
    retry: typing.Optional[typing.Union[DataHttpRetry, typing.Dict[builtins.str, typing.Any]]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61a149b03a57fdba51f40235c91954dba6a70c08100210b3f6415f2a72abd1a1(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a9976926007362727ba46d39d34cc37325fb0abf65b12fa7408881586c95e41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d19afdc64ff831a5029bd1d31f9e5d74134eb61d20a6b84d20f24c08bce16e8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9597d6e2e2c8828af78c93d228daf35b79cca01a09bedad65ee76cbe7b4dc5a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b102819c1c00055ec6c4e6009490d1ea76febc24ba3788f0dccbe68472caa22(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb75bbe2280973db0e399bbcb80f72879e613a8852dd8816be6e56ee4d97707f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d01263d0beceb77a3aaa9f3dc2f952559e4dc223f6412bdd77cc04338609870(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a74bd45d9b8a30578befabcf666ca96bd1f9bef3b6e84638b0934128d782b51(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56342ca3a5f8a383c7aa7363c40000689eb017e1d4a08f440bf27cac06150376(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63c7570b908cd9916d86ef50e54da516dfc1d30d4f00a51c428bab8efd6bef04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee2b6a3664a80e642a2ef1d255302a3f3dc3d391999cb8f3d6103cac8420d573(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    url: builtins.str,
    ca_cert_pem: typing.Optional[builtins.str] = None,
    client_cert_pem: typing.Optional[builtins.str] = None,
    client_key_pem: typing.Optional[builtins.str] = None,
    insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    method: typing.Optional[builtins.str] = None,
    request_body: typing.Optional[builtins.str] = None,
    request_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    request_timeout_ms: typing.Optional[jsii.Number] = None,
    retry: typing.Optional[typing.Union[DataHttpRetry, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5db3ea948028eba5857abc78a333d807c1e084b83b50b80801b01c9a63f2d524(
    *,
    attempts: typing.Optional[jsii.Number] = None,
    max_delay_ms: typing.Optional[jsii.Number] = None,
    min_delay_ms: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cf266833e9dd8e06f847ea44a4e068fb0ee801803b7ebef25f70a7de5dfcd02(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba6ceaf9624235fec7754791a324617747f68d6b3bc1dcfb74de6d279a0aa7ef(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5f294fe63a7fd316b6ec5164799a68a0d8639c0e2fc23d8bd552231c0f7d60a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d59f2427a3deeb5b67ceab4f858492ff5754a45bc2792465bae30603cbe442f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a2d49cc40232891cff2e743c36c379a77b753843ddef54acaa1aa0c95341d88(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataHttpRetry]],
) -> None:
    """Type checking stubs"""
    pass
