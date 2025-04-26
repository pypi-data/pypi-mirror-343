# ChatCompletionRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**messages** | [**List[ChatCompletionRequestMessage]**](ChatCompletionRequestMessage.md) | Chat context | 
**model** | **str** | Gabber llm_id | 
**metadata** | **object** |  | [optional] 
**gabber** | [**ChatCompletionRequestGabber**](ChatCompletionRequestGabber.md) |  | [optional] 
**stream** | **bool** | If set, partial message deltas will be sent, like in ChatGPT.  | [optional] [default to False]
**temperature** | **float** | Temperature for sampling from the model. Higher values mean more randomness.  | [optional] 
**max_tokens** | **int** | Maximum number of tokens to generate. Requests can be up to 4096 tokens.  | [optional] 
**tools** | [**List[ChatCompletionTool]**](ChatCompletionTool.md) | List of tools to call during the completion. Each tool will be called in the order they are listed.  | [optional] 
**tool_choice** | [**ChatCompletionToolChoiceOption**](ChatCompletionToolChoiceOption.md) |  | [optional] 
**parallel_tool_calls** | **bool** | Whether to enable parallel function calling | [optional] [default to True]

## Example

```python
from gabber.generated.gabber.models.chat_completion_request import ChatCompletionRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionRequest from a JSON string
chat_completion_request_instance = ChatCompletionRequest.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionRequest.to_json())

# convert the object into a dict
chat_completion_request_dict = chat_completion_request_instance.to_dict()
# create an instance of ChatCompletionRequest from a dict
chat_completion_request_from_dict = ChatCompletionRequest.from_dict(chat_completion_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


