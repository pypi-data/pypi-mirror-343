# ListRealtimeSessions200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**next_page** | **str** | The token for the next page of results, or null if there are no more pages. | [optional] 
**total_count** | **int** | The total number of items. | 
**values** | [**List[RealtimeSession]**](RealtimeSession.md) | The list of items. | 

## Example

```python
from gabber.generated.gabber.models.list_realtime_sessions200_response import ListRealtimeSessions200Response

# TODO update the JSON string below
json = "{}"
# create an instance of ListRealtimeSessions200Response from a JSON string
list_realtime_sessions200_response_instance = ListRealtimeSessions200Response.from_json(json)
# print the JSON string representation of the object
print(ListRealtimeSessions200Response.to_json())

# convert the object into a dict
list_realtime_sessions200_response_dict = list_realtime_sessions200_response_instance.to_dict()
# create an instance of ListRealtimeSessions200Response from a dict
list_realtime_sessions200_response_from_dict = ListRealtimeSessions200Response.from_dict(list_realtime_sessions200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


