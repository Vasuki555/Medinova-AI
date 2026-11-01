from pathlib import Path
import csv
import json
import re
from collections import defaultdict


# ============================================================
# EXPERIMENT 3B — FINAL AUTOMATIC EVALUATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

BASE_DIR = (
    PROJECT_ROOT
    / "experiments"
    / "results"
    / "experiment_3"
)

EVAL_DIR = BASE_DIR / "evaluation_3b"
RAW_DIR = BASE_DIR / "raw_outputs"

DATASET_CSV = EVAL_DIR / "experiment_3b_evaluation_dataset.csv"

OUT_CSV = EVAL_DIR / "experiment_3b_final_results.csv"
OUT_SUMMARY = EVAL_DIR / "experiment_3b_final_summary.txt"


# ============================================================
# PILOT / FINAL CASES
# ============================================================

PILOT_IDS = [
    "E3P001", "E3P002", "E3P003", "E3P004", "E3P005",
    "E3P006", "E3P007", "E3P008", "E3P009", "E3P010",
    "E3P011", "E3P012", "E3P013", "E3P014", "E3P015",
    "E3P016", "E3P017", "E3P018", "E3P019", "E3P020",
    "E3P021", "E3P022", "E3P023", "E3P024", "E3P025",
    "E3P026", "E3P027", "E3P028", "E3P029", "E3P030",
]


# ============================================================
# CHECK
# ============================================================

if not DATASET_CSV.exists():
    raise FileNotFoundError(DATASET_CSV)

if not RAW_DIR.exists():
    raise FileNotFoundError(RAW_DIR)


# ============================================================
# HELPERS
# ============================================================

