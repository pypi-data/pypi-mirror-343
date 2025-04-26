# HumanData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**created_at** | **datetime** |  | 
**human** | **str** |  | 
**project** | **str** |  | 
**type** | [**HumanDataType**](HumanDataType.md) |  | 
**value** | **str** |  | 

## Example

```python
from gabber.generated.gabber.models.human_data import HumanData

# TODO update the JSON string below
json = "{}"
# create an instance of HumanData from a JSON string
human_data_instance = HumanData.from_json(json)
# print the JSON string representation of the object
print(HumanData.to_json())

# convert the object into a dict
human_data_dict = human_data_instance.to_dict()
# create an instance of HumanData from a dict
human_data_from_dict = HumanData.from_dict(human_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


