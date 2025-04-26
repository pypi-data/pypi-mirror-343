# RevokeUsageTokenRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**human** | **str** | The human ID to revoke the token for | 

## Example

```python
from gabber.generated.gabber.models.revoke_usage_token_request import RevokeUsageTokenRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RevokeUsageTokenRequest from a JSON string
revoke_usage_token_request_instance = RevokeUsageTokenRequest.from_json(json)
# print the JSON string representation of the object
print(RevokeUsageTokenRequest.to_json())

# convert the object into a dict
revoke_usage_token_request_dict = revoke_usage_token_request_instance.to_dict()
# create an instance of RevokeUsageTokenRequest from a dict
revoke_usage_token_request_from_dict = RevokeUsageTokenRequest.from_dict(revoke_usage_token_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


