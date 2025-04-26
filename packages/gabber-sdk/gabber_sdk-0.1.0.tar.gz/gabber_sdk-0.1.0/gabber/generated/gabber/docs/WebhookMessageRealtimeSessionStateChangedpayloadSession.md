# WebhookMessageRealtimeSessionStateChangedpayloadSession


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The unique identifier of the RealtimeSession. | 
**state** | **str** | The current state of the RealtimeSession. | 
**created_at** | **datetime** | The time the RealtimeSession was created. | 
**ended_at** | **datetime** | The time the RealtimeSession ended. | [optional] 
**project** | **str** | The project identifier. | 
**human** | **str** | The human identifier. | [optional] 
**simulated** | **bool** | Whether the session is simulated or not. | 
**config** | [**RealtimeSessionConfig**](RealtimeSessionConfig.md) |  | 
**data** | [**List[RealtimeSessionData]**](RealtimeSessionData.md) |  | 
**extra** | **object** | Extra configuration for the RealtimeSession. Usually this is for internal purposes. | [optional] 

## Example

```python
from gabber.generated.gabber.models.webhook_message_realtime_session_state_changedpayload_session import WebhookMessageRealtimeSessionStateChangedpayloadSession

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookMessageRealtimeSessionStateChangedpayloadSession from a JSON string
webhook_message_realtime_session_state_changedpayload_session_instance = WebhookMessageRealtimeSessionStateChangedpayloadSession.from_json(json)
# print the JSON string representation of the object
print(WebhookMessageRealtimeSessionStateChangedpayloadSession.to_json())

# convert the object into a dict
webhook_message_realtime_session_state_changedpayload_session_dict = webhook_message_realtime_session_state_changedpayload_session_instance.to_dict()
# create an instance of WebhookMessageRealtimeSessionStateChangedpayloadSession from a dict
webhook_message_realtime_session_state_changedpayload_session_from_dict = WebhookMessageRealtimeSessionStateChangedpayloadSession.from_dict(webhook_message_realtime_session_state_changedpayload_session_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


