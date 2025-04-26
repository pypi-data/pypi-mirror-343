# ChatCompletionStreamResponseDeltaGabber

If the audio output modality is requested, this object contains data

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**voice** | [**ChatCompletionStreamResponseDeltaGabberVoice**](ChatCompletionStreamResponseDeltaGabberVoice.md) |  | [optional] 

## Example

```python
from gabber.generated.gabber.models.chat_completion_stream_response_delta_gabber import ChatCompletionStreamResponseDeltaGabber

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionStreamResponseDeltaGabber from a JSON string
chat_completion_stream_response_delta_gabber_instance = ChatCompletionStreamResponseDeltaGabber.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionStreamResponseDeltaGabber.to_json())

# convert the object into a dict
chat_completion_stream_response_delta_gabber_dict = chat_completion_stream_response_delta_gabber_instance.to_dict()
# create an instance of ChatCompletionStreamResponseDeltaGabber from a dict
chat_completion_stream_response_delta_gabber_from_dict = ChatCompletionStreamResponseDeltaGabber.from_dict(chat_completion_stream_response_delta_gabber_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


