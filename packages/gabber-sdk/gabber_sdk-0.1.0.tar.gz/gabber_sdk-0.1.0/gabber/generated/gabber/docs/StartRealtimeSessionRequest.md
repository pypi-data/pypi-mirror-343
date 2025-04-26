# StartRealtimeSessionRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**simulated** | **bool** | Whether the session is simulated. | [optional] 
**config** | [**RealtimeSessionConfigCreate**](RealtimeSessionConfigCreate.md) |  | 
**extra** | **Dict[str, object]** | Extra data for certain Gabber partner integrations. | [optional] 

## Example

```python
from gabber.generated.gabber.models.start_realtime_session_request import StartRealtimeSessionRequest

# TODO update the JSON string below
json = "{}"
# create an instance of StartRealtimeSessionRequest from a JSON string
start_realtime_session_request_instance = StartRealtimeSessionRequest.from_json(json)
# print the JSON string representation of the object
print(StartRealtimeSessionRequest.to_json())

# convert the object into a dict
start_realtime_session_request_dict = start_realtime_session_request_instance.to_dict()
# create an instance of StartRealtimeSessionRequest from a dict
start_realtime_session_request_from_dict = StartRealtimeSessionRequest.from_dict(start_realtime_session_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


