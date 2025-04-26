# DummyGet200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**webhook_message** | [**WebhookMessage**](WebhookMessage.md) |  | [optional] 
**tts_websocket_request_message** | [**TTSWebsocketRequestMessage**](TTSWebsocketRequestMessage.md) |  | [optional] 
**tts_websocket_response_message** | [**TTSWebsocketResponseMessage**](TTSWebsocketResponseMessage.md) |  | [optional] 

## Example

```python
from gabber.generated.gabber.models.dummy_get200_response import DummyGet200Response

# TODO update the JSON string below
json = "{}"
# create an instance of DummyGet200Response from a JSON string
dummy_get200_response_instance = DummyGet200Response.from_json(json)
# print the JSON string representation of the object
print(DummyGet200Response.to_json())

# convert the object into a dict
dummy_get200_response_dict = dummy_get200_response_instance.to_dict()
# create an instance of DummyGet200Response from a dict
dummy_get200_response_from_dict = DummyGet200Response.from_dict(dummy_get200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


