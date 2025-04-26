# AttachLivekitRoom200ResponseConfigGenerative

Configuration for the generative AI in the RealtimeSession.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**llm** | [**AttachLivekitRoom200ResponseConfigGenerativeLlm**](AttachLivekitRoom200ResponseConfigGenerativeLlm.md) |  | 
**voice_override** | [**AttachLivekitRoom200ResponseConfigGenerativeVoiceOverride**](AttachLivekitRoom200ResponseConfigGenerativeVoiceOverride.md) |  | [optional] 
**persona** | [**AttachLivekitRoom200ResponseConfigGenerativePersona**](AttachLivekitRoom200ResponseConfigGenerativePersona.md) |  | [optional] 
**scenario** | [**AttachLivekitRoom200ResponseConfigGenerativeScenario**](AttachLivekitRoom200ResponseConfigGenerativeScenario.md) |  | [optional] 
**context** | [**AttachLivekitRoom200ResponseConfigGenerativeContext**](AttachLivekitRoom200ResponseConfigGenerativeContext.md) |  | 
**tool_definitions** | [**List[AttachLivekitRoom200ResponseConfigGenerativeToolDefinitionsInner]**](AttachLivekitRoom200ResponseConfigGenerativeToolDefinitionsInner.md) | The tool definitions to use for the generative AI. | 
**extra** | **Dict[str, object]** | Extra configuration for the generative AI. Usually this is for internal purposes. | [optional] 

## Example

```python
from gabber.generated.gabber_internal.models.attach_livekit_room200_response_config_generative import AttachLivekitRoom200ResponseConfigGenerative

# TODO update the JSON string below
json = "{}"
# create an instance of AttachLivekitRoom200ResponseConfigGenerative from a JSON string
attach_livekit_room200_response_config_generative_instance = AttachLivekitRoom200ResponseConfigGenerative.from_json(json)
# print the JSON string representation of the object
print(AttachLivekitRoom200ResponseConfigGenerative.to_json())

# convert the object into a dict
attach_livekit_room200_response_config_generative_dict = attach_livekit_room200_response_config_generative_instance.to_dict()
# create an instance of AttachLivekitRoom200ResponseConfigGenerative from a dict
attach_livekit_room200_response_config_generative_from_dict = AttachLivekitRoom200ResponseConfigGenerative.from_dict(attach_livekit_room200_response_config_generative_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


