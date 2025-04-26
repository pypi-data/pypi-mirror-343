# UpdateUsageLimitsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**limits** | [**List[UsageLimit]**](UsageLimit.md) |  | 
**human_id** | **str** | The ID of the human that the token is for. (this is typically your user id from your system) | [optional] 
**human** | **str** | The human that the token is for. (this is typically your user id from your system) | 

## Example

```python
from gabber.generated.gabber.models.update_usage_limits_request import UpdateUsageLimitsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateUsageLimitsRequest from a JSON string
update_usage_limits_request_instance = UpdateUsageLimitsRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateUsageLimitsRequest.to_json())

# convert the object into a dict
update_usage_limits_request_dict = update_usage_limits_request_instance.to_dict()
# create an instance of UpdateUsageLimitsRequest from a dict
update_usage_limits_request_from_dict = UpdateUsageLimitsRequest.from_dict(update_usage_limits_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


