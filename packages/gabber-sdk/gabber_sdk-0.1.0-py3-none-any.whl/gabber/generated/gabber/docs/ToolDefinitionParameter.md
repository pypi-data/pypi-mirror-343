# ToolDefinitionParameter


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**description** | **str** |  | 
**type** | **str** |  | 
**required** | **bool** |  | 
**default** | **str** |  | [optional] 

## Example

```python
from gabber.generated.gabber.models.tool_definition_parameter import ToolDefinitionParameter

# TODO update the JSON string below
json = "{}"
# create an instance of ToolDefinitionParameter from a JSON string
tool_definition_parameter_instance = ToolDefinitionParameter.from_json(json)
# print the JSON string representation of the object
print(ToolDefinitionParameter.to_json())

# convert the object into a dict
tool_definition_parameter_dict = tool_definition_parameter_instance.to_dict()
# create an instance of ToolDefinitionParameter from a dict
tool_definition_parameter_from_dict = ToolDefinitionParameter.from_dict(tool_definition_parameter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


