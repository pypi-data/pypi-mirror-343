# CheckUsageTokenRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**human** | **str** | The human ID to check the token for | 

## Example

```python
from gabber.generated.gabber.models.check_usage_token_request import CheckUsageTokenRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CheckUsageTokenRequest from a JSON string
check_usage_token_request_instance = CheckUsageTokenRequest.from_json(json)
# print the JSON string representation of the object
print(CheckUsageTokenRequest.to_json())

# convert the object into a dict
check_usage_token_request_dict = check_usage_token_request_instance.to_dict()
# create an instance of CheckUsageTokenRequest from a dict
check_usage_token_request_from_dict = CheckUsageTokenRequest.from_dict(check_usage_token_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


