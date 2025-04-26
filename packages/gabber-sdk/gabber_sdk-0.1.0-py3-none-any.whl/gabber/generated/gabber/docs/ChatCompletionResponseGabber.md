# ChatCompletionResponseGabber

Gabber-specific fields

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**usage** | [**List[Usage]**](Usage.md) | Gabber usage for this request | 
**message_data** | [**List[ChatCompletionResponseGabberMessageData]**](ChatCompletionResponseGabberMessageData.md) |  | 
**advanced_memory** | [**ContextAdvancedMemoryQueryResult**](ContextAdvancedMemoryQueryResult.md) |  | [optional] 

## Example

```python
from gabber.generated.gabber.models.chat_completion_response_gabber import ChatCompletionResponseGabber

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionResponseGabber from a JSON string
chat_completion_response_gabber_instance = ChatCompletionResponseGabber.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionResponseGabber.to_json())

# convert the object into a dict
chat_completion_response_gabber_dict = chat_completion_response_gabber_instance.to_dict()
# create an instance of ChatCompletionResponseGabber from a dict
chat_completion_response_gabber_from_dict = ChatCompletionResponseGabber.from_dict(chat_completion_response_gabber_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


