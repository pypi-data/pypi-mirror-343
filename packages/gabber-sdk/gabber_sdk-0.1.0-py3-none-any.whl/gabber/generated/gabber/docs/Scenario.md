# Scenario


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** |  | 
**id** | **str** |  | 
**name** | **str** |  | 
**project** | **str** |  | 
**prompt** | **str** |  | 
**human** | **str** |  | [optional] 

## Example

```python
from gabber.generated.gabber.models.scenario import Scenario

# TODO update the JSON string below
json = "{}"
# create an instance of Scenario from a JSON string
scenario_instance = Scenario.from_json(json)
# print the JSON string representation of the object
print(Scenario.to_json())

# convert the object into a dict
scenario_dict = scenario_instance.to_dict()
# create an instance of Scenario from a dict
scenario_from_dict = Scenario.from_dict(scenario_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


