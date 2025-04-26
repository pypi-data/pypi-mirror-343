# RealtimeSessionDTMFRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**digits** | [**List[RealtimeSessionDTMFDigit]**](RealtimeSessionDTMFDigit.md) |  | 

## Example

```python
from gabber.generated.gabber.models.realtime_session_dtmf_request import RealtimeSessionDTMFRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RealtimeSessionDTMFRequest from a JSON string
realtime_session_dtmf_request_instance = RealtimeSessionDTMFRequest.from_json(json)
# print the JSON string representation of the object
print(RealtimeSessionDTMFRequest.to_json())

# convert the object into a dict
realtime_session_dtmf_request_dict = realtime_session_dtmf_request_instance.to_dict()
# create an instance of RealtimeSessionDTMFRequest from a dict
realtime_session_dtmf_request_from_dict = RealtimeSessionDTMFRequest.from_dict(realtime_session_dtmf_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


