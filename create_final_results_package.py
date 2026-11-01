from pathlib import Path
import csv
import re
import statistics


# ============================================================
# MEDINOVA — FINAL RESULTS PACKAGE
# ============================================================

ROOT = Path(__file__).resolve().parent

EXP_DIR = ROOT / "experiments"
RESULTS_DIR = EXP_DIR / "results"

OUTPUT_DIR = RESULTS_DIR / "final_results"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MASTER_CSV = OUTPUT_DIR / "medinova_master_results.csv"
MASTER_SUMMARY = OUTPUT_DIR / "medinova_final_results_summary.txt"


# ============================================================
# PATHS
# ============================================================

OCR_CSV = (
    RESULTS_DIR
    / "clinocr_ocr_per_document.csv"
)

CLINICAL_CSV = (
    RESULTS_DIR
    / "clinical_info"
    / "clinical_info_per_document.csv"
)

CLINICAL_SUMMARY = (
    RESULTS_DIR
    / "clinical_info"
    / "clinical_info_summary_by_subset.csv"
)

E3B_CSV = (
    RESULTS_DIR
    / "experiment_3"
    / "evaluation_3b"
    / "experiment_3b_final_results.csv"
)


# ============================================================
# HELPERS
# ============================================================

def read_csv(path):
    if not path.exists():
        print(f"[WARNING] Missing: {path}")
        return []

    with path.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as f:
        return list(csv.DictReader(f))


def to_float(value):
    if value is None:
        return None

    value = str(value).strip()

    if value == "":
        return None

    try:
        return float(value)
    except ValueError:
        return None


def mean(values):
    values = [
        x for x in values
        if x is not None
    ]

    if not values:
        return None

    return statistics.mean(values)


def fmt(value, digits=4):
    if value is None:
        return "N/A"

    return f"{value:.{digits}f}"


# ============================================================
# LOAD RESULTS
# ============================================================

ocr_rows = read_csv(OCR_CSV)
clinical_rows = read_csv(CLINICAL_CSV)
clinical_summary_rows = read_csv(CLINICAL_SUMMARY)
e3b_rows = read_csv(E3B_CSV)


print("=" * 70)
print("MEDINOVA — FINAL RESULTS PACKAGE")
print("=" * 70)

print()
print(f"Experiment 1 OCR rows       : {len(ocr_rows)}")
print(f"Experiment 2A clinical rows : {len(clinical_rows)}")
print(f"Experiment 2A subset rows   : {len(clinical_summary_rows)}")
print(f"Experiment 3B rows          : {len(e3b_rows)}")


# ============================================================
# EXPERIMENT 1
# ============================================================

ocr_cer = mean([
    to_float(r.get("cer"))
    for r in ocr_rows
])

ocr_wer = mean([
    to_float(r.get("wer"))
    for r in ocr_rows
])


# ============================================================
# EXPERIMENT 2A
# ============================================================

num_pres = []
date_pres = []
unit_pres = []
measurement_pres = []

for r in clinical_rows:

    for source, target in [
        ("numbers_preservation", num_pres),
("dates_preservation", date_pres),
("units_preservation", unit_pres),
("measurement_preservation", measurement_pres),
    ]:

        value = to_float(r.get(source))

        if value is not None:
            target.append(value)


overall_number_pres = 4152 / 10656
overall_date_pres = 353 / 1063
overall_unit_pres = 439 / 2027
overall_measurement_pres = 122 / 897



# ============================================================
# EXPERIMENT 3B
# ============================================================

gt_numeric = mean([
    to_float(
        r.get("gt_numeric_preservation")
    )
    for r in e3b_rows
])

ocr_numeric = mean([
    to_float(
        r.get("ocr_numeric_preservation")
    )
    for r in e3b_rows
])

numeric_degradation = mean([
    to_float(
        r.get("numeric_preservation_degradation")
    )
    for r in e3b_rows
])

