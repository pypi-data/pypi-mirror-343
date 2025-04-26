# AttachLivekitRoom200ResponseConfigInput

Configuration for the output of the RealtimeSession.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**interruptable** | **bool** | Whether the system allows interruption during speech. | [default to True]
**parallel_listening** | **bool** | Whether the AI should continue listening while speaking. If true, the AI will produce another response immediately after the first one. This is only relevant if interruptable is false.  | [default to False]

## Example

```python
from gabber.generated.gabber_internal.models.attach_livekit_room200_response_config_input import AttachLivekitRoom200ResponseConfigInput

# TODO update the JSON string below
json = "{}"
# create an instance of AttachLivekitRoom200ResponseConfigInput from a JSON string
attach_livekit_room200_response_config_input_instance = AttachLivekitRoom200ResponseConfigInput.from_json(json)
# print the JSON string representation of the object
print(AttachLivekitRoom200ResponseConfigInput.to_json())

# convert the object into a dict
attach_livekit_room200_response_config_input_dict = attach_livekit_room200_response_config_input_instance.to_dict()
# create an instance of AttachLivekitRoom200ResponseConfigInput from a dict
attach_livekit_room200_response_config_input_from_dict = AttachLivekitRoom200ResponseConfigInput.from_dict(attach_livekit_room200_response_config_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


