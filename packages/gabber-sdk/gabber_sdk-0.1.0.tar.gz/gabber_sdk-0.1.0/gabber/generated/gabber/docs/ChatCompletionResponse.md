# ChatCompletionResponse

Represents a completion response from the API. Note: both the streamed and non-streamed response objects share the same shape. 

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**choices** | [**List[ChatCompletionResponseChoicesInner]**](ChatCompletionResponseChoicesInner.md) | A list of chat completion choices. | 
**model** | **str** | The model used for completion. | 
**gabber** | [**ChatCompletionResponseGabber**](ChatCompletionResponseGabber.md) |  | [optional] 

## Example

```python
from gabber.generated.gabber.models.chat_completion_response import ChatCompletionResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionResponse from a JSON string
chat_completion_response_instance = ChatCompletionResponse.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionResponse.to_json())

# convert the object into a dict
chat_completion_response_dict = chat_completion_response_instance.to_dict()
# create an instance of ChatCompletionResponse from a dict
chat_completion_response_from_dict = ChatCompletionResponse.from_dict(chat_completion_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


