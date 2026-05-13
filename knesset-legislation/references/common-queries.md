# Common Ready-to-Use Queries

Base URL: `https://knesset.gov.il/OdataV4/ParliamentInfo/`

---

## Bills & Laws

```
# 20 most recently published laws in Knesset 25
.../KNS_Bill?$filter=KnessetNum eq 25&$orderby=PublicationDate desc&$top=20

# Search bill by keyword in title
.../KNS_Bill?$filter=contains(Name,'ביטוח')&$top=10

# Get specific bill + its initiators + documents
.../KNS_Bill?$filter=Id eq 2216582&$expand=KNS_BillInitiator($orderby=IsInitiator desc,Ordinal),KNS_DocumentBill

# Bills proposed by a specific MK (PersonID=30776)
.../KNS_BillInitiator?$filter=PersonID eq 30776 and IsInitiator eq true&$expand=KNS_Bill

# Bill with highest serial number in Knesset 25
.../KNS_Bill?$filter=KnessetNum eq 25&$orderby=Number desc&$top=1
```

## Israel Laws (parent law corpus)

```
# All currently valid basic laws (חוקי יסוד)
.../KNS_IsraelLaw?$filter=IsBasicLaw eq true and LawValidityID eq 1

# Search valid laws by subject
.../KNS_IsraelLaw?$filter=contains(Name,'חינוך') and LawValidityID eq 1

# Law with full classification, ministry, and history
.../KNS_IsraelLaw?$filter=Id eq 2020919&$expand=KNS_IsraelLawClassificiation,KNS_IsraelLawMinistry($expand=KNS_GovMinistry),KNS_IsraelLawBinding
```

## MKs & Persons

```
# Find MK by last name
.../KNS_Person?$filter=contains(LastName,'נתניהו')

# All currently serving MKs (both position IDs cover male/female forms)
.../KNS_PersonToPosition?$filter=PositionID in (43,61) and FinishDate eq null&$expand=KNS_Person&$orderby=KNS_Person/LastName,KNS_Person/FirstName&$count=true

# All roles held by a specific person (ID=532)
.../KNS_Person?$filter=Id eq 532&$expand=KNS_PersonToPosition($orderby=StartDate,Id)

# All Justice Ministers ever
.../KNS_PersonToPosition?$filter=contains(GovMinistryName,'המשפטים')&$orderby=StartDate

# All committee chairs in current Knesset (PositionID=41)
.../KNS_PersonToPosition?$filter=PositionID eq 41 and FinishDate eq null&$expand=KNS_Person
```

## Factions

```
# All factions in Knesset 25
.../KNS_Faction?$filter=KnessetNum eq 25&$orderby=Name

# Members of a specific faction (ID=1100 = Labor in K25)
.../KNS_PersonToPosition?$filter=FactionID eq 1100 and PositionID eq 54 and FinishDate eq null&$expand=KNS_Person
```

## Committees

```
# Primary committees of Knesset 25 (CommitteeTypeID=71 = standing committee)
.../KNS_Committee?$filter=KnessetNum eq 25 and CommitteeTypeID eq 71&$orderby=Name

# Committee sessions for a specific committee, excluding cancelled (StatusID 193)
.../KNS_CommitteeSession?$filter=CommitteeID eq 926 and StatusID ne 193&$orderby=Number

# Session + its agenda items + documents
.../KNS_CommitteeSession?$filter=Id eq 2214483&$expand=KNS_CmtSessionItem,KNS_DocumentCommitteeSession
```

## Plenum

```
# Latest 5 plenary sessions in Knesset 25
.../KNS_PlenumSession?$filter=KnessetNum eq 25&$orderby=Number desc&$top=5

# Items discussed in a plenary session (IsDiscussion=1 = continuation item)
.../KNS_PlmSessionItem?$filter=PlenumSessionID eq 2219138 and IsDiscussion eq 1&$orderby=Ordinal

# Latest 3 sessions with official transcripts (GroupTypeID=28 = Divrei HaKnesset)
.../KNS_PlenumSession?$filter=KnessetNum eq 25&$expand=KNS_DocumentPlenumSession($filter=GroupTypeID eq 28)&$orderby=Number desc&$top=3
```

## Votes

```
# Latest votes
.../KNS_PlenumVote?$orderby=Id desc&$top=10

# Get a specific vote
.../KNS_PlenumVote?$filter=Id eq 42594

# Per-MK results for a vote
.../KNS_PlenumVoteResult?$filter=VoteID eq 42594&$orderby=Id

# No-confidence votes
.../KNS_PlenumVote?$filter=IsNoConfidenceInGov eq true&$orderby=VoteDateTime desc
```

## Parliamentary Questions (שאילתות)

```
# Questions submitted to a specific ministry
.../KNS_Query?$filter=contains(GovMinistryName,'ביטחון')&$top=10&$orderby=SubmitDate desc

# Count of regular questions in Knesset 24 (TypeID=48 = regular)
.../KNS_Query?$filter=KnessetNum eq 24 and TypeID eq 48&$count=true&$top=0

# Specific question + documents
.../KNS_Query?$filter=Id eq 2199342&$expand=KNS_DocumentQuery
```

## Agenda Proposals (הצעות לסדר-היום)

```
# Count of proposals in Knesset 24
.../KNS_Agenda?$filter=KnessetNum eq 24&$count=true&$top=0

# Urgent agenda proposals (ClassificationDesc contains דחופה)
.../KNS_Agenda?$filter=KnessetNum eq 25 and contains(ClassificationDesc,'דחופה')&$top=20

# Proposals submitted by a specific MK
.../KNS_Agenda?$filter=InitiatorPersonID eq 532&$top=10
```

## Secondary Legislation (חקיקת משנה)

```
# Regulations published in 2024
.../KNS_SecondaryLaw?$filter=TypeID eq 1 and PublicationDate gt 2024-01-01&$top=20

# Specific item + regulator + authorizing law
.../KNS_SecondaryLaw?$filter=Id eq 2198278&$expand=KNS_SecLawRegulator,KNS_SecLawAuthorizingLaw

# Proclamations (ClassificationDesc = אכרזה)
.../KNS_SecondaryLaw?$filter=contains(ClassificationDesc,'אכרזה')&$top=10
```

## Code Lookups

```
# Current Knesset session
.../KNS_KnessetDates?$filter=IsCurrent eq true

# Current active session (started in past, ends in future)
.../KNS_KnessetDates?$filter=PlenumFinish gt now() and PlenumStart lt now()

# All status codes for bills (TypeID=2)
.../KNS_Status?$filter=TypeID eq 2&$orderby=Id

# All item types
.../KNS_ItemType?$orderby=Id

# All government ministries
.../KNS_GovMinistry?$filter=IsActive eq true&$orderby=Name
```
