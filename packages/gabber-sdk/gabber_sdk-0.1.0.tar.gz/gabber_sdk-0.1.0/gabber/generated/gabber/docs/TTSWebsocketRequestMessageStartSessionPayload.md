# TTSWebsocketRequestMessageStartSessionPayload


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**voice** | **str** | The voice to use for the session. | 

## Example

```python
from gabber.generated.gabber.models.tts_websocket_request_message_start_session_payload import TTSWebsocketRequestMessageStartSessionPayload

# TODO update the JSON string below
json = "{}"
# create an instance of TTSWebsocketRequestMessageStartSessionPayload from a JSON string
tts_websocket_request_message_start_session_payload_instance = TTSWebsocketRequestMessageStartSessionPayload.from_json(json)
# print the JSON string representation of the object
print(TTSWebsocketRequestMessageStartSessionPayload.to_json())

# convert the object into a dict
tts_websocket_request_message_start_session_payload_dict = tts_websocket_request_message_start_session_payload_instance.to_dict()
# create an instance of TTSWebsocketRequestMessageStartSessionPayload from a dict
tts_websocket_request_message_start_session_payload_from_dict = TTSWebsocketRequestMessageStartSessionPayload.from_dict(tts_websocket_request_message_start_session_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


