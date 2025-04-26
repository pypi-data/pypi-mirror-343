# UsageLimit


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | [**UsageType**](UsageType.md) |  | 
**value** | **float** |  | 

## Example

```python
from gabber.generated.gabber.models.usage_limit import UsageLimit

# TODO update the JSON string below
json = "{}"
# create an instance of UsageLimit from a JSON string
usage_limit_instance = UsageLimit.from_json(json)
# print the JSON string representation of the object
print(UsageLimit.to_json())

# convert the object into a dict
usage_limit_dict = usage_limit_instance.to_dict()
# create an instance of UsageLimit from a dict
usage_limit_from_dict = UsageLimit.from_dict(usage_limit_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


