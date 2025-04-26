# RealtimeSessionDTMFDigit


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**digit** | **str** | The DTMF digit to send | 
**duration** | **int** | The duration in milliseconds to play the tone | 

## Example

```python
from gabber.generated.gabber.models.realtime_session_dtmf_digit import RealtimeSessionDTMFDigit

# TODO update the JSON string below
json = "{}"
# create an instance of RealtimeSessionDTMFDigit from a JSON string
realtime_session_dtmf_digit_instance = RealtimeSessionDTMFDigit.from_json(json)
# print the JSON string representation of the object
print(RealtimeSessionDTMFDigit.to_json())

# convert the object into a dict
realtime_session_dtmf_digit_dict = realtime_session_dtmf_digit_instance.to_dict()
# create an instance of RealtimeSessionDTMFDigit from a dict
realtime_session_dtmf_digit_from_dict = RealtimeSessionDTMFDigit.from_dict(realtime_session_dtmf_digit_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