def normalize(text):
    text = str(text or "").lower()
    text = text.replace("\\", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def read_text(path):
    if not path.exists():
        return ""
    return path.read_text(
        encoding="utf-8",
        errors="replace"
    ).strip()


def extract_numbers(text):
    """
    Extract clinically relevant numeric tokens.

    Keeps decimals, dates, percentages, ratios and
    simple numeric expressions.
    """
    text = str(text or "")

    patterns = [
        r"\b\d{1,4}/\d{1,4}/\d{2,4}\b",
        r"\b\d{4}-\d{1,2}-\d{1,2}\b",
        r"\b\d+(?:\.\d+)?%\b",
        r"\b\d+(?:\.\d+)?\s*(?:mg|mcg|g|kg|cm|mm|ml|mL|bpm|mmhg|°f|°c)\b",
        r"\b\d+(?:\.\d+)?\b",
    ]

    found = []

    for pattern in patterns:
        found.extend(re.findall(pattern, text, flags=re.I))

    return found


def number_key(value):
    """
    Normalize numeric expressions for comparison.
    """
    value = normalize(value)

    value = value.replace(" ", "")

    return value


def numeric_preservation(reference, generated):
    """
    Percentage of unique reference numeric tokens
    appearing in generated text.
    """

    ref_numbers = extract_numbers(reference)
    gen_numbers = extract_numbers(generated)

    ref_keys = set(number_key(x) for x in ref_numbers)
    gen_keys = set(number_key(x) for x in gen_numbers)

    if not ref_keys:
        return None, 0, 0

    matched = len(ref_keys & gen_keys)

    return (
        matched / len(ref_keys),
        matched,
        len(ref_keys)
    )


def word_overlap(reference, generated):
    """
    Simple normalized lexical overlap.
    This is NOT a clinical factuality score.
    """

    ref_words = set(
        re.findall(
            r"[a-zA-Z]{3,}",
            normalize(reference)
        )
    )

    gen_words = set(
        re.findall(
            r"[a-zA-Z]{3,}",
            normalize(generated)
        )
    )

    if not ref_words:
        return None

    return len(ref_words & gen_words) / len(ref_words)


def requested_sections(output):
    """
    Check whether the model output contains the requested
    section headings from the Experiment 3A prompt.
    """

    text = normalize(output)

    sections = {
        "summary":
            "report summary" in text,

        "key_findings":
            "key findings" in text,

        "important_values":
            "abnormal or important values" in text,

        "plain_language":
            "plain-language explanation" in text
            or "plain language explanation" in text,

        "medications":
            "medications / treatment information" in text
            or "medications" in text,

        "unclear":
            "information that is unclear or missing" in text
            or "unclear / missing information" in text,
    }

    count = sum(sections.values())

    return sections, count / len(sections)


def output_quality(output):
    """
    Descriptive output diagnostics.
    """

    length = len(output)

    sections, section_rate = requested_sections(output)

    return {
        "output_characters": length,
        "section_completion_rate": section_rate,
        "has_report_summary": int(sections["summary"]),
        "has_key_findings": int(sections["key_findings"]),
        "has_important_values": int(
            sections["important_values"]
        ),
        "has_plain_language": int(
            sections["plain_language"]
        ),
        "has_medications": int(
            sections["medications"]
        ),
        "has_unclear": int(
            sections["unclear"]
        ),
    }


# ============================================================
# LOAD DATASET
# ============================================================

with DATASET_CSV.open(
    "r",
    encoding="utf-8-sig",
    newline=""
) as f:

    dataset_rows = list(
        csv.DictReader(f)
    )


# ============================================================
# GROUP DATASET BY PILOT ID
# ============================================================

dataset_by_id = defaultdict(list)

for row in dataset_rows:

    pilot_id = row.get(
        "pilot_id",
        ""
    )

    dataset_by_id[pilot_id].append(row)


# ============================================================
# EVALUATE
# ============================================================

results = []

missing = []

for pilot_id in PILOT_IDS:

    rows = dataset_by_id.get(
        pilot_id,
        []
    )

    if not rows:

        missing.append(
            f"{pilot_id}: dataset row missing"
        )

        continue


    # --------------------------------------------------------
    # Extract metadata
    # --------------------------------------------------------

    row = rows[0]

    subset = row.get(
        "subset",
        ""
    )

    template = row.get(
        "template",
        ""
    )

    sample = row.get(
        "sample",
        ""
    )


    # --------------------------------------------------------
    # Ground truth / OCR input
    # --------------------------------------------------------

    gt_text = (
        row.get("ground_truth_text")
        or row.get("gt_text")
        or row.get("reference_text")
        or row.get("ground_truth")
        or ""
    )

    ocr_text = (
        row.get("ocr_text")
        or row.get("ocr")
        or ""
    )


    # --------------------------------------------------------
    # Existing raw Gemini outputs
    # --------------------------------------------------------

    gt_output_path = (
        RAW_DIR
        / f"{pilot_id}_gt_gemini.txt"
    )

    ocr_output_path = (
        RAW_DIR
        / f"{pilot_id}_ocr_gemini.txt"
    )

    gt_output = read_text(
        gt_output_path
    )

    ocr_output = read_text(
        ocr_output_path
    )


    if not gt_output:
        missing.append(
            f"{pilot_id}: GT Gemini output missing"
        )

    if not ocr_output:
        missing.append(
            f"{pilot_id}: OCR Gemini output missing"
        )


    # --------------------------------------------------------
    # Numeric preservation
    # --------------------------------------------------------

    gt_np, gt_num_match, ref_num_count = (
        numeric_preservation(
            gt_text,
            gt_output
        )
    )

    ocr_np, ocr_num_match, _ = (
        numeric_preservation(
            gt_text,
            ocr_output
        )
    )


    # --------------------------------------------------------
    # Lexical overlap
    # --------------------------------------------------------

    gt_overlap = word_overlap(
        gt_text,
        gt_output
    )

    ocr_overlap = word_overlap(
        gt_text,
        ocr_output
    )


    # --------------------------------------------------------
    # Output diagnostics
    # --------------------------------------------------------

    gt_quality = output_quality(
        gt_output
    )

    ocr_quality = output_quality(
        ocr_output
    )


    # --------------------------------------------------------
    # Degradation
    # --------------------------------------------------------

    if (
        gt_np is not None
        and ocr_np is not None
    ):

        numeric_degradation = (
            gt_np - ocr_np
        )

    else:

        numeric_degradation = None


    if (
        gt_overlap is not None
        and ocr_overlap is not None
    ):

        lexical_degradation = (
            gt_overlap - ocr_overlap
        )

    else:

        lexical_degradation = None


    section_degradation = (
        gt_quality["section_completion_rate"]
        -
        ocr_quality["section_completion_rate"]
    )


    # --------------------------------------------------------
    # Result row
    # --------------------------------------------------------

    results.append({

        "pilot_id":
            pilot_id,

        "subset":
            subset,

        "template":
            template,

        "sample":
            sample,

        "reference_numeric_tokens":
            ref_num_count,

        "gt_numeric_tokens_preserved":
            gt_num_match,

        "ocr_numeric_tokens_preserved":
            ocr_num_match,

        "gt_numeric_preservation":
            gt_np,

        "ocr_numeric_preservation":
            ocr_np,

        "numeric_preservation_degradation":
            numeric_degradation,

        "gt_lexical_overlap":
            gt_overlap,

        "ocr_lexical_overlap":
            ocr_overlap,

        "lexical_overlap_degradation":
            lexical_degradation,

        "gt_output_characters":
            gt_quality["output_characters"],

        "ocr_output_characters":
            ocr_quality["output_characters"],

        "gt_section_completion_rate":
            gt_quality["section_completion_rate"],

        "ocr_section_completion_rate":
            ocr_quality["section_completion_rate"],

        "section_completion_degradation":
            section_degradation,

        "gt_has_summary":
            gt_quality["has_report_summary"],

        "ocr_has_summary":
            ocr_quality["has_report_summary"],

        "gt_has_key_findings":
            gt_quality["has_key_findings"],

        "ocr_has_key_findings":
            ocr_quality["has_key_findings"],

        "gt_has_important_values":
            gt_quality["has_important_values"],

        "ocr_has_important_values":
            ocr_quality["has_important_values"],

        "gt_has_plain_language":
            gt_quality["has_plain_language"],

        "ocr_has_plain_language":
            ocr_quality["has_plain_language"],

        "gt_has_medications":
            gt_quality["has_medications"],

        "ocr_has_medications":
            ocr_quality["has_medications"],

        "gt_has_unclear_section":
            gt_quality["has_unclear"],

        "ocr_has_unclear_section":
            ocr_quality["has_unclear"],

    })


# ============================================================
# WRITE CSV
# ============================================================

if results:

    fieldnames = list(
        results[0].keys()
    )

    with OUT_CSV.open(
        "w",
        encoding="utf-8",
        newline=""
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(results)


# ============================================================
# SUMMARY
# ============================================================

def mean(values):

    values = [
        v for v in values
        if v is not None
    ]

    if not values:
        return None

    return sum(values) / len(values)


overall_gt_np = mean([
    r["gt_numeric_preservation"]
    for r in results
])

overall_ocr_np = mean([
    r["ocr_numeric_preservation"]
    for r in results
])

overall_num_deg = mean([
    r["numeric_preservation_degradation"]
    for r in results
])

overall_gt_overlap = mean([
    r["gt_lexical_overlap"]
    for r in results
])

overall_ocr_overlap = mean([
    r["ocr_lexical_overlap"]
    for r in results
])

overall_gt_sections = mean([
    r["gt_section_completion_rate"]
    for r in results
])

overall_ocr_sections = mean([
    r["ocr_section_completion_rate"]
    for r in results
])


# ============================================================
# SUBSET SUMMARY
# ============================================================

subset_groups = defaultdict(list)

for r in results:
    subset_groups[
        r["subset"]
    ].append(r)


with OUT_SUMMARY.open(
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "EXPERIMENT 3B — FINAL AUTOMATIC EVALUATION\n"
    )

    f.write("=" * 70 + "\n\n")

    f.write(
        "IMPORTANT:\n"
        "These are automatic proxy metrics.\n"
        "They are NOT clinical expert factuality scores.\n"
        "No manually assigned clinical scores are included.\n\n"
    )

    f.write(
        f"Documents evaluated: {len(results)}\n"
    )

    f.write(
        f"Missing-data warnings: {len(missing)}\n\n"
    )


    f.write(
        "OVERALL RESULTS\n"
    )

    f.write("-" * 70 + "\n")

    f.write(
        f"GT numeric preservation: "
        f"{overall_gt_np:.4f}\n"
    )

    f.write(
        f"OCR numeric preservation: "
        f"{overall_ocr_np:.4f}\n"
    )

    f.write(
        f"Numeric preservation degradation: "
        f"{overall_num_deg:.4f}\n\n"
    )

    f.write(
        f"GT lexical overlap: "
        f"{overall_gt_overlap:.4f}\n"
    )

    f.write(
        f"OCR lexical overlap: "
        f"{overall_ocr_overlap:.4f}\n\n"
    )

    f.write(
        f"GT section completion: "
        f"{overall_gt_sections:.4f}\n"
    )

    f.write(
        f"OCR section completion: "
        f"{overall_ocr_sections:.4f}\n\n"
    )


    f.write(
        "SUBSET RESULTS\n"
    )

    f.write("-" * 70 + "\n\n")


    for subset in sorted(
        subset_groups.keys()
    ):

        group = subset_groups[subset]

        gt_np = mean([
            r["gt_numeric_preservation"]
            for r in group
        ])

        ocr_np = mean([
            r["ocr_numeric_preservation"]
            for r in group
        ])

        num_deg = mean([
            r["numeric_preservation_degradation"]
            for r in group
        ])

        gt_overlap = mean([
            r["gt_lexical_overlap"]
            for r in group
        ])

        ocr_overlap = mean([
            r["ocr_lexical_overlap"]
            for r in group
        ])

        gt_sections = mean([
            r["gt_section_completion_rate"]
            for r in group
        ])

        ocr_sections = mean([
            r["ocr_section_completion_rate"]
            for r in group
        ])


        f.write(
            f"[{subset}]\n"
        )

        f.write(
            f"Documents: {len(group)}\n"
        )

        f.write(
            f"GT numeric preservation: "
            f"{gt_np:.4f}\n"
        )

        f.write(
            f"OCR numeric preservation: "
            f"{ocr_np:.4f}\n"
        )

        f.write(
            f"Numeric degradation: "
            f"{num_deg:.4f}\n"
        )

        f.write(
            f"GT lexical overlap: "
            f"{gt_overlap:.4f}\n"
        )

        f.write(
            f"OCR lexical overlap: "
            f"{ocr_overlap:.4f}\n"
        )

        f.write(
            f"GT section completion: "
            f"{gt_sections:.4f}\n"
        )

        f.write(
            f"OCR section completion: "
            f"{ocr_sections:.4f}\n\n"
        )


    if missing:

        f.write(
            "WARNINGS\n"
        )

        f.write("-" * 70 + "\n")

        for item in missing:

            f.write(
                item + "\n"
            )


# ============================================================
# TERMINAL OUTPUT
# ============================================================

print("=" * 70)
print(
    "EXPERIMENT 3B — FINAL AUTOMATIC EVALUATION"
)
print("=" * 70)

print(
    f"Documents evaluated: {len(results)}"
)

print(
    f"Warnings: {len(missing)}"
)

print()
print("Overall:")
print(
    f"  GT numeric preservation  : "
    f"{overall_gt_np:.4f}"
)

print(
    f"  OCR numeric preservation : "
    f"{overall_ocr_np:.4f}"
)

print(
    f"  Numeric degradation      : "
    f"{overall_num_deg:.4f}"
)

print()
print(
    f"  GT lexical overlap       : "
    f"{overall_gt_overlap:.4f}"
)

print(
    f"  OCR lexical overlap      : "
    f"{overall_ocr_overlap:.4f}"
)

print()
print(
    f"  GT section completion    : "
    f"{overall_gt_sections:.4f}"
)

print(
    f"  OCR section completion   : "
    f"{overall_ocr_sections:.4f}"
)

print()
print("CSV:")
print(OUT_CSV)

print()
print("Summary:")
print(OUT_SUMMARY)

print("=" * 70)