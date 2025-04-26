# TTSWebsocketRequestMessagePushTextPayload


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**text** | **str** | The text to push to the session. | 

## Example

```python
from gabber.generated.gabber.models.tts_websocket_request_message_push_text_payload import TTSWebsocketRequestMessagePushTextPayload

# TODO update the JSON string below
json = "{}"
# create an instance of TTSWebsocketRequestMessagePushTextPayload from a JSON string
tts_websocket_request_message_push_text_payload_instance = TTSWebsocketRequestMessagePushTextPayload.from_json(json)
# print the JSON string representation of the object
print(TTSWebsocketRequestMessagePushTextPayload.to_json())

# convert the object into a dict
tts_websocket_request_message_push_text_payload_dict = tts_websocket_request_message_push_text_payload_instance.to_dict()
# create an instance of TTSWebsocketRequestMessagePushTextPayload from a dict
tts_websocket_request_message_push_text_payload_from_dict = TTSWebsocketRequestMessagePushTextPayload.from_dict(tts_websocket_request_message_push_text_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


