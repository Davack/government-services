---
name: knesset-legislation
description: >-
  [What] Queries the Israeli Knesset parliamentary database via OData v4 API.
  [When] Use when the user asks about the Israeli parliament, legislation, MKs,
  votes, committees, or parliamentary procedures. Trigger phrases: knesset,
  chok, hatzaat chok, chaver knesset, vaada, hatzba'a, she'ila, malia, sia'a,
  כנסת, חוק, הצעת חוק, ח"כ, ועדה, הצבעה, שאילתה, מליאה, סיעה.
  [Capabilities] Covers bills and enacted laws (KNS_Bill / KNS_IsraelLaw),
  committees and sessions (KNS_Committee / KNS_CommitteeSession), plenum
  sessions and votes (KNS_PlenumSession / KNS_PlenumVote), parliamentary
  questions (KNS_Query), agenda proposals (KNS_Agenda), secondary legislation
  (KNS_SecondaryLaw), MK positions (KNS_Person / KNS_PersonToPosition), and
  faction data (KNS_Faction). Do NOT use for Israeli company registration (use
  israeli-company-lookup instead) or non-parliamentary government data.
license: MIT
allowed-tools: Bash(python:*)
compatibility: All API calls use Python requests via Bash. No WebFetch. Works with Claude Code, Claude.ai, Cursor.
---

# Knesset Parliamentary Data

## Overview

The Knesset exposes its full parliamentary database via an **OData v4 REST API** (real-time, no auth required). This skill instructs you on how to query it for any parliamentary data: bills, enacted laws, MKs, committees, votes, parliamentary questions, agenda proposals, and secondary legislation.

**Base URL:** `https://knesset.gov.il/OdataV4/ParliamentInfo/`

---

## Step 1: Identify the Target Table

| User request                       | Primary table                             |
| ---------------------------------- | ----------------------------------------- |
| Bills, laws, legislation           | `KNS_Bill`                                |
| Parent laws (law corpus)           | `KNS_IsraelLaw`                           |
| Regulations, orders, decrees       | `KNS_SecondaryLaw`                        |
| MKs, ministers, persons            | `KNS_Person` / `KNS_PersonToPosition`     |
| Factions / parties                 | `KNS_Faction`                             |
| Committees                         | `KNS_Committee`                           |
| Committee sessions / meetings      | `KNS_CommitteeSession`                    |
| Plenum / plenary sessions          | `KNS_PlenumSession`                       |
| Plenary votes                      | `KNS_PlenumVote` / `KNS_PlenumVoteResult` |
| Parliamentary questions (שאילתות)  | `KNS_Query`                               |
| Agenda proposals (הצעות לסדר-היום) | `KNS_Agenda`                              |
| Knesset session dates              | `KNS_KnessetDates`                        |
| Government ministries              | `KNS_GovMinistry`                         |
| Status codes                       | `KNS_Status`                              |
| Item type codes                    | `KNS_ItemType`                            |

---

## Step 2: Build the OData v4 Query

### URL structure

```
GET https://knesset.gov.il/OdataV4/ParliamentInfo/<TableName>?<params>
```

### Query parameters

| Parameter            | Purpose                         | Example                           |
| -------------------- | ------------------------------- | --------------------------------- |
| `$filter`            | Filter rows                     | `$filter=KnessetNum eq 25`        |
| `$select`            | Choose fields                   | `$select=Id,Name,PublicationDate` |
| `$top`               | Limit rows returned             | `$top=100`                        |
| `$skip`              | Offset (pagination)             | `$skip=100`                       |
| `$orderby`           | Sort                            | `$orderby=PublicationDate desc`   |
| `$expand`            | Join related table inline       | `$expand=KNS_BillInitiator`       |
| `$count=true`        | Include total count in response | `$count=true`                     |
| `$count=true&$top=0` | Count only, no rows             | `$count=true&$top=0`              |

### $filter operators

