# WebhookMessageToolCallFunction


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the function to call. | 
**arguments** | **object** | The named arguments to call the function with the function was called with | 

## Example

```python
from gabber.generated.gabber.models.webhook_message_tool_call_function import WebhookMessageToolCallFunction

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookMessageToolCallFunction from a JSON string
webhook_message_tool_call_function_instance = WebhookMessageToolCallFunction.from_json(json)
# print the JSON string representation of the object
print(WebhookMessageToolCallFunction.to_json())

# convert the object into a dict
webhook_message_tool_call_function_dict = webhook_message_tool_call_function_instance.to_dict()
# create an instance of WebhookMessageToolCallFunction from a dict
webhook_message_tool_call_function_from_dict = WebhookMessageToolCallFunction.from_dict(webhook_message_tool_call_function_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


