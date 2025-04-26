# UpdateSessionRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**time_limit_s** | **float** |  | [optional] 
**voice_override** | **str** |  | [optional] 

## Example

```python
from gabber.generated.gabber.models.update_session_request import UpdateSessionRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateSessionRequest from a JSON string
update_session_request_instance = UpdateSessionRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateSessionRequest.to_json())

# convert the object into a dict
update_session_request_dict = update_session_request_instance.to_dict()
# create an instance of UpdateSessionRequest from a dict
update_session_request_from_dict = UpdateSessionRequest.from_dict(update_session_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


