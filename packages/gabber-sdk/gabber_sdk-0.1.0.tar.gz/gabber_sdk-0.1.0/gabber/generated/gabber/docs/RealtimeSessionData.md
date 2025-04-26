# RealtimeSessionData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**value** | **str** |  | 

## Example

```python
from gabber.generated.gabber.models.realtime_session_data import RealtimeSessionData

# TODO update the JSON string below
json = "{}"
# create an instance of RealtimeSessionData from a JSON string
realtime_session_data_instance = RealtimeSessionData.from_json(json)
# print the JSON string representation of the object
print(RealtimeSessionData.to_json())

# convert the object into a dict
realtime_session_data_dict = realtime_session_data_instance.to_dict()
# create an instance of RealtimeSessionData from a dict
realtime_session_data_from_dict = RealtimeSessionData.from_dict(realtime_session_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