| Operator          | Meaning          | Example                                |
| ----------------- | ---------------- | -------------------------------------- |
| `eq`              | Equal            | `KnessetNum eq 25`                     |
| `ne`              | Not equal        | `StatusID ne 193`                      |
| `gt`              | Greater than     | `PublicationDate gt 2024-01-01`        |
| `lt`              | Less than        | `PublicationDate lt 2025-01-01`        |
| `ge`              | Greater or equal | `KnessetNum ge 20`                     |
| `le`              | Less or equal    | `KnessetNum le 25`                     |
| `and`             | Logical AND      | `KnessetNum eq 25 and StatusID eq 118` |
| `or`              | Logical OR       | `TypeID eq 1 or TypeID eq 2`           |
| `contains(F,'v')` | Substring search | `contains(Name,'ביטוח')`               |
| `in (v1,v2)`      | Set membership   | `PositionID in (43,61)`                |
| `eq null`         | Is null          | `FinishDate eq null`                   |
| `now()`           | Current datetime | `PlenumFinish gt now()`                |

### $expand syntax

```
# Simple expand
$expand=KNS_BillInitiator

# Expand with nested ordering
$expand=KNS_BillInitiator($orderby=IsInitiator desc,Ordinal)

# Expand with nested filter
$expand=KNS_DocumentBill($filter=GroupTypeID eq 5)

# Multiple expands
$expand=KNS_BillInitiator,KNS_DocumentBill,KNS_BillName

# Expand with nested expand
$expand=KNS_IsraelLawMinistry($expand=KNS_GovMinistry)
```

### Ordering by expanded field

```
$expand=KNS_Person&$orderby=KNS_Person/LastName,KNS_Person/FirstName
```

---

## Step 3: Execute the Query

Use Python `requests` (always available via Bash):

```python
import requests, json

BASE = "https://knesset.gov.il/OdataV4/ParliamentInfo/"
headers = {"Accept": "application/json", "User-Agent": "Mozilla/5.0"}

r = requests.get(
    BASE + "KNS_Bill",
    params={
        "$filter": "KnessetNum eq 25",
        "$orderby": "PublicationDate desc",
        "$top": "20",
        "$select": "Id,Name,SubTypeDesc,PublicationDate"
    },
    headers=headers,
    timeout=30
)
data = r.json()
records = data.get("value", [])            # list of rows
count   = data.get("@odata.count")         # total count (when $count=true)
next_link = data.get("@odata.nextLink")    # pagination URL (when more pages exist)

for rec in records:
    print(rec)
```

---

## Step 4: Common Ready-to-Use Queries

Consult `references/common-queries.md` for ready-to-use query snippets by topic (bills, laws, MKs, factions, committees, plenum, votes, questions, agenda proposals, secondary legislation, code lookups).

---

## Examples

### Example 1
**User says:** "Who are the current MKs from Likud?" / "מי הם ח"כי הליכוד הנוכחיים?"
**Result:** Query `KNS_Faction?$filter=KnessetNum eq 25 and contains(Name,'ליכוד')` to get the faction ID, then `KNS_PersonToPosition?$filter=FactionID eq <id> and PositionID eq 54 and FinishDate eq null&$expand=KNS_Person&$orderby=KNS_Person/LastName` to list members. Present as a table: name, faction, start date.

### Example 2
**User says:** "Show me the last 10 bills proposed on the topic of housing." / "הציגו לי את 10 הצעות החוק האחרונות בנושא דיור"
**Result:** Query `KNS_Bill?$filter=contains(Name,'דיור') or contains(Name,'שכירות') or contains(Name,'דירה')&$orderby=PublicationDate desc&$top=10&$select=Id,Name,SubTypeDesc,PublicationDate`. Present as a numbered list with bill name, type, and date. Offer to expand with initiators.

