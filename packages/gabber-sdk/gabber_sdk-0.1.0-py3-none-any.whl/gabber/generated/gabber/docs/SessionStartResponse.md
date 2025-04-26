# SessionStartResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**session** | [**Session**](Session.md) |  | 
**persona** | [**Persona**](Persona.md) |  | [optional] 
**scenario** | [**Scenario**](Scenario.md) |  | [optional] 
**connection_details** | [**SessionStartResponseConnectionDetails**](SessionStartResponseConnectionDetails.md) |  | 

## Example

```python
from gabber.generated.gabber.models.session_start_response import SessionStartResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SessionStartResponse from a JSON string
session_start_response_instance = SessionStartResponse.from_json(json)
# print the JSON string representation of the object
print(SessionStartResponse.to_json())

# convert the object into a dict
session_start_response_dict = session_start_response_instance.to_dict()
# create an instance of SessionStartResponse from a dict
session_start_response_from_dict = SessionStartResponse.from_dict(session_start_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


