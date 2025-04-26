# ChatCompletionResponseMessageGabberVoice


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**audio_url** | **str** | This will be the URL to the audio file | 
**expires_at** | **int** | The Unix timestamp (in seconds) when the audio file expires | 

## Example

```python
from gabber.generated.gabber.models.chat_completion_response_message_gabber_voice import ChatCompletionResponseMessageGabberVoice

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionResponseMessageGabberVoice from a JSON string
chat_completion_response_message_gabber_voice_instance = ChatCompletionResponseMessageGabberVoice.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionResponseMessageGabberVoice.to_json())

# convert the object into a dict
chat_completion_response_message_gabber_voice_dict = chat_completion_response_message_gabber_voice_instance.to_dict()
# create an instance of ChatCompletionResponseMessageGabberVoice from a dict
chat_completion_response_message_gabber_voice_from_dict = ChatCompletionResponseMessageGabberVoice.from_dict(chat_completion_response_message_gabber_voice_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


