# WebhookMessageToolCallsFinished


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**payload** | [**WebhookMessageToolCallsFinishedPayload**](WebhookMessageToolCallsFinishedPayload.md) |  | 

## Example

```python
from gabber.generated.gabber.models.webhook_message_tool_calls_finished import WebhookMessageToolCallsFinished

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookMessageToolCallsFinished from a JSON string
webhook_message_tool_calls_finished_instance = WebhookMessageToolCallsFinished.from_json(json)
# print the JSON string representation of the object
print(WebhookMessageToolCallsFinished.to_json())

# convert the object into a dict
webhook_message_tool_calls_finished_dict = webhook_message_tool_calls_finished_instance.to_dict()
# create an instance of WebhookMessageToolCallsFinished from a dict
webhook_message_tool_calls_finished_from_dict = WebhookMessageToolCallsFinished.from_dict(webhook_message_tool_calls_finished_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


