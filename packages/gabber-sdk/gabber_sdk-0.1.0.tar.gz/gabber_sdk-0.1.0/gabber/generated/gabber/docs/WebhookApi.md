# gabber.generated.gabber.WebhookApi

All URIs are relative to *https://api.gabber.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**webhook_post**](WebhookApi.md#webhook_post) | **POST** /webhook | Webhook


# **webhook_post**
> webhook_post(x_webhook_signature, webhook_message)

Webhook

Receives events from the server.

### Example


```python
import gabber.generated.gabber
from gabber.generated.gabber.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.gabber.dev
# See configuration.py for a list of all supported configuration parameters.
configuration = gabber.generated.gabber.Configuration(
    host = "https://api.gabber.dev"
)


# Enter a context with an instance of the API client
async with gabber.generated.gabber.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gabber.generated.gabber.WebhookApi(api_client)
    x_webhook_signature = 'x_webhook_signature_example' # str | Hex string of HMAC-SHA256 signature of the request body signed using your configured service key
    webhook_message = gabber.generated.gabber.WebhookMessage() # WebhookMessage | 

    try:
        # Webhook
        await api_instance.webhook_post(x_webhook_signature, webhook_message)
    except Exception as e:
        print("Exception when calling WebhookApi->webhook_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_webhook_signature** | **str**| Hex string of HMAC-SHA256 signature of the request body signed using your configured service key | 
 **webhook_message** | [**WebhookMessage**](WebhookMessage.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Webhook received successfully |  -  |
**400** | Invalid request data |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

