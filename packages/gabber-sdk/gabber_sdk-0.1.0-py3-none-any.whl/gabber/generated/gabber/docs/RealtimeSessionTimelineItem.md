# RealtimeSessionTimelineItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**seconds** | **float** |  | [optional] 
**type** | **str** |  | [optional] 

## Example

```python
from gabber.generated.gabber.models.realtime_session_timeline_item import RealtimeSessionTimelineItem

# TODO update the JSON string below
json = "{}"
# create an instance of RealtimeSessionTimelineItem from a JSON string
realtime_session_timeline_item_instance = RealtimeSessionTimelineItem.from_json(json)
# print the JSON string representation of the object
print(RealtimeSessionTimelineItem.to_json())

# convert the object into a dict
realtime_session_timeline_item_dict = realtime_session_timeline_item_instance.to_dict()
# create an instance of RealtimeSessionTimelineItem from a dict
realtime_session_timeline_item_from_dict = RealtimeSessionTimelineItem.from_dict(realtime_session_timeline_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


