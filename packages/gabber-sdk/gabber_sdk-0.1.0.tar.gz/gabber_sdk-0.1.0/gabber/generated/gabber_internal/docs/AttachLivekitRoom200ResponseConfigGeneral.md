# AttachLivekitRoom200ResponseConfigGeneral


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**time_limit_s** | **int** | The time limit in seconds for the RealtimeSession. | [optional] 
**save_messages** | **bool** | Whether to save messages in the RealtimeSession. These will be saved to the context provided in the generative config. If no context is provided, a new context will be created when the session starts.  | [default to True]

## Example

```python
from gabber.generated.gabber_internal.models.attach_livekit_room200_response_config_general import AttachLivekitRoom200ResponseConfigGeneral

# TODO update the JSON string below
json = "{}"
# create an instance of AttachLivekitRoom200ResponseConfigGeneral from a JSON string
attach_livekit_room200_response_config_general_instance = AttachLivekitRoom200ResponseConfigGeneral.from_json(json)
# print the JSON string representation of the object
print(AttachLivekitRoom200ResponseConfigGeneral.to_json())

# convert the object into a dict
attach_livekit_room200_response_config_general_dict = attach_livekit_room200_response_config_general_instance.to_dict()
# create an instance of AttachLivekitRoom200ResponseConfigGeneral from a dict
attach_livekit_room200_response_config_general_from_dict = AttachLivekitRoom200ResponseConfigGeneral.from_dict(attach_livekit_room200_response_config_general_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


