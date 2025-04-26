# UpdateUsageTokenTTLRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**human** | **str** | The human ID to update the TTL for | 
**ttl_seconds** | **int** | The new TTL in seconds | 

## Example

```python
from gabber.generated.gabber.models.update_usage_token_ttl_request import UpdateUsageTokenTTLRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateUsageTokenTTLRequest from a JSON string
update_usage_token_ttl_request_instance = UpdateUsageTokenTTLRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateUsageTokenTTLRequest.to_json())

# convert the object into a dict
update_usage_token_ttl_request_dict = update_usage_token_ttl_request_instance.to_dict()
# create an instance of UpdateUsageTokenTTLRequest from a dict
update_usage_token_ttl_request_from_dict = UpdateUsageTokenTTLRequest.from_dict(update_usage_token_ttl_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


