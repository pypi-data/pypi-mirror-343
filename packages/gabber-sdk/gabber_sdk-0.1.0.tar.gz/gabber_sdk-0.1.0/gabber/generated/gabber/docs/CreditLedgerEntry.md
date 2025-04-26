# CreditLedgerEntry


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** |  | 
**id** | **str** |  | 
**credit** | **str** |  | 
**human** | **str** |  | 
**amount** | **int** |  | 
**balance** | **int** |  | 
**idempotency_key** | **str** |  | 

## Example

```python
from gabber.generated.gabber.models.credit_ledger_entry import CreditLedgerEntry

# TODO update the JSON string below
json = "{}"
# create an instance of CreditLedgerEntry from a JSON string
credit_ledger_entry_instance = CreditLedgerEntry.from_json(json)
# print the JSON string representation of the object
print(CreditLedgerEntry.to_json())

# convert the object into a dict
credit_ledger_entry_dict = credit_ledger_entry_instance.to_dict()
# create an instance of CreditLedgerEntry from a dict
credit_ledger_entry_from_dict = CreditLedgerEntry.from_dict(credit_ledger_entry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


