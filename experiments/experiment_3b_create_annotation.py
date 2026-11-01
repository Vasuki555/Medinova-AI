from pathlib import Path
import csv


# ============================================================
# EXPERIMENT 3B — CREATE PILOT ANNOTATION SHEET
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

EVAL_DIR = (
    PROJECT_ROOT
    / "experiments"
    / "results"
    / "experiment_3"
    / "evaluation_3b"
)

INPUT_CSV = (
    EVAL_DIR
    / "experiment_3b_evaluation_dataset.csv"
)

OUTPUT_CSV = (
    EVAL_DIR
    / "experiment_3b_pilot_annotation.csv"
)

# One representative document from each subset
PILOT_IDS = [
    "E3P001",  # normal
    "E3P006",  # handwriting
    "E3P011",  # poor
    "E3P016",  # rotated
    "E3P021",  # tables
    "E3P026",  # mixed
]


# ============================================================
# LOAD DATASET
# ============================================================

if not INPUT_CSV.exists():
    raise FileNotFoundError(
        f"Dataset not found:\n{INPUT_CSV}"
    )

with INPUT_CSV.open(
    "r",
    encoding="utf-8-sig",
    newline=""
) as f:

    rows = list(csv.DictReader(f))


# ============================================================
# SELECT PILOT DOCUMENTS
# ============================================================

selected = []

for pilot_id in PILOT_IDS:

    matches = [
        row
        for row in rows
        if row["pilot_id"] == pilot_id
    ]

    if not matches:
        raise ValueError(
            f"Missing pilot ID: {pilot_id}"
        )

    selected.append(matches[0])


# ============================================================
# CREATE ANNOTATION SHEET
# ============================================================

fieldnames = [

    # Document information
    "pilot_id",
    "subset",
    "template",
    "sample",

    # Reference clinical facts
    "fact_id",
    "fact_category",
    "reference_fact",

    # GT condition
    "gt_preservation_score",

    # OCR condition
    "ocr_preservation_score",

    # Notes
    "gt_evidence",
    "ocr_evidence",
    "annotation_notes",

]


with OUTPUT_CSV.open(
    "w",
    encoding="utf-8",
    newline=""
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=fieldnames
    )

    writer.writeheader()

    for row in selected:

        # Create one blank annotation row.
        # Additional fact rows will be added manually
        # after reviewing the original GT text.

        writer.writerow({
            "pilot_id":
                row["pilot_id"],

            "subset":
                row["subset"],

            "template":
                row["template"],

            "sample":
                row["sample"],

            "fact_id":
                "",

            "fact_category":
                "",

            "reference_fact":
                "",

            "gt_preservation_score":
                "",

            "ocr_preservation_score":
                "",

            "gt_evidence":
                "",

            "ocr_evidence":
                "",

            "annotation_notes":
                "",
        })


# ============================================================
# SUMMARY
# ============================================================

print("=" * 70)
print("EXPERIMENT 3B — PILOT ANNOTATION SHEET")
print("=" * 70)

print(f"Pilot documents: {len(selected)}")

print()
print("Selected documents:")

for row in selected:
    print(
        f"  {row['pilot_id']} "
        f"→ {row['subset']} "
        f"(template {row['template']}, "
        f"sample {row['sample']})"
    )

print()
print("Output:")
print(OUTPUT_CSV)

print()
print("Scoring:")
print("  2 = correctly preserved")
print("  1 = partially preserved / less precise")
print("  0 = missing or incorrect")

print("=" * 70)