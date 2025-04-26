# gabber.generated.gabber.UsageApi

All URIs are relative to *https://api.gabber.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**check_usage_token**](UsageApi.md#check_usage_token) | **POST** /v1/usage/token/check | Check a usage token
[**create_usage_token**](UsageApi.md#create_usage_token) | **POST** /v1/usage/token | Create a new usage token
[**get_usage_limits**](UsageApi.md#get_usage_limits) | **GET** /v1/usage/limits | Get usage limits
[**revoke_usage_token**](UsageApi.md#revoke_usage_token) | **POST** /v1/usage/token/revoke | Revoke a usage token
[**update_usage_token**](UsageApi.md#update_usage_token) | **PUT** /v1/usage/token | Update limits on a usage token
[**update_usage_token_ttl**](UsageApi.md#update_usage_token_ttl) | **POST** /v1/usage/token/update_ttl | Update the TTL of a usage token


# **check_usage_token**
> CheckUsageToken200Response check_usage_token(check_usage_token_request)

Check a usage token

Checks the validity of a human token

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.check_usage_token200_response import CheckUsageToken200Response
from gabber.generated.gabber.models.check_usage_token_request import CheckUsageTokenRequest
from gabber.generated.gabber.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.gabber.dev
# See configuration.py for a list of all supported configuration parameters.
configuration = gabber.generated.gabber.Configuration(
    host = "https://api.gabber.dev"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
async with gabber.generated.gabber.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gabber.generated.gabber.UsageApi(api_client)
    check_usage_token_request = gabber.generated.gabber.CheckUsageTokenRequest() # CheckUsageTokenRequest | 

    try:
        # Check a usage token
        api_response = await api_instance.check_usage_token(check_usage_token_request)
        print("The response of UsageApi->check_usage_token:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsageApi->check_usage_token: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **check_usage_token_request** | [**CheckUsageTokenRequest**](CheckUsageTokenRequest.md)|  | 

### Return type

[**CheckUsageToken200Response**](CheckUsageToken200Response.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Token is valid |  -  |
**404** | Token not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_usage_token**
> CreateUsageToken200Response create_usage_token(usage_token_request)

Create a new usage token

Requests a token for a human

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.create_usage_token200_response import CreateUsageToken200Response
from gabber.generated.gabber.models.usage_token_request import UsageTokenRequest
from gabber.generated.gabber.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.gabber.dev
# See configuration.py for a list of all supported configuration parameters.
configuration = gabber.generated.gabber.Configuration(
    host = "https://api.gabber.dev"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
async with gabber.generated.gabber.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gabber.generated.gabber.UsageApi(api_client)
    usage_token_request = gabber.generated.gabber.UsageTokenRequest() # UsageTokenRequest | 

    try:
        # Create a new usage token
        api_response = await api_instance.create_usage_token(usage_token_request)
        print("The response of UsageApi->create_usage_token:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsageApi->create_usage_token: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **usage_token_request** | [**UsageTokenRequest**](UsageTokenRequest.md)|  | 

### Return type

[**CreateUsageToken200Response**](CreateUsageToken200Response.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Token created successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_usage_limits**
> List[UsageLimit] get_usage_limits(x_human_id=x_human_id)

Get usage limits

Gets the usage limits of a token

### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (JWT) Authentication (BearerAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.usage_limit import UsageLimit
from gabber.generated.gabber.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.gabber.dev
# See configuration.py for a list of all supported configuration parameters.
configuration = gabber.generated.gabber.Configuration(
    host = "https://api.gabber.dev"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure Bearer authorization (JWT): BearerAuth
configuration = gabber.generated.gabber.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with gabber.generated.gabber.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gabber.generated.gabber.UsageApi(api_client)
    x_human_id = 'x_human_id_example' # str | When using x-api-key authentication, this header is used to scope requests to a specific human. (optional)

    try:
        # Get usage limits
        api_response = await api_instance.get_usage_limits(x_human_id=x_human_id)
        print("The response of UsageApi->get_usage_limits:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsageApi->get_usage_limits: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_human_id** | **str**| When using x-api-key authentication, this header is used to scope requests to a specific human. | [optional] 

### Return type

[**List[UsageLimit]**](UsageLimit.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Token created successfully |  -  |
**400** | Bad request |  -  |
**429** | Usage limit exceeded |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **revoke_usage_token**
> revoke_usage_token(revoke_usage_token_request)

Revoke a usage token

Revokes a human token

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.revoke_usage_token_request import RevokeUsageTokenRequest
from gabber.generated.gabber.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.gabber.dev
# See configuration.py for a list of all supported configuration parameters.
configuration = gabber.generated.gabber.Configuration(
    host = "https://api.gabber.dev"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
async with gabber.generated.gabber.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gabber.generated.gabber.UsageApi(api_client)
    revoke_usage_token_request = gabber.generated.gabber.RevokeUsageTokenRequest() # RevokeUsageTokenRequest | 

    try:
        # Revoke a usage token
        await api_instance.revoke_usage_token(revoke_usage_token_request)
    except Exception as e:
        print("Exception when calling UsageApi->revoke_usage_token: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **revoke_usage_token_request** | [**RevokeUsageTokenRequest**](RevokeUsageTokenRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Token revoked successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_usage_token**
> Dict[str, object] update_usage_token(update_usage_limits_request)

Update limits on a usage token

Updates the usage limits of a human

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.update_usage_limits_request import UpdateUsageLimitsRequest
from gabber.generated.gabber.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.gabber.dev
# See configuration.py for a list of all supported configuration parameters.
configuration = gabber.generated.gabber.Configuration(
    host = "https://api.gabber.dev"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
async with gabber.generated.gabber.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gabber.generated.gabber.UsageApi(api_client)
    update_usage_limits_request = gabber.generated.gabber.UpdateUsageLimitsRequest() # UpdateUsageLimitsRequest | 

    try:
        # Update limits on a usage token
        api_response = await api_instance.update_usage_token(update_usage_limits_request)
        print("The response of UsageApi->update_usage_token:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsageApi->update_usage_token: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **update_usage_limits_request** | [**UpdateUsageLimitsRequest**](UpdateUsageLimitsRequest.md)|  | 

### Return type

**Dict[str, object]**

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Usage limits updated successfully |  -  |
**400** | Bad request |  -  |
**429** | Usage limit exceeded |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_usage_token_ttl**
> update_usage_token_ttl(update_usage_token_ttl_request)

Update the TTL of a usage token

Updates the TTL of a human tokan

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.update_usage_token_ttl_request import UpdateUsageTokenTTLRequest
from gabber.generated.gabber.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.gabber.dev
# See configuration.py for a list of all supported configuration parameters.
configuration = gabber.generated.gabber.Configuration(
    host = "https://api.gabber.dev"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
async with gabber.generated.gabber.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gabber.generated.gabber.UsageApi(api_client)
    update_usage_token_ttl_request = gabber.generated.gabber.UpdateUsageTokenTTLRequest() # UpdateUsageTokenTTLRequest | 

    try:
        # Update the TTL of a usage token
        await api_instance.update_usage_token_ttl(update_usage_token_ttl_request)
    except Exception as e:
        print("Exception when calling UsageApi->update_usage_token_ttl: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **update_usage_token_ttl_request** | [**UpdateUsageTokenTTLRequest**](UpdateUsageTokenTTLRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Token ttl updated successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

