# SessionStartRequestOneOf1


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**time_limit_s** | **int** |  | [optional] 
**voice_override** | **str** |  | [optional] 
**llm** | **str** |  | [optional] 
**scenario** | **str** |  | [optional] 
**persona** | **str** |  | [optional] 
**save_messages** | **bool** | save session messages | [optional] [default to True]
**extra** | **object** | reserved for internal use | [optional] 

## Example

```python
from gabber.generated.gabber.models.session_start_request_one_of1 import SessionStartRequestOneOf1

# TODO update the JSON string below
json = "{}"
# create an instance of SessionStartRequestOneOf1 from a JSON string
session_start_request_one_of1_instance = SessionStartRequestOneOf1.from_json(json)
# print the JSON string representation of the object
print(SessionStartRequestOneOf1.to_json())

# convert the object into a dict
session_start_request_one_of1_dict = session_start_request_one_of1_instance.to_dict()
# create an instance of SessionStartRequestOneOf1 from a dict
session_start_request_one_of1_from_dict = SessionStartRequestOneOf1.from_dict(session_start_request_one_of1_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


