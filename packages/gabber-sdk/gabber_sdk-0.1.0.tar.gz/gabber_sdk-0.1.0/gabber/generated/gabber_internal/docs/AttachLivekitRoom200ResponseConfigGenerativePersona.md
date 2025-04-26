# AttachLivekitRoom200ResponseConfigGenerativePersona


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** |  | 
**description** | **str** |  | 
**id** | **str** |  | 
**image_url** | **str** |  | [optional] 
**name** | **str** |  | 
**project** | **str** |  | 
**human** | **str** |  | [optional] 
**gender** | **str** |  | [optional] 
**tags** | [**List[AttachLivekitRoom200ResponseConfigGenerativePersonaTagsInner]**](AttachLivekitRoom200ResponseConfigGenerativePersonaTagsInner.md) |  | [optional] 
**voice** | **str** |  | 

## Example

```python
from gabber.generated.gabber_internal.models.attach_livekit_room200_response_config_generative_persona import AttachLivekitRoom200ResponseConfigGenerativePersona

# TODO update the JSON string below
json = "{}"
# create an instance of AttachLivekitRoom200ResponseConfigGenerativePersona from a JSON string
attach_livekit_room200_response_config_generative_persona_instance = AttachLivekitRoom200ResponseConfigGenerativePersona.from_json(json)
# print the JSON string representation of the object
print(AttachLivekitRoom200ResponseConfigGenerativePersona.to_json())

# convert the object into a dict
attach_livekit_room200_response_config_generative_persona_dict = attach_livekit_room200_response_config_generative_persona_instance.to_dict()
# create an instance of AttachLivekitRoom200ResponseConfigGenerativePersona from a dict
attach_livekit_room200_response_config_generative_persona_from_dict = AttachLivekitRoom200ResponseConfigGenerativePersona.from_dict(attach_livekit_room200_response_config_generative_persona_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


