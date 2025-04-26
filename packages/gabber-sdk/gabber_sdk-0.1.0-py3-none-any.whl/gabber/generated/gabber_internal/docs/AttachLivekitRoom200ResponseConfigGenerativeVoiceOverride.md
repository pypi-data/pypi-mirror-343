# AttachLivekitRoom200ResponseConfigGenerativeVoiceOverride


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** |  | 
**id** | **str** |  | 
**name** | **str** |  | 
**language** | **str** |  | 
**service** | **str** |  | [optional] 
**model** | **str** |  | [optional] 
**voice** | **str** |  | [optional] 
**embeddings** | **List[float]** |  | [optional] 
**cartesia_voice_id** | **str** |  | [optional] 
**elevenlabs_voice_id** | **str** |  | [optional] 
**project** | **str** |  | [optional] 
**human** | **str** |  | [optional] 
**preview_url** | **str** |  | [optional] 
**pricing** | [**AttachLivekitRoom200ResponseConfigGenerativeVoiceOverridePricing**](AttachLivekitRoom200ResponseConfigGenerativeVoiceOverridePricing.md) |  | 
**tags** | [**List[AttachLivekitRoom200ResponseConfigGenerativeVoiceOverrideTagsInner]**](AttachLivekitRoom200ResponseConfigGenerativeVoiceOverrideTagsInner.md) | Tags associated with this voice | 
**extra** | **Dict[str, object]** | Extra configuration for the voice. Usually this is for internal purposes. | [optional] 

## Example

```python
from gabber.generated.gabber_internal.models.attach_livekit_room200_response_config_generative_voice_override import AttachLivekitRoom200ResponseConfigGenerativeVoiceOverride

# TODO update the JSON string below
json = "{}"
# create an instance of AttachLivekitRoom200ResponseConfigGenerativeVoiceOverride from a JSON string
attach_livekit_room200_response_config_generative_voice_override_instance = AttachLivekitRoom200ResponseConfigGenerativeVoiceOverride.from_json(json)
# print the JSON string representation of the object
print(AttachLivekitRoom200ResponseConfigGenerativeVoiceOverride.to_json())

# convert the object into a dict
attach_livekit_room200_response_config_generative_voice_override_dict = attach_livekit_room200_response_config_generative_voice_override_instance.to_dict()
# create an instance of AttachLivekitRoom200ResponseConfigGenerativeVoiceOverride from a dict
attach_livekit_room200_response_config_generative_voice_override_from_dict = AttachLivekitRoom200ResponseConfigGenerativeVoiceOverride.from_dict(attach_livekit_room200_response_config_generative_voice_override_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


