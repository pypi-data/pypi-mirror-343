# RealtimeSessionInitiateOutboundCallRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**source_phone_number** | **str** | The phone number to call from | 
**destination_phone_number** | **str** | The phone number to call | 

## Example

```python
from gabber.generated.gabber.models.realtime_session_initiate_outbound_call_request import RealtimeSessionInitiateOutboundCallRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RealtimeSessionInitiateOutboundCallRequest from a JSON string
realtime_session_initiate_outbound_call_request_instance = RealtimeSessionInitiateOutboundCallRequest.from_json(json)
# print the JSON string representation of the object
print(RealtimeSessionInitiateOutboundCallRequest.to_json())

# convert the object into a dict
realtime_session_initiate_outbound_call_request_dict = realtime_session_initiate_outbound_call_request_instance.to_dict()
# create an instance of RealtimeSessionInitiateOutboundCallRequest from a dict
realtime_session_initiate_outbound_call_request_from_dict = RealtimeSessionInitiateOutboundCallRequest.from_dict(realtime_session_initiate_outbound_call_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


