# gabber.generated.gabber_internal.PhoneApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_phone_attachment**](PhoneApi.md#get_phone_attachment) | **GET** /v1/internal/phone/get_attachment | Get phone attachment


# **get_phone_attachment**
> PhoneNumberAttachment get_phone_attachment(number)

Get phone attachment

Get phone attachment

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import gabber.generated.gabber_internal
from gabber.generated.gabber_internal.models.phone_number_attachment import PhoneNumberAttachment
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
    api_instance = gabber.generated.gabber_internal.PhoneApi(api_client)
    number = 'number_example' # str | 

    try:
        # Get phone attachment
        api_response = await api_instance.get_phone_attachment(number)
        print("The response of PhoneApi->get_phone_attachment:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PhoneApi->get_phone_attachment: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **number** | **str**|  | 

### Return type

[**PhoneNumberAttachment**](PhoneNumberAttachment.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Phone attachment found |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

