# Voice


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
**pricing** | [**VoicePricing**](VoicePricing.md) | Pricing details for this voice | 
**tags** | [**List[VoiceTag]**](VoiceTag.md) | Tags associated with this voice | 
**extra** | **object** | Extra configuration for the voice. Usually this is for internal purposes. | [optional] 

## Example

```python
from gabber.generated.gabber.models.voice import Voice

# TODO update the JSON string below
json = "{}"
# create an instance of Voice from a JSON string
voice_instance = Voice.from_json(json)
# print the JSON string representation of the object
print(Voice.to_json())

# convert the object into a dict
voice_dict = voice_instance.to_dict()
# create an instance of Voice from a dict
voice_from_dict = Voice.from_dict(voice_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


