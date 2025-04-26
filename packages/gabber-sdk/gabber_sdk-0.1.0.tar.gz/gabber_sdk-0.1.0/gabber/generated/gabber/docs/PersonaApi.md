# gabber.generated.gabber.PersonaApi

All URIs are relative to *https://api.gabber.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_persona**](PersonaApi.md#create_persona) | **POST** /v1/persona | Create a persona
[**delete_persona**](PersonaApi.md#delete_persona) | **DELETE** /v1/persona/{persona_id} | Delete a persona
[**get_persona**](PersonaApi.md#get_persona) | **GET** /v1/persona/{persona_id} | Get a persona
[**list_personas**](PersonaApi.md#list_personas) | **GET** /v1/persona/list | Get a list of personas
[**update_persona**](PersonaApi.md#update_persona) | **PUT** /v1/persona/{persona_id} | Update a persona


# **create_persona**
> Persona create_persona(create_persona_request, x_human_id=x_human_id)

Create a persona

### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (JWT) Authentication (BearerAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.create_persona_request import CreatePersonaRequest
from gabber.generated.gabber.models.persona import Persona
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
    api_instance = gabber.generated.gabber.PersonaApi(api_client)
    create_persona_request = gabber.generated.gabber.CreatePersonaRequest() # CreatePersonaRequest | 
    x_human_id = 'x_human_id_example' # str | When using x-api-key authentication, this header is used to scope requests to a specific human. (optional)

    try:
        # Create a persona
        api_response = await api_instance.create_persona(create_persona_request, x_human_id=x_human_id)
        print("The response of PersonaApi->create_persona:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PersonaApi->create_persona: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_persona_request** | [**CreatePersonaRequest**](CreatePersonaRequest.md)|  | 
 **x_human_id** | **str**| When using x-api-key authentication, this header is used to scope requests to a specific human. | [optional] 

### Return type

[**Persona**](Persona.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Persona created successfully |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_persona**
> DeletePersona200Response delete_persona(persona_id, x_human_id=x_human_id)

Delete a persona

### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (JWT) Authentication (BearerAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.delete_persona200_response import DeletePersona200Response
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
    api_instance = gabber.generated.gabber.PersonaApi(api_client)
    persona_id = 'persona_id_example' # str | 
    x_human_id = 'x_human_id_example' # str | When using x-api-key authentication, this header is used to scope requests to a specific human. (optional)

    try:
        # Delete a persona
        api_response = await api_instance.delete_persona(persona_id, x_human_id=x_human_id)
        print("The response of PersonaApi->delete_persona:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PersonaApi->delete_persona: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **persona_id** | **str**|  | 
 **x_human_id** | **str**| When using x-api-key authentication, this header is used to scope requests to a specific human. | [optional] 

### Return type

[**DeletePersona200Response**](DeletePersona200Response.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Persona deleted successfully |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_persona**
> Persona get_persona(persona_id, x_human_id=x_human_id)

Get a persona

### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (JWT) Authentication (BearerAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.persona import Persona
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
    api_instance = gabber.generated.gabber.PersonaApi(api_client)
    persona_id = 'persona_id_example' # str | 
    x_human_id = 'x_human_id_example' # str | When using x-api-key authentication, this header is used to scope requests to a specific human. (optional)

    try:
        # Get a persona
        api_response = await api_instance.get_persona(persona_id, x_human_id=x_human_id)
        print("The response of PersonaApi->get_persona:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PersonaApi->get_persona: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **persona_id** | **str**|  | 
 **x_human_id** | **str**| When using x-api-key authentication, this header is used to scope requests to a specific human. | [optional] 

### Return type

[**Persona**](Persona.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Persona fetched successfully |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_personas**
> ListPersonas200Response list_personas(x_human_id=x_human_id)

Get a list of personas

### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (JWT) Authentication (BearerAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.list_personas200_response import ListPersonas200Response
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
    api_instance = gabber.generated.gabber.PersonaApi(api_client)
    x_human_id = 'x_human_id_example' # str | When using x-api-key authentication, this header is used to scope requests to a specific human. (optional)

    try:
        # Get a list of personas
        api_response = await api_instance.list_personas(x_human_id=x_human_id)
        print("The response of PersonaApi->list_personas:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PersonaApi->list_personas: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_human_id** | **str**| When using x-api-key authentication, this header is used to scope requests to a specific human. | [optional] 

### Return type

[**ListPersonas200Response**](ListPersonas200Response.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of personas |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_persona**
> Persona update_persona(persona_id, update_persona_request, x_human_id=x_human_id)

Update a persona

### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (JWT) Authentication (BearerAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.persona import Persona
from gabber.generated.gabber.models.update_persona_request import UpdatePersonaRequest
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
    api_instance = gabber.generated.gabber.PersonaApi(api_client)
    persona_id = 'persona_id_example' # str | 
    update_persona_request = gabber.generated.gabber.UpdatePersonaRequest() # UpdatePersonaRequest | 
    x_human_id = 'x_human_id_example' # str | When using x-api-key authentication, this header is used to scope requests to a specific human. (optional)

    try:
        # Update a persona
        api_response = await api_instance.update_persona(persona_id, update_persona_request, x_human_id=x_human_id)
        print("The response of PersonaApi->update_persona:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PersonaApi->update_persona: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **persona_id** | **str**|  | 
 **update_persona_request** | [**UpdatePersonaRequest**](UpdatePersonaRequest.md)|  | 
 **x_human_id** | **str**| When using x-api-key authentication, this header is used to scope requests to a specific human. | [optional] 

### Return type

[**Persona**](Persona.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Persona updated successfully |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

