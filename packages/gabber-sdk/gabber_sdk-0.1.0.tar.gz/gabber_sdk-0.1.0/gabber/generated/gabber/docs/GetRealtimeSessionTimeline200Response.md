# GetRealtimeSessionTimeline200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**next_page** | **str** | The URL to the next page of items. | [optional] 
**total_count** | **int** | The total number of items. | 
**values** | [**List[RealtimeSessionTimelineItem]**](RealtimeSessionTimelineItem.md) | The list of items. | 

## Example

```python
from gabber.generated.gabber.models.get_realtime_session_timeline200_response import GetRealtimeSessionTimeline200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetRealtimeSessionTimeline200Response from a JSON string
get_realtime_session_timeline200_response_instance = GetRealtimeSessionTimeline200Response.from_json(json)
# print the JSON string representation of the object
print(GetRealtimeSessionTimeline200Response.to_json())

# convert the object into a dict
get_realtime_session_timeline200_response_dict = get_realtime_session_timeline200_response_instance.to_dict()
# create an instance of GetRealtimeSessionTimeline200Response from a dict
get_realtime_session_timeline200_response_from_dict = GetRealtimeSessionTimeline200Response.from_dict(get_realtime_session_timeline200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