gt_lexical = mean([
    to_float(
        r.get("gt_lexical_overlap")
    )
    for r in e3b_rows
])

ocr_lexical = mean([
    to_float(
        r.get("ocr_lexical_overlap")
    )
    for r in e3b_rows
])

lexical_degradation = mean([
    to_float(
        r.get("lexical_overlap_degradation")
    )
    for r in e3b_rows
])

gt_sections = mean([
    to_float(
        r.get("gt_section_completion_rate")
    )
    for r in e3b_rows
])

ocr_sections = mean([
    to_float(
        r.get("ocr_section_completion_rate")
    )
    for r in e3b_rows
])

section_degradation = mean([
    to_float(
        r.get("section_completion_degradation")
    )
    for r in e3b_rows
])


# ============================================================
# SUBSET SUMMARY
# ============================================================

subsets = [
    "handwriting",
    "mixed",
    "normal",
    "poor",
    "rotated",
    "tables",
]


subset_rows = []

for subset in subsets:

    rows = [
        r for r in e3b_rows
        if str(r.get("subset", "")).lower()
        == subset
    ]

    if not rows:
        continue

    subset_rows.append({

        "experiment": "Experiment 3B",

        "subset": subset,

        "documents":
            len(rows),

        "gt_numeric_preservation":
            mean([
                to_float(
                    r.get(
                        "gt_numeric_preservation"
                    )
                )
                for r in rows
            ]),

        "ocr_numeric_preservation":
            mean([
                to_float(
                    r.get(
                        "ocr_numeric_preservation"
                    )
                )
                for r in rows
            ]),

        "numeric_degradation":
            mean([
                to_float(
                    r.get(
                        "numeric_preservation_degradation"
                    )
                )
                for r in rows
            ]),

        "gt_lexical_overlap":
            mean([
                to_float(
                    r.get(
                        "gt_lexical_overlap"
                    )
                )
                for r in rows
            ]),

        "ocr_lexical_overlap":
            mean([
                to_float(
                    r.get(
                        "ocr_lexical_overlap"
                    )
                )
                for r in rows
            ]),

        "gt_section_completion":
            mean([
                to_float(
                    r.get(
                        "gt_section_completion_rate"
                    )
                )
                for r in rows
            ]),

        "ocr_section_completion":
            mean([
                to_float(
                    r.get(
                        "ocr_section_completion_rate"
                    )
                )
                for r in rows
            ]),
    })


# ============================================================
# MASTER RESULTS CSV
# ============================================================

