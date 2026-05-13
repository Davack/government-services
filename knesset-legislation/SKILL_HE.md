---
name: knesset-legislation
description: >-
  [מה] שואל את מסד הנתונים הפרלמנטרי של הכנסת דרך OData v4 API.
  [מתי] השתמש כשהמשתמש שואל על הכנסת, חקיקה, חברי כנסת, הצבעות, ועדות
  או הליכים פרלמנטריים. ביטויי טריגר: כנסת, חוק, הצעת חוק, ח"כ, ועדה,
  הצבעה, שאילתה, מליאה, סיעה.
  [יכולות] מכסה הצעות חוק וחוקים, ועדות וישיבותיהן, ישיבות מליאה והצבעות,
  שאילתות פרלמנטריות, הצעות לסדר-היום, חקיקת משנה, תפקידי ח"כים ונתוני
  סיעות. אין להשתמש לחיפוש חברות ישראליות (השתמשו ב-israeli-company-lookup)
  או נתוני ממשלה שאינם פרלמנטריים.
license: MIT
allowed-tools: Bash(python:*)
compatibility: כל קריאות ה-API מתבצעות דרך Python requests ב-Bash. עובד עם Claude Code, Claude.ai, Cursor.
metadata:
  author: Davack
  version: 1.0.0
  category: government-services
  tags:
    he:
      - כנסת
      - חקיקה
      - פרלמנט
      - חוק
      - הצבעה
      - ועדה
      - חבר-כנסת
      - סיעה
      - ישראל
    en:
      - knesset
      - legislation
      - parliament
      - israeli-law
      - vote
      - committee
      - mk
      - faction
      - israel
  display_name:
    he: מאגר החקיקה הלאומי
    en: The National Legislation Database
  display_description:
    he: >-
      שאילתת מסד הנתונים הפרלמנטרי של הכנסת דרך OData v4 API. לשימוש עבור
      הצעות חוק, חוקים, חברי כנסת, ועדות, ישיבות, הצבעות, שאילתות
      פרלמנטריות, הצעות לסדר-היום וחקיקת משנה.
    en: >-
      Query the Knesset parliamentary database via OData v4 API. Covers bills,
      enacted laws, MKs, committees, votes, parliamentary questions, agenda
      proposals, and secondary legislation.
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
    - gemini-cli
---

# נתוני הכנסת הישראלית

## הוראות

### שלב 1: זיהוי הטבלה הרלוונטית

| בקשת המשתמש                 | טבלה ראשית                                |
| --------------------------- | ----------------------------------------- |
| הצעות חוק, חוקים, חקיקה     | `KNS_Bill`                                |
| חוקי אם (ספר החוקים)        | `KNS_IsraelLaw`                           |
| תקנות, צווים, פקודות        | `KNS_SecondaryLaw`                        |
| חברי כנסת, שרים, אישים      | `KNS_Person` / `KNS_PersonToPosition`     |
| סיעות ומפלגות               | `KNS_Faction`                             |
| ועדות                       | `KNS_Committee`                           |
| ישיבות ועדה                 | `KNS_CommitteeSession`                    |
| ישיבות מליאה                | `KNS_PlenumSession`                       |
| הצבעות במליאה               | `KNS_PlenumVote` / `KNS_PlenumVoteResult` |
| שאילתות פרלמנטריות (שאילתות) | `KNS_Query`                               |
| הצעות לסדר-היום             | `KNS_Agenda`                              |
| תאריכי מושבי הכנסת          | `KNS_KnessetDates`                        |
| משרדי ממשלה                 | `KNS_GovMinistry`                         |
| קודי סטטוס                  | `KNS_Status`                              |
| קודי סוג פריט               | `KNS_ItemType`                            |

### שלב 2: בניית שאילתת OData v4

**מבנה ה-URL:**
```
GET https://knesset.gov.il/OdataV4/ParliamentInfo/<שם הטבלה>?<פרמטרים>
```

