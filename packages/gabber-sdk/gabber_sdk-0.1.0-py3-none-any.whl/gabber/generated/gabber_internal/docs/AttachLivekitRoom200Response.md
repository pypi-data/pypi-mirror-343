# AttachLivekitRoom200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The unique identifier of the RealtimeSession. | 
**state** | **str** | The current state of the RealtimeSession. | 
**created_at** | **datetime** | The time the RealtimeSession was created. | 
**ended_at** | **datetime** | The time the RealtimeSession ended. | [optional] 
**project** | **str** | The project identifier. | 
**human** | **str** | The human identifier. | [optional] 
**simulated** | **bool** | Whether the session is simulated or not. | 
**config** | [**AttachLivekitRoom200ResponseConfig**](AttachLivekitRoom200ResponseConfig.md) |  | 
**data** | [**List[AttachLivekitRoom200ResponseDataInner]**](AttachLivekitRoom200ResponseDataInner.md) |  | 
**extra** | **Dict[str, object]** | Extra configuration for the RealtimeSession. Usually this is for internal purposes. | [optional] 

## Example

```python
from gabber.generated.gabber_internal.models.attach_livekit_room200_response import AttachLivekitRoom200Response

# TODO update the JSON string below
json = "{}"
# create an instance of AttachLivekitRoom200Response from a JSON string
attach_livekit_room200_response_instance = AttachLivekitRoom200Response.from_json(json)
# print the JSON string representation of the object
print(AttachLivekitRoom200Response.to_json())

# convert the object into a dict
attach_livekit_room200_response_dict = attach_livekit_room200_response_instance.to_dict()
# create an instance of AttachLivekitRoom200Response from a dict
attach_livekit_room200_response_from_dict = AttachLivekitRoom200Response.from_dict(attach_livekit_room200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


