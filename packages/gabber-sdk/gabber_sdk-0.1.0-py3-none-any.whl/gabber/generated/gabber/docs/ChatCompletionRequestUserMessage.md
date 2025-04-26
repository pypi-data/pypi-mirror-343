# ChatCompletionRequestUserMessage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | [**ChatCompletionRequestUserMessageContent**](ChatCompletionRequestUserMessageContent.md) |  | 
**role** | **str** | The role of the messages author. | 

## Example

```python
from gabber.generated.gabber.models.chat_completion_request_user_message import ChatCompletionRequestUserMessage

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionRequestUserMessage from a JSON string
chat_completion_request_user_message_instance = ChatCompletionRequestUserMessage.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionRequestUserMessage.to_json())

# convert the object into a dict
chat_completion_request_user_message_dict = chat_completion_request_user_message_instance.to_dict()
# create an instance of ChatCompletionRequestUserMessage from a dict
chat_completion_request_user_message_from_dict = ChatCompletionRequestUserMessage.from_dict(chat_completion_request_user_message_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


