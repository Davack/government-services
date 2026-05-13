# Secondary Legislation Tables: Full Field Reference

Base URL: `https://knesset.gov.il/OdataV4/ParliamentInfo/`

---

## Overview

Secondary legislation (חקיקת משנה) covers regulations, orders, rules, decisions, proclamations, and other legal instruments issued under the authority of primary legislation (חוקי אב). The Knesset is involved in these through committee oversight.

This section also covers:
- **Reports under law** (דיווחים על פי חוק): mandatory government reports to the Knesset
- **Other legal actions** (פעולות אחרות על פי חוק): other parliamentary actions required by law

**Important:** The data in these tables is still being compiled and is not yet complete. It is a work-in-progress by the Knesset's legal department and national legislation database team.

Relevant web interfaces:
- Reports: `https://main.knesset.gov.il/APPS/secondaryLaw/main/potential`
- Actions: `https://main.knesset.gov.il/APPS/secondaryLaw/main/actions`

---

## KNS_SecondaryLaw: Secondary Legislation Items

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Item ID |
| `KnessetNum` | int | Knesset number |
| `Name` | string | Item name |
| `CompletionCauseID` | int | Completion cause code |
| `CompletionCauseDesc` | string | Completion cause description |
| `PostponementReasonID` | int | Postponement reason code |
| `PostponementReasonDesc` | string | Postponement reason description |
| `KnessetInvolvementID` | int | Knesset involvement type code |
| `KnessetInvolvementDesc` | string | Knesset involvement type description |
| `CommitteeID` | int | Handling committee ID |
| `PublicationSeriesID` | int | Publication series code |
| `PublicationSeriesDesc` | string | Publication series description |
| `MagazineNumber` | string | Issue number in publication series |
| `PageNumber` | string | Page number |
| `PublicationDate` | datetime | Publication date in official gazette (Reshumot) |
| `MajorAuthorizingLawID` | int | Primary authorizing law ID |
| `CommitteeReceivedDate` | datetime | Date received by committee |
| `CommitteeApprovalDate` | datetime | Date approved by committee |
| `ApprovalDateWithoutDiscussion` | datetime | Date approved without discussion |
| `IsAmmendingLawOriginal` | boolean | Is this amending the original law? |
| `ClassificationID` | int | Sub-classification code |
| `ClassificationDesc` | string | **תקנות** (regulations) / **צו** (order) / **כללים** (rules) / **החלטה** (decision) / **הודעה** (notice) / **אכרזה** (proclamation) / **תקנון** (by-laws) / **הוראות** (instructions) / **תיקון טעות** (correction) / **אחר** (other) |
| `IsEmergency` | boolean | Emergency legislation? |
| `SecretaryReceivedDate` | datetime | Date received by Knesset secretariat |
| `PlenumApprovalDate` | datetime | Date approved by plenum |
| `TypeID` | int | Type code |
| `TypeDesc` | string | **חקיקת משנה** (secondary legislation) / **דיווח על פי חוק** (statutory report) / **פעולה אחרת על פי חוק** (other legal action) |
| `StatusID` | int | Status code |
| `StatusName` | string | Status description |
| `IsCurrent` | boolean | Is this the current version? |
| `LastUpdatedDate` | datetime | Last update |

**TypeID values:** 1=secondary legislation, 2=statutory report, 3=other legal action

**ClassificationDesc values for secondary legislation:**
- תקנות: regulations (most common)
- צו: order
- כללים: rules
- החלטה: decision
- הודעה: notice
- אכרזה: proclamation
- תקנון: by-laws/constitution
- הוראות: instructions/directives
- תיקון טעות: error correction
- אחר: other

