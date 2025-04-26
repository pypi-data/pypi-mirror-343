# SessionTimelineItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**seconds** | **float** |  | [optional] 
**type** | **str** |  | [optional] 

## Example

```python
from gabber.generated.gabber.models.session_timeline_item import SessionTimelineItem

# TODO update the JSON string below
json = "{}"
# create an instance of SessionTimelineItem from a JSON string
session_timeline_item_instance = SessionTimelineItem.from_json(json)
# print the JSON string representation of the object
print(SessionTimelineItem.to_json())

# convert the object into a dict
session_timeline_item_dict = session_timeline_item_instance.to_dict()
# create an instance of SessionTimelineItem from a dict
session_timeline_item_from_dict = SessionTimelineItem.from_dict(session_timeline_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


