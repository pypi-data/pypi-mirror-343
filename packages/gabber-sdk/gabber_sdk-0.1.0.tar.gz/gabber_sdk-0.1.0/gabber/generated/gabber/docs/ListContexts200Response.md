# ListContexts200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**next_page** | **str** | The URL to the next page of items. | [optional] 
**total_count** | **int** | The total number of items. | 
**values** | [**List[Context]**](Context.md) | The list of items. | 

## Example

```python
from gabber.generated.gabber.models.list_contexts200_response import ListContexts200Response

# TODO update the JSON string below
json = "{}"
# create an instance of ListContexts200Response from a JSON string
list_contexts200_response_instance = ListContexts200Response.from_json(json)
# print the JSON string representation of the object
print(ListContexts200Response.to_json())

# convert the object into a dict
list_contexts200_response_dict = list_contexts200_response_instance.to_dict()
# create an instance of ListContexts200Response from a dict
list_contexts200_response_from_dict = ListContexts200Response.from_dict(list_contexts200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


