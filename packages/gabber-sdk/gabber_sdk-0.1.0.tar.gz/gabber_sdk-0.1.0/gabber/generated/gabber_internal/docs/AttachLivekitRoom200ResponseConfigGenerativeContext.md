# AttachLivekitRoom200ResponseConfigGenerativeContext


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**created_at** | **datetime** |  | 
**project** | **str** |  | 
**human** | **str** |  | [optional] 
**latest_messages** | [**List[AttachLivekitRoom200ResponseConfigGenerativeContextLatestMessagesInner]**](AttachLivekitRoom200ResponseConfigGenerativeContextLatestMessagesInner.md) |  | 

## Example

```python
from gabber.generated.gabber_internal.models.attach_livekit_room200_response_config_generative_context import AttachLivekitRoom200ResponseConfigGenerativeContext

# TODO update the JSON string below
json = "{}"
# create an instance of AttachLivekitRoom200ResponseConfigGenerativeContext from a JSON string
attach_livekit_room200_response_config_generative_context_instance = AttachLivekitRoom200ResponseConfigGenerativeContext.from_json(json)
# print the JSON string representation of the object
print(AttachLivekitRoom200ResponseConfigGenerativeContext.to_json())

# convert the object into a dict
attach_livekit_room200_response_config_generative_context_dict = attach_livekit_room200_response_config_generative_context_instance.to_dict()
# create an instance of AttachLivekitRoom200ResponseConfigGenerativeContext from a dict
attach_livekit_room200_response_config_generative_context_from_dict = AttachLivekitRoom200ResponseConfigGenerativeContext.from_dict(attach_livekit_room200_response_config_generative_context_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


