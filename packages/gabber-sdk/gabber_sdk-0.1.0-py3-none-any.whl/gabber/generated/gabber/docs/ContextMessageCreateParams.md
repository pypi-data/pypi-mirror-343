# ContextMessageCreateParams


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**speaking_ended_at** | **datetime** |  | [optional] 
**speaking_started_at** | **datetime** |  | [optional] 
**role** | **str** |  | 
**content** | **str** |  | 
**tool_calls** | [**List[ContextMessageToolCall]**](ContextMessageToolCall.md) |  | [optional] 
**advanced_memory** | **bool** | When set to true, gabber will use it&#39;s advanced memory system to generate responses. | [optional] 

## Example

```python
from gabber.generated.gabber.models.context_message_create_params import ContextMessageCreateParams

# TODO update the JSON string below
json = "{}"
# create an instance of ContextMessageCreateParams from a JSON string
context_message_create_params_instance = ContextMessageCreateParams.from_json(json)
# print the JSON string representation of the object
print(ContextMessageCreateParams.to_json())

# convert the object into a dict
context_message_create_params_dict = context_message_create_params_instance.to_dict()
# create an instance of ContextMessageCreateParams from a dict
context_message_create_params_from_dict = ContextMessageCreateParams.from_dict(context_message_create_params_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


