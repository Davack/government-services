#!/usr/bin/env python3
"""
Knesset OData Query Utility

Query the Israeli Knesset parliamentary database (OData v4 API).

Usage:
    python query_knesset.py tables
    python query_knesset.py examples
    python query_knesset.py query --table KNS_Bill --filter "KnessetNum eq 25" --top 10
    python query_knesset.py query --table KNS_Person --filter "contains(LastName,'נתניהו')"
"""

import argparse
import json
import sys

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

BASE_URL = "https://knesset.gov.il/OdataV4/ParliamentInfo/"
HEADERS = {"Accept": "application/json", "User-Agent": "Mozilla/5.0"}

TABLES = {
    "KNS_Bill": "Bills and proposed legislation",
    "KNS_IsraelLaw": "Enacted laws (parent law corpus)",
    "KNS_SecondaryLaw": "Secondary legislation (regulations, orders, decrees)",
    "KNS_Person": "MKs, ministers, and other persons",
    "KNS_PersonToPosition": "Person-to-position assignments (faction, role, committee)",
    "KNS_Faction": "Factions and parties",
    "KNS_Committee": "Knesset committees",
    "KNS_CommitteeSession": "Committee sessions and meetings",
    "KNS_PlenumSession": "Plenary sessions",
    "KNS_PlmSessionItem": "Items discussed in plenary sessions",
    "KNS_PlenumVote": "Plenary votes",
    "KNS_PlenumVoteResult": "Per-MK vote results",
    "KNS_Query": "Parliamentary questions (שאילתות)",
    "KNS_Agenda": "Agenda proposals (הצעות לסדר-היום)",
    "KNS_KnessetDates": "Knesset session dates",
    "KNS_GovMinistry": "Government ministries",
    "KNS_Status": "Status codes",
    "KNS_ItemType": "Item type codes",
    "KNS_BillInitiator": "Bill initiators (MKs who proposed a bill)",
    "KNS_DocumentBill": "Documents attached to bills",
    "KNS_DocumentCommitteeSession": "Documents attached to committee sessions",
    "KNS_DocumentPlenumSession": "Documents attached to plenary sessions",
    "KNS_DocumentQuery": "Documents attached to parliamentary questions",
    "KNS_IsraelLawClassificiation": "Law classification (note: intentional typo in name)",
    "KNS_IsraelLawMinistry": "Ministry responsible for a law",
    "KNS_CmtSessionItem": "Agenda items in a committee session",
    "KNS_SecLawRegulator": "Regulator responsible for secondary legislation",
    "KNS_SecLawAuthorizingLaw": "Authorizing law for secondary legislation",
}

EXAMPLES = [
    {
        "label": "20 most recently published bills in Knesset 25",
        "table": "KNS_Bill",
        "params": {
            "$filter": "KnessetNum eq 25",
            "$orderby": "PublicationDate desc",
            "$top": "20",
            "$select": "Id,Name,SubTypeDesc,PublicationDate",
        },
    },
    {
        "label": "Search bills by keyword in title",
        "table": "KNS_Bill",
        "params": {
            "$filter": "contains(Name,'ביטוח')",
            "$top": "10",
            "$select": "Id,Name,PublicationDate",
        },
    },
    {
        "label": "All currently serving MKs",
        "table": "KNS_PersonToPosition",
        "params": {
            "$filter": "PositionID in (43,61) and FinishDate eq null",
            "$expand": "KNS_Person",
            "$orderby": "KNS_Person/LastName,KNS_Person/FirstName",
            "$count": "true",
        },
    },
    {
        "label": "Find MK by last name",
        "table": "KNS_Person",
        "params": {"$filter": "contains(LastName,'נתניהו')"},
    },
    {
        "label": "All factions in Knesset 25",
        "table": "KNS_Faction",
        "params": {"$filter": "KnessetNum eq 25", "$orderby": "Name"},
    },
    {
        "label": "Standing committees of Knesset 25",
        "table": "KNS_Committee",
        "params": {
            "$filter": "KnessetNum eq 25 and CommitteeTypeID eq 71",
            "$orderby": "Name",
        },
    },
    {
        "label": "Latest 5 plenary sessions in Knesset 25",
        "table": "KNS_PlenumSession",
        "params": {
            "$filter": "KnessetNum eq 25",
            "$orderby": "Number desc",
            "$top": "5",
        },
    },
    {
        "label": "Latest 10 votes",
        "table": "KNS_PlenumVote",
        "params": {"$orderby": "Id desc", "$top": "10"},
    },
    {
        "label": "No-confidence votes",
        "table": "KNS_PlenumVote",
        "params": {
            "$filter": "IsNoConfidenceInGov eq true",
            "$orderby": "VoteDateTime desc",
        },
    },
    {
        "label": "Current Knesset session",
        "table": "KNS_KnessetDates",
        "params": {"$filter": "IsCurrent eq true"},
    },
    {
        "label": "All currently valid basic laws (חוקי יסוד)",
        "table": "KNS_IsraelLaw",
        "params": {"$filter": "IsBasicLaw eq true and LawValidityID eq 1"},
    },
    {
        "label": "Count of parliamentary questions in Knesset 24",
        "table": "KNS_Query",
        "params": {
            "$filter": "KnessetNum eq 24 and TypeID eq 48",
            "$count": "true",
            "$top": "0",
        },
    },
]


