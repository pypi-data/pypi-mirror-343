# gabber.generated.gabber_internal.RealtimeApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**attach_livekit_room**](RealtimeApi.md#attach_livekit_room) | **POST** /v1/internal/realtime/livekit/attach | Create realtime session from livekit room
[**realtime_session_time_limit_exceeded**](RealtimeApi.md#realtime_session_time_limit_exceeded) | **POST** /v1/internal/realtime/{session}/time_limit_exceeded | Realtime session time limit exceeded
[**update_realtime_session_state**](RealtimeApi.md#update_realtime_session_state) | **POST** /v1/internal/realtime/{session}/update_state | Update realtime session state


# **attach_livekit_room**
> AttachLivekitRoom200Response attach_livekit_room(realtime_livekit_attach_request)

Create realtime session from livekit room

Creates a new realtime session from an existing livekit room

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import gabber.generated.gabber_internal
from gabber.generated.gabber_internal.models.attach_livekit_room200_response import AttachLivekitRoom200Response
from gabber.generated.gabber_internal.models.realtime_livekit_attach_request import RealtimeLivekitAttachRequest
from gabber.generated.gabber_internal.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gabber.generated.gabber_internal.Configuration(
    host = "http://localhost"
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
async with gabber.generated.gabber_internal.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gabber.generated.gabber_internal.RealtimeApi(api_client)
    realtime_livekit_attach_request = gabber.generated.gabber_internal.RealtimeLivekitAttachRequest() # RealtimeLivekitAttachRequest | 

    try:
        # Create realtime session from livekit room
        api_response = await api_instance.attach_livekit_room(realtime_livekit_attach_request)
        print("The response of RealtimeApi->attach_livekit_room:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RealtimeApi->attach_livekit_room: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **realtime_livekit_attach_request** | [**RealtimeLivekitAttachRequest**](RealtimeLivekitAttachRequest.md)|  | 

### Return type

[**AttachLivekitRoom200Response**](AttachLivekitRoom200Response.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Sesssion attached |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **realtime_session_time_limit_exceeded**
> realtime_session_time_limit_exceeded(session)

Realtime session time limit exceeded

Realtime session time limit exceeded

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import gabber.generated.gabber_internal
from gabber.generated.gabber_internal.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gabber.generated.gabber_internal.Configuration(
    host = "http://localhost"
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
async with gabber.generated.gabber_internal.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gabber.generated.gabber_internal.RealtimeApi(api_client)
    session = 'session_example' # str | 

    try:
        # Realtime session time limit exceeded
        await api_instance.realtime_session_time_limit_exceeded(session)
    except Exception as e:
        print("Exception when calling RealtimeApi->realtime_session_time_limit_exceeded: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session** | **str**|  | 

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
**200** | Session time limit exceeded |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_realtime_session_state**
> update_realtime_session_state(session, update_realtime_session_state_request)

Update realtime session state

Update realtime session state

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import gabber.generated.gabber_internal
from gabber.generated.gabber_internal.models.update_realtime_session_state_request import UpdateRealtimeSessionStateRequest
from gabber.generated.gabber_internal.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gabber.generated.gabber_internal.Configuration(
    host = "http://localhost"
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
async with gabber.generated.gabber_internal.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gabber.generated.gabber_internal.RealtimeApi(api_client)
    session = 'session_example' # str | 
    update_realtime_session_state_request = gabber.generated.gabber_internal.UpdateRealtimeSessionStateRequest() # UpdateRealtimeSessionStateRequest | 

    try:
        # Update realtime session state
        await api_instance.update_realtime_session_state(session, update_realtime_session_state_request)
    except Exception as e:
        print("Exception when calling RealtimeApi->update_realtime_session_state: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session** | **str**|  | 
 **update_realtime_session_state_request** | [**UpdateRealtimeSessionStateRequest**](UpdateRealtimeSessionStateRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Session state updated |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

