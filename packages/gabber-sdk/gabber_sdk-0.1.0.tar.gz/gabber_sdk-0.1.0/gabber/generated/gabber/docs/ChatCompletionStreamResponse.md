# ChatCompletionStreamResponse

Represents a streamed chunk of a chat completion response returned by model, based on the provided input.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | A unique identifier for the chat completion. Each chunk has the same ID. | 
**choices** | [**List[ChatCompletionStreamResponseChoice]**](ChatCompletionStreamResponseChoice.md) | A list of chat completion choices. Can contain more than one elements if &#x60;n&#x60; is greater than 1. Can also be empty for the last chunk if you set &#x60;stream_options: {\&quot;include_usage\&quot;: true}&#x60;.  | 
**created** | **int** | The Unix timestamp (in seconds) of when the chat completion was created. Each chunk has the same timestamp. | 
**model** | **str** | The model to generate the completion. | 
**object** | **str** | The object type, which is always &#x60;chat.completion.chunk&#x60;. | 
**gabber** | [**ChatCompletionResponseGabber**](ChatCompletionResponseGabber.md) |  | [optional] 

## Example

```python
from gabber.generated.gabber.models.chat_completion_stream_response import ChatCompletionStreamResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionStreamResponse from a JSON string
chat_completion_stream_response_instance = ChatCompletionStreamResponse.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionStreamResponse.to_json())

# convert the object into a dict
chat_completion_stream_response_dict = chat_completion_stream_response_instance.to_dict()
# create an instance of ChatCompletionStreamResponse from a dict
chat_completion_stream_response_from_dict = ChatCompletionStreamResponse.from_dict(chat_completion_stream_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