### Example 3
**User says:** "Did MK Moshe Gafni vote in favor of the budget?" / "האם ח"כ גפני הצביע בעד התקציב?"
**Result:** Find the person via `KNS_Person?$filter=contains(LastName,'גפני')`. Find the vote via `KNS_PlenumVote?$filter=contains(VoteTitle,'תקציב')&$orderby=VoteDateTime desc&$top=5`. Then fetch `KNS_PlenumVoteResult?$filter=VoteID eq <id> and MkId eq <id>` and report `ResultDesc` ("בעד" / "נגד" / "נמנע").

### Example 4
**User says:** "How many parliamentary questions were asked about the Justice Ministry in Knesset 25?" / "כמה שאילתות הוגשו למשרד המשפטים בכנסת 25?"
**Result:** First look up ministry IDs via `KNS_GovMinistry?$filter=contains(Name,'משפטים')&$select=Id,Name`, collect the `Id` values, then query `KNS_Query?$filter=KnessetNum eq 25 and GovMinistryID in (<ids>)&$count=true&$top=0` and report the `@odata.count` value. Note: `GovMinistryName` does not exist on `KNS_Query`; filter by `GovMinistryID`.

---

## Step 5: Format and Present Results

- Present records in a clear table or numbered list
- Show the exact API URL used (for reproducibility)
- If the response has `@odata.nextLink`, note that more pages exist
- If `@odata.count` is present, show the total count
- Offer relevant follow-up expansions (e.g. "want to include bill documents?")
- For FilePath fields: the value is the full URL to the document

---

## Critical Gotchas

| Issue                  | Detail                                                                                                                        |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **Primary key field**  | In v4, the PK is always `Id`: never `BillID`, `PersonID`, `CommitteeID` etc.                                                  |
| **Intentional typo**   | `KNS_IsraelLawClassificiation`: note double 'i'. Do NOT fix it.                                                               |
| **Cancelled sessions** | `KNS_CommitteeSession` StatusID **193** = cancelled. Always filter with `StatusID ne 193` unless you want cancelled sessions. |
| **Ordinal bug**        | `KNS_PlmSessionItem`: sorting by `Ordinal` is broken (known API bug). Don't rely on it.                                       |
| **IsCurrent flag**     | `IsCurrent` is computed from FinishDate. Prefer filtering by `KnessetNum eq 25` over `IsCurrent eq true` for reliability.     |
| **MK position IDs**    | 43 = ח"כ (male), 61 = ח"כית (female), 41 = committee chair, 54 = faction member                                               |
| **Transcript docs**    | `GroupTypeID eq 28` in `KNS_DocumentPlenumSession` = official Divrei HaKnesset transcript                                     |
| **Knesset 0**          | Knesset number 0 in the system = Provisional State Council (מועצת המדינה הזמנית)                                              |
| **Data quality**       | Quality improves from Knesset 17+. Older records may have gaps.                                                               |
| **v2 vs v4**           | `KNS_Law` and `KNS_DocumentLaw` exist ONLY in v2. In v4 those records moved into `KNS_Bill`. Use v4 exclusively.              |
| **Datetime format**    | Use ISO 8601: `2024-01-01` for date, `2015-06-01T00:00:01Z` for datetime with time                                            |
| **VoteTitle not ItemTitle** | `KNS_PlenumVote` uses `VoteTitle` for the vote description. `ItemTitle` does not exist and returns 400.                  |
| **MkId not PersonID**  | `KNS_PlenumVoteResult` uses `MkId` for the MK foreign key, not `PersonID`. Use `ResultDesc` for the outcome ("בעד"/"נגד"/"נמנע"); `ResultCode` values are not 1/2/3. |
| **GovMinistryID not GovMinistryName** | `KNS_Query` stores `GovMinistryID` (integer), not a name field. Look up IDs first via `KNS_GovMinistry?$filter=contains(Name,'...')`, then filter by `GovMinistryID in (<ids>)`. |
| **Faction member PositionID** | To list MKs by faction, filter `KNS_PersonToPosition` with `PositionID eq 54` (faction member), not `in (43,61)` (general MK role). The general MK role is not tied to a specific faction record. |