**פרמטרי שאילתה:**

| פרמטר                | מטרה                | דוגמה                             |
| -------------------- | ------------------- | --------------------------------- |
| `$filter`            | סינון שורות         | `$filter=KnessetNum eq 25`        |
| `$select`            | בחירת שדות          | `$select=Id,Name,PublicationDate` |
| `$top`               | הגבלת תוצאות        | `$top=100`                        |
| `$skip`              | דילוג (עמודים)      | `$skip=100`                       |
| `$orderby`           | מיון                | `$orderby=PublicationDate desc`   |
| `$expand`            | Join עם טבלה קשורה  | `$expand=KNS_BillInitiator`       |
| `$count=true`        | כלול ספירה כוללת    | `$count=true`                     |
| `$count=true&$top=0` | ספירה בלבד          | `$count=true&$top=0`              |

**אופרטורי $filter:**

| אופרטור           | משמעות          | דוגמה                                  |
| ----------------- | --------------- | -------------------------------------- |
| `eq`              | שווה            | `KnessetNum eq 25`                     |
| `ne`              | לא שווה         | `StatusID ne 193`                      |
| `gt`              | גדול מ          | `PublicationDate gt 2024-01-01`        |
| `lt`              | קטן מ           | `PublicationDate lt 2025-01-01`        |
| `and`             | וגם             | `KnessetNum eq 25 and StatusID eq 118` |
| `or`              | או              | `TypeID eq 1 or TypeID eq 2`           |
| `contains(F,'v')` | חיפוש תת-מחרוזת | `contains(Name,'ביטוח')`               |
| `in (v1,v2)`      | שייכות לקבוצה   | `PositionID in (43,61)`                |
| `eq null`         | ריק             | `FinishDate eq null`                   |
| `now()`           | תאריך/שעה נוכחי | `PlenumFinish gt now()`                |

### שלב 3: הרצת השאילתה

השתמשו ב-Python `requests` דרך Bash:

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
records = data.get("value", [])         # רשימת שורות
count = data.get("@odata.count")        # ספירה כוללת (כשמשתמשים ב-$count=true)
next_link = data.get("@odata.nextLink") # קישור לעמוד הבא (כשיש עוד תוצאות)
```

### שלב 4: עיצוב והצגת התוצאות

- הציגו רשומות בטבלה ברורה או רשימה ממוספרת
- הציגו את כתובת ה-API שנוצרה (לשחזור)
- אם התגובה מכילה `@odata.nextLink` — ציינו שיש עמודים נוספים
- אם מוצג `@odata.count` — הציגו את הספירה הכוללת
- שדות `FilePath` מכילים כתובת URL מלאה למסמך
- הציעו הרחבות רלוונטיות (למשל "רוצים לכלול את מגישי הצעת החוק?")

## שאילתות נפוצות

### הצעות חוק וחוקים

```
# 20 הצעות חוק אחרונות בכנסת 25
.../KNS_Bill?$filter=KnessetNum eq 25&$orderby=PublicationDate desc&$top=20

# חיפוש הצעת חוק לפי מילת מפתח
.../KNS_Bill?$filter=contains(Name,'ביטוח')&$top=10

# הצעת חוק + מגישיה + מסמכים
.../KNS_Bill?$filter=Id eq 2216582&$expand=KNS_BillInitiator($orderby=IsInitiator desc,Ordinal),KNS_DocumentBill
```

### חברי כנסת ואישים

```
# חיפוש ח"כ לפי שם משפחה
.../KNS_Person?$filter=contains(LastName,'נתניהו')

# כל ח"כים המכהנים כיום
.../KNS_PersonToPosition?$filter=PositionID in (43,61) and FinishDate eq null&$expand=KNS_Person&$orderby=KNS_Person/LastName,KNS_Person/FirstName&$count=true