**Example queries:**
```
# Get a specific secondary law item
.../KNS_SecondaryLaw?$filter=Id eq 2198278

# Secondary legislation (regulations) published in 2024
.../KNS_SecondaryLaw?$filter=TypeID eq 1 and PublicationDate gt 2024-01-01&$top=20&$orderby=PublicationDate desc

# Proclamations (אכרזה)
.../KNS_SecondaryLaw?$filter=contains(ClassificationDesc,'אכרזה')&$top=10

# Emergency regulations
.../KNS_SecondaryLaw?$filter=IsEmergency eq true&$top=10&$orderby=PublicationDate desc

# Secondary law with all related info (regulator + authorizing law + documents)
.../KNS_SecondaryLaw?$filter=Id eq 2198278&$expand=KNS_SecLawRegulator,KNS_SecLawAuthorizingLaw,KNS_DocumentSecondaryLaw

# Items assigned to a specific committee
.../KNS_SecondaryLaw?$filter=CommitteeID eq 926&$top=20

# Statutory reports (TypeID=2)
.../KNS_SecondaryLaw?$filter=TypeID eq 2&$top=20
```

---

## KNS_SecLawRegulator: Regulator Details

Which ministry or body is responsible for issuing the secondary legislation.

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Row ID |
| `SecondaryLawID` | int | Secondary law ID |
| `RegulatorTypeID` | int | Regulator type code |
| `RegulatorTypeDesc` | string | Regulator type (e.g. **משרדים** = ministries) |
| `RegulatorID` | int | Regulator ID |
| `RegulatorDesc` | string | Regulator name (e.g. משרד האוצר) |
| `LastUpdatedDate` | datetime | Last update |

**Example:**
```
.../KNS_SecondaryLaw?$filter=Id eq 2198278&$expand=KNS_SecLawRegulator
```

---

## KNS_SecLawAuthorizingLaw: Authorizing Primary Law

Links secondary legislation to the primary law that grants authority to issue it.

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Row ID |
| `AuthorizingLawID` | int | ID of the authorizing primary law (FK → KNS_Bill or KNS_IsraelLaw) |
| `SecondaryLawID` | int | Secondary law ID |
| `LastUpdatedDate` | datetime | Last update |

**Example:**
```
.../KNS_SecondaryLaw?$filter=Id eq 2198278&$expand=KNS_SecLawAuthorizingLaw
```

---

## KNS_DocumentSecondaryLaw: Secondary Legislation Documents

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Row ID |
| `SecondaryLawId` | int | Secondary law ID |
| `GroupTypeID` | byte | Document type code |
| `GroupTypeDesc` | string | Document type (e.g. חקיקת משנה - פניית הגורם המוסמך) |
| `ApplicationID` | byte | File format code |
| `ApplicationDesc` | string | File format (PDF, Word, etc.) |
| `FilePath` | string | Full URL to document |
| `LastUpdatedDate` | DateTimeOffset | Last update |

**Example:**
```
.../KNS_SecondaryLaw?$filter=Id eq 2198278&$expand=KNS_DocumentSecondaryLaw

# Proclamation with documents
.../KNS_SecondaryLaw?$filter=Id eq 2227959&$expand=KNS_DocumentSecondaryLaw
```

---

## KNS_SecToSecBinding: Relations Between Secondary Laws

Tracks amendments and other relationships between secondary legislation items.

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Row ID |
| `SecChildID` | int | Child/amending item ID |
| `SecChildTypeID` | int | Child item type |
| `SecParentID` | int | Parent/amended item ID |
| `SecParentTypeID` | int | Parent item type |
| `SecMainID` | int | Main/root item ID |
| `SecMainTypeID` | int | Main item type |
| `BindingTypeID` | int | Binding type code |
| `BindingTypeDesc` | string | Binding type (e.g. **מתקן** = amending) |
| `IsTempLegislation` | boolean | Is the amendment temporary? |
| `IsSecondaryAmendment` | boolean | Is this a secondary (indirect) amendment? |
| `CorrectionNumber` | int | Amendment number |
| `AmendmentTypeID` | int | Amendment type code |
| `AmendmentTypeDesc` | string | Amendment type (e.g. **ישיר** = direct) |
| `ParagraphNumber` | string | Section/paragraph number |
| `LastUpdatedDate` | datetime | Last update |

**Example:**
```
# Secondary law item 2089728 and what amended it
.../KNS_SecondaryLaw?$filter=Id eq 2089728&$expand=KNS_SecToSecBinding
```
