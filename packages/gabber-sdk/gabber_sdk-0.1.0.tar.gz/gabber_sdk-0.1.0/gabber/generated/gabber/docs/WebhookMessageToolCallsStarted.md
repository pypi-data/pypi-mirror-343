# WebhookMessageToolCallsStarted


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**payload** | [**WebhookMessageToolCallsStartedPayload**](WebhookMessageToolCallsStartedPayload.md) |  | 

## Example

```python
from gabber.generated.gabber.models.webhook_message_tool_calls_started import WebhookMessageToolCallsStarted

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookMessageToolCallsStarted from a JSON string
webhook_message_tool_calls_started_instance = WebhookMessageToolCallsStarted.from_json(json)
# print the JSON string representation of the object
print(WebhookMessageToolCallsStarted.to_json())

# convert the object into a dict
webhook_message_tool_calls_started_dict = webhook_message_tool_calls_started_instance.to_dict()
# create an instance of WebhookMessageToolCallsStarted from a dict
webhook_message_tool_calls_started_from_dict = WebhookMessageToolCallsStarted.from_dict(webhook_message_tool_calls_started_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