def show_tables() -> None:
    print("=== Knesset OData v4 Tables ===\n")
    print(f"Base URL: {BASE_URL}\n")
    for name, description in TABLES.items():
        print(f"  {name}")
        print(f"    {description}")
        print()


def show_examples() -> None:
    print("=== Example Queries ===\n")
    for i, ex in enumerate(EXAMPLES, 1):
        params = "&".join(f"{k}={v}" for k, v in ex["params"].items())
        url = f"{BASE_URL}{ex['table']}?{params}"
        print(f"  {i}. {ex['label']}")
        print(f"     {url}")
        print()


def run_query(table: str, params: dict) -> None:
    if not HAS_REQUESTS:
        print("Error: 'requests' library not installed. Run: pip install requests")
        sys.exit(1)

    url = BASE_URL + table
    print(f"GET {url}")
    print(f"Params: {json.dumps(params, ensure_ascii=False, indent=2)}\n")

    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=30)
        r.raise_for_status()
        data = r.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        sys.exit(1)

    count = data.get("@odata.count")
    next_link = data.get("@odata.nextLink")
    records = data.get("value", [])

    if count is not None:
        print(f"Total count: {count}")
    print(f"Records returned: {len(records)}")
    if next_link:
        print(f"More pages: {next_link}")
    print()

    for rec in records:
        print(json.dumps(rec, ensure_ascii=False, indent=2))
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Knesset OData Query Utility")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    subparsers.add_parser("tables", help="List all available tables")
    subparsers.add_parser("examples", help="Show example queries")

    qp = subparsers.add_parser("query", help="Execute an OData query")
    qp.add_argument("--table", required=True, help="Table name (e.g. KNS_Bill)")
    qp.add_argument("--filter", dest="filter_", metavar="FILTER", help="OData $filter expression")
    qp.add_argument("--select", help="Comma-separated field names")
    qp.add_argument("--expand", help="OData $expand expression")
    qp.add_argument("--orderby", help="OData $orderby expression")
    qp.add_argument("--top", type=int, default=10, help="Max rows to return (default: 10)")
    qp.add_argument("--skip", type=int, help="Rows to skip (pagination)")
    qp.add_argument("--count", action="store_true", help="Include total count")

    args = parser.parse_args()

    if args.command == "tables":
        show_tables()
    elif args.command == "examples":
        show_examples()
    elif args.command == "query":
        params = {"$top": str(args.top)}
        if args.filter_:
            params["$filter"] = args.filter_
        if args.select:
            params["$select"] = args.select
        if args.expand:
            params["$expand"] = args.expand
        if args.orderby:
            params["$orderby"] = args.orderby
        if args.skip is not None:
            params["$skip"] = str(args.skip)
        if args.count:
            params["$count"] = "true"
        run_query(args.table, params)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
