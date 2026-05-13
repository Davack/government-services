# Committees Tables: Full Field Reference

Base URL: `https://knesset.gov.il/OdataV4/ParliamentInfo/`

---

## KNS_Committee: All Knesset Committees

Every committee established in every Knesset, from Knesset 1 to present. Sub-committees are linked to their parent via `ParentCommitteeID`.

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Committee ID |
| `Name` | string | Committee name |
| `CategoryID` | int | Category code |
| `CategoryDesc` | string | Category name: the thematic group this committee belongs to across Knessets (e.g. "פנים" for the Interior Committee regardless of exact name changes) |
| `KnessetNum` | int | Knesset number |
| `CommitteeTypeID` | int | Committee type code |
| `CommitteeTypeDesc` | string | **קבועה** (standing) / **מיוחדת** (special) / **משנה** (sub-committee) / **משותפת** (joint) / **הכנסת** (House committee) |
| `Email` | string | Committee email address |
| `StartDate` | datetime | Date established |
| `FinishDate` | datetime | Date dissolved (null if still active) |
| `AdditionalTypeID` | int | Sub-type code |
| `AdditionalTypeDesc` | string | **קבועה** / **מיוחדת** / **חקירה** (investigation) |
| `ParentCommitteeID` | int | Parent committee ID (for sub-committees) |
| `CommitteeParentName` | string | Parent committee name |
| `IsCurrent` | bit | Computed from FinishDate: prefer filtering by `KnessetNum` |
| `LastUpdatedDate` | datetime | Last update |

**CommitteeTypeID=71** = standing (קבועה) committee: use this to get the main committees.

**Example queries:**
```
# Standing committees of Knesset 25
.../KNS_Committee?$filter=KnessetNum eq 25 and CommitteeTypeID eq 71&$orderby=Name

# Sub-committees of committee 4187
.../KNS_Committee?$filter=ParentCommitteeID eq 4187

# All committees in the "Interior" category across all Knessets
.../KNS_Committee?$filter=CategoryID eq 28&$orderby=KnessetNum

# All committees of Knesset 25 (all types)
.../KNS_Committee?$filter=KnessetNum eq 25&$orderby=CommitteeTypeDesc,Name
```

---

## KNS_CommitteeSession: Committee Meetings

Every session held (or scheduled) by every committee.

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Session ID |
| `Number` | int | Session number within this committee |
| `KnessetNum` | int | Knesset number |
| `TypeID` | int | Session type code |
| `TypeDesc` | string(125) | **רגילה** (regular) / **סיור** (tour/site visit) |
| `SessionSubTypeId` | int | Classification code |
| `SessionSubTypeDesc` | string | **פתוחה** (open) / **חסויה** (closed) |
| `CommitteeID` | int | Committee ID |
| `Location` | nstring(500) | Location |
| `SessionUrl` | nstring | Ignore in v4: use `KNS_BroadcastCommitteSession` instead |
| `BroadcastUrl` | nstring | Broadcast URL |
| `StartDate` | datetime | Start datetime |
| `FinishDate` | datetime | End datetime |
| `Note` | string(500) | Notes |
| `StatusID` | int | Status code: **193 = cancelled** |
| `LastUpdatedDate` | datetime | Last update |

**IMPORTANT:** Always add `StatusID ne 193` to exclude cancelled sessions.

**Example queries:**
```
# Non-cancelled sessions for committee 926 (Economy Committee, K20)
.../KNS_CommitteeSession?$filter=CommitteeID eq 926 and StatusID ne 193&$orderby=Number

# Sessions in a date range for a committee
.../KNS_CommitteeSession?$filter=CommitteeID eq 926 and StatusID ne 193 and StartDate gt 2015-06-01T00:00:01Z and StartDate lt 2015-06-10T00:00:01Z&$orderby=Number

# Specific session + its agenda items + documents
.../KNS_CommitteeSession?$filter=Id eq 2214483&$expand=KNS_CmtSessionItem,KNS_DocumentCommitteeSession
```

---

## KNS_CmtSessionItem: Items on Committee Agenda

The items placed on each committee session's agenda.

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Row ID |
| `ItemID` | int | Item ID (cross-references KNS_Bill, KNS_Query, etc. based on ItemTypeID) |
| `CommitteeSessionID` | int | Session ID |
| `Ordinal` | int | Item order in the session |
| `StatusID` | int | Status code at time of session |
| `Name` | string(255) | Item name as it appears in the session |
| `ItemTypeID` | int | Item type code (FK → KNS_ItemType) |
| `LastUpdatedDate` | datetime | Last update |

**Example:**
```
# All items on session 551024
.../KNS_CmtSessionItem?$filter=CommitteeSessionID eq 551024&$orderby=Ordinal
```

---

## KNS_DocumentCommitteeSession: Session Documents

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Document ID |
| `CommitteeSessionID` | int | Session ID |
| `GroupTypeID` | tinyint | Document type code |
| `GroupTypeDesc` | string(100) | Document type (protocol, transcript, etc.) |
| `ApplicationID` | tinyint | File format code |
| `ApplicationDesc` | string(10) | File format: Word / PDF / TIFF |
| `FilePath` | string(600) | Full URL to document |
| `LastUpdatedDate` | datetime | Last update |

**Note (v4 fix):** Duplicate record IDs that existed in v2 have been corrected in v4.

**Example:**
```
# Documents for a specific session
.../KNS_DocumentCommitteeSession?$filter=CommitteeSessionID eq 2214788&$orderby=Id
```

---

## KNS_JointCommittee: Joint Committee Members

Tracks which committees participate in a joint committee.

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Row ID |
| `CommitteeID` | int | The joint committee ID |
| `ParticipantCommitteeID` | int | A participating committee ID |
| `LastUpdatedDate` | datetime | Last update |

**Example:**
```
# Committees that make up joint committee 4202
.../KNS_JointCommittee?$filter=CommitteeID eq 4202
```

---

## KNS_BroadcastCommitteSession: Session Broadcast Links (v4 only)

Maps committee sessions to their live-stream/broadcast URLs. Only available in OData v4.

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Session ID (= CommitteeSession ID) |
| `BroadcastId` | int | Broadcast identifier |
| `BroadcastUrl` | string | URL to the session recording/live-stream |

**Example:**
```
.../KNS_BroadcastCommitteSession?$filter=Id eq 2214483
```

---

## KNS_CmtSiteCode: Committee ID Mapping

Maps the internal Sanhedrin committee ID to the website committee ID (needed for constructing some website URLs).

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Row ID |
| `KnsID` | int | Committee ID in the Sanhedrin system (used in all OData tables) |
| `SiteId` | int | Committee ID used in the Knesset website (for URL construction) |

**Example:**
```
# Website ID for committee 4187 (National Security Committee, K25)
.../KNS_CmtSiteCode?$filter=KnsID eq 4187
```
