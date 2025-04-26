# ListContextMessages200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**next_page** | **str** | The URL to the next page of items. | [optional] 
**total_count** | **int** | The total number of items. | 
**values** | [**List[ContextMessage]**](ContextMessage.md) | The list of items. | 

## Example

```python
from gabber.generated.gabber.models.list_context_messages200_response import ListContextMessages200Response

# TODO update the JSON string below
json = "{}"
# create an instance of ListContextMessages200Response from a JSON string
list_context_messages200_response_instance = ListContextMessages200Response.from_json(json)
# print the JSON string representation of the object
print(ListContextMessages200Response.to_json())

# convert the object into a dict
list_context_messages200_response_dict = list_context_messages200_response_instance.to_dict()
# create an instance of ListContextMessages200Response from a dict
list_context_messages200_response_from_dict = ListContextMessages200Response.from_dict(list_context_messages200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