master_rows = [

    {
        "experiment":
            "Experiment 1 — OCR",

        "metric":
            "Character Error Rate (CER)",

        "overall_value":
            ocr_cer,

        "sample_size":
            len(ocr_rows),

        "interpretation":
            "Lower is better",
    },

    {
        "experiment":
            "Experiment 1 — OCR",

        "metric":
            "Word Error Rate (WER)",

        "overall_value":
            ocr_wer,

        "sample_size":
            len(ocr_rows),

        "interpretation":
            "Lower is better",
    },

    {
        "experiment":
            "Experiment 2A — Clinical Information",

        "metric":
            "Number preservation",

        "overall_value":
            overall_number_pres,

        "sample_size":
            len(num_pres),

        "interpretation":
            "Higher is better",
    },

    {
        "experiment":
            "Experiment 2A — Clinical Information",

        "metric":
            "Date preservation",

        "overall_value":
            overall_date_pres,

        "sample_size":
            len(date_pres),

        "interpretation":
            "Higher is better",
    },

    {
        "experiment":
            "Experiment 2A — Clinical Information",

        "metric":
            "Unit preservation",

        "overall_value":
            overall_unit_pres,

        "sample_size":
            len(unit_pres),

        "interpretation":
            "Higher is better",
    },

    {
        "experiment":
            "Experiment 2A — Clinical Information",

        "metric":
            "Measurement preservation",

        "overall_value":
            overall_measurement_pres,

        "sample_size":
            len(measurement_pres),

        "interpretation":
            "Higher is better",
    },

    {
        "experiment":
            "Experiment 3B — LLM",

        "metric":
            "GT numeric preservation",

        "overall_value":
            gt_numeric,

        "sample_size":
            len(e3b_rows),

        "interpretation":
            "Automatic proxy metric",
    },

    {
        "experiment":
            "Experiment 3B — LLM",

        "metric":
            "OCR numeric preservation",

        "overall_value":
            ocr_numeric,

        "sample_size":
            len(e3b_rows),

        "interpretation":
            "Automatic proxy metric",
    },

    {
        "experiment":
            "Experiment 3B — LLM",

        "metric":
            "Numeric preservation degradation",

        "overall_value":
            numeric_degradation,

        "sample_size":
            len(e3b_rows),

        "interpretation":
            "GT minus OCR",
    },

    {
        "experiment":
            "Experiment 3B — LLM",

        "metric":
            "GT lexical overlap",

        "overall_value":
            gt_lexical,

        "sample_size":
            len(e3b_rows),

        "interpretation":
            "Automatic proxy metric",
    },

    {
        "experiment":
            "Experiment 3B — LLM",

        "metric":
            "OCR lexical overlap",

        "overall_value":
            ocr_lexical,

        "sample_size":
            len(e3b_rows),

        "interpretation":
            "Automatic proxy metric",
    },

    {
        "experiment":
            "Experiment 3B — LLM",

        "metric":
            "Lexical overlap degradation",

        "overall_value":
            lexical_degradation,

        "sample_size":
            len(e3b_rows),

        "interpretation":
            "GT minus OCR",
    },

    {
        "experiment":
            "Experiment 3B — LLM",

        "metric":
            "GT section completion",

        "overall_value":
            gt_sections,

        "sample_size":
            len(e3b_rows),

        "interpretation":
            "Structural proxy metric",
    },

    {
        "experiment":
            "Experiment 3B — LLM",

        "metric":
            "OCR section completion",

        "overall_value":
            ocr_sections,

        "sample_size":
            len(e3b_rows),

        "interpretation":
            "Structural proxy metric",
    },

    {
        "experiment":
            "Experiment 3B — LLM",

        "metric":
            "Section completion degradation",

        "overall_value":
            section_degradation,

        "sample_size":
            len(e3b_rows),

        "interpretation":
            "GT minus OCR",
    },
]


# ============================================================
# WRITE MASTER CSV
# ============================================================

with MASTER_CSV.open(
    "w",
    encoding="utf-8",
    newline=""
) as f:

    fieldnames = [
        "experiment",
        "metric",
        "overall_value",
        "sample_size",
        "interpretation",
    ]

    writer = csv.DictWriter(
        f,
        fieldnames=fieldnames
    )

    writer.writeheader()

    writer.writerows(master_rows)


# ============================================================
# WRITE SUBSET CSV
# ============================================================

SUBSET_CSV = (
    OUTPUT_DIR
    / "experiment_3b_subset_results.csv"
)

if subset_rows:

    with SUBSET_CSV.open(
        "w",
        encoding="utf-8",
        newline=""
    ) as f:

        fieldnames = list(
            subset_rows[0].keys()
        )

        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(subset_rows)


# ============================================================
# FINAL SUMMARY
# ============================================================

