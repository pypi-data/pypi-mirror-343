# WebhookMessageRealtimeSessionTimeLimitExceeded


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**payload** | [**WebhookMessageRealtimeSessionTimeLimitExceededPayload**](WebhookMessageRealtimeSessionTimeLimitExceededPayload.md) |  | 

## Example

```python
from gabber.generated.gabber.models.webhook_message_realtime_session_time_limit_exceeded import WebhookMessageRealtimeSessionTimeLimitExceeded

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookMessageRealtimeSessionTimeLimitExceeded from a JSON string
webhook_message_realtime_session_time_limit_exceeded_instance = WebhookMessageRealtimeSessionTimeLimitExceeded.from_json(json)
# print the JSON string representation of the object
print(WebhookMessageRealtimeSessionTimeLimitExceeded.to_json())

# convert the object into a dict
webhook_message_realtime_session_time_limit_exceeded_dict = webhook_message_realtime_session_time_limit_exceeded_instance.to_dict()
# create an instance of WebhookMessageRealtimeSessionTimeLimitExceeded from a dict
webhook_message_realtime_session_time_limit_exceeded_from_dict = WebhookMessageRealtimeSessionTimeLimitExceeded.from_dict(webhook_message_realtime_session_time_limit_exceeded_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


