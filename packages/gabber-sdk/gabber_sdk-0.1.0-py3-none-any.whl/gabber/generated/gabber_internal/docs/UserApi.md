# gabber.generated.gabber_internal.UserApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_user**](UserApi.md#get_user) | **GET** /v1/internal/user | Get user by id
[**login_google_user**](UserApi.md#login_google_user) | **POST** /v1/internal/user/login_google_user | Login a google user


# **get_user**
> User get_user(user_id=user_id, email=email, google_user_id=google_user_id)

Get user by id

Get user by id

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import gabber.generated.gabber_internal
from gabber.generated.gabber_internal.models.user import User
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
    api_instance = gabber.generated.gabber_internal.UserApi(api_client)
    user_id = 'user_id_example' # str |  (optional)
    email = 'email_example' # str |  (optional)
    google_user_id = 'google_user_id_example' # str |  (optional)

    try:
        # Get user by id
        api_response = await api_instance.get_user(user_id=user_id, email=email, google_user_id=google_user_id)
        print("The response of UserApi->get_user:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->get_user: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**|  | [optional] 
 **email** | **str**|  | [optional] 
 **google_user_id** | **str**|  | [optional] 

### Return type

[**User**](User.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | User found |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **login_google_user**
> LoginGoogleUser200Response login_google_user(login_google_user_request)

Login a google user

Login a google user

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import gabber.generated.gabber_internal
from gabber.generated.gabber_internal.models.login_google_user200_response import LoginGoogleUser200Response
from gabber.generated.gabber_internal.models.login_google_user_request import LoginGoogleUserRequest
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
    api_instance = gabber.generated.gabber_internal.UserApi(api_client)
    login_google_user_request = gabber.generated.gabber_internal.LoginGoogleUserRequest() # LoginGoogleUserRequest | 

    try:
        # Login a google user
        api_response = await api_instance.login_google_user(login_google_user_request)
        print("The response of UserApi->login_google_user:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->login_google_user: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **login_google_user_request** | [**LoginGoogleUserRequest**](LoginGoogleUserRequest.md)|  | 

### Return type

[**LoginGoogleUser200Response**](LoginGoogleUser200Response.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | User logged in |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

