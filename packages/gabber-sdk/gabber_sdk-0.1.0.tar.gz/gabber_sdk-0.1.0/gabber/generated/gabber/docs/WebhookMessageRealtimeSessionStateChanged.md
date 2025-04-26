# WebhookMessageRealtimeSessionStateChanged


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**payload** | [**WebhookMessageRealtimeSessionStateChangedPayload**](WebhookMessageRealtimeSessionStateChangedPayload.md) |  | 

## Example

```python
from gabber.generated.gabber.models.webhook_message_realtime_session_state_changed import WebhookMessageRealtimeSessionStateChanged

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookMessageRealtimeSessionStateChanged from a JSON string
webhook_message_realtime_session_state_changed_instance = WebhookMessageRealtimeSessionStateChanged.from_json(json)
# print the JSON string representation of the object
print(WebhookMessageRealtimeSessionStateChanged.to_json())

# convert the object into a dict
webhook_message_realtime_session_state_changed_dict = webhook_message_realtime_session_state_changed_instance.to_dict()
# create an instance of WebhookMessageRealtimeSessionStateChanged from a dict
webhook_message_realtime_session_state_changed_from_dict = WebhookMessageRealtimeSessionStateChanged.from_dict(webhook_message_realtime_session_state_changed_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