---

## Bundled Resources

### Scripts

- `scripts/query_knesset.py`: Query the Knesset OData API from the command line. Supports subcommands: `tables` (list all tables), `examples` (show ready-to-use queries), `query` (execute a query). Run: `python scripts/query_knesset.py --help`

### References

| File                                  | Contents                                      |
| ------------------------------------- | --------------------------------------------- |
| `references/common-queries.md`        | Ready-to-use query snippets for all topics    |
| `references/tables-bills.md`          | All bill/law table fields in detail           |
| `references/tables-committees.md`     | All committee table fields in detail          |
| `references/tables-members.md`        | MKs, positions, factions: all fields          |
| `references/tables-plenum-votes.md`   | Plenum sessions and votes: all fields         |
| `references/tables-agenda-queries.md` | Agenda proposals and parliamentary questions  |
| `references/tables-secondary-law.md`  | Secondary legislation tables                  |
| `references/odata-syntax.md`          | Complete OData v4 syntax and pagination guide |

## Error Handling / Troubleshooting

### Error: empty `value` array despite expecting results

Cause: Date filter using wrong format (e.g. `01/01/2024` instead of `2024-01-01`), or Hebrew text in `$filter` not UTF-8 encoded.
Solution: Use ISO 8601 dates. Pass `$filter` as a query parameter (not inline in the URL): `requests` will handle encoding automatically. Never manually URL-encode Hebrew characters.

### Error: 500 Internal Server Error

Cause: Usually a malformed `$expand` chain: nested expands with invalid field names, or expanding a field that doesn't exist on that table.
Solution: Simplify the query. Remove `$expand` first to confirm the base query works, then add expansions one at a time. Check `references/` for valid field names.

### Error: `$filter` on expanded field returns nothing

Cause: Filtering on a field inside `$expand` uses a nested syntax, not a top-level filter.
Solution: Use `$expand=Table($filter=Field eq Value)` not `$filter=Table/Field eq Value`.

### Error: wrong count / pagination seems off

Cause: `$count=true` must be paired with `$top`: omitting `$top` returns the API default page size (usually 10), not all records.
Solution: Set `$count=true` to get the total, then paginate using `$skip` and `$top`, following `@odata.nextLink` until it's absent.

### Error: committee session query returns cancelled sessions

Cause: The API includes cancelled sessions (StatusID=193) by default.
Solution: Always add `and StatusID ne 193` to `KNS_CommitteeSession` filters unless cancelled sessions are specifically wanted.

---

## Reference Links

Official sources for verifying and updating the information in this skill:

| Source                           | URL                                                                                   | What to Check                                      |
| -------------------------------- | ------------------------------------------------------------------------------------- | -------------------------------------------------- |
| Knesset databases portal         | https://main.knesset.gov.il/activity/info/pages/databases.aspx                        | Available datasets, API announcements              |
| Bills search (web UI)            | https://main.knesset.gov.il/Activity/Legislation/Laws/Pages/LawSuggestionsSearch.aspx | Verify bill data against API results               |
| Agenda proposals (web UI)        | https://main.knesset.gov.il/apps/agenda/search                                        | Verify proposal data against API results           |
| Parliamentary questions (web UI) | https://main.knesset.gov.il/apps/query/search                                         | Verify query data against API results              |
| Plenum votes (web UI)            | https://main.knesset.gov.il/activity/plenum/votes/pages/default.aspx                  | Verify vote data against API results               |
| OData v4 table list              | https://knesset.gov.il/OdataV4/ParliamentInfo                                         | Discover available tables, check for new additions |
| OData v4 metadata                | https://knesset.gov.il/OdataV4/ParliamentInfo/$metadata                               | Full schema: field names, types, relationships     |
| OData standard                   | https://www.odata.org                                                                 | OData v4 spec for syntax reference                 |
