# SessionStartRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**history** | [**List[HistoryMessage]**](HistoryMessage.md) |  | [optional] 
**time_limit_s** | **int** |  | [optional] 
**voice_override** | **str** |  | [optional] 
**llm** | **str** |  | [optional] 
**persona** | **str** |  | [optional] 
**save_messages** | **bool** | save session messages | [optional] [default to True]
**extra** | **object** | reserved for internal use | [optional] 
**scenario** | **str** |  | [optional] 

## Example

```python
from gabber.generated.gabber.models.session_start_request import SessionStartRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SessionStartRequest from a JSON string
session_start_request_instance = SessionStartRequest.from_json(json)
# print the JSON string representation of the object
print(SessionStartRequest.to_json())

# convert the object into a dict
session_start_request_dict = session_start_request_instance.to_dict()
# create an instance of SessionStartRequest from a dict
session_start_request_from_dict = SessionStartRequest.from_dict(session_start_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


