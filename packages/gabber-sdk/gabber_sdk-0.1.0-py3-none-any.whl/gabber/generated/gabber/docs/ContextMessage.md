# ContextMessage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**speaking_ended_at** | **datetime** |  | [optional] 
**speaking_started_at** | **datetime** |  | [optional] 
**created_at** | **datetime** |  | 
**role** | **str** |  | 
**realtime_session** | **str** |  | [optional] 
**content** | [**List[ContextMessageContent]**](ContextMessageContent.md) |  | 
**tool_calls** | [**List[ContextMessageToolCall]**](ContextMessageToolCall.md) |  | [optional] 

## Example

```python
from gabber.generated.gabber.models.context_message import ContextMessage

# TODO update the JSON string below
json = "{}"
# create an instance of ContextMessage from a JSON string
context_message_instance = ContextMessage.from_json(json)
# print the JSON string representation of the object
print(ContextMessage.to_json())

# convert the object into a dict
context_message_dict = context_message_instance.to_dict()
# create an instance of ContextMessage from a dict
context_message_from_dict = ContextMessage.from_dict(context_message_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


