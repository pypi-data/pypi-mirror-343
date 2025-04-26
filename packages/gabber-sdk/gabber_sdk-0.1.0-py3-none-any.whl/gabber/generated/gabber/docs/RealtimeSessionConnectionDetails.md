# RealtimeSessionConnectionDetails


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** | The URL to connect to the RealtimeSession | 
**token** | **str** | The token to use to connect to the RealtimeSession | 

## Example

```python
from gabber.generated.gabber.models.realtime_session_connection_details import RealtimeSessionConnectionDetails

# TODO update the JSON string below
json = "{}"
# create an instance of RealtimeSessionConnectionDetails from a JSON string
realtime_session_connection_details_instance = RealtimeSessionConnectionDetails.from_json(json)
# print the JSON string representation of the object
print(RealtimeSessionConnectionDetails.to_json())

# convert the object into a dict
realtime_session_connection_details_dict = realtime_session_connection_details_instance.to_dict()
# create an instance of RealtimeSessionConnectionDetails from a dict
realtime_session_connection_details_from_dict = RealtimeSessionConnectionDetails.from_dict(realtime_session_connection_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


