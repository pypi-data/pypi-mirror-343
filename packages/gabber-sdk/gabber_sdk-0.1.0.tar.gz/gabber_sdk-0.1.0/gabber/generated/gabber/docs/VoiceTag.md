# VoiceTag


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Machine-readable tag name | 
**human_name** | **str** | Human-readable tag name for display | 

## Example

```python
from gabber.generated.gabber.models.voice_tag import VoiceTag

# TODO update the JSON string below
json = "{}"
# create an instance of VoiceTag from a JSON string
voice_tag_instance = VoiceTag.from_json(json)
# print the JSON string representation of the object
print(VoiceTag.to_json())

# convert the object into a dict
voice_tag_dict = voice_tag_instance.to_dict()
# create an instance of VoiceTag from a dict
voice_tag_from_dict = VoiceTag.from_dict(voice_tag_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


