# ContextMessageToolCallFunction


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**arguments** | **object** |  | 

## Example

```python
from gabber.generated.gabber.models.context_message_tool_call_function import ContextMessageToolCallFunction

# TODO update the JSON string below
json = "{}"
# create an instance of ContextMessageToolCallFunction from a JSON string
context_message_tool_call_function_instance = ContextMessageToolCallFunction.from_json(json)
# print the JSON string representation of the object
print(ContextMessageToolCallFunction.to_json())

# convert the object into a dict
context_message_tool_call_function_dict = context_message_tool_call_function_instance.to_dict()
# create an instance of ContextMessageToolCallFunction from a dict
context_message_tool_call_function_from_dict = ContextMessageToolCallFunction.from_dict(context_message_tool_call_function_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


