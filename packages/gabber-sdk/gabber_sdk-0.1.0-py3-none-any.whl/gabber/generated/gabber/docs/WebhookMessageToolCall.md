# WebhookMessageToolCall


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**tool_definition_id** | **str** |  | 
**function** | [**WebhookMessageToolCallFunction**](WebhookMessageToolCallFunction.md) |  | 

## Example

```python
from gabber.generated.gabber.models.webhook_message_tool_call import WebhookMessageToolCall

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookMessageToolCall from a JSON string
webhook_message_tool_call_instance = WebhookMessageToolCall.from_json(json)
# print the JSON string representation of the object
print(WebhookMessageToolCall.to_json())

# convert the object into a dict
webhook_message_tool_call_dict = webhook_message_tool_call_instance.to_dict()
# create an instance of WebhookMessageToolCall from a dict
webhook_message_tool_call_from_dict = WebhookMessageToolCall.from_dict(webhook_message_tool_call_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


