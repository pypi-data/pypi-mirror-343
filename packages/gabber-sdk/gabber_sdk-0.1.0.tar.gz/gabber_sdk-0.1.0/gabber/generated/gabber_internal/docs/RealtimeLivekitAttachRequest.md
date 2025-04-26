# RealtimeLivekitAttachRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**config** | [**RealtimeLivekitAttachRequestConfig**](RealtimeLivekitAttachRequestConfig.md) |  | 
**livekit_room** | **str** |  | 
**data** | [**List[AttachLivekitRoom200ResponseDataInner]**](AttachLivekitRoom200ResponseDataInner.md) |  | [optional] 

## Example

```python
from gabber.generated.gabber_internal.models.realtime_livekit_attach_request import RealtimeLivekitAttachRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RealtimeLivekitAttachRequest from a JSON string
realtime_livekit_attach_request_instance = RealtimeLivekitAttachRequest.from_json(json)
# print the JSON string representation of the object
print(RealtimeLivekitAttachRequest.to_json())

# convert the object into a dict
realtime_livekit_attach_request_dict = realtime_livekit_attach_request_instance.to_dict()
# create an instance of RealtimeLivekitAttachRequest from a dict
realtime_livekit_attach_request_from_dict = RealtimeLivekitAttachRequest.from_dict(realtime_livekit_attach_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


