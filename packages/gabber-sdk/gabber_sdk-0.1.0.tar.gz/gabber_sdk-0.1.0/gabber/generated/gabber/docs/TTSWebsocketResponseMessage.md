# TTSWebsocketResponseMessage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | [**TTSWebsocketResponseMessageType**](TTSWebsocketResponseMessageType.md) |  | 
**session** | **str** | The session ID for the TTS session. | 
**payload** | [**TTSWebsocketResponseMessagePayload**](TTSWebsocketResponseMessagePayload.md) |  | 

## Example

```python
from gabber.generated.gabber.models.tts_websocket_response_message import TTSWebsocketResponseMessage

# TODO update the JSON string below
json = "{}"
# create an instance of TTSWebsocketResponseMessage from a JSON string
tts_websocket_response_message_instance = TTSWebsocketResponseMessage.from_json(json)
# print the JSON string representation of the object
print(TTSWebsocketResponseMessage.to_json())

# convert the object into a dict
tts_websocket_response_message_dict = tts_websocket_response_message_instance.to_dict()
# create an instance of TTSWebsocketResponseMessage from a dict
tts_websocket_response_message_from_dict = TTSWebsocketResponseMessage.from_dict(tts_websocket_response_message_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


