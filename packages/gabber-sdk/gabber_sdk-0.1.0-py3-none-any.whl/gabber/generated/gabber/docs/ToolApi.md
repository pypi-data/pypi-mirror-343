# gabber.generated.gabber.ToolApi

All URIs are relative to *https://api.gabber.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_tool_definition**](ToolApi.md#create_tool_definition) | **POST** /v1/tool | Create a tool definition
[**delete_tool_definition**](ToolApi.md#delete_tool_definition) | **DELETE** /v1/tool/{tool} | Delete a tool definition
[**get_tool_call_result**](ToolApi.md#get_tool_call_result) | **GET** /v1/tool/call/{call}/result | Get a tool call result
[**get_tool_definition**](ToolApi.md#get_tool_definition) | **GET** /v1/tool/{tool} | Get a tool definition
[**list_tool_definitions**](ToolApi.md#list_tool_definitions) | **GET** /v1/tool/list | List tools
[**update_tool_definition**](ToolApi.md#update_tool_definition) | **PUT** /v1/tool/{tool} | Update a tool definition


# **create_tool_definition**
> ToolDefinition create_tool_definition(create_tool_definition_request)

Create a tool definition

Create a tool definition

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.create_tool_definition_request import CreateToolDefinitionRequest
from gabber.generated.gabber.models.tool_definition import ToolDefinition
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
    api_instance = gabber.generated.gabber.ToolApi(api_client)
    create_tool_definition_request = gabber.generated.gabber.CreateToolDefinitionRequest() # CreateToolDefinitionRequest | 

    try:
        # Create a tool definition
        api_response = await api_instance.create_tool_definition(create_tool_definition_request)
        print("The response of ToolApi->create_tool_definition:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ToolApi->create_tool_definition: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_tool_definition_request** | [**CreateToolDefinitionRequest**](CreateToolDefinitionRequest.md)|  | 

### Return type

[**ToolDefinition**](ToolDefinition.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Tool created |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_tool_definition**
> delete_tool_definition(tool)

Delete a tool definition

Delete a tool definition

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import gabber.generated.gabber
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
    api_instance = gabber.generated.gabber.ToolApi(api_client)
    tool = 'tool_example' # str | 

    try:
        # Delete a tool definition
        await api_instance.delete_tool_definition(tool)
    except Exception as e:
        print("Exception when calling ToolApi->delete_tool_definition: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tool** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Tool deleted |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_tool_call_result**
> ToolCallResult get_tool_call_result(call)

Get a tool call result

Get a tool call result

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.tool_call_result import ToolCallResult
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
    api_instance = gabber.generated.gabber.ToolApi(api_client)
    call = 'call_example' # str | 

    try:
        # Get a tool call result
        api_response = await api_instance.get_tool_call_result(call)
        print("The response of ToolApi->get_tool_call_result:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ToolApi->get_tool_call_result: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **call** | **str**|  | 

### Return type

[**ToolCallResult**](ToolCallResult.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Tool call status fetched |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_tool_definition**
> ToolDefinition get_tool_definition(tool)

Get a tool definition

Get a tool definition

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.tool_definition import ToolDefinition
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
    api_instance = gabber.generated.gabber.ToolApi(api_client)
    tool = 'tool_example' # str | 

    try:
        # Get a tool definition
        api_response = await api_instance.get_tool_definition(tool)
        print("The response of ToolApi->get_tool_definition:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ToolApi->get_tool_definition: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tool** | **str**|  | 

### Return type

[**ToolDefinition**](ToolDefinition.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Tool fetched |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_tool_definitions**
> ListToolDefinitions200Response list_tool_definitions()

List tools

List tools

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.list_tool_definitions200_response import ListToolDefinitions200Response
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
    api_instance = gabber.generated.gabber.ToolApi(api_client)

    try:
        # List tools
        api_response = await api_instance.list_tool_definitions()
        print("The response of ToolApi->list_tool_definitions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ToolApi->list_tool_definitions: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ListToolDefinitions200Response**](ListToolDefinitions200Response.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of tools |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_tool_definition**
> ToolDefinition update_tool_definition(tool, create_tool_definition_request)

Update a tool definition

Update a tool definition

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.create_tool_definition_request import CreateToolDefinitionRequest
from gabber.generated.gabber.models.tool_definition import ToolDefinition
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
    api_instance = gabber.generated.gabber.ToolApi(api_client)
    tool = 'tool_example' # str | 
    create_tool_definition_request = gabber.generated.gabber.CreateToolDefinitionRequest() # CreateToolDefinitionRequest | 

    try:
        # Update a tool definition
        api_response = await api_instance.update_tool_definition(tool, create_tool_definition_request)
        print("The response of ToolApi->update_tool_definition:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ToolApi->update_tool_definition: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tool** | **str**|  | 
 **create_tool_definition_request** | [**CreateToolDefinitionRequest**](CreateToolDefinitionRequest.md)|  | 

### Return type

[**ToolDefinition**](ToolDefinition.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Tool updated |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

