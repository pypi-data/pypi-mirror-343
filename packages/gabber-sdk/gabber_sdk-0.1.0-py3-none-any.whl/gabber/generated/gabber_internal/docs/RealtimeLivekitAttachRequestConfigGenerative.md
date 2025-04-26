# RealtimeLivekitAttachRequestConfigGenerative

Configuration for the generative AI in the RealtimeSession.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**llm** | **str** | The LLM to use for the RealtimeSession. | 
**voice_override** | **str** | The voice to use for the RealtimeSession. | [optional] 
**persona** | **str** | The persona to use for the RealtimeSession. | [optional] 
**scenario** | **str** | The scenario to use for the RealtimeSession. | [optional] 
**context** | **str** | The context to use for the RealtimeSession. If unspecified, a new context will be created. | [optional] 
**tool_definitions** | **List[str]** | The tool definitions to use for the generative AI. | [optional] 
**extra** | **Dict[str, object]** | Extra configuration for the generative AI. Usually this is for internal purposes. | [optional] 

## Example

```python
from gabber.generated.gabber_internal.models.realtime_livekit_attach_request_config_generative import RealtimeLivekitAttachRequestConfigGenerative

# TODO update the JSON string below
json = "{}"
# create an instance of RealtimeLivekitAttachRequestConfigGenerative from a JSON string
realtime_livekit_attach_request_config_generative_instance = RealtimeLivekitAttachRequestConfigGenerative.from_json(json)
# print the JSON string representation of the object
print(RealtimeLivekitAttachRequestConfigGenerative.to_json())

# convert the object into a dict
realtime_livekit_attach_request_config_generative_dict = realtime_livekit_attach_request_config_generative_instance.to_dict()
# create an instance of RealtimeLivekitAttachRequestConfigGenerative from a dict
realtime_livekit_attach_request_config_generative_from_dict = RealtimeLivekitAttachRequestConfigGenerative.from_dict(realtime_livekit_attach_request_config_generative_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


