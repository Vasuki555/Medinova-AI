from pathlib import Path
import json


# ============================================================
# EXPERIMENT 3B — PILOT REVIEW EXPORT
# VERSION 2
#
# IMPORTANT:
# Read the FULL Gemini outputs directly from the existing
# Experiment 3A raw_outputs directory.
#
# No Gemini API calls.
# No modification of Experiment 3A results.
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

EVAL_DIR = (
    PROJECT_ROOT
    / "experiments"
    / "results"
    / "experiment_3"
    / "evaluation_3b"
)

RAW_DIR = (
    PROJECT_ROOT
    / "experiments"
    / "results"
    / "experiment_3"
    / "raw_outputs"
)

DATASET_JSON = (
    EVAL_DIR
    / "experiment_3b_evaluation_dataset.json"
)

OUTPUT_MD = (
    EVAL_DIR
    / "experiment_3b_pilot_review.md"
)

PILOT_IDS = [
    "E3P001",
    "E3P006",
    "E3P011",
    "E3P016",
    "E3P021",
    "E3P026",
]


# ============================================================
# CHECK FILES
# ============================================================

if not DATASET_JSON.exists():
    raise FileNotFoundError(
        f"Dataset not found:\n{DATASET_JSON}"
    )

if not RAW_DIR.exists():
    raise FileNotFoundError(
        f"Raw output directory not found:\n{RAW_DIR}"
    )


# ============================================================
# LOAD 3B DATASET
# ============================================================

with DATASET_JSON.open("r", encoding="utf-8") as f:
    data = json.load(f)


if isinstance(data, dict):

    if "records" in data:
        records = data["records"]

    elif "items" in data:
        records = data["items"]

    elif "data" in data:
        records = data["data"]

    else:
        records = []

        for key, value in data.items():

            if isinstance(value, dict):

                item = dict(value)

                if "pilot_id" not in item:
                    item["pilot_id"] = key

                records.append(item)

else:
    records = data


# ============================================================
# HELPERS
# ============================================================

def get_value(record, *keys, default=""):

    for key in keys:

        if key in record and record[key] is not None:
            return record[key]

    return default


def read_text(path):

    if not path.exists():
        return (
            f"[FILE NOT FOUND]\n"
            f"{path}"
        )

    return path.read_text(
        encoding="utf-8",
        errors="replace"
    ).strip()


# ============================================================
# CREATE REVIEW DOCUMENT
# ============================================================

exported = 0

