# UpdateScenarioRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**project** | **str** |  | [optional] 
**prompt** | **str** |  | [optional] 

## Example

```python
from gabber.generated.gabber.models.update_scenario_request import UpdateScenarioRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateScenarioRequest from a JSON string
update_scenario_request_instance = UpdateScenarioRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateScenarioRequest.to_json())

# convert the object into a dict
update_scenario_request_dict = update_scenario_request_instance.to_dict()
# create an instance of UpdateScenarioRequest from a dict
update_scenario_request_from_dict = UpdateScenarioRequest.from_dict(update_scenario_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


