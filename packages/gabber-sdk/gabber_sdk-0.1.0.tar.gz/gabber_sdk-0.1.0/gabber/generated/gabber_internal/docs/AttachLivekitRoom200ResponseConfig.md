# AttachLivekitRoom200ResponseConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**general** | [**AttachLivekitRoom200ResponseConfigGeneral**](AttachLivekitRoom200ResponseConfigGeneral.md) |  | 
**input** | [**AttachLivekitRoom200ResponseConfigInput**](AttachLivekitRoom200ResponseConfigInput.md) |  | 
**generative** | [**AttachLivekitRoom200ResponseConfigGenerative**](AttachLivekitRoom200ResponseConfigGenerative.md) |  | 
**output** | [**AttachLivekitRoom200ResponseConfigOutput**](AttachLivekitRoom200ResponseConfigOutput.md) |  | 

## Example

```python
from gabber.generated.gabber_internal.models.attach_livekit_room200_response_config import AttachLivekitRoom200ResponseConfig

# TODO update the JSON string below
json = "{}"
# create an instance of AttachLivekitRoom200ResponseConfig from a JSON string
attach_livekit_room200_response_config_instance = AttachLivekitRoom200ResponseConfig.from_json(json)
# print the JSON string representation of the object
print(AttachLivekitRoom200ResponseConfig.to_json())

# convert the object into a dict
attach_livekit_room200_response_config_dict = attach_livekit_room200_response_config_instance.to_dict()
# create an instance of AttachLivekitRoom200ResponseConfig from a dict
attach_livekit_room200_response_config_from_dict = AttachLivekitRoom200ResponseConfig.from_dict(attach_livekit_room200_response_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


