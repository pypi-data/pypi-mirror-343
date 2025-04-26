# ToolDefinitionCallSettings


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**destination** | [**ToolDefinitionCallSettingsDestination**](ToolDefinitionCallSettingsDestination.md) |  | 

## Example

```python
from gabber.generated.gabber.models.tool_definition_call_settings import ToolDefinitionCallSettings

# TODO update the JSON string below
json = "{}"
# create an instance of ToolDefinitionCallSettings from a JSON string
tool_definition_call_settings_instance = ToolDefinitionCallSettings.from_json(json)
# print the JSON string representation of the object
print(ToolDefinitionCallSettings.to_json())

# convert the object into a dict
tool_definition_call_settings_dict = tool_definition_call_settings_instance.to_dict()
# create an instance of ToolDefinitionCallSettings from a dict
tool_definition_call_settings_from_dict = ToolDefinitionCallSettings.from_dict(tool_definition_call_settings_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


