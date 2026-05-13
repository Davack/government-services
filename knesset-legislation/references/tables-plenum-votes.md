# Plenum & Votes Tables: Full Field Reference

Base URL: `https://knesset.gov.il/OdataV4/ParliamentInfo/`

---

## KNS_PlenumSession: Plenary Sessions

Every plenary (full Knesset floor) session.

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Session ID |
| `Number` | int | Sequential session number within this Knesset |
| `KnessetNum` | int | Knesset number |
| `Name` | string(255) | Session name |
| `StartDate` | datetime | Start date and time |
| `FinishDate` | datetime | End date and time |
| `IsSpecialMeeting` | bit | Special session (e.g. memorial session)? |
| `LastUpdatedDate` | datetime | Last update |

**Example queries:**
```
# Latest 10 plenary sessions in Knesset 25
.../KNS_PlenumSession?$filter=KnessetNum eq 25&$orderby=Number desc&$top=10

# Specific session by ID
.../KNS_PlenumSession?$filter=Id eq 2219138

# Special sessions in Knesset 25
.../KNS_PlenumSession?$filter=KnessetNum eq 25 and IsSpecialMeeting eq true

# Session with agenda items (discussions only)
.../KNS_PlenumSession?$filter=Id eq 2219138&$expand=KNS_PlmSessionItem($filter=IsDiscussion eq 1;$orderby=Ordinal)

# Latest 3 sessions + official transcripts
.../KNS_PlenumSession?$filter=KnessetNum eq 25&$expand=KNS_DocumentPlenumSession($filter=GroupTypeID eq 28)&$orderby=Number desc&$top=3
```

---

## KNS_PlmSessionItem: Items on Plenary Agenda

The items placed on each plenary session's agenda.

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Row ID |
| `ItemID` | int | Item ID (cross-references bill, query, agenda etc. based on ItemTypeID) |
| `PlenumSessionID` | int | Session ID |
| `ItemTypeID` | int | Item type code (FK → KNS_ItemType) |
| `ItemTypeDesc` | string(125) | Item type description |
| `Ordinal` | int | Position in the session: **KNOWN BUG: sorting by Ordinal is broken** |
| `Name` | string(255) | Item name as shown in session |
| `StatusID` | int | Status code |
| `IsDiscussion` | int | 1=continuation/discussion item, 0=first appearance |
| `LastUpdatedDate` | datetime | Last update |

**IMPORTANT:** The `Ordinal` field cannot be relied upon for sorting in this table (known API bug).

**Example queries:**
```
# Discussion items for a session (without broken Ordinal sort)
.../KNS_PlmSessionItem?$filter=PlenumSessionID eq 2219138 and IsDiscussion eq 1

# All items on a session regardless of type
.../KNS_PlmSessionItem?$filter=PlenumSessionID eq 2219138
```

---

## KNS_DocumentPlenumSession: Plenary Session Documents

Documents associated with plenary sessions: including the official Knesset transcript (Divrei HaKnesset).

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Document ID |
| `PlenumSessionID` | int | Session ID |
| `GroupTypeID` | tinyint | Document type code |
| `GroupTypeDesc` | string(100) | Document type description |
| `ApplicationID` | tinyint | File format code |
| `ApplicationDesc` | string(10) | File format: Word / PDF / TIFF |
| `FilePath` | string(600) | Full URL to document |
| `LastUpdatedDate` | datetime | Last update |

**GroupTypeID=28** = Divrei HaKnesset (דברי הכנסת): the official verbatim transcript.

**Example queries:**
```
# All documents for a session
.../KNS_PlenumSession?$filter=Id eq 2219138&$expand=KNS_DocumentPlenumSession

# Official transcript only
.../KNS_DocumentPlenumSession?$filter=PlenumSessionID eq 2219138 and GroupTypeID eq 28
```

---

## KNS_PlenumVote: Votes Taken in Plenary

The record of every vote taken on the Knesset floor.

| Field | Type | Description |
|---|---|---|
| `Id` (= `VoteID`) | int32 | Vote ID: note: field is `Id` in filter but response shows as `VoteID` |
| `VoteDateTime` | DateTimeOffset | Date and time of the vote |
| `SessionID` | int32 | Plenary session ID (FK → KNS_PlenumSession) |
| `ItemID` | int32 | Item voted on |
| `Ordinal` | int32 | Vote order within the session |
| `VoteMethodID` | int32 | Voting method code |
| `VoteMethodDesc` | string | **אלקטרונית** (electronic) / **ידנית** (manual) / **שמית** (by name/roll call) |
| `VoteStatusCode` | int32 | Status code |
| `VoteStatusDesc` | string | Status description (מפורסם = published) |
| `VoteTitle` | string | Vote title |
| `VoteSubject` | string | Vote subtitle |
| `IsNoConfidenceInGov` | boolean | Is this a no-confidence vote? |
| `LastModified` | DateTimeOffset | Last update |
| `ForOptionID` | int32 | "For" option code |
| `ForOptionDesc` | string | "For" option description |
| `AgainstOptionID` | int32 | "Against" option code |
| `AgainstOptionDesc` | string | "Against" option description |

**Example queries:**
```
# Latest 10 votes
.../KNS_PlenumVote?$orderby=Id desc&$top=10

# Get a specific vote
.../KNS_PlenumVote?$filter=Id eq 42594

# All votes in a plenary session
.../KNS_PlenumVote?$filter=SessionID eq 2219138&$orderby=Ordinal

# No-confidence votes (historic)
.../KNS_PlenumVote?$filter=IsNoConfidenceInGov eq true&$orderby=VoteDateTime desc

# Roll-call (nominal) votes
.../KNS_PlenumVote?$filter=VoteMethodID eq [nominal_code]&$orderby=VoteDateTime desc&$top=10
```

---

## KNS_PlenumVoteResult: Per-MK Vote Results

The individual vote cast by each MK for each plenary vote.

| Field | Type | Description |
|---|---|---|
| `Id` | int32 (PK) | Row ID |
| `MKID` | int32 | MK person ID (FK → KNS_Person) |
| `VoteID` | int32 | Vote ID (FK → KNS_PlenumVote) |
| `VoteDate` | DateTimeOffset | Vote date |
| `ResultCode` | int32 | Vote result code |
| `ResultDesc` | string | Vote result: **בעד** (for) / **נגד** (against) / **נמנע** (abstain) |
| `LastModified_DateTime` | DateTimeOffset | Last update |

**Example queries:**
```
# All MK votes for a specific vote
.../KNS_PlenumVoteResult?$filter=VoteID eq 42594&$orderby=Id

# How a specific MK voted (MKID=532)
.../KNS_PlenumVoteResult?$filter=MKID eq 532 and VoteID eq 42594

# All votes by a specific MK on recent sessions
.../KNS_PlenumVoteResult?$filter=MKID eq 532&$orderby=VoteDate desc&$top=20
```

**Note:** The `MKID` in this table uses the Knesset website's internal vote system ID, which may differ from the Sanhedrin PersonID. Use `KNS_MkSiteCode` to map between them if needed.
