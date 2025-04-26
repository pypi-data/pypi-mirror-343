# ToolDefinition


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**name** | **str** |  | 
**description** | **str** |  | 
**parameters** | [**List[ToolDefinitionParameter]**](ToolDefinitionParameter.md) |  | 
**call_settings** | [**ToolDefinitionCallSettings**](ToolDefinitionCallSettings.md) |  | 

## Example

```python
from gabber.generated.gabber.models.tool_definition import ToolDefinition

# TODO update the JSON string below
json = "{}"
# create an instance of ToolDefinition from a JSON string
tool_definition_instance = ToolDefinition.from_json(json)
# print the JSON string representation of the object
print(ToolDefinition.to_json())

# convert the object into a dict
tool_definition_dict = tool_definition_instance.to_dict()
# create an instance of ToolDefinition from a dict
tool_definition_from_dict = ToolDefinition.from_dict(tool_definition_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


