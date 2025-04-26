# AttachLivekitRoom200ResponseConfigGenerativeToolDefinitionsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**name** | **str** |  | 
**description** | **str** |  | 
**parameters** | [**List[AttachLivekitRoom200ResponseConfigGenerativeToolDefinitionsInnerParametersInner]**](AttachLivekitRoom200ResponseConfigGenerativeToolDefinitionsInnerParametersInner.md) |  | 
**call_settings** | [**AttachLivekitRoom200ResponseConfigGenerativeToolDefinitionsInnerCallSettings**](AttachLivekitRoom200ResponseConfigGenerativeToolDefinitionsInnerCallSettings.md) |  | 

## Example

```python
from gabber.generated.gabber_internal.models.attach_livekit_room200_response_config_generative_tool_definitions_inner import AttachLivekitRoom200ResponseConfigGenerativeToolDefinitionsInner

# TODO update the JSON string below
json = "{}"
# create an instance of AttachLivekitRoom200ResponseConfigGenerativeToolDefinitionsInner from a JSON string
attach_livekit_room200_response_config_generative_tool_definitions_inner_instance = AttachLivekitRoom200ResponseConfigGenerativeToolDefinitionsInner.from_json(json)
# print the JSON string representation of the object
print(AttachLivekitRoom200ResponseConfigGenerativeToolDefinitionsInner.to_json())

# convert the object into a dict
attach_livekit_room200_response_config_generative_tool_definitions_inner_dict = attach_livekit_room200_response_config_generative_tool_definitions_inner_instance.to_dict()
# create an instance of AttachLivekitRoom200ResponseConfigGenerativeToolDefinitionsInner from a dict
attach_livekit_room200_response_config_generative_tool_definitions_inner_from_dict = AttachLivekitRoom200ResponseConfigGenerativeToolDefinitionsInner.from_dict(attach_livekit_room200_response_config_generative_tool_definitions_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


