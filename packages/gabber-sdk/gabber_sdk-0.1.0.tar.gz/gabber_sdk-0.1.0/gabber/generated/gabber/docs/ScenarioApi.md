# gabber.generated.gabber.ScenarioApi

All URIs are relative to *https://api.gabber.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_scenario**](ScenarioApi.md#create_scenario) | **POST** /v1/scenario | Create a scenario
[**delete_scenario**](ScenarioApi.md#delete_scenario) | **DELETE** /v1/scenario/{scenario_id} | Delete a scenario
[**get_scenario**](ScenarioApi.md#get_scenario) | **GET** /v1/scenario/{scenario_id} | Get a scenario
[**list_scenarios**](ScenarioApi.md#list_scenarios) | **GET** /v1/scenario/list | Get a list of scenarios
[**update_scenario**](ScenarioApi.md#update_scenario) | **PUT** /v1/scenario/{scenario_id} | Update a scenario


# **create_scenario**
> Scenario create_scenario(create_scenario_request)

Create a scenario

### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (JWT) Authentication (BearerAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.create_scenario_request import CreateScenarioRequest
from gabber.generated.gabber.models.scenario import Scenario
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
    api_instance = gabber.generated.gabber.ScenarioApi(api_client)
    create_scenario_request = gabber.generated.gabber.CreateScenarioRequest() # CreateScenarioRequest | 

    try:
        # Create a scenario
        api_response = await api_instance.create_scenario(create_scenario_request)
        print("The response of ScenarioApi->create_scenario:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScenarioApi->create_scenario: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_scenario_request** | [**CreateScenarioRequest**](CreateScenarioRequest.md)|  | 

### Return type

[**Scenario**](Scenario.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Scenario deleted successfully |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_scenario**
> DeleteScenario200Response delete_scenario(scenario_id, x_human_id=x_human_id)

Delete a scenario

### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (JWT) Authentication (BearerAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.delete_scenario200_response import DeleteScenario200Response
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
    api_instance = gabber.generated.gabber.ScenarioApi(api_client)
    scenario_id = 'scenario_id_example' # str | 
    x_human_id = 'x_human_id_example' # str | When using x-api-key authentication, this header is used to scope requests to a specific human. (optional)

    try:
        # Delete a scenario
        api_response = await api_instance.delete_scenario(scenario_id, x_human_id=x_human_id)
        print("The response of ScenarioApi->delete_scenario:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScenarioApi->delete_scenario: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scenario_id** | **str**|  | 
 **x_human_id** | **str**| When using x-api-key authentication, this header is used to scope requests to a specific human. | [optional] 

### Return type

[**DeleteScenario200Response**](DeleteScenario200Response.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Scenario deleted successfully |  -  |
**400** | Bad request |  -  |
**404** | Scenario not found |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_scenario**
> Scenario get_scenario(scenario_id, x_human_id=x_human_id)

Get a scenario

### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (JWT) Authentication (BearerAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.scenario import Scenario
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
    api_instance = gabber.generated.gabber.ScenarioApi(api_client)
    scenario_id = 'scenario_id_example' # str | 
    x_human_id = 'x_human_id_example' # str | When using x-api-key authentication, this header is used to scope requests to a specific human. (optional)

    try:
        # Get a scenario
        api_response = await api_instance.get_scenario(scenario_id, x_human_id=x_human_id)
        print("The response of ScenarioApi->get_scenario:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScenarioApi->get_scenario: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scenario_id** | **str**|  | 
 **x_human_id** | **str**| When using x-api-key authentication, this header is used to scope requests to a specific human. | [optional] 

### Return type

[**Scenario**](Scenario.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Scenario fetched successfully |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_scenarios**
> ListScenarios200Response list_scenarios(x_human_id=x_human_id)

Get a list of scenarios

### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (JWT) Authentication (BearerAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.list_scenarios200_response import ListScenarios200Response
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
    api_instance = gabber.generated.gabber.ScenarioApi(api_client)
    x_human_id = 'x_human_id_example' # str | When using x-api-key authentication, this header is used to scope requests to a specific human. (optional)

    try:
        # Get a list of scenarios
        api_response = await api_instance.list_scenarios(x_human_id=x_human_id)
        print("The response of ScenarioApi->list_scenarios:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScenarioApi->list_scenarios: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_human_id** | **str**| When using x-api-key authentication, this header is used to scope requests to a specific human. | [optional] 

### Return type

[**ListScenarios200Response**](ListScenarios200Response.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of scenarios |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_scenario**
> Scenario update_scenario(scenario_id, update_scenario_request, x_human_id=x_human_id)

Update a scenario

### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (JWT) Authentication (BearerAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.scenario import Scenario
from gabber.generated.gabber.models.update_scenario_request import UpdateScenarioRequest
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
    api_instance = gabber.generated.gabber.ScenarioApi(api_client)
    scenario_id = 'scenario_id_example' # str | 
    update_scenario_request = gabber.generated.gabber.UpdateScenarioRequest() # UpdateScenarioRequest | 
    x_human_id = 'x_human_id_example' # str | When using x-api-key authentication, this header is used to scope requests to a specific human. (optional)

    try:
        # Update a scenario
        api_response = await api_instance.update_scenario(scenario_id, update_scenario_request, x_human_id=x_human_id)
        print("The response of ScenarioApi->update_scenario:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScenarioApi->update_scenario: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scenario_id** | **str**|  | 
 **update_scenario_request** | [**UpdateScenarioRequest**](UpdateScenarioRequest.md)|  | 
 **x_human_id** | **str**| When using x-api-key authentication, this header is used to scope requests to a specific human. | [optional] 

### Return type

[**Scenario**](Scenario.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Scenario updated successfully |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

