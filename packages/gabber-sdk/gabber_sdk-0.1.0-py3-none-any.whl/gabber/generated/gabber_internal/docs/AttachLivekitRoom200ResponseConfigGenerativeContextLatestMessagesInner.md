# AttachLivekitRoom200ResponseConfigGenerativeContextLatestMessagesInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**speaking_ended_at** | **datetime** |  | [optional] 
**speaking_started_at** | **datetime** |  | [optional] 
**created_at** | **datetime** |  | 
**role** | **str** |  | 
**realtime_session** | **str** |  | [optional] 
**content** | [**List[AttachLivekitRoom200ResponseConfigGenerativeContextLatestMessagesInnerContentInner]**](AttachLivekitRoom200ResponseConfigGenerativeContextLatestMessagesInnerContentInner.md) |  | 
**tool_calls** | [**List[AttachLivekitRoom200ResponseConfigGenerativeContextLatestMessagesInnerToolCallsInner]**](AttachLivekitRoom200ResponseConfigGenerativeContextLatestMessagesInnerToolCallsInner.md) |  | [optional] 

## Example

```python
from gabber.generated.gabber_internal.models.attach_livekit_room200_response_config_generative_context_latest_messages_inner import AttachLivekitRoom200ResponseConfigGenerativeContextLatestMessagesInner

# TODO update the JSON string below
json = "{}"
# create an instance of AttachLivekitRoom200ResponseConfigGenerativeContextLatestMessagesInner from a JSON string
attach_livekit_room200_response_config_generative_context_latest_messages_inner_instance = AttachLivekitRoom200ResponseConfigGenerativeContextLatestMessagesInner.from_json(json)
# print the JSON string representation of the object
print(AttachLivekitRoom200ResponseConfigGenerativeContextLatestMessagesInner.to_json())

# convert the object into a dict
attach_livekit_room200_response_config_generative_context_latest_messages_inner_dict = attach_livekit_room200_response_config_generative_context_latest_messages_inner_instance.to_dict()
# create an instance of AttachLivekitRoom200ResponseConfigGenerativeContextLatestMessagesInner from a dict
attach_livekit_room200_response_config_generative_context_latest_messages_inner_from_dict = AttachLivekitRoom200ResponseConfigGenerativeContextLatestMessagesInner.from_dict(attach_livekit_room200_response_config_generative_context_latest_messages_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


