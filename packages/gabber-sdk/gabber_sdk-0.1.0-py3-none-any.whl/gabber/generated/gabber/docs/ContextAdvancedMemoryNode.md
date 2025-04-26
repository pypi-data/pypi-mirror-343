# ContextAdvancedMemoryNode


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**created_at** | **datetime** |  | 
**updated_at** | **datetime** |  | 
**name** | **str** |  | 
**summary** | **str** |  | 

## Example

```python
from gabber.generated.gabber.models.context_advanced_memory_node import ContextAdvancedMemoryNode

# TODO update the JSON string below
json = "{}"
# create an instance of ContextAdvancedMemoryNode from a JSON string
context_advanced_memory_node_instance = ContextAdvancedMemoryNode.from_json(json)
# print the JSON string representation of the object
print(ContextAdvancedMemoryNode.to_json())

# convert the object into a dict
context_advanced_memory_node_dict = context_advanced_memory_node_instance.to_dict()
# create an instance of ContextAdvancedMemoryNode from a dict
context_advanced_memory_node_from_dict = ContextAdvancedMemoryNode.from_dict(context_advanced_memory_node_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