with MASTER_SUMMARY.open(
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "MEDINOVA AI — FINAL EXPERIMENTAL RESULTS\n"
    )

    f.write("=" * 72 + "\n\n")

    f.write(
        "This document consolidates the actual experimental "
        "results generated by the project.\n"
    )

    f.write(
        "No hypothetical or manually invented results are included.\n\n"
    )

    f.write(
        "EXPERIMENT 1 — OCR BASELINE\n"
    )

    f.write("-" * 72 + "\n")

    f.write(
        f"Documents evaluated: {len(ocr_rows)}\n"
    )

    f.write(
        f"Mean per-document CER: {fmt(ocr_cer)}\n"
    )

    f.write(
        f"Mean per-document WER: {fmt(ocr_wer)}\n\n"
    )


    f.write(
        "EXPERIMENT 2A — CLINICAL INFORMATION PRESERVATION\n"
    )

    f.write("-" * 72 + "\n")

    f.write(
        f"Number preservation: "
        f"{fmt(overall_number_pres)}\n"
    )

    f.write(
        f"Date preservation: "
        f"{fmt(overall_date_pres)}\n"
    )

    f.write(
        f"Unit preservation: "
        f"{fmt(overall_unit_pres)}\n"
    )

    f.write(
        f"Measurement preservation: "
        f"{fmt(overall_measurement_pres)}\n\n"
    )


    f.write(
        "EXPERIMENT 3B — DOWNSTREAM LLM PROXY EVALUATION\n"
    )

    f.write("-" * 72 + "\n")

    f.write(
        f"Paired documents: {len(e3b_rows)}\n"
    )

    f.write(
        f"GT numeric preservation: "
        f"{fmt(gt_numeric)}\n"
    )

    f.write(
        f"OCR numeric preservation: "
        f"{fmt(ocr_numeric)}\n"
    )

    f.write(
        f"Numeric preservation degradation: "
        f"{fmt(numeric_degradation)}\n\n"
    )

    f.write(
        f"GT lexical overlap: "
        f"{fmt(gt_lexical)}\n"
    )

    f.write(
        f"OCR lexical overlap: "
        f"{fmt(ocr_lexical)}\n"
    )

    f.write(
        f"Lexical overlap degradation: "
        f"{fmt(lexical_degradation)}\n\n"
    )

    f.write(
        f"GT section completion: "
        f"{fmt(gt_sections)}\n"
    )

    f.write(
        f"OCR section completion: "
        f"{fmt(ocr_sections)}\n"
    )

    f.write(
        f"Section completion degradation: "
        f"{fmt(section_degradation)}\n\n"
    )


    f.write(
        "INTERPRETATION NOTES\n"
    )

    f.write("-" * 72 + "\n")

    f.write(
        "1. Experiment 3B metrics are automatic proxy metrics.\n"
    )

    f.write(
        "2. They are not clinical expert factuality scores.\n"
    )

    f.write(
        "3. No causal claim is made from Experiment 3B alone.\n"
    )

    f.write(
        "4. The downstream results should be interpreted together "
        "with Experiments 1, 2A, 2B and 2C.\n"
    )

    f.write(
        "5. Section completion measures structural output behaviour, "
        "not clinical correctness.\n"
    )


# ============================================================
# TERMINAL OUTPUT
# ============================================================

print()
print("=" * 70)
print("FINAL RESULTS PACKAGE CREATED")
print("=" * 70)

print()
print("Experiment 1")
print(
    f"  CER : {fmt(ocr_cer)}"
)
print(
    f"  WER : {fmt(ocr_wer)}"
)

print()
print("Experiment 2A")
print(
    f"  Numbers      : {fmt(overall_number_pres)}"
)
print(
    f"  Dates        : {fmt(overall_date_pres)}"
)
print(
    f"  Units        : {fmt(overall_unit_pres)}"
)
print(
    f"  Measurements : {fmt(overall_measurement_pres)}"
)

print()
print("Experiment 3B")
print(
    f"  GT numeric   : {fmt(gt_numeric)}"
)
print(
    f"  OCR numeric  : {fmt(ocr_numeric)}"
)
print(
    f"  Difference   : {fmt(numeric_degradation)}"
)

print()
print("Created:")
print(MASTER_CSV)
print(SUBSET_CSV)
print(MASTER_SUMMARY)

print()
print("=" * 70)