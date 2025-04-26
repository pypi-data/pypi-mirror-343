# TTSWebsocketResponseMessageErrorPayload


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** | The error message. | 

## Example

```python
from gabber.generated.gabber.models.tts_websocket_response_message_error_payload import TTSWebsocketResponseMessageErrorPayload

# TODO update the JSON string below
json = "{}"
# create an instance of TTSWebsocketResponseMessageErrorPayload from a JSON string
tts_websocket_response_message_error_payload_instance = TTSWebsocketResponseMessageErrorPayload.from_json(json)
# print the JSON string representation of the object
print(TTSWebsocketResponseMessageErrorPayload.to_json())

# convert the object into a dict
tts_websocket_response_message_error_payload_dict = tts_websocket_response_message_error_payload_instance.to_dict()
# create an instance of TTSWebsocketResponseMessageErrorPayload from a dict
tts_websocket_response_message_error_payload_from_dict = TTSWebsocketResponseMessageErrorPayload.from_dict(tts_websocket_response_message_error_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


