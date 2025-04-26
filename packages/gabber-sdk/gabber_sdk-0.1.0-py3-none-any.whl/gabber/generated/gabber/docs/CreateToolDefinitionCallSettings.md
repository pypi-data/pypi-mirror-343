# CreateToolDefinitionCallSettings


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**destination** | [**CreateToolDefinitionCallSettingsDestination**](CreateToolDefinitionCallSettingsDestination.md) |  | 

## Example

```python
from gabber.generated.gabber.models.create_tool_definition_call_settings import CreateToolDefinitionCallSettings

# TODO update the JSON string below
json = "{}"
# create an instance of CreateToolDefinitionCallSettings from a JSON string
create_tool_definition_call_settings_instance = CreateToolDefinitionCallSettings.from_json(json)
# print the JSON string representation of the object
print(CreateToolDefinitionCallSettings.to_json())

# convert the object into a dict
create_tool_definition_call_settings_dict = create_tool_definition_call_settings_instance.to_dict()
# create an instance of CreateToolDefinitionCallSettings from a dict
create_tool_definition_call_settings_from_dict = CreateToolDefinitionCallSettings.from_dict(create_tool_definition_call_settings_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


