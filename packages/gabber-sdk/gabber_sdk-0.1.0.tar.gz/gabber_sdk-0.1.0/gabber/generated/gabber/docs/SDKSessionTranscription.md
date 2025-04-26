# SDKSessionTranscription


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**agent** | **bool** |  | 
**final** | **bool** |  | 
**created_at** | **datetime** |  | 
**speaking_ended_at** | **datetime** |  | 
**text** | **str** |  | 
**tool_calls** | [**List[ContextMessageToolCall]**](ContextMessageToolCall.md) |  | [optional] 

## Example

```python
from gabber.generated.gabber.models.sdk_session_transcription import SDKSessionTranscription

# TODO update the JSON string below
json = "{}"
# create an instance of SDKSessionTranscription from a JSON string
sdk_session_transcription_instance = SDKSessionTranscription.from_json(json)
# print the JSON string representation of the object
print(SDKSessionTranscription.to_json())

# convert the object into a dict
sdk_session_transcription_dict = sdk_session_transcription_instance.to_dict()
# create an instance of SDKSessionTranscription from a dict
sdk_session_transcription_from_dict = SDKSessionTranscription.from_dict(sdk_session_transcription_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


