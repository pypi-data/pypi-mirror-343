# RealtimeSessionGenerativeConfigUpdate

Configuration for the generative AI in the RealtimeSession.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**llm** | **str** | The LLM to use for the RealtimeSession. | [optional] 
**voice_override** | **str** | The voice to use for the RealtimeSession. | [optional] 
**persona** | **str** | The persona to use for the RealtimeSession. | [optional] 
**scenario** | **str** | The scenario to use for the RealtimeSession. | [optional] 
**context** | **str** | The context to use for the RealtimeSession. If unspecified, a new context will be created. | [optional] 
**tool_definitions** | **List[str]** | The tool definitions to use for the generative AI. | [optional] 
**extra** | **object** | Extra configuration for the generative AI. Usually this is for internal purposes. | [optional] 

## Example

```python
from gabber.generated.gabber.models.realtime_session_generative_config_update import RealtimeSessionGenerativeConfigUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of RealtimeSessionGenerativeConfigUpdate from a JSON string
realtime_session_generative_config_update_instance = RealtimeSessionGenerativeConfigUpdate.from_json(json)
# print the JSON string representation of the object
print(RealtimeSessionGenerativeConfigUpdate.to_json())

# convert the object into a dict
realtime_session_generative_config_update_dict = realtime_session_generative_config_update_instance.to_dict()
# create an instance of RealtimeSessionGenerativeConfigUpdate from a dict
realtime_session_generative_config_update_from_dict = RealtimeSessionGenerativeConfigUpdate.from_dict(realtime_session_generative_config_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


