# ListCredits200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**next_page** | **str** | The token for the next page of results, or null if there are no more pages. | 
**total_count** | **int** | The total number of items available. | 
**values** | [**List[Credit]**](Credit.md) | The array of credits. | 

## Example

```python
from gabber.generated.gabber.models.list_credits200_response import ListCredits200Response

# TODO update the JSON string below
json = "{}"
# create an instance of ListCredits200Response from a JSON string
list_credits200_response_instance = ListCredits200Response.from_json(json)
# print the JSON string representation of the object
print(ListCredits200Response.to_json())

# convert the object into a dict
list_credits200_response_dict = list_credits200_response_instance.to_dict()
# create an instance of ListCredits200Response from a dict
list_credits200_response_from_dict = ListCredits200Response.from_dict(list_credits200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


