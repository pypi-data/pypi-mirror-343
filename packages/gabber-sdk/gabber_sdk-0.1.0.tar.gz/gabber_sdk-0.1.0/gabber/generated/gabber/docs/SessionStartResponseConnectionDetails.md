# SessionStartResponseConnectionDetails


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**token** | **str** |  | [optional] 
**url** | **str** |  | [optional] 

## Example

```python
from gabber.generated.gabber.models.session_start_response_connection_details import SessionStartResponseConnectionDetails

# TODO update the JSON string below
json = "{}"
# create an instance of SessionStartResponseConnectionDetails from a JSON string
session_start_response_connection_details_instance = SessionStartResponseConnectionDetails.from_json(json)
# print the JSON string representation of the object
print(SessionStartResponseConnectionDetails.to_json())

# convert the object into a dict
session_start_response_connection_details_dict = session_start_response_connection_details_instance.to_dict()
# create an instance of SessionStartResponseConnectionDetails from a dict
session_start_response_connection_details_from_dict = SessionStartResponseConnectionDetails.from_dict(session_start_response_connection_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


