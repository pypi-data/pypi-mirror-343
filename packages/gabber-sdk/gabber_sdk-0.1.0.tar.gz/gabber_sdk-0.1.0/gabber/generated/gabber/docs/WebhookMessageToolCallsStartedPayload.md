# WebhookMessageToolCallsStartedPayload


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**realtime_session** | **str** |  | [optional] 
**group** | **str** |  | 
**tool_calls** | [**List[WebhookMessageToolCall]**](WebhookMessageToolCall.md) |  | 

## Example

```python
from gabber.generated.gabber.models.webhook_message_tool_calls_started_payload import WebhookMessageToolCallsStartedPayload

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookMessageToolCallsStartedPayload from a JSON string
webhook_message_tool_calls_started_payload_instance = WebhookMessageToolCallsStartedPayload.from_json(json)
# print the JSON string representation of the object
print(WebhookMessageToolCallsStartedPayload.to_json())

# convert the object into a dict
webhook_message_tool_calls_started_payload_dict = webhook_message_tool_calls_started_payload_instance.to_dict()
# create an instance of WebhookMessageToolCallsStartedPayload from a dict
webhook_message_tool_calls_started_payload_from_dict = WebhookMessageToolCallsStartedPayload.from_dict(webhook_message_tool_calls_started_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


