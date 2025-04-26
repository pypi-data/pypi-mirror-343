# WebhookMessageRealtimeSessionMessageCommittedPayload


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | [**ContextMessage**](ContextMessage.md) |  | 
**realtime_session_id** | **str** |  | [optional] 

## Example

```python
from gabber.generated.gabber.models.webhook_message_realtime_session_message_committed_payload import WebhookMessageRealtimeSessionMessageCommittedPayload

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookMessageRealtimeSessionMessageCommittedPayload from a JSON string
webhook_message_realtime_session_message_committed_payload_instance = WebhookMessageRealtimeSessionMessageCommittedPayload.from_json(json)
# print the JSON string representation of the object
print(WebhookMessageRealtimeSessionMessageCommittedPayload.to_json())

# convert the object into a dict
webhook_message_realtime_session_message_committed_payload_dict = webhook_message_realtime_session_message_committed_payload_instance.to_dict()
# create an instance of WebhookMessageRealtimeSessionMessageCommittedPayload from a dict
webhook_message_realtime_session_message_committed_payload_from_dict = WebhookMessageRealtimeSessionMessageCommittedPayload.from_dict(webhook_message_realtime_session_message_committed_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


