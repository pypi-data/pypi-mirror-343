# Credit

*This work is derived from* **[@PatWalters](https://github.com/PatWalters)** *'s fantastic* [`rd_filters`](https://github.com/PatWalters/rd_filters) *repo*.

# SA-Filter

Easily apply the functional group filters from the ChEMBL database.

:warning: **No other physico-chemical property is checked, only the presence of structural alerts.**


These alerts were derived from ChEMBL (version 23),  and span 8 sets of alerts.
**All alerts are checked.**


| Rule Set                                                | Number of Alerts |
|---------------------------------------------------------|-----------------:|
| BMS                                                     |              180 |
| Dundee                                                  |              105 |
| Glaxo                                                   |               55 |
| Inpharmatica                                            |               91 |
| LINT                                                    |               57 |
| MLSMR                                                   |              116 |
| [PAINS](https://pubs.acs.org/doi/abs/10.1021/jm901137j) |              479 |
| SureChEMBL                                              |              166 |

The SMARTS patterns in a number of these alerts were not compatible with the RDKit
so **@PatWalters** edited them and included a complete list of the changes made is in the file **Notes.txt**. 

## Installation

`pip install sa-sift`

## Usage

One can easily identify alerts from a list of SMILES.

```python

from sa_filter import SAFilter

# Parse rules
safilter = SAFilter()

# Obtain quick list of booleans stating if a given molecule contains any alert.
print(safilter.contains_alert(['c1ccccc1', 'CN=[N+](N)N', 'CCCCCCCCCCCCC(=O)O']))

# Obtain details on the matched alerts.
print(safilter.contains_alert(['c1ccccc1', 'CN=[N+](N)N', 'CCCCCCCCCCCCC(=O)O']), return_alerts=True)
```
