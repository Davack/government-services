# OData v4 Syntax Guide: Knesset API

Base URL: `https://knesset.gov.il/OdataV4/ParliamentInfo/`

---

## Quick Reference

```
GET <base>/<Table>?$filter=<expr>&$select=<fields>&$top=<n>&$skip=<n>&$orderby=<field> [asc|desc]&$expand=<table>&$count=true
```

---

## $filter: Row Filtering

### Comparison operators

| Operator | Meaning | Example |
|---|---|---|
| `eq` | Equal | `KnessetNum eq 25` |
| `ne` | Not equal | `StatusID ne 193` |
| `gt` | Greater than | `PublicationDate gt 2024-01-01` |
| `lt` | Less than | `PublicationDate lt 2025-01-01` |
| `ge` | Greater or equal | `KnessetNum ge 20` |
| `le` | Less or equal | `KnessetNum le 10` |

### Logical operators

```
$filter=KnessetNum eq 25 and SubTypeDesc eq 'פרטית'
$filter=TypeID eq 1 or TypeID eq 2
$filter=not (StatusID eq 193)
```

### Functions

| Function | Example |
|---|---|
| `contains(Field,'value')` | `contains(Name,'ביטוח')` |
| `startswith(Field,'value')` | `startswith(LastName,'כה')` |
| `endswith(Field,'value')` | `endswith(Name,'התשפ"ה')` |
| `now()` | `PlenumFinish gt now()` |

### Set membership

```
$filter=PositionID in (43,61)
$filter=CommitteeID in (4208,4209,4197)
```

### Null checks

```
$filter=FinishDate eq null        # field is null
$filter=FinishDate ne null        # field is not null
```

### Date/time formats

```
# Date only
$filter=PublicationDate gt 2024-01-01

# Date with time (ISO 8601 UTC)
$filter=StartDate gt 2015-06-01T00:00:01Z

# Current time
$filter=PlenumFinish gt now() and PlenumStart lt now()
```

---

## $select: Field Projection

Return only specific fields (reduces response size):

```
$select=Id,Name,KnessetNum,PublicationDate
$select=Id,LastName,FirstName,IsCurrent
```

---

## $top and $skip: Pagination

```
$top=100                    # return first 100 rows
$skip=100&$top=100          # return rows 101-200 (page 2)
$top=0                      # return zero rows (useful with $count=true)
```

The API returns a `@odata.nextLink` in the response when more pages exist. Follow that URL to get the next page.

---

## $orderby: Sorting

```
$orderby=PublicationDate desc          # newest first
$orderby=Name                          # alphabetical ascending
$orderby=LastName asc,FirstName asc    # multi-field sort
$orderby=KNS_Person/LastName           # sort by expanded field
```

---

## $expand: Joining Related Tables

Expand joins a related table's records inline in the response.

### Simple expand
```
$expand=KNS_BillInitiator
$expand=KNS_BillInitiator,KNS_DocumentBill,KNS_BillName
```

### Expand with nested operators (use semicolons inside the parens)
```
$expand=KNS_BillInitiator($orderby=IsInitiator desc,Ordinal)
$expand=KNS_BillInitiator($filter=IsInitiator eq true)
$expand=KNS_DocumentBill($filter=GroupTypeID eq 5)
$expand=KNS_PlmSessionItem($filter=IsDiscussion eq 1;$orderby=Ordinal)
```

### Nested expand (expand within an expand)
```
$expand=KNS_IsraelLawMinistry($expand=KNS_GovMinistry)
$expand=KNS_CommitteeSession($expand=KNS_DocumentCommitteeSession)
```

### Sorting by an expanded field
```
$expand=KNS_Person&$orderby=KNS_Person/LastName,KNS_Person/FirstName
```

---

## $count: Counting Records

```
# Include count in response (along with data)
$count=true

# Count only: no data rows returned
$count=true&$top=0
```

Response with `$count=true` includes an `@odata.count` field at the top level.

---

## Response Structure

```json
{
  "@odata.context": "https://knesset.gov.il/OdataV4/ParliamentInfo/$metadata#KNS_Bill",
  "@odata.count": 12345,
  "@odata.nextLink": "https://knesset.gov.il/OdataV4/ParliamentInfo/KNS_Bill?$skip=100&...",
  "value": [
    { "Id": 5, "KnessetNum": 1, "Name": "חוק שכר חברי הכנסת...", ... },
    ...
  ]
}
```

- `value`: array of result rows
- `@odata.count`: total matching rows (when `$count=true`)
- `@odata.nextLink`: URL of next page (when results are paginated)

---

## Python Fetch Pattern

```python
import requests

BASE = "https://knesset.gov.il/OdataV4/ParliamentInfo/"
HEADERS = {"Accept": "application/json", "User-Agent": "Mozilla/5.0"}

def fetch_knesset(table, params):
    r = requests.get(BASE + table, params=params, headers=HEADERS, timeout=30)
    r.raise_for_status()
    data = r.json()
    return data.get("value", []), data.get("@odata.count"), data.get("@odata.nextLink")

# Example: recent bills
records, total, next_url = fetch_knesset("KNS_Bill", {
    "$filter": "KnessetNum eq 25",
    "$orderby": "PublicationDate desc",
    "$top": "20",
    "$select": "Id,Name,SubTypeDesc,PublicationDate",
    "$count": "true"
})
print(f"Total matching: {total}")
for r in records:
    print(r["Id"], r["Name"], r.get("PublicationDate","")[:10])
```

### Fetching all pages

```python
def fetch_all(table, params):
    results = []
    params["$top"] = "100"
    r = requests.get(BASE + table, params=params, headers=HEADERS, timeout=30)
    data = r.json()
    results.extend(data.get("value", []))
    next_url = data.get("@odata.nextLink")
    while next_url:
        r = requests.get(next_url, headers=HEADERS, timeout=30)
        data = r.json()
        results.extend(data.get("value", []))
        next_url = data.get("@odata.nextLink")
    return results
```

---

## Exploring the API

```
# List all available tables
GET https://knesset.gov.il/OdataV4/ParliamentInfo

# Full metadata (all tables, fields, relationships)
GET https://knesset.gov.il/OdataV4/ParliamentInfo/$metadata
```

---

## Key Gotchas Summary

| Issue | Rule |
|---|---|
| Primary key name | Always `Id` in v4: never `BillID`, `PersonID`, etc. |
| Intentional typo | `KNS_IsraelLawClassificiation`: two 'i's. Do NOT fix. |
| Cancelled sessions | `StatusID ne 193` to exclude cancelled committee sessions |
| Ordinal sort bug | `KNS_PlmSessionItem.$orderby=Ordinal` is broken (known API bug) |
| IsCurrent | Computed field: prefer `KnessetNum eq 25` over `IsCurrent eq true` |
| Datetime format | ISO 8601: `2024-01-01` or `2024-01-01T00:00:01Z` |
| Hebrew text | API returns Hebrew strings; use Hebrew in `contains()` filters |
| v2 tables | `KNS_Law` and `KNS_DocumentLaw` only exist in v2; use v4 only |
| Knesset 0 | Provisional State Council (מועצת המדינה הזמנית) |
| MK position IDs | 43=ח"כ (m), 61=ח"כית (f), 41=committee chair, 54=faction member |
| Transcript docs | `GroupTypeID eq 28` in `KNS_DocumentPlenumSession` = official transcript |
| MK ID mapping | `KNS_MkSiteCode` and `KNS_CmtSiteCode` map Sanhedrin IDs to website IDs |