# כל שרי המשפטים לאורך ההיסטוריה
.../KNS_PersonToPosition?$filter=contains(GovMinistryName,'המשפטים')&$orderby=StartDate
```

### ועדות

```
# ועדות קבועות של כנסת 25
.../KNS_Committee?$filter=KnessetNum eq 25 and CommitteeTypeID eq 71&$orderby=Name

# ישיבות ועדה (ללא ביטולים)
.../KNS_CommitteeSession?$filter=CommitteeID eq 926 and StatusID ne 193&$orderby=Number
```

### הצבעות

```
# הצבעות אחרונות
.../KNS_PlenumVote?$orderby=Id desc&$top=10

# תוצאות ח"כ בהצבעה ספציפית
.../KNS_PlenumVoteResult?$filter=VoteID eq 42594&$orderby=Id

# הצבעות אי-אמון
.../KNS_PlenumVote?$filter=IsNoConfidenceInGov eq true&$orderby=VoteDateTime desc
```

### שאילתות פרלמנטריות

```
# שאילתות לפי משרד (קודם מצאו GovMinistryID ב-KNS_GovMinistry, לאחר מכן:)
.../KNS_Query?$filter=GovMinistryID in (<ids>)&$top=10&$orderby=SubmitDate desc

# ספירת שאילתות בכנסת 24
.../KNS_Query?$filter=KnessetNum eq 24 and TypeID eq 48&$count=true&$top=0
```

## דוגמאות

### דוגמה 1: מי הם ח"כי הליכוד הנוכחיים?
המשתמש אומר: "מי הם ח"כי הליכוד הנוכחיים?"

פעולות:
1. שאלו את `KNS_Faction?$filter=KnessetNum eq 25 and contains(Name,'ליכוד')` לקבלת מזהה הסיעה.
2. שאלו את `KNS_PersonToPosition?$filter=FactionID eq <id> and PositionID eq 54 and FinishDate eq null&$expand=KNS_Person&$orderby=KNS_Person/LastName`.

תוצאה: טבלה עם שם, סיעה, תאריך תחילת כהונה.

---

### דוגמה 2: הצעות חוק בנושא דיור
המשתמש אומר: "הציגו לי את 10 הצעות החוק האחרונות בנושא דיור."

פעולות:
1. שאלו את `KNS_Bill?$filter=contains(Name,'דיור') or contains(Name,'שכירות') or contains(Name,'דירה')&$orderby=PublicationDate desc&$top=10&$select=Id,Name,SubTypeDesc,PublicationDate`.

תוצאה: רשימה ממוספרת עם שם הצעת החוק, סוג ותאריך. הציעו הרחבה עם מגישים.

---

### דוגמה 3: הצבעת ח"כ ספציפי
המשתמש אומר: "האם ח"כ גפני הצביע בעד התקציב?"

פעולות:
1. מצאו את האדם: `KNS_Person?$filter=contains(LastName,'גפני')`.
2. מצאו את ההצבעה: `KNS_PlenumVote?$filter=contains(VoteTitle,'תקציב')&$orderby=VoteDateTime desc&$top=5`.
3. שאלו: `KNS_PlenumVoteResult?$filter=VoteID eq <id> and MkId eq <id>`.

תוצאה: דווחו על `ResultDesc` ("בעד" / "נגד" / "נמנע").

---

### דוגמה 4: ספירת שאילתות פרלמנטריות
המשתמש אומר: "כמה שאילתות הוגשו למשרד המשפטים בכנסת 25?"

פעולות:
1. חפשו מזהי משרד: `KNS_GovMinistry?$filter=contains(Name,'משפטים')&$select=Id,Name`.
2. שאלו: `KNS_Query?$filter=KnessetNum eq 25 and GovMinistryID in (<ids>)&$count=true&$top=0`.

תוצאה: דווחו על ערך `@odata.count` מהתגובה. שימו לב: `GovMinistryName` אינו קיים ב-`KNS_Query`; יש לסנן לפי `GovMinistryID`.

## משאבים מצורפים

### סקריפטים
- `scripts/query_knesset.py` — שאילת מסד הנתונים של הכנסת. פקודות משנה: `tables` (רשימת טבלאות), `examples` (שאילתות לדוגמה), `query` (הרצת שאילתה). להרצה: `python scripts/query_knesset.py --help`

### חומרי עזר

| קובץ                                  | תוכן                                     |
| ------------------------------------- | ---------------------------------------- |
| `references/common-queries.md`        | שאילתות מוכנות לשימוש לפי נושא           |
| `references/tables-bills.md`          | כל שדות טבלאות הצעות החוק               |
| `references/tables-committees.md`     | כל שדות טבלאות הוועדות                   |
| `references/tables-members.md`        | ח"כים, תפקידים, סיעות                    |
| `references/tables-plenum-votes.md`   | ישיבות מליאה והצבעות                    |
| `references/tables-agenda-queries.md` | הצעות לסדר-היום ושאילתות פרלמנטריות     |
| `references/tables-secondary-law.md`  | טבלאות חקיקת משנה                        |
| `references/odata-syntax.md`          | תחביר OData v4 מלא ומדריך עמודים         |

## מלכודות נפוצות

| בעיה                     | פירוט                                                                                                          |
| ------------------------ | -------------------------------------------------------------------------------------------------------------- |
| **שדה מפתח ראשי**        | ב-v4 המפתח תמיד `Id`, לא `BillID`, `PersonID`, `CommitteeID` וכו'.                                            |
| **שגיאת כתיב מכוונת**    | `KNS_IsraelLawClassificiation` — שני אותיות i. אל תתקנו.                                                      |
| **ישיבות שבוטלו**        | `StatusID` 193 = בוטלה. תמיד סננו עם `StatusID ne 193` ב-`KNS_CommitteeSession`.                              |
| **באג סדר בפריטי מליאה** | מיון לפי `Ordinal` ב-`KNS_PlmSessionItem` שבור. אל תסמכו עליו.                                                |
| **דגל IsCurrent**        | עדיפו `KnessetNum eq 25` על פני `IsCurrent eq true`.                                                          |
| **מזהי תפקיד ח"כ**       | 43 = ח"כ (זכר), 61 = ח"כית (נקבה), 41 = יו"ר ועדה, 54 = חבר סיעה.                                           |
| **פרוטוקולים רשמיים**    | `GroupTypeID eq 28` ב-`KNS_DocumentPlenumSession` = דברי הכנסת.                                               |
| **כנסת 0**               | מספר כנסת 0 = מועצת המדינה הזמנית.                                                                            |
| **איכות נתונים**         | האיכות משתפרת מכנסת 17 ואילך. רשומות ישנות יותר עלולות להיות חסרות.                                          |
| **v2 מול v4**            | `KNS_Law` ו-`KNS_DocumentLaw` קיימים רק ב-v2. ב-v4 הרשומות הועברו ל-`KNS_Bill`. השתמשו ב-v4 בלבד.           |
| **פורמט תאריך**          | ISO 8601: `2024-01-01` לתאריך, `2015-06-01T00:00:01Z` לתאריך עם שעה.                                         |
| **VoteTitle לא ItemTitle** | ב-`KNS_PlenumVote` השדה הוא `VoteTitle`. `ItemTitle` אינו קיים ויחזיר 400.                                  |
| **MkId לא PersonID**     | ב-`KNS_PlenumVoteResult` מפתח ח"כ הוא `MkId`, לא `PersonID`. השתמשו ב-`ResultDesc` לתוצאה ("בעד"/"נגד"/"נמנע"); ערכי `ResultCode` אינם 1/2/3. |
| **GovMinistryID לא GovMinistryName** | ב-`KNS_Query` קיים `GovMinistryID` (מספר), לא שדה שם. חפשו מזהים תחילה ב-`KNS_GovMinistry?$filter=contains(Name,'...')` וסננו לפי `GovMinistryID in (<ids>)`. |
| **PositionID לחברי סיעה** | כדי לרשום ח"כים לפי סיעה, סננו `KNS_PersonToPosition` עם `PositionID eq 54` (חבר סיעה), לא `in (43,61)` (תפקיד ח"כ כללי שאינו קשור לסיעה ספציפית). |

## קישורי עזר

| מקור                              | כתובת                                                                                   | מה לבדוק                                      |
| --------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------- |
| פורטל מסדי הנתונים של הכנסת      | https://main.knesset.gov.il/activity/info/pages/databases.aspx                          | מערכי נתונים זמינים, הודעות API               |
| חיפוש הצעות חוק (ממשק ווב)       | https://main.knesset.gov.il/Activity/Legislation/Laws/Pages/LawSuggestionsSearch.aspx  | אימות נתוני הצעות חוק מול תוצאות ה-API        |
| הצעות לסדר-היום (ממשק ווב)       | https://main.knesset.gov.il/apps/agenda/search                                          | אימות נתוני הצעות מול תוצאות ה-API            |
| שאילתות פרלמנטריות (ממשק ווב)    | https://main.knesset.gov.il/apps/query/search                                           | אימות נתוני שאילתות מול תוצאות ה-API          |
| הצבעות מליאה (ממשק ווב)          | https://main.knesset.gov.il/activity/plenum/votes/pages/default.aspx                   | אימות נתוני הצבעות מול תוצאות ה-API           |
| רשימת טבלאות OData v4            | https://knesset.gov.il/OdataV4/ParliamentInfo                                           | טבלאות זמינות, בדיקת תוספות חדשות             |
| מטה-נתוני OData v4               | https://knesset.gov.il/OdataV4/ParliamentInfo/$metadata                                 | סכמה מלאה: שמות שדות, סוגים, קשרים           |

## פתרון בעיות

### שגיאה: מערך value ריק למרות ציפייה לתוצאות
סיבה: פורמט תאריך שגוי (לדוגמה `01/01/2024` במקום `2024-01-01`), או טקסט עברי ב-`$filter` שאינו מקודד UTF-8.
פתרון: השתמשו ב-ISO 8601. העבירו `$filter` כפרמטר שאילתה (לא inline ב-URL) — `requests` יטפל בקידוד אוטומטית.

### שגיאה: 500 Internal Server Error
סיבה: שרשרת `$expand` פגומה, שמות שדות לא תקינים, או הרחבת שדה שאינו קיים בטבלה.
פתרון: פשטו את השאילתה. הסירו `$expand` תחילה כדי לוודא שהשאילתה הבסיסית עובדת, ואז הוסיפו הרחבות אחת-אחת. בדקו את `references/` לשמות שדות תקינים.

### שגיאה: $filter על שדה מורחב לא מחזיר תוצאות
סיבה: סינון על שדה בתוך `$expand` דורש תחביר מקונן.
פתרון: השתמשו ב-`$expand=Table($filter=Field eq Value)` ולא ב-`$filter=Table/Field eq Value`.

### שגיאה: ספירה שגויה או בעיות בעמודים
סיבה: `$count=true` ללא `$top` מחזיר גודל עמוד ברירת המחדל (בדרך כלל 10), לא את כל הרשומות.
פתרון: קבעו `$count=true` לקבלת הסה"כ, ואז עשו עמודים לפי `$skip` ו-`$top` תוך מעקב אחר `@odata.nextLink`.

### שגיאה: שאילתת ועדה מחזירה ישיבות שבוטלו
סיבה: ה-API כולל ישיבות שבוטלו (StatusID=193) כברירת מחדל.
פתרון: תמיד הוסיפו `and StatusID ne 193` לפילטרים של `KNS_CommitteeSession`, אלא אם הביטולים נדרשים ספציפית.
