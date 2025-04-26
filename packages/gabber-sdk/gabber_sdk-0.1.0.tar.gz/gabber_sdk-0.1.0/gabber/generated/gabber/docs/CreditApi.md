# gabber.generated.gabber.CreditApi

All URIs are relative to *https://api.gabber.dev*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_credit**](CreditApi.md#create_credit) | **POST** /v1/credit | Create a new credit type
[**create_credit_ledger_entry**](CreditApi.md#create_credit_ledger_entry) | **POST** /v1/credit/{credit}/ledger | Create a new credit ledger entry
[**get_credit**](CreditApi.md#get_credit) | **GET** /v1/credit/{credit} | Get a single credit object
[**get_latest_credit_ledger_entry**](CreditApi.md#get_latest_credit_ledger_entry) | **GET** /v1/credit/{credit}/ledger/latest | Get the latest credit ledger entry for a human. Requires a human id.
[**list_credits**](CreditApi.md#list_credits) | **GET** /v1/credit/list | Get a list of credits


# **create_credit**
> Credit create_credit(create_credit_request, x_human_id=x_human_id)

Create a new credit type

Creates a new credit based on the input request data.


### Example

* Api Key Authentication (ApiKeyAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.create_credit_request import CreateCreditRequest
from gabber.generated.gabber.models.credit import Credit
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
    api_instance = gabber.generated.gabber.CreditApi(api_client)
    create_credit_request = gabber.generated.gabber.CreateCreditRequest() # CreateCreditRequest | 
    x_human_id = 'x_human_id_example' # str | When using x-api-key authentication, this header is used to scope requests to a specific human. (optional)

    try:
        # Create a new credit type
        api_response = await api_instance.create_credit(create_credit_request, x_human_id=x_human_id)
        print("The response of CreditApi->create_credit:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CreditApi->create_credit: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_credit_request** | [**CreateCreditRequest**](CreateCreditRequest.md)|  | 
 **x_human_id** | **str**| When using x-api-key authentication, this header is used to scope requests to a specific human. | [optional] 

### Return type

[**Credit**](Credit.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Credit created successfully |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_credit_ledger_entry**
> CreditLedgerEntry create_credit_ledger_entry(credit, create_credit_ledger_entry_request, x_human_id=x_human_id)

Create a new credit ledger entry

Creates a new credit ledger entry for human. Requires a human id.

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.create_credit_ledger_entry_request import CreateCreditLedgerEntryRequest
from gabber.generated.gabber.models.credit_ledger_entry import CreditLedgerEntry
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
    api_instance = gabber.generated.gabber.CreditApi(api_client)
    credit = 'credit_example' # str | 
    create_credit_ledger_entry_request = gabber.generated.gabber.CreateCreditLedgerEntryRequest() # CreateCreditLedgerEntryRequest | 
    x_human_id = 'x_human_id_example' # str | When using x-api-key authentication, this header is used to scope requests to a specific human. (optional)

    try:
        # Create a new credit ledger entry
        api_response = await api_instance.create_credit_ledger_entry(credit, create_credit_ledger_entry_request, x_human_id=x_human_id)
        print("The response of CreditApi->create_credit_ledger_entry:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CreditApi->create_credit_ledger_entry: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **credit** | **str**|  | 
 **create_credit_ledger_entry_request** | [**CreateCreditLedgerEntryRequest**](CreateCreditLedgerEntryRequest.md)|  | 
 **x_human_id** | **str**| When using x-api-key authentication, this header is used to scope requests to a specific human. | [optional] 

### Return type

[**CreditLedgerEntry**](CreditLedgerEntry.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Credit ledger entry created successfully |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_credit**
> Credit get_credit(credit, x_human_id=x_human_id)

Get a single credit object

### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (JWT) Authentication (BearerAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.credit import Credit
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
    api_instance = gabber.generated.gabber.CreditApi(api_client)
    credit = 'credit_example' # str | 
    x_human_id = 'x_human_id_example' # str | When using x-api-key authentication, this header is used to scope requests to a specific human. (optional)

    try:
        # Get a single credit object
        api_response = await api_instance.get_credit(credit, x_human_id=x_human_id)
        print("The response of CreditApi->get_credit:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CreditApi->get_credit: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **credit** | **str**|  | 
 **x_human_id** | **str**| When using x-api-key authentication, this header is used to scope requests to a specific human. | [optional] 

### Return type

[**Credit**](Credit.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Credit fetched successfully |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_latest_credit_ledger_entry**
> CreditLedgerEntry get_latest_credit_ledger_entry(credit, x_human_id=x_human_id)

Get the latest credit ledger entry for a human. Requires a human id.

### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (JWT) Authentication (BearerAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.credit_ledger_entry import CreditLedgerEntry
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
    api_instance = gabber.generated.gabber.CreditApi(api_client)
    credit = 'credit_example' # str | 
    x_human_id = 'x_human_id_example' # str | When using x-api-key authentication, this header is used to scope requests to a specific human. (optional)

    try:
        # Get the latest credit ledger entry for a human. Requires a human id.
        api_response = await api_instance.get_latest_credit_ledger_entry(credit, x_human_id=x_human_id)
        print("The response of CreditApi->get_latest_credit_ledger_entry:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CreditApi->get_latest_credit_ledger_entry: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **credit** | **str**|  | 
 **x_human_id** | **str**| When using x-api-key authentication, this header is used to scope requests to a specific human. | [optional] 

### Return type

[**CreditLedgerEntry**](CreditLedgerEntry.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Credit balance fetched successfully |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_credits**
> ListCredits200Response list_credits(x_human_id=x_human_id)

Get a list of credits

### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (JWT) Authentication (BearerAuth):

```python
import gabber.generated.gabber
from gabber.generated.gabber.models.list_credits200_response import ListCredits200Response
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
    api_instance = gabber.generated.gabber.CreditApi(api_client)
    x_human_id = 'x_human_id_example' # str | When using x-api-key authentication, this header is used to scope requests to a specific human. (optional)

    try:
        # Get a list of credits
        api_response = await api_instance.list_credits(x_human_id=x_human_id)
        print("The response of CreditApi->list_credits:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CreditApi->list_credits: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_human_id** | **str**| When using x-api-key authentication, this header is used to scope requests to a specific human. | [optional] 

### Return type

[**ListCredits200Response**](ListCredits200Response.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of credits |  -  |
**400** | Bad request |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

