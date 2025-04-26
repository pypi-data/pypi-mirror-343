# ContextAdvancedMemoryQueryResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**nodes** | [**List[ContextAdvancedMemoryNode]**](ContextAdvancedMemoryNode.md) |  | 
**edges** | [**List[ContextAdvancedMemoryEdge]**](ContextAdvancedMemoryEdge.md) |  | 

## Example

```python
from gabber.generated.gabber.models.context_advanced_memory_query_result import ContextAdvancedMemoryQueryResult

# TODO update the JSON string below
json = "{}"
# create an instance of ContextAdvancedMemoryQueryResult from a JSON string
context_advanced_memory_query_result_instance = ContextAdvancedMemoryQueryResult.from_json(json)
# print the JSON string representation of the object
print(ContextAdvancedMemoryQueryResult.to_json())

# convert the object into a dict
context_advanced_memory_query_result_dict = context_advanced_memory_query_result_instance.to_dict()
# create an instance of ContextAdvancedMemoryQueryResult from a dict
context_advanced_memory_query_result_from_dict = ContextAdvancedMemoryQueryResult.from_dict(context_advanced_memory_query_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


