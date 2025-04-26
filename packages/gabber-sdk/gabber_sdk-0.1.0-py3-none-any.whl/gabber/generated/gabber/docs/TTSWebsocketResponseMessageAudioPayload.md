# TTSWebsocketResponseMessageAudioPayload


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**audio** | **str** | The audio data in base64 format. | 
**sample_rate** | **int** | The sample rate of the audio data. | 
**channels** | **int** | The number of channels in the audio data. | 
**audio_format** | **str** | The format of the audio data. | 
**encoding** | **str** | The encoding of the audio data. | 

## Example

```python
from gabber.generated.gabber.models.tts_websocket_response_message_audio_payload import TTSWebsocketResponseMessageAudioPayload

# TODO update the JSON string below
json = "{}"
# create an instance of TTSWebsocketResponseMessageAudioPayload from a JSON string
tts_websocket_response_message_audio_payload_instance = TTSWebsocketResponseMessageAudioPayload.from_json(json)
# print the JSON string representation of the object
print(TTSWebsocketResponseMessageAudioPayload.to_json())

# convert the object into a dict
tts_websocket_response_message_audio_payload_dict = tts_websocket_response_message_audio_payload_instance.to_dict()
# create an instance of TTSWebsocketResponseMessageAudioPayload from a dict
tts_websocket_response_message_audio_payload_from_dict = TTSWebsocketResponseMessageAudioPayload.from_dict(tts_websocket_response_message_audio_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


