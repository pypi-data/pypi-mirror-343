# ChatCompletionRequestSystemMessage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | [**ChatCompletionRequestSystemMessageContent**](ChatCompletionRequestSystemMessageContent.md) |  | 
**role** | **str** | The role of the messages author. | 

## Example

```python
from gabber.generated.gabber.models.chat_completion_request_system_message import ChatCompletionRequestSystemMessage

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionRequestSystemMessage from a JSON string
chat_completion_request_system_message_instance = ChatCompletionRequestSystemMessage.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionRequestSystemMessage.to_json())

# convert the object into a dict
chat_completion_request_system_message_dict = chat_completion_request_system_message_instance.to_dict()
# create an instance of ChatCompletionRequestSystemMessage from a dict
chat_completion_request_system_message_from_dict = ChatCompletionRequestSystemMessage.from_dict(chat_completion_request_system_message_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


