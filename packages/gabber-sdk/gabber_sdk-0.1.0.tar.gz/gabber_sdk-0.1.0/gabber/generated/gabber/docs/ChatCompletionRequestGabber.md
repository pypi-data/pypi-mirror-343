# ChatCompletionRequestGabber


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**voice** | **str** | Gabber voice id | [optional] 
**context** | **str** | Gabber memory context id | [optional] 
**advanced_memory** | **bool** | When set to true, gabber will use it&#39;s advanced memory system to generate responses. A context must be set to enable this feature. | [optional] 

## Example

```python
from gabber.generated.gabber.models.chat_completion_request_gabber import ChatCompletionRequestGabber

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionRequestGabber from a JSON string
chat_completion_request_gabber_instance = ChatCompletionRequestGabber.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionRequestGabber.to_json())

# convert the object into a dict
chat_completion_request_gabber_dict = chat_completion_request_gabber_instance.to_dict()
# create an instance of ChatCompletionRequestGabber from a dict
chat_completion_request_gabber_from_dict = ChatCompletionRequestGabber.from_dict(chat_completion_request_gabber_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


