# TTSWebsocketRequestMessage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | [**TTSWebsocketRequestMessageType**](TTSWebsocketRequestMessageType.md) |  | 
**session** | **str** | The session ID for the TTS session. | 
**payload** | [**TTSWebsocketRequestMessagePayload**](TTSWebsocketRequestMessagePayload.md) |  | 

## Example

```python
from gabber.generated.gabber.models.tts_websocket_request_message import TTSWebsocketRequestMessage

# TODO update the JSON string below
json = "{}"
# create an instance of TTSWebsocketRequestMessage from a JSON string
tts_websocket_request_message_instance = TTSWebsocketRequestMessage.from_json(json)
# print the JSON string representation of the object
print(TTSWebsocketRequestMessage.to_json())

# convert the object into a dict
tts_websocket_request_message_dict = tts_websocket_request_message_instance.to_dict()
# create an instance of TTSWebsocketRequestMessage from a dict
tts_websocket_request_message_from_dict = TTSWebsocketRequestMessage.from_dict(tts_websocket_request_message_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


