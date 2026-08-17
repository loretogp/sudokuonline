#!/usr/bin/env python3
"""Generates the day's 3 sudoku puzzles (Fácil/Medio/Difícil) and every
derived static artifact: dated JSON files, data/today.json, per-day HTML
pages under sudokus/, data/listing.json, play.html and sitemap.xml.

Pure stdlib, no git operations of any kind — this script only writes files.
Safe to re-run: if today's files already exist it does nothing (idempotent).

Usage:
    python3 tools/generate_daily_puzzles.py [--date YYYY-MM-DD]
"""
import argparse
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from sudoku.difficulty import TIERS, dig_holes  # noqa: E402
from sudoku.grid import generate_full_grid  # noqa: E402
from sudoku.render import (  # noqa: E402
    render_archive_page,
    render_puzzle_page,
    render_sitemap,
)
from sudoku.solver import count_solutions, solve  # noqa: E402

STATIC_PAGES = [
    "play.html",
    "sudoku-rules.html",
    "tecnicas.html",
    "historia.html",
    "faq.html",
    "about.html",
    "contact.html",
    "privacy.html",
]

MONTH_NAMES_ES = [
    "", "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]


def target_date(cli_date):
    if cli_date:
        return date.fromisoformat(cli_date)
    return datetime.now(ZoneInfo("America/Santiago")).date()


def display_date(d):
    return f"{d.day} de {MONTH_NAMES_ES[d.month]} de {d.year}"


def load_listing():
    path = REPO_ROOT / "data" / "listing.json"
    if not path.exists():
        return {"puzzles": []}
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def generate_one_puzzle(tier):
    solution = generate_full_grid()
    puzzle, clues = dig_holes(solution, tier["target_clues"])

    # Blocking self-check: never write a puzzle that isn't uniquely solvable
    # and whose solution doesn't match the stored one.
    if count_solutions(puzzle, limit=2) != 1:
        raise RuntimeError(f"{tier['key']}: generated puzzle is not uniquely solvable")
    solved = solve(puzzle)
    if solved != solution:
        raise RuntimeError(f"{tier['key']}: solver result does not match stored solution")

    return puzzle, solution, clues


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="Override target date (YYYY-MM-DD), for testing.")
    args = parser.parse_args()

    d = target_date(args.date)
    date_str = d.isoformat()
    yyyymm = f"{d.year}{d.month:02d}"
    disp = display_date(d)
    year = d.year

    listing = load_listing()
    existing_dates = {entry["date"] for entry in listing["puzzles"]}
    if date_str in existing_dates:
        print(f"{date_str} already generated, skipping.")
        return

    all_dates_sorted = sorted(existing_dates | {date_str})
    idx = all_dates_sorted.index(date_str)
    prev_date = all_dates_sorted[idx - 1] if idx > 0 else None
    next_date = all_dates_sorted[idx + 1] if idx < len(all_dates_sorted) - 1 else None

    today_snapshot = {"date": date_str, "puzzles": {}}
    new_listing_entries = []

    for order, tier in enumerate(TIERS):
        print(f"Generando {tier['label']} ({date_str})...")
        puzzle, solution, clues = generate_one_puzzle(tier)

        title = f"Sudoku {tier['label']} — {disp}"
        record = {
            "date": date_str,
            "difficulty": tier["key"],
            "difficulty_label": tier["label"],
            "clues": clues,
            "title": title,
            "puzzle": puzzle,
            "solution": solution,
        }

        json_name = f"daily-puzzle-{d.strftime('%Y%m%d')}-{tier['key']}.json"
        json_rel_path = f"data/{yyyymm}/{json_name}"
        save_json(REPO_ROOT / json_rel_path, record)

        today_snapshot["puzzles"][tier["key"]] = record

        page_rel_path = f"sudokus/{date_str}-{tier['key']}.html"
        page_html = render_puzzle_page(
            date_str=date_str,
            difficulty_key=tier["key"],
            difficulty_label=tier["label"],
            clues=clues,
            data_file_name=json_rel_path,
            prev_date=prev_date,
            next_date=next_date,
            display_date=disp,
            year=year,
        )
        (REPO_ROOT / page_rel_path).write_text(page_html, encoding="utf-8")

        new_listing_entries.append({
            "date": date_str,
            "difficulty": tier["key"],
            "difficulty_label": tier["label"],
            "difficulty_order": order,
            "clues": clues,
            "title": title,
            "page": page_rel_path,
            "data_file": json_rel_path,
        })

    save_json(REPO_ROOT / "data" / "today.json", today_snapshot)

    listing["puzzles"].extend(new_listing_entries)
    listing["puzzles"].sort(key=lambda e: (e["date"], e["difficulty_order"]), reverse=True)
    save_json(REPO_ROOT / "data" / "listing.json", listing)

    # The previous day's pages were generated with next_date=None (they were
    # the latest day at the time). Now that today exists, patch them so
    # their "Día siguiente" link points here instead of staying dead.
    if prev_date:
        prev_prev_date = all_dates_sorted[idx - 2] if idx - 1 > 0 else None
        prev_entries = [e for e in listing["puzzles"] if e["date"] == prev_date]
        for entry in prev_entries:
            page_html = render_puzzle_page(
                date_str=prev_date,
                difficulty_key=entry["difficulty"],
                difficulty_label=entry["difficulty_label"],
                clues=entry["clues"],
                data_file_name=entry["data_file"],
                prev_date=prev_prev_date,
                next_date=date_str,
                display_date=display_date(date.fromisoformat(prev_date)),
                year=date.fromisoformat(prev_date).year,
            )
            (REPO_ROOT / entry["page"]).write_text(page_html, encoding="utf-8")

    archive_html = render_archive_page(listing["puzzles"], year)
    (REPO_ROOT / "play.html").write_text(archive_html, encoding="utf-8")

    sitemap_xml = render_sitemap(listing["puzzles"], STATIC_PAGES)
    (REPO_ROOT / "sitemap.xml").write_text(sitemap_xml, encoding="utf-8")

    print(f"Listo: {date_str} generado ({len(TIERS)} niveles).")


if __name__ == "__main__":
    main()
