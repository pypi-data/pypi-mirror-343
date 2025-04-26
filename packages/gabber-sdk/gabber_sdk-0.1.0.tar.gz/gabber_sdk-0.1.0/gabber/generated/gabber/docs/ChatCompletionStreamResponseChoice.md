# ChatCompletionStreamResponseChoice


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**delta** | [**ChatCompletionStreamResponseDelta**](ChatCompletionStreamResponseDelta.md) |  | 
**finish_reason** | **str** | The reason the model stopped generating tokens. | 
**index** | **int** |  | 

## Example

```python
from gabber.generated.gabber.models.chat_completion_stream_response_choice import ChatCompletionStreamResponseChoice

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionStreamResponseChoice from a JSON string
chat_completion_stream_response_choice_instance = ChatCompletionStreamResponseChoice.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionStreamResponseChoice.to_json())

# convert the object into a dict
chat_completion_stream_response_choice_dict = chat_completion_stream_response_choice_instance.to_dict()
# create an instance of ChatCompletionStreamResponseChoice from a dict
chat_completion_stream_response_choice_from_dict = ChatCompletionStreamResponseChoice.from_dict(chat_completion_stream_response_choice_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


