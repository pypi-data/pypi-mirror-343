# CreateToolDefinitionRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**description** | **str** |  | 
**parameters** | [**List[ToolDefinitionParameter]**](ToolDefinitionParameter.md) |  | 
**call_settings** | [**CreateToolDefinitionCallSettings**](CreateToolDefinitionCallSettings.md) |  | 

## Example

```python
from gabber.generated.gabber.models.create_tool_definition_request import CreateToolDefinitionRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateToolDefinitionRequest from a JSON string
create_tool_definition_request_instance = CreateToolDefinitionRequest.from_json(json)
# print the JSON string representation of the object
print(CreateToolDefinitionRequest.to_json())

# convert the object into a dict
create_tool_definition_request_dict = create_tool_definition_request_instance.to_dict()
# create an instance of CreateToolDefinitionRequest from a dict
create_tool_definition_request_from_dict = CreateToolDefinitionRequest.from_dict(create_tool_definition_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


