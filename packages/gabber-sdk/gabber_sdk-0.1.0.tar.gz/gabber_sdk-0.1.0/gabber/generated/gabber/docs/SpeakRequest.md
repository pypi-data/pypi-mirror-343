# SpeakRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**text** | **str** | The text to be spoken by the agent. | 

## Example

```python
from gabber.generated.gabber.models.speak_request import SpeakRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SpeakRequest from a JSON string
speak_request_instance = SpeakRequest.from_json(json)
# print the JSON string representation of the object
print(SpeakRequest.to_json())

# convert the object into a dict
speak_request_dict = speak_request_instance.to_dict()
# create an instance of SpeakRequest from a dict
speak_request_from_dict = SpeakRequest.from_dict(speak_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


