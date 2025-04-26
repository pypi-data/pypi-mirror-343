# AttachLivekitRoom200ResponseConfigOutput

Configuration for the output of the RealtimeSession.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**stream_transcript** | **bool** | Whether to stream agent spoken transcript or send full transcript when it&#39;s available all at once. | 
**speech_synthesis_enabled** | **bool** | Whether to enable speech synthesis for the RealtimeSession. | [default to True]
**answer_message** | **str** | The message for the agent to speak first when the human joins. If exluded the agent will not speak first. | [optional] 

## Example

```python
from gabber.generated.gabber_internal.models.attach_livekit_room200_response_config_output import AttachLivekitRoom200ResponseConfigOutput

# TODO update the JSON string below
json = "{}"
# create an instance of AttachLivekitRoom200ResponseConfigOutput from a JSON string
attach_livekit_room200_response_config_output_instance = AttachLivekitRoom200ResponseConfigOutput.from_json(json)
# print the JSON string representation of the object
print(AttachLivekitRoom200ResponseConfigOutput.to_json())

# convert the object into a dict
attach_livekit_room200_response_config_output_dict = attach_livekit_room200_response_config_output_instance.to_dict()
# create an instance of AttachLivekitRoom200ResponseConfigOutput from a dict
attach_livekit_room200_response_config_output_from_dict = AttachLivekitRoom200ResponseConfigOutput.from_dict(attach_livekit_room200_response_config_output_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


