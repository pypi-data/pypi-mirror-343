# UsageTokenRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**limits** | [**List[UsageLimit]**](UsageLimit.md) |  | [optional] 
**human_id** | **str** | The ID of the human that the token is for. (this is typically your user id from your system). Deprecated. Use &#x60;human&#x60;&#x60; instead. | [optional] 
**human** | **str** | The human that the token is for. (this is typically your user id from your system) | 
**ttl_seconds** | **int** | The time to live for the token in seconds. Defaults to 3600 (1 hour). | [optional] [default to 3600]

## Example

```python
from gabber.generated.gabber.models.usage_token_request import UsageTokenRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UsageTokenRequest from a JSON string
usage_token_request_instance = UsageTokenRequest.from_json(json)
# print the JSON string representation of the object
print(UsageTokenRequest.to_json())

# convert the object into a dict
usage_token_request_dict = usage_token_request_instance.to_dict()
# create an instance of UsageTokenRequest from a dict
usage_token_request_from_dict = UsageTokenRequest.from_dict(usage_token_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


