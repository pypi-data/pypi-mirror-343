# CheckUsageToken200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ttl_seconds** | **int** | The TTL of the token in seconds | 

## Example

```python
from gabber.generated.gabber.models.check_usage_token200_response import CheckUsageToken200Response

# TODO update the JSON string below
json = "{}"
# create an instance of CheckUsageToken200Response from a JSON string
check_usage_token200_response_instance = CheckUsageToken200Response.from_json(json)
# print the JSON string representation of the object
print(CheckUsageToken200Response.to_json())

# convert the object into a dict
check_usage_token200_response_dict = check_usage_token200_response_instance.to_dict()
# create an instance of CheckUsageToken200Response from a dict
check_usage_token200_response_from_dict = CheckUsageToken200Response.from_dict(check_usage_token200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


