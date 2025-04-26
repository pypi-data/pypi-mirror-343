# ChatCompletionResponseGabberMessageData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message_index** | **int** |  | 
**content_index** | **int** |  | 
**type** | **str** |  | 
**data** | [**ChatCompletionResponseGabberMessageDataData**](ChatCompletionResponseGabberMessageDataData.md) |  | 

## Example

```python
from gabber.generated.gabber.models.chat_completion_response_gabber_message_data import ChatCompletionResponseGabberMessageData

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionResponseGabberMessageData from a JSON string
chat_completion_response_gabber_message_data_instance = ChatCompletionResponseGabberMessageData.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionResponseGabberMessageData.to_json())

# convert the object into a dict
chat_completion_response_gabber_message_data_dict = chat_completion_response_gabber_message_data_instance.to_dict()
# create an instance of ChatCompletionResponseGabberMessageData from a dict
chat_completion_response_gabber_message_data_from_dict = ChatCompletionResponseGabberMessageData.from_dict(chat_completion_response_gabber_message_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


