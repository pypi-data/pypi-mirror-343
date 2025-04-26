# LLM


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** |  | 
**id** | **str** |  | 
**name** | **str** |  | 
**project** | **str** |  | [optional] 
**type** | **str** |  | 
**compliance** | **bool** |  | 
**description** | **str** |  | 

## Example

```python
from gabber.generated.gabber.models.llm import LLM

# TODO update the JSON string below
json = "{}"
# create an instance of LLM from a JSON string
llm_instance = LLM.from_json(json)
# print the JSON string representation of the object
print(LLM.to_json())

# convert the object into a dict
llm_dict = llm_instance.to_dict()
# create an instance of LLM from a dict
llm_from_dict = LLM.from_dict(llm_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


