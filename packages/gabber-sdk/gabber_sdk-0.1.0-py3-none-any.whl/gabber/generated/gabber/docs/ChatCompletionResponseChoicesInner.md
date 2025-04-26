# ChatCompletionResponseChoicesInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | [**ChatCompletionResponseMessage**](ChatCompletionResponseMessage.md) |  | 

## Example

```python
from gabber.generated.gabber.models.chat_completion_response_choices_inner import ChatCompletionResponseChoicesInner

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionResponseChoicesInner from a JSON string
chat_completion_response_choices_inner_instance = ChatCompletionResponseChoicesInner.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionResponseChoicesInner.to_json())

# convert the object into a dict
chat_completion_response_choices_inner_dict = chat_completion_response_choices_inner_instance.to_dict()
# create an instance of ChatCompletionResponseChoicesInner from a dict
chat_completion_response_choices_inner_from_dict = ChatCompletionResponseChoicesInner.from_dict(chat_completion_response_choices_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


