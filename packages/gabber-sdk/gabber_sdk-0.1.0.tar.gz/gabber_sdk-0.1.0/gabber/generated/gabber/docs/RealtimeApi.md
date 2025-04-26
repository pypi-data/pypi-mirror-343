# gabber.generated.gabber.RealtimeApi

All URIs are relative to *https://api.gabber.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**attach_human**](RealtimeApi.md#attach_human) | **POST** /v1/realtime/session/{session}/attach_human | Attach a human to a RealtimeSession
[**dtmf**](RealtimeApi.md#dtmf) | **POST** /v1/realtime/{session}/dtmf | DTMF
[**end_realtime_session**](RealtimeApi.md#end_realtime_session) | **POST** /v1/realtime/{session}/end | End a RealtimeSession.
[**get_realtime_session**](RealtimeApi.md#get_realtime_session) | **GET** /v1/realtime/{session} | Get a RealtimeSession.
[**get_realtime_session_messages**](RealtimeApi.md#get_realtime_session_messages) | **GET** /v1/realtime/{session}/messages | Get a RealtimeSession messages.
[**get_realtime_session_timeline**](RealtimeApi.md#get_realtime_session_timeline) | **GET** /v1/realtime/{session}/timeline | Get a RealtimeSession timeline.
[**initiate_outbound_call**](RealtimeApi.md#initiate_outbound_call) | **POST** /v1/realtime/{session}/outbound_call | Initiate an outbound call.
[**list_realtime_sessions**](RealtimeApi.md#list_realtime_sessions) | **GET** /v1/realtime/list | List Realtime Sessions.
[**speak**](RealtimeApi.md#speak) | **POST** /v1/realtime/{session}/speak | Speak
[**start_realtime_session**](RealtimeApi.md#start_realtime_session) | **POST** /v1/realtime/start | Start a new RealtimeSession.
[**update_realtime_session**](RealtimeApi.md#update_realtime_session) | **POST** /v1/realtime/{session}/update | Update a RealtimeSession.


# **attach_human**
> RealtimeSession attach_human(session, attach_human_request)

Attach a human to a RealtimeSession

Attaches a human to a RealtimeSession. This is useful for previously anonymous sessions, for example sessions created via a phone call.

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.attach_human_request import AttachHumanRequest
from gabber.generated.gabber.models.realtime_session import RealtimeSession
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
    api_instance = gabber.generated.gabber.RealtimeApi(api_client)
    session = 'session_example' # str | The unique identifier of the RealtimeSession.
    attach_human_request = gabber.generated.gabber.AttachHumanRequest() # AttachHumanRequest | 

    try:
        # Attach a human to a RealtimeSession
        api_response = await api_instance.attach_human(session, attach_human_request)
        print("The response of RealtimeApi->attach_human:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RealtimeApi->attach_human: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session** | **str**| The unique identifier of the RealtimeSession. | 
 **attach_human_request** | [**AttachHumanRequest**](AttachHumanRequest.md)|  | 

### Return type

[**RealtimeSession**](RealtimeSession.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Token created successfully |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dtmf**
> dtmf(session, realtime_session_dtmf_request)

DTMF

For a live session, force agent to send DTMF tones

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.realtime_session_dtmf_request import RealtimeSessionDTMFRequest
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
    api_instance = gabber.generated.gabber.RealtimeApi(api_client)
    session = 'session_example' # str | The unique identifier of the RealtimeSession.
    realtime_session_dtmf_request = gabber.generated.gabber.RealtimeSessionDTMFRequest() # RealtimeSessionDTMFRequest | 

    try:
        # DTMF
        await api_instance.dtmf(session, realtime_session_dtmf_request)
    except Exception as e:
        print("Exception when calling RealtimeApi->dtmf: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session** | **str**| The unique identifier of the RealtimeSession. | 
 **realtime_session_dtmf_request** | [**RealtimeSessionDTMFRequest**](RealtimeSessionDTMFRequest.md)|  | 

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
**200** | DTMF queued successfully |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **end_realtime_session**
> RealtimeSession end_realtime_session(session, x_human_id=x_human_id)

End a RealtimeSession.

End the RealtimeSession with the given identifier.


### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (JWT) Authentication (BearerAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.realtime_session import RealtimeSession
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
    api_instance = gabber.generated.gabber.RealtimeApi(api_client)
    session = 'session_example' # str | The unique identifier of the RealtimeSession.
    x_human_id = 'x_human_id_example' # str | When using x-api-key authentication, this header is used to scope requests to a specific human. (optional)

    try:
        # End a RealtimeSession.
        api_response = await api_instance.end_realtime_session(session, x_human_id=x_human_id)
        print("The response of RealtimeApi->end_realtime_session:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RealtimeApi->end_realtime_session: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session** | **str**| The unique identifier of the RealtimeSession. | 
 **x_human_id** | **str**| When using x-api-key authentication, this header is used to scope requests to a specific human. | [optional] 

### Return type

[**RealtimeSession**](RealtimeSession.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Session ended successfully |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_realtime_session**
> RealtimeSession get_realtime_session(session, x_human_id=x_human_id)

Get a RealtimeSession.

End the RealtimeSession with the given identifier.


### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (JWT) Authentication (BearerAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.realtime_session import RealtimeSession
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
    api_instance = gabber.generated.gabber.RealtimeApi(api_client)
    session = 'session_example' # str | The unique identifier of the RealtimeSession.
    x_human_id = 'x_human_id_example' # str | When using x-api-key authentication, this header is used to scope requests to a specific human. (optional)

    try:
        # Get a RealtimeSession.
        api_response = await api_instance.get_realtime_session(session, x_human_id=x_human_id)
        print("The response of RealtimeApi->get_realtime_session:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RealtimeApi->get_realtime_session: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session** | **str**| The unique identifier of the RealtimeSession. | 
 **x_human_id** | **str**| When using x-api-key authentication, this header is used to scope requests to a specific human. | [optional] 

### Return type

[**RealtimeSession**](RealtimeSession.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Session fetched successfully |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_realtime_session_messages**
> GetRealtimeSessionMessages200Response get_realtime_session_messages(session, x_human_id=x_human_id)

Get a RealtimeSession messages.

Get all ContextMessages associated with the given RealtimeSession.


### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (JWT) Authentication (BearerAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.get_realtime_session_messages200_response import GetRealtimeSessionMessages200Response
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
    api_instance = gabber.generated.gabber.RealtimeApi(api_client)
    session = 'session_example' # str | The unique identifier of the RealtimeSession.
    x_human_id = 'x_human_id_example' # str | When using x-api-key authentication, this header is used to scope requests to a specific human. (optional)

    try:
        # Get a RealtimeSession messages.
        api_response = await api_instance.get_realtime_session_messages(session, x_human_id=x_human_id)
        print("The response of RealtimeApi->get_realtime_session_messages:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RealtimeApi->get_realtime_session_messages: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session** | **str**| The unique identifier of the RealtimeSession. | 
 **x_human_id** | **str**| When using x-api-key authentication, this header is used to scope requests to a specific human. | [optional] 

### Return type

[**GetRealtimeSessionMessages200Response**](GetRealtimeSessionMessages200Response.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Session messages fetched successfully |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_realtime_session_timeline**
> GetRealtimeSessionTimeline200Response get_realtime_session_timeline(session, x_human_id=x_human_id)

Get a RealtimeSession timeline.

Get the timeline of the RealtimeSession with the given identifier.


### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (JWT) Authentication (BearerAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.get_realtime_session_timeline200_response import GetRealtimeSessionTimeline200Response
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
    api_instance = gabber.generated.gabber.RealtimeApi(api_client)
    session = 'session_example' # str | The unique identifier of the RealtimeSession.
    x_human_id = 'x_human_id_example' # str | When using x-api-key authentication, this header is used to scope requests to a specific human. (optional)

    try:
        # Get a RealtimeSession timeline.
        api_response = await api_instance.get_realtime_session_timeline(session, x_human_id=x_human_id)
        print("The response of RealtimeApi->get_realtime_session_timeline:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RealtimeApi->get_realtime_session_timeline: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session** | **str**| The unique identifier of the RealtimeSession. | 
 **x_human_id** | **str**| When using x-api-key authentication, this header is used to scope requests to a specific human. | [optional] 

### Return type

[**GetRealtimeSessionTimeline200Response**](GetRealtimeSessionTimeline200Response.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Session timeline fetched successfully |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **initiate_outbound_call**
> RealtimeSession initiate_outbound_call(session, realtime_session_initiate_outbound_call_request)

Initiate an outbound call.

Initiate an outbound call from a RealtimeSession.


### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (JWT) Authentication (BearerAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.realtime_session import RealtimeSession
from gabber.generated.gabber.models.realtime_session_initiate_outbound_call_request import RealtimeSessionInitiateOutboundCallRequest
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
    api_instance = gabber.generated.gabber.RealtimeApi(api_client)
    session = 'session_example' # str | The unique identifier of the RealtimeSession.
    realtime_session_initiate_outbound_call_request = gabber.generated.gabber.RealtimeSessionInitiateOutboundCallRequest() # RealtimeSessionInitiateOutboundCallRequest | 

    try:
        # Initiate an outbound call.
        api_response = await api_instance.initiate_outbound_call(session, realtime_session_initiate_outbound_call_request)
        print("The response of RealtimeApi->initiate_outbound_call:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RealtimeApi->initiate_outbound_call: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session** | **str**| The unique identifier of the RealtimeSession. | 
 **realtime_session_initiate_outbound_call_request** | [**RealtimeSessionInitiateOutboundCallRequest**](RealtimeSessionInitiateOutboundCallRequest.md)|  | 

### Return type

[**RealtimeSession**](RealtimeSession.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Session called successfully |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_realtime_sessions**
> ListRealtimeSessions200Response list_realtime_sessions(x_human_id=x_human_id, page=page)

List Realtime Sessions.

List all Realtime Sessions.


### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (JWT) Authentication (BearerAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.list_realtime_sessions200_response import ListRealtimeSessions200Response
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
    api_instance = gabber.generated.gabber.RealtimeApi(api_client)
    x_human_id = 'x_human_id_example' # str | When using x-api-key authentication, this header is used to scope requests to a specific human. (optional)
    page = 'page_example' # str | Page token for pagination (optional)

    try:
        # List Realtime Sessions.
        api_response = await api_instance.list_realtime_sessions(x_human_id=x_human_id, page=page)
        print("The response of RealtimeApi->list_realtime_sessions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RealtimeApi->list_realtime_sessions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_human_id** | **str**| When using x-api-key authentication, this header is used to scope requests to a specific human. | [optional] 
 **page** | **str**| Page token for pagination | [optional] 

### Return type

[**ListRealtimeSessions200Response**](ListRealtimeSessions200Response.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Realtime Sessions fetched successfully |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **speak**
> RealtimeSession speak(session, speak_request)

Speak

For a live session, force the agent to speak a given text.

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.realtime_session import RealtimeSession
from gabber.generated.gabber.models.speak_request import SpeakRequest
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
    api_instance = gabber.generated.gabber.RealtimeApi(api_client)
    session = 'session_example' # str | The unique identifier of the RealtimeSession.
    speak_request = gabber.generated.gabber.SpeakRequest() # SpeakRequest | 

    try:
        # Speak
        api_response = await api_instance.speak(session, speak_request)
        print("The response of RealtimeApi->speak:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RealtimeApi->speak: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session** | **str**| The unique identifier of the RealtimeSession. | 
 **speak_request** | [**SpeakRequest**](SpeakRequest.md)|  | 

### Return type

[**RealtimeSession**](RealtimeSession.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Speak request sent successfully |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **start_realtime_session**
> RealtimeSessionStartResponse start_realtime_session(start_realtime_session_request, x_human_id=x_human_id)

Start a new RealtimeSession.

Start a new RealtimeSession with the given configuration.


### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (JWT) Authentication (BearerAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.realtime_session_start_response import RealtimeSessionStartResponse
from gabber.generated.gabber.models.start_realtime_session_request import StartRealtimeSessionRequest
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
    api_instance = gabber.generated.gabber.RealtimeApi(api_client)
    start_realtime_session_request = gabber.generated.gabber.StartRealtimeSessionRequest() # StartRealtimeSessionRequest | 
    x_human_id = 'x_human_id_example' # str | When using x-api-key authentication, this header is used to scope requests to a specific human. (optional)

    try:
        # Start a new RealtimeSession.
        api_response = await api_instance.start_realtime_session(start_realtime_session_request, x_human_id=x_human_id)
        print("The response of RealtimeApi->start_realtime_session:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RealtimeApi->start_realtime_session: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_realtime_session_request** | [**StartRealtimeSessionRequest**](StartRealtimeSessionRequest.md)|  | 
 **x_human_id** | **str**| When using x-api-key authentication, this header is used to scope requests to a specific human. | [optional] 

### Return type

[**RealtimeSessionStartResponse**](RealtimeSessionStartResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Session created successfully |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_realtime_session**
> RealtimeSession update_realtime_session(session, realtime_session_config_update, x_human_id=x_human_id)

Update a RealtimeSession.

Update the RealtimeSession with the given identifier.


### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (JWT) Authentication (BearerAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.realtime_session import RealtimeSession
from gabber.generated.gabber.models.realtime_session_config_update import RealtimeSessionConfigUpdate
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
    api_instance = gabber.generated.gabber.RealtimeApi(api_client)
    session = 'session_example' # str | The unique identifier of the RealtimeSession.
    realtime_session_config_update = gabber.generated.gabber.RealtimeSessionConfigUpdate() # RealtimeSessionConfigUpdate | 
    x_human_id = 'x_human_id_example' # str | When using x-api-key authentication, this header is used to scope requests to a specific human. (optional)

    try:
        # Update a RealtimeSession.
        api_response = await api_instance.update_realtime_session(session, realtime_session_config_update, x_human_id=x_human_id)
        print("The response of RealtimeApi->update_realtime_session:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RealtimeApi->update_realtime_session: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session** | **str**| The unique identifier of the RealtimeSession. | 
 **realtime_session_config_update** | [**RealtimeSessionConfigUpdate**](RealtimeSessionConfigUpdate.md)|  | 
 **x_human_id** | **str**| When using x-api-key authentication, this header is used to scope requests to a specific human. | [optional] 

### Return type

[**RealtimeSession**](RealtimeSession.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Session updated successfully |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

