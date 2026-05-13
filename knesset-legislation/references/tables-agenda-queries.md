# Agenda Proposals & Parliamentary Questions: Full Field Reference

Base URL: `https://knesset.gov.il/OdataV4/ParliamentInfo/`

---

## KNS_Agenda: Agenda Proposals (הצעות לסדר-היום)

MKs can propose topics for discussion in the Knesset plenum or for urgent committee discussion. This table contains all agenda proposals.

Types of agenda proposals:
- **רגילה**: Regular: submitted for plenum discussion
- **דחופה**: Urgent: submitted for same-week plenum discussion
- **דיון מהיר**: Fast-track: sent for urgent committee discussion (must be scheduled within 10 days)
- **תקופת פגרה**: Recess-period proposal

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Proposal ID (was `AgendaID` in v2) |
| `Number` | int | Proposal serial number |
| `ClassificationID` | int | Proposal type code |
| `ClassificationDesc` | string | **רגילה** / **דחופה** / **דיון מהיר** / **תקופת פגרה** |
| `LeadingAgendaID` | int | ID of the umbrella combined proposal (if this is part of a bundle) |
| `KnessetNum` | int | Knesset number |
| `Name` | string | Proposal title |
| `SubTypeID` | int | Sub-type code |
| `SubTypeDesc` | string | **כוללת** (combined/umbrella) / **עצמאית** (standalone) |
| `StatusID` | int | Status code (FK → KNS_Status) |
| `InitiatorPersonID` | int | Submitting MK's person ID |
| `GovRecommendationID` | int | Government's recommendation code |
| `GovRecommendationDesc` | string | Government's recommendation text |
| `PresidentDecisionDate` | datetime | Date of Knesset Speaker's decision |
| `PostopenmentReasonID` | int | Postponement reason code |
| `PostopenmentReasonDesc` | string | Postponement reason description |
| `CommitteeID` | int | Assigned handling committee |
| `RecommendCommitteeID` | int | Recommended committee |
| `MinisterPersonID` | int | Responding minister's person ID |
| `LastUpdatedDate` | datetime | Last update |

**Example queries:**
```
# Count of proposals in Knesset 24
.../KNS_Agenda?$filter=KnessetNum eq 24&$count=true&$top=0

# Urgent proposals in Knesset 25
.../KNS_Agenda?$filter=KnessetNum eq 25 and contains(ClassificationDesc,'דחופה')&$top=20

# Fast-track committee discussion proposals
.../KNS_Agenda?$filter=KnessetNum eq 25 and contains(ClassificationDesc,'דיון מהיר')&$top=20

# Proposals by a specific MK
.../KNS_Agenda?$filter=InitiatorPersonID eq 532&$top=10&$orderby=Id desc

# Specific proposal with documents
.../KNS_Agenda?$filter=Id eq 2202059&$expand=KNS_DocumentAgenda

# Items inside a combined (umbrella) proposal
.../KNS_Agenda?$filter=LeadingAgendaID eq 2166943

# Proposals sent to a specific committee
.../KNS_Agenda?$filter=CommitteeID eq 926&$top=20&$orderby=Id desc
```

---

## KNS_DocumentAgenda: Agenda Proposal Documents

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Document ID (was `DocumentAgendaID` in v2) |
| `AgendaID` | int | Proposal ID (FK → KNS_Agenda) |
| `GroupTypeID` | tinyint | Document type code |
| `GroupTypeDesc` | string(100) | Document type description |
| `ApplicationID` | tinyint | File format code |
| `ApplicationDesc` | string(10) | File format: Word / PDF / TIFF |
| `FilePath` | string(600) | Full URL to document |
| `LastUpdatedDate` | datetime | Last update |

**Example:**
```
.../KNS_Agenda?$filter=Id eq 2202059&$expand=KNS_DocumentAgenda
```

---

## KNS_Query: Parliamentary Questions (שאילתות)

MKs can submit questions to ministers. Three types exist:
- **רגילה**: Regular: answered in plenum; up to 30 per MK per session
- **דחופה**: Urgent: Speaker-designated urgent; answered in plenum same week; up to 4 per MK per session
- **ישירה**: Direct: answered in writing; NOT included in OData (only regular and urgent are)

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Query ID (was `QueryID` in v2) |
| `Number` | int | Query serial number |
| `KnessetNum` | int | Knesset number |
| `Name` | string(255) | Question title |
| `TypeID` | int | Type code |
| `TypeDesc` | string(125) | **רגילה** (regular) / **דחופה** (urgent) |
| `StatusID` | int | Status code |
| `PersonID` | int | Submitting MK's person ID |
| `GovMinistryID` | int | Ministry questioned |
| `SubmitDate` | datetime | Date submitted |
| `ReplyMinisterDate` | datetime | Date minister answered (actual) |
| `ReplyDatePlanned` | datetime | Planned reply date |
| `LastUpdatedDate` | datetime | Last update |

**TypeID values:** 48=regular (רגילה), 49=urgent (דחופה)

**Example queries:**
```
# Questions submitted to defense ministry
.../KNS_Query?$filter=contains(GovMinistryName,'ביטחון')&$top=10&$orderby=SubmitDate desc

# Count regular questions in Knesset 24 (TypeID=48)
.../KNS_Query?$filter=KnessetNum eq 24 and TypeID eq 48&$count=true&$top=0

# Questions by a specific MK
.../KNS_Query?$filter=PersonID eq 532&$top=10&$orderby=SubmitDate desc

# Unanswered questions
.../KNS_Query?$filter=KnessetNum eq 25 and ReplyMinisterDate eq null&$top=20

# Specific question + documents
.../KNS_Query?$filter=Id eq 2199342&$expand=KNS_DocumentQuery($orderby=GroupTypeID,ApplicationDesc)

# Questions submitted to Justice Ministry
.../KNS_Query?$filter=contains(GovMinistryName,'משפטים')&$top=10&$orderby=SubmitDate desc
```

---

## KNS_DocumentQuery: Query Documents

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Document ID (was `DocumentQueryID` in v2) |
| `QueryID` | int | Query ID (FK → KNS_Query) |
| `GroupTypeID` | tinyint | Document type code |
| `GroupTypeDesc` | string(100) | Document type (question text, reply, etc.) |
| `ApplicationID` | tinyint | File format code |
| `ApplicationDesc` | string(10) | File format: Word / PDF / TIFF |
| `FilePath` | string(600) | Full URL to document |
| `LastUpdatedDate` | datetime | Last update |

**Example:**
```
.../KNS_DocumentQuery?$filter=QueryID eq 2198871&$orderby=GroupTypeID
```
