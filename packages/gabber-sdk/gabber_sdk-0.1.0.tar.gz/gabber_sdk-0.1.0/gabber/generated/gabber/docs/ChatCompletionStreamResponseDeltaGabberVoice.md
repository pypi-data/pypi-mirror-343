# ChatCompletionStreamResponseDeltaGabberVoice


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**audio_url** | **str** | This will be the URL to the audio file | 
**expires_at** | **int** | The Unix timestamp (in seconds) when the audio file expires | 

## Example

```python
from gabber.generated.gabber.models.chat_completion_stream_response_delta_gabber_voice import ChatCompletionStreamResponseDeltaGabberVoice

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionStreamResponseDeltaGabberVoice from a JSON string
chat_completion_stream_response_delta_gabber_voice_instance = ChatCompletionStreamResponseDeltaGabberVoice.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionStreamResponseDeltaGabberVoice.to_json())

# convert the object into a dict
chat_completion_stream_response_delta_gabber_voice_dict = chat_completion_stream_response_delta_gabber_voice_instance.to_dict()
# create an instance of ChatCompletionStreamResponseDeltaGabberVoice from a dict
chat_completion_stream_response_delta_gabber_voice_from_dict = ChatCompletionStreamResponseDeltaGabberVoice.from_dict(chat_completion_stream_response_delta_gabber_voice_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


