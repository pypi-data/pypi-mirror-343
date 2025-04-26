# RealtimeSessionGenerativeConfig

Configuration for the generative AI in the RealtimeSession.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**llm** | [**LLM**](LLM.md) |  | 
**voice_override** | [**Voice**](Voice.md) |  | [optional] 
**persona** | [**Persona**](Persona.md) |  | [optional] 
**scenario** | [**Scenario**](Scenario.md) |  | [optional] 
**context** | [**Context**](Context.md) |  | 
**tool_definitions** | [**List[ToolDefinition]**](ToolDefinition.md) | The tool definitions to use for the generative AI. | 
**extra** | **object** | Extra configuration for the generative AI. Usually this is for internal purposes. | [optional] 

## Example

```python
from gabber.generated.gabber.models.realtime_session_generative_config import RealtimeSessionGenerativeConfig

# TODO update the JSON string below
json = "{}"
# create an instance of RealtimeSessionGenerativeConfig from a JSON string
realtime_session_generative_config_instance = RealtimeSessionGenerativeConfig.from_json(json)
# print the JSON string representation of the object
print(RealtimeSessionGenerativeConfig.to_json())

# convert the object into a dict
realtime_session_generative_config_dict = realtime_session_generative_config_instance.to_dict()
# create an instance of RealtimeSessionGenerativeConfig from a dict
realtime_session_generative_config_from_dict = RealtimeSessionGenerativeConfig.from_dict(realtime_session_generative_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


