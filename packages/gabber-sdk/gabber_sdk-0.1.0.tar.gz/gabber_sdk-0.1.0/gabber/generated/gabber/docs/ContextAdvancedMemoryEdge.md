# ContextAdvancedMemoryEdge


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**created_at** | **datetime** |  | 
**updated_at** | **datetime** |  | 
**invalidated_at** | **datetime** |  | [optional] 
**source_node** | **str** |  | 
**target_node** | **str** |  | 
**fact** | **str** |  | 
**relation** | **str** |  | 

## Example

```python
from gabber.generated.gabber.models.context_advanced_memory_edge import ContextAdvancedMemoryEdge

# TODO update the JSON string below
json = "{}"
# create an instance of ContextAdvancedMemoryEdge from a JSON string
context_advanced_memory_edge_instance = ContextAdvancedMemoryEdge.from_json(json)
# print the JSON string representation of the object
print(ContextAdvancedMemoryEdge.to_json())

# convert the object into a dict
context_advanced_memory_edge_dict = context_advanced_memory_edge_instance.to_dict()
# create an instance of ContextAdvancedMemoryEdge from a dict
context_advanced_memory_edge_from_dict = ContextAdvancedMemoryEdge.from_dict(context_advanced_memory_edge_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


