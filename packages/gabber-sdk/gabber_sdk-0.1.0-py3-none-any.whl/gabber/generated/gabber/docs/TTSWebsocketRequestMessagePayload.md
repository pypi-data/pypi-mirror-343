# TTSWebsocketRequestMessagePayload


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**voice** | **str** | The voice to use for the session. | 
**text** | **str** | The text to push to the session. | 

## Example

```python
from gabber.generated.gabber.models.tts_websocket_request_message_payload import TTSWebsocketRequestMessagePayload

# TODO update the JSON string below
json = "{}"
# create an instance of TTSWebsocketRequestMessagePayload from a JSON string
tts_websocket_request_message_payload_instance = TTSWebsocketRequestMessagePayload.from_json(json)
# print the JSON string representation of the object
print(TTSWebsocketRequestMessagePayload.to_json())

# convert the object into a dict
tts_websocket_request_message_payload_dict = tts_websocket_request_message_payload_instance.to_dict()
# create an instance of TTSWebsocketRequestMessagePayload from a dict
tts_websocket_request_message_payload_from_dict = TTSWebsocketRequestMessagePayload.from_dict(tts_websocket_request_message_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


