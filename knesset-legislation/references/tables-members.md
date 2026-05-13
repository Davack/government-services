# Members of Knesset Tables: Full Field Reference

Base URL: `https://knesset.gov.il/OdataV4/ParliamentInfo/`

---

## KNS_Person: All MKs and Government Members

Every person who has ever served as an MK or government minister, from the founding of the state to present.

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Person ID |
| `LastName` | string(50) | Last name (Hebrew) |
| `FirstName` | string(50) | First name (Hebrew) |
| `GenderID` | int | Gender code |
| `GenderDesc` | string(125) | Gender description |
| `Email` | string(100) | Email address |
| `IsCurrent` | bit | Currently serving? (computed: prefer filtering via KNS_PersonToPosition) |
| `LastUpdatedDate` | datetime | Last update |

**Search is Hebrew-only.** Use `contains(LastName,'...')` with Hebrew text.

**Example queries:**
```
# Find MK by last name
.../KNS_Person?$filter=contains(LastName,'נתניהו')

# Get person by ID with all their positions
.../KNS_Person?$filter=Id eq 532&$expand=KNS_PersonToPosition($orderby=StartDate,Id)

# Find persons whose last name contains a string
.../KNS_Person?$filter=contains(LastName,'לפיד')&$orderby=Id
```

---

## KNS_Position: Position Types

The catalog of all position types that exist in the Knesset system.

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Position ID |
| `Description` | string(250) | Position name (חבר כנסת / חברת כנסת / יו"ר ועדה / שר / שרה etc.) |
| `GenderID` | int | Gender code for this position form |
| `GenderDesc` | string(125) | Gender description |
| `LastUpdatedDate` | datetime | Last update |

**Key position IDs:**
| ID | Description |
|---|---|
| 43 | חבר כנסת (male MK) |
| 61 | חברת כנסת (female MK) |
| 41 | יו"ר ועדה (committee chair) |
| 54 | חבר סיעה (faction member) |
| 37 | שר (male minister) |
| 39 | שרה (female minister) |
| 57 | ראש ממשלה (Prime Minister) |
| 67 | ראשת ממשלה (female PM) |

**Example:**
```
# All position types
.../KNS_Position?$orderby=Description
```

---

## KNS_PersonToPosition: Roles Held by Persons

The central join table linking persons to their roles, factions, committees, and ministries across all Knessets.

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Row ID |
| `PersonID` | int | Person ID (FK → KNS_Person) |
| `PositionID` | int | Position type ID (FK → KNS_Position) |
| `KnessetNum` | int | Knesset number |
| `GovMinistryID` | int | Ministry ID (for minister positions) |
| `GovMinistryName` | string(50) | Ministry name |
| `DutyDesc` | string(250) | Specific duty (e.g. "השר לענייני מודיעין") |
| `FactionID` | int | Faction ID (FK → KNS_Faction) |
| `FactionName` | string(50) | Faction name |
| `GovernmentNum` | int | Government number (for minister positions) |
| `CommitteeID` | int | Committee ID (for committee positions) |
| `CommitteeName` | string(250) | Committee name |
| `StartDate` | datetime | Role start date |
| `FinishDate` | datetime | Role end date (null = currently active) |
| `IsCurrent` | bit | Currently active? |
| `LastUpdatedDate` | datetime | Last update |

**Example queries:**
```
# All currently serving MKs (both gender position IDs)
.../KNS_PersonToPosition?$filter=PositionID in (43,61) and FinishDate eq null&$expand=KNS_Person&$orderby=KNS_Person/LastName,KNS_Person/FirstName&$count=true

# Count currently serving MKs (should be 120)
.../KNS_PersonToPosition?$filter=PositionID in (43,61) and FinishDate eq null&$count=true&$top=0

# All roles of a specific person
.../KNS_PersonToPosition?$filter=PersonID eq 532&$expand=KNS_Position&$orderby=StartDate

# All Justice Ministers ever
.../KNS_PersonToPosition?$filter=contains(GovMinistryName,'המשפטים')&$orderby=StartDate&$expand=KNS_Person

# Current committee chairs
.../KNS_PersonToPosition?$filter=PositionID eq 41 and FinishDate eq null&$expand=KNS_Person,KNS_Committee_fake

# Chairs of 3 specific committees
.../KNS_PersonToPosition?$filter=CommitteeID in (4208,4209,4197) and PositionID eq 41 and FinishDate eq null&$expand=KNS_Person,KNS_Position

# All members of Knesset 25 who were in faction X
.../KNS_PersonToPosition?$filter=KnessetNum eq 25 and FactionID eq 1100&$expand=KNS_Person&$orderby=KNS_Person/LastName
```

---

## KNS_Faction: Factions / Parliamentary Groups

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Faction ID |
| `Name` | string(50) | Faction name |
| `KnessetNum` | int | Knesset number |
| `StartDate` | datetime | Faction start date |
| `FinishDate` | datetime | Faction end date (null if active) |
| `IsCurrent` | bit | Currently active? |
| `LastUpdatedDate` | datetime | Last update |

Each Knesset has its own faction records: factions are re-established for each Knesset.

**Example queries:**
```
# All factions in Knesset 25
.../KNS_Faction?$filter=KnessetNum eq 25&$orderby=Name

# Find a faction by name
.../KNS_Faction?$filter=KnessetNum eq 25 and contains(Name,'ליכוד')

# Members of faction ID 1100 in Knesset 25
.../KNS_PersonToPosition?$filter=FactionID eq 1100 and PositionID eq 54 and FinishDate eq null&$expand=KNS_Person&$orderby=KNS_Person/LastName
```

---

## KNS_MkSiteCode: MK ID Mapping

For historical reasons, the Knesset website uses a different ID for MKs than the Sanhedrin internal system (which is what all OData tables use). This mapping table lets you translate between the two.

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Row ID |
| `KnsID` | int | MK ID in the Sanhedrin system (used in all OData tables) |
| `SiteId` | int | MK ID in the Knesset website (used in some website URLs) |

**Example:**
```
# Shimon Peres: internal ID=456, website ID=104
.../KNS_MkSiteCode?$filter=KnsID eq 456

# Full mapping table
.../KNS_MkSiteCode?$orderby=Id
```

Website URL for an MK uses the SiteId:
`https://main.knesset.gov.il/mk/Apps/mk/mk-personal-details/<SiteId>`
