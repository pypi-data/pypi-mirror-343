# Session


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** |  | 
**ended_at** | **datetime** |  | [optional] 
**id** | **str** |  | 
**livekit_room** | **str** |  | 
**metadata** | **object** |  | 
**persona** | **str** |  | 
**project** | **str** |  | 
**scenario** | **str** |  | 
**llm** | **str** |  | [optional] 
**state** | **str** |  | 
**voice_override** | **str** |  | [optional] 
**time_limit_s** | **int** |  | 

## Example

```python
from gabber.generated.gabber.models.session import Session

# TODO update the JSON string below
json = "{}"
# create an instance of Session from a JSON string
session_instance = Session.from_json(json)
# print the JSON string representation of the object
print(Session.to_json())

# convert the object into a dict
session_dict = session_instance.to_dict()
# create an instance of Session from a dict
session_from_dict = Session.from_dict(session_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


