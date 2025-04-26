# CreateCreditLedgerEntryRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amount** | **int** |  | 
**idempotency_key** | **str** |  | 

## Example

```python
from gabber.generated.gabber.models.create_credit_ledger_entry_request import CreateCreditLedgerEntryRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateCreditLedgerEntryRequest from a JSON string
create_credit_ledger_entry_request_instance = CreateCreditLedgerEntryRequest.from_json(json)
# print the JSON string representation of the object
print(CreateCreditLedgerEntryRequest.to_json())

# convert the object into a dict
create_credit_ledger_entry_request_dict = create_credit_ledger_entry_request_instance.to_dict()
# create an instance of CreateCreditLedgerEntryRequest from a dict
create_credit_ledger_entry_request_from_dict = CreateCreditLedgerEntryRequest.from_dict(create_credit_ledger_entry_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


