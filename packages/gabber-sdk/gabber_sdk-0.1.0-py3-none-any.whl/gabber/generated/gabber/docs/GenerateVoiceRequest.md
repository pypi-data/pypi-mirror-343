# GenerateVoiceRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**text** | **str** | Text to synthesize into voice | 
**voice_id** | **str** |  | 
**moderation** | **bool** | Whether to moderate the text. | [optional] 

## Example

```python
from gabber.generated.gabber.models.generate_voice_request import GenerateVoiceRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GenerateVoiceRequest from a JSON string
generate_voice_request_instance = GenerateVoiceRequest.from_json(json)
# print the JSON string representation of the object
print(GenerateVoiceRequest.to_json())

# convert the object into a dict
generate_voice_request_dict = generate_voice_request_instance.to_dict()
# create an instance of GenerateVoiceRequest from a dict
generate_voice_request_from_dict = GenerateVoiceRequest.from_dict(generate_voice_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


