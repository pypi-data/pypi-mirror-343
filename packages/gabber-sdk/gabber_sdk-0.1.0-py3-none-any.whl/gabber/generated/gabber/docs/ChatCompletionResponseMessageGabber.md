# ChatCompletionResponseMessageGabber

If the audio output modality is requested, this object contains data

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**voice** | [**ChatCompletionResponseMessageGabberVoice**](ChatCompletionResponseMessageGabberVoice.md) |  | [optional] 

## Example

```python
from gabber.generated.gabber.models.chat_completion_response_message_gabber import ChatCompletionResponseMessageGabber

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionResponseMessageGabber from a JSON string
chat_completion_response_message_gabber_instance = ChatCompletionResponseMessageGabber.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionResponseMessageGabber.to_json())

# convert the object into a dict
chat_completion_response_message_gabber_dict = chat_completion_response_message_gabber_instance.to_dict()
# create an instance of ChatCompletionResponseMessageGabber from a dict
chat_completion_response_message_gabber_from_dict = ChatCompletionResponseMessageGabber.from_dict(chat_completion_response_message_gabber_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


