# Bills & Laws Tables: Full Field Reference

Base URL: `https://knesset.gov.il/OdataV4/ParliamentInfo/`

---

## KNS_Bill: All Bills and Enacted Laws

The primary legislation table. Contains every bill processed by the Knesset from Knesset 1 to present, plus all laws from other periods (British Mandate, Provisional State Council, consolidated/new versions).

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Bill ID (was `BillID` in v2) |
| `KnessetNum` | int | Knesset number (0=Provisional Council, 1-25+) |
| `Name` | string | Bill name (current; historical names in `KNS_BillName`) |
| `TypeID` | int | Type code (v4 only) |
| `TypeDesc` | string | Type description (v4 only) |
| `SubTypeID` | int | Sub-type code |
| `SubTypeDesc` | string | Sub-type: **פרטית** (private/MK), **ממשלתית** (government), **ועדה** (committee) |
| `PrivateNumber` | int | Serial number in the Knesset bill series (פ' number) |
| `CommitteeID` | int | Handling committee ID (null until assigned) |
| `StatusID` | int | Status code: see `KNS_Status` (TypeID=2 for bills) |
| `Number` | int | Publication number (כ' for Knesset bills, מ' for govt bills; null before first reading) |
| `PostponementReasonID` | int | Reason code if bill was halted |
| `PostponementReasonDesc` | string | Reason description |
| `PublicationDate` | datetime | Date published in Sefer HaHukim (null until published) |
| `PublicationSeriesID` | int | Publication series code |
| `PublicationSeriesDesc` | string | Series: ספר החוקים / דיני מדינת ישראל / עיתון רשמי / חוקי ארץ ישראל |
| `PublicationSeriesFirstCallID` | int | Series for first reading publication |
| `PublicationSeriesFirstCallDesc` | string | Series description for first reading |
| `MagazineNumber` | int | Issue number in Sefer HaHukim |
| `PageNumber` | int | Page number in Sefer HaHukim |
| `IsContinuationBill` | bit | Whether continuity law (דין רציפות) applies |
| `SummaryLaw` | string | Law summary (only for bills passed in 3rd reading, Knesset 17+) |
| `LastUpdatedDate` | datetime | Last update timestamp |

**Status 118** = passed in third reading (enacted law).

**Example queries:**
```
# Recent enacted laws
.../KNS_Bill?$filter=KnessetNum eq 25 and StatusID eq 118&$orderby=PublicationDate desc&$top=20

# Private bills proposed in Knesset 25
.../KNS_Bill?$filter=KnessetNum eq 25 and SubTypeDesc eq 'פרטית'&$top=20

# Bills containing keyword
.../KNS_Bill?$filter=contains(Name,'חינוך')&$top=10

# Full bill details including names, initiators, documents
.../KNS_Bill?$filter=Id eq 2216582&$expand=KNS_BillName,KNS_BillInitiator($orderby=IsInitiator desc,Ordinal),KNS_DocumentBill
```

---

## KNS_BillName: Historical Bill Names

Bills can be renamed between readings. This table holds all previous names.

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Row ID |
| `BillID` | int | Bill ID (FK → KNS_Bill) |
| `Name` | string(500) | Historical name |
| `NameHistoryTypeID` | int | Change type code |
| `NameHistoryTypeDesc` | string(125) | Change type (שם לקריאה הראשונה / שם לקריאה השנייה etc.) |
| `LastUpdatedDate` | datetime | Last update |

**Example:**
```
.../KNS_Bill?$filter=Id eq 2216582&$expand=KNS_BillName
```

---

## KNS_BillInitiator: Proposing MKs

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Row ID |
| `BillID` | int | Bill ID |
| `PersonID` | int | MK ID (FK → KNS_Person) |
| `IsInitiator` | bit | 1=primary initiator, 0=co-signer |
| `Ordinal` | int | Position in the proposers list |
| `LastUpdatedDate` | datetime | Last update |

**Example:**
```
# All bills where PersonID=30776 is primary initiator
.../KNS_BillInitiator?$filter=PersonID eq 30776 and IsInitiator eq true and Ordinal eq 1&$expand=KNS_Bill
```

---

## KNS_BillHistoryInitiator: Removed Initiators

MKs who were removed from a bill's proposers list.

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Row ID |
| `BillID` | int | Bill ID |
| `PersonID` | int | MK ID |
| `IsInitiator` | bit | Was primary initiator? |
| `StartDate` | datetime | Date added to proposers |
| `EndDate` | datetime | Date removed |
| `ReasonID` | int | Removal reason code |
| `ReasonDesc` | string(125) | Removal reason description |
| `LastUpdatedDate` | datetime | Last update |

---

## KNS_BillUnion: Merged Bills

Bills that were merged into another bill.

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Row ID |
| `MainBillID` | int | The leading bill after merge |
| `UnionBillID` | int | The bill that was merged in |
| `LastUpdatedDate` | datetime | Last update |

**Example:**
```
# Bills merged INTO bill 2214465
.../KNS_BillUnion?$filter=MainBillID eq 2214465&$expand=KNS_Bill
```

---

## KNS_BillSplit: Split Bills

Bills that were split off from another bill.

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Row ID |
| `MainBillID` | int | Original bill |
| `SplitBillID` | int | New bill created by split (null until split is approved) |
| `Name` | string(250) | Proposed name of split bill |
| `LastUpdatedDate` | datetime | Last update |

---

## KNS_DocumentBill: Bill Documents

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Document ID |
| `BillID` | int | Bill ID |
| `GroupTypeID` | tinyint | Document type code |
| `GroupTypeDesc` | string(100) | Document type (נוסח לקריאה הראשונה / חוק - נוסח לא רשמי / חוק - פרסום ברשומות etc.) |
| `ApplicationID` | tinyint | File format code |
| `ApplicationDesc` | string(10) | File format: **Word**, **PDF**, **TIFF** |
| `FilePath` | string(600) | Full URL to document |
| `LastUpdatedDate` | datetime | Last update |

---

## KNS_IsraelLaw: Parent Laws (Law Corpus)

The authoritative list of all laws of the State of Israel: both enacted in the Knesset and from prior periods.

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Law ID |
| `KnessetNum` | int | Knesset that enacted the original law |
| `Name` | string(255) | Law name |
| `IsBasicLaw` | bit | Is this a Basic Law (חוק יסוד)? |
| `IsFavoriteLaw` | bit | Is this a key reference law? (Interpretation Law, Criminal Law etc.) |
| `IsBudgetLaw` | bit | Is this a budget law? |
| `PublicationDate` | datetime | First publication date |
| `LatestPublicationDate` | datetime | Publication date of most recent amendment |
| `LawValidityID` | int | Validity code |
| `LawValidityDesc` | string(125) | **תקף** (valid) / **בטל** (repealed) / **פקע** (expired) / **נושן** (obsolete) |
| `ValidityStartDate` | datetime | Validity start |
| `ValidityStartDateNotes` | string(500) | Notes on validity start |
| `ValidityFinishDate` | datetime | Expiry date |
| `ValidityFinishDateNotes` | string(500) | Notes on expiry |
| `LastUpdatedDate` | datetime | Last update |

**LawValidityID values:** 1=תקף, 2=בטל, 3=פקע, 4=נושן

**Example:**
```
# All valid Basic Laws
.../KNS_IsraelLaw?$filter=IsBasicLaw eq true and LawValidityID eq 1

# Full law details with classifications and ministry
.../KNS_IsraelLaw?$filter=Id eq 2020919&$expand=KNS_IsraelLawClassificiation,KNS_IsraelLawMinistry($expand=KNS_GovMinistry),KNS_IsraelLawName,KNS_IsraelLawBinding
```

---

## KNS_IsraelLawName: Historical Law Names

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Row ID |
| `IsraelLawID` | int | Parent law ID |
| `LawID` | int | Bill/law that caused the name change |
| `LawTypeID` | int | Type of that law |
| `Name` | string(500) | Previous name |
| `LastUpdatedDate` | datetime | Last update |

---

## KNS_IsraelLawMinistry: Responsible Ministry

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Row ID |
| `IsraelLawID` | int | Law ID |
| `GovMinistryID` | int | Ministry ID (FK → KNS_GovMinistry) |
| `LastUpdatedDate` | datetime | Last update |

**Expand example:**
```
.../KNS_IsraelLaw?$filter=Id eq 2020919&$expand=KNS_IsraelLawMinistry($expand=KNS_GovMinistry)
```

---

## KNS_IsraelLawClassificiation: Subject Classification

**Note:** The name `Classificiation` has a deliberate double-'i' typo. Do NOT correct it.

~45 subject categories assigned by the national legislation database team.

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Row ID |
| `IsraelLawID` | int | Law ID |
| `ClassificiationID` | int | Category code |
| `ClassificiationDesc` | string(50) | Category name (בחירות / ביטחון / חינוך / בריאות etc.) |
| `LastUpdatedDate` | datetime | Last update |

---

## KNS_IsraelLawBinding: Law Replacement Chain

Tracks when one Israel Law replaced another.

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Row ID |
| `IsraelLawID` | int | The new/replacement law |
| `IsraelLawReplacedID` | int | The law that was replaced |
| `LawID` | int | The bill that caused the replacement |
| `LawTypeID` | int | Type of that bill |
| `LastUpdatedDate` | datetime | Last update |

---

## KNS_LawBinding: Bill→IsraelLaw Links

Links enacted bills to the Israel Law they created or amended. Updated only after publication in Sefer HaHukim.

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Row ID |
| `LawID` | int | Bill/law ID |
| `LawTypeID` | int | Bill type |
| `IsraelLawID` | int | Linked Israel Law |
| `ParentLawID` | int | Parent law ID (for grandchild links) |
| `LawParentTypeID` | int | Parent law type |
| `BindingType` | int | Binding type code |
| `BindingTypeDesc` | string(125) | Binding type description |
| `PageNumber` | string(50) | Page number |
| `AmendmentType` | int | Amendment type code |
| `AmendmentTypeDesc` | string(125) | Amendment type description |
| `LastUpdatedDate` | datetime | Last update |

---

## KNS_DocumentIsraelLaw: Israel Law Documents

| Field | Type | Description |
|---|---|---|
| `Id` | int (PK) | Row ID |
| `IsraelLawID` | int | Law ID |
| `GroupTypeID` | int | Document type code |
| `GroupTypeDesc` | string | Document type description |
| `ApplicationID` | int | File format code |
| `ApplicationDesc` | string | File format |
| `FilePath` | string | Full URL to document |
| `LastUpdatedDate` | datetime | Last update |
