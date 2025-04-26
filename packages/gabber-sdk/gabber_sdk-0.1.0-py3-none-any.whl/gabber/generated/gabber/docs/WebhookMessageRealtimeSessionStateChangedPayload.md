# WebhookMessageRealtimeSessionStateChangedPayload


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**previous_realtime_session** | [**WebhookMessageRealtimeSessionStateChangedpayloadSession**](WebhookMessageRealtimeSessionStateChangedpayloadSession.md) |  | [optional] 
**current_realtime_session** | [**WebhookMessageRealtimeSessionStateChangedpayloadSession**](WebhookMessageRealtimeSessionStateChangedpayloadSession.md) |  | 

## Example

```python
from gabber.generated.gabber.models.webhook_message_realtime_session_state_changed_payload import WebhookMessageRealtimeSessionStateChangedPayload

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookMessageRealtimeSessionStateChangedPayload from a JSON string
webhook_message_realtime_session_state_changed_payload_instance = WebhookMessageRealtimeSessionStateChangedPayload.from_json(json)
# print the JSON string representation of the object
print(WebhookMessageRealtimeSessionStateChangedPayload.to_json())

# convert the object into a dict
webhook_message_realtime_session_state_changed_payload_dict = webhook_message_realtime_session_state_changed_payload_instance.to_dict()
# create an instance of WebhookMessageRealtimeSessionStateChangedPayload from a dict
webhook_message_realtime_session_state_changed_payload_from_dict = WebhookMessageRealtimeSessionStateChangedPayload.from_dict(webhook_message_realtime_session_state_changed_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


