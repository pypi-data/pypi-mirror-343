# RealtimeSessionStartResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**session** | [**RealtimeSession**](RealtimeSession.md) |  | 
**connection_details** | [**RealtimeSessionConnectionDetails**](RealtimeSessionConnectionDetails.md) |  | 

## Example

```python
from gabber.generated.gabber.models.realtime_session_start_response import RealtimeSessionStartResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RealtimeSessionStartResponse from a JSON string
realtime_session_start_response_instance = RealtimeSessionStartResponse.from_json(json)
# print the JSON string representation of the object
print(RealtimeSessionStartResponse.to_json())

# convert the object into a dict
realtime_session_start_response_dict = realtime_session_start_response_instance.to_dict()
# create an instance of RealtimeSessionStartResponse from a dict
realtime_session_start_response_from_dict = RealtimeSessionStartResponse.from_dict(realtime_session_start_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


