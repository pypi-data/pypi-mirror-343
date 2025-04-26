# UpdateVoiceRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**language** | **str** | The language of the voice | 
**tags** | **List[str]** | Tags to associate with this voice | [optional] 

## Example

```python
from gabber.generated.gabber.models.update_voice_request import UpdateVoiceRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateVoiceRequest from a JSON string
update_voice_request_instance = UpdateVoiceRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateVoiceRequest.to_json())

# convert the object into a dict
update_voice_request_dict = update_voice_request_instance.to_dict()
# create an instance of UpdateVoiceRequest from a dict
update_voice_request_from_dict = UpdateVoiceRequest.from_dict(update_voice_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


