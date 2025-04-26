# RealtimeLivekitAttachRequestConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**general** | [**AttachLivekitRoom200ResponseConfigGeneral**](AttachLivekitRoom200ResponseConfigGeneral.md) |  | 
**input** | [**AttachLivekitRoom200ResponseConfigInput**](AttachLivekitRoom200ResponseConfigInput.md) |  | 
**generative** | [**RealtimeLivekitAttachRequestConfigGenerative**](RealtimeLivekitAttachRequestConfigGenerative.md) |  | 
**output** | [**AttachLivekitRoom200ResponseConfigOutput**](AttachLivekitRoom200ResponseConfigOutput.md) |  | 

## Example

```python
from gabber.generated.gabber_internal.models.realtime_livekit_attach_request_config import RealtimeLivekitAttachRequestConfig

# TODO update the JSON string below
json = "{}"
# create an instance of RealtimeLivekitAttachRequestConfig from a JSON string
realtime_livekit_attach_request_config_instance = RealtimeLivekitAttachRequestConfig.from_json(json)
# print the JSON string representation of the object
print(RealtimeLivekitAttachRequestConfig.to_json())

# convert the object into a dict
realtime_livekit_attach_request_config_dict = realtime_livekit_attach_request_config_instance.to_dict()
# create an instance of RealtimeLivekitAttachRequestConfig from a dict
realtime_livekit_attach_request_config_from_dict = RealtimeLivekitAttachRequestConfig.from_dict(realtime_livekit_attach_request_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


