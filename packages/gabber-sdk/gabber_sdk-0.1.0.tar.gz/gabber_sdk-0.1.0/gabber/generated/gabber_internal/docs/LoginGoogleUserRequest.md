# LoginGoogleUserRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**access_token** | **str** |  | 

## Example

```python
from gabber.generated.gabber_internal.models.login_google_user_request import LoginGoogleUserRequest

# TODO update the JSON string below
json = "{}"
# create an instance of LoginGoogleUserRequest from a JSON string
login_google_user_request_instance = LoginGoogleUserRequest.from_json(json)
# print the JSON string representation of the object
print(LoginGoogleUserRequest.to_json())

# convert the object into a dict
login_google_user_request_dict = login_google_user_request_instance.to_dict()
# create an instance of LoginGoogleUserRequest from a dict
login_google_user_request_from_dict = LoginGoogleUserRequest.from_dict(login_google_user_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


