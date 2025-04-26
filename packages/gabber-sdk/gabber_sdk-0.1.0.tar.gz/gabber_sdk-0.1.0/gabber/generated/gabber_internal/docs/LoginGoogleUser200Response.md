# LoginGoogleUser200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user** | [**User**](User.md) |  | 
**token** | **str** |  | 
**new_user** | **bool** |  | 

## Example

```python
from gabber.generated.gabber_internal.models.login_google_user200_response import LoginGoogleUser200Response

# TODO update the JSON string below
json = "{}"
# create an instance of LoginGoogleUser200Response from a JSON string
login_google_user200_response_instance = LoginGoogleUser200Response.from_json(json)
# print the JSON string representation of the object
print(LoginGoogleUser200Response.to_json())

# convert the object into a dict
login_google_user200_response_dict = login_google_user200_response_instance.to_dict()
# create an instance of LoginGoogleUser200Response from a dict
login_google_user200_response_from_dict = LoginGoogleUser200Response.from_dict(login_google_user200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


