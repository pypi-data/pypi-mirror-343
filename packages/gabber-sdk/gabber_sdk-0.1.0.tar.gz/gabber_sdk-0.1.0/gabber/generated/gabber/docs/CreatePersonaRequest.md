# CreatePersonaRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** |  | 
**image_url** | **str** |  | [optional] 
**name** | **str** |  | 
**gender** | **str** |  | [optional] 
**voice** | **str** |  | 

## Example

```python
from gabber.generated.gabber.models.create_persona_request import CreatePersonaRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreatePersonaRequest from a JSON string
create_persona_request_instance = CreatePersonaRequest.from_json(json)
# print the JSON string representation of the object
print(CreatePersonaRequest.to_json())

# convert the object into a dict
create_persona_request_dict = create_persona_request_instance.to_dict()
# create an instance of CreatePersonaRequest from a dict
create_persona_request_from_dict = CreatePersonaRequest.from_dict(create_persona_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