with OUTPUT_MD.open(
    "w",
    encoding="utf-8"
) as f:

    f.write("# Experiment 3B — Pilot Review\n\n")

    f.write(
        "This document contains the six pilot cases selected "
        "for manual clinical-fact annotation.\n\n"
    )

    f.write(
        "The original ClinOCR-Bench ground-truth report is "
        "treated as the factual reference. The Gemini outputs "
        "are taken directly from the existing Experiment 3A "
        "raw output files.\n\n"
    )

    f.write("## Scoring Protocol\n\n")

    f.write(
        "- **2** = correctly preserved\n"
        "- **1** = partially preserved / less precise\n"
        "- **0** = missing or incorrect\n\n"
    )

    f.write(
        "**No scores are assigned automatically.**\n\n"
    )

    f.write("---\n\n")


    # ========================================================
    # EACH PILOT
    # ========================================================

    for pilot_id in PILOT_IDS:

        matches = [
            r for r in records
            if str(
                get_value(r, "pilot_id")
            ) == pilot_id
        ]

        if not matches:

            print(
                f"WARNING: Dataset record not found: {pilot_id}"
            )

            continue

        record = matches[0]

        subset = str(
            get_value(record, "subset")
        )

        template = str(
            get_value(record, "template")
        )

        sample = str(
            get_value(record, "sample")
        )


        # ----------------------------------------------------
        # RAW GEMINI FILES
        # ----------------------------------------------------

        gt_gemini_path = (
            RAW_DIR
            / f"{pilot_id}_gt_gemini.txt"
        )

        ocr_gemini_path = (
            RAW_DIR
            / f"{pilot_id}_ocr_gemini.txt"
        )


        gt_gemini = read_text(
            gt_gemini_path
        )

        ocr_gemini = read_text(
            ocr_gemini_path
        )


        # ----------------------------------------------------
        # GT / OCR TEXT
        # ----------------------------------------------------

        gt_text = get_value(
            record,
            "ground_truth_text",
            "gt_text",
            "reference_text",
            "ground_truth"
        )

        ocr_text = get_value(
            record,
            "ocr_text",
            "ocr_text_content",
            "ocr"
        )


        # If the JSON contains no text, try nested
        # condition structures.

        if not gt_text and isinstance(record, dict):

            gt_condition = record.get(
                "gt",
                record.get(
                    "ground_truth_condition",
                    {}
                )
            )

            if isinstance(gt_condition, dict):

                gt_text = get_value(
                    gt_condition,
                    "text",
                    "input_text",
                    "report_text",
                    "ground_truth_text"
                )


        if not ocr_text and isinstance(record, dict):

            ocr_condition = record.get(
                "ocr",
                record.get(
                    "ocr_condition",
                    {}
                )
            )

            if isinstance(ocr_condition, dict):

                ocr_text = get_value(
                    ocr_condition,
                    "text",
                    "input_text",
                    "report_text",
                    "ocr_text"
                )


        # ----------------------------------------------------
        # WRITE CASE
        # ----------------------------------------------------

        f.write(f"# {pilot_id}\n\n")

        f.write(
            f"**Subset:** {subset}  \n"
            f"**Template:** {template}  \n"
            f"**Sample:** {sample}\n\n"
        )


        # ====================================================
        # 1 — ORIGINAL GT
        # ====================================================

        f.write(
            "## 1. Original Ground Truth Report\n\n"
        )

        f.write(
            str(gt_text).strip()
            if gt_text
            else "[GROUND TRUTH TEXT NOT FOUND]"
        )

        f.write("\n\n---\n\n")


        # ====================================================
        # 2 — GEMINI GT CONDITION
        # ====================================================

        f.write(
            "## 2. Gemini Output — Ground Truth Condition\n\n"
        )

        f.write(
            gt_gemini
            if gt_gemini
            else "[GEMINI GT OUTPUT NOT FOUND]"
        )

        f.write("\n\n---\n\n")


        # ====================================================
        # 3 — OCR TEXT
        # ====================================================

        f.write(
            "## 3. OCR Text\n\n"
        )

        f.write(
            str(ocr_text).strip()
            if ocr_text
            else "[OCR TEXT NOT FOUND]"
        )

        f.write("\n\n---\n\n")


        # ====================================================
        # 4 — GEMINI OCR CONDITION
        # ====================================================

        f.write(
            "## 4. Gemini Output — OCR Condition\n\n"
        )

        f.write(
            ocr_gemini
            if ocr_gemini
            else "[GEMINI OCR OUTPUT NOT FOUND]"
        )

        f.write("\n\n---\n\n")


        # ====================================================
        # 5 — ANNOTATION TABLE
        # ====================================================

        f.write(
            "## 5. Manual Clinical Fact Annotation\n\n"
        )

        f.write(
            "| Fact ID | Category | Reference Fact | "
            "GT Score | OCR Score | GT Evidence | "
            "OCR Evidence | Notes |\n"
        )

        f.write(
            "|---|---|---|---:|---:|---|---|---|\n"
        )

        for i in range(1, 16):

            f.write(
                f"| F{i} | | | | | | | |\n"
            )

        f.write("\n")


        f.write(
            "### Allowed Categories\n\n"
            "- DIAGNOSIS\n"
            "- FINDING\n"
            "- NUMERICAL_VALUE\n"
            "- MEASUREMENT\n"
            "- UNIT\n"
            "- DATE\n"
            "- MEDICATION\n"
            "- DOSAGE\n"
            "- CLINICAL_INSTRUCTION\n"
            "- OTHER_CLINICAL_FACT\n\n"
        )

        f.write(
            "### Scoring\n\n"
            "**2** = correctly preserved  \n"
            "**1** = partially preserved / less precise  \n"
            "**0** = missing or incorrect\n\n"
        )

        f.write("---\n\n")

        exported += 1


# ============================================================
# FINAL SUMMARY
# ============================================================

print("=" * 70)
print("EXPERIMENT 3B — PILOT REVIEW EXPORT v2")
print("=" * 70)

print(
    f"Pilot records exported: {exported}/{len(PILOT_IDS)}"
)

print()
print("Raw Gemini output directory:")
print(RAW_DIR)

print()
print("Review file:")
print(OUTPUT_MD)

print()
print("No Gemini API calls were made.")
print("Existing Experiment 3A results were not modified.")

print("=" * 70)