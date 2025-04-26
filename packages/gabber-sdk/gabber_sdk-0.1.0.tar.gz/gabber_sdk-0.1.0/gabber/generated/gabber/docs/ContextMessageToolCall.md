# ContextMessageToolCall


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**type** | **str** |  | 
**function** | [**ContextMessageToolCallFunction**](ContextMessageToolCallFunction.md) |  | 

## Example

```python
from gabber.generated.gabber.models.context_message_tool_call import ContextMessageToolCall

# TODO update the JSON string below
json = "{}"
# create an instance of ContextMessageToolCall from a JSON string
context_message_tool_call_instance = ContextMessageToolCall.from_json(json)
# print the JSON string representation of the object
print(ContextMessageToolCall.to_json())

# convert the object into a dict
context_message_tool_call_dict = context_message_tool_call_instance.to_dict()
# create an instance of ContextMessageToolCall from a dict
context_message_tool_call_from_dict = ContextMessageToolCall.from_dict(context_message_tool_call_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


