"""
Experiment 2A — Clinical Information Preservation Proxy Analysis
MediNova / ClinOCR-Bench

This version fixes the Ground Truth filename matching for ClinOCR-Bench.
It intentionally evaluates only the 328 OCR evaluation documents.
The 56 exemplar documents are present in GT but correctly absent from OCR.

This is a PROXY analysis, not a validated clinical-entity annotation study.
"""

from pathlib import Path
import zipfile
import re
from collections import Counter
import pandas as pd

# Run this script from the MediNova project root.
OCR_ZIP = Path(r"experiments/results/ocr_text.zip")
GT_ZIP = Path(r"experiments/ground_truth.zip")
OUT_DIR = Path(r"experiments/results/clinical_info")

OUT_DIR.mkdir(parents=True, exist_ok=True)

NUMBER_RE = re.compile(
    r"(?<![A-Za-z])[-+]?\d+(?:[.,]\d+)*(?:[eE][-+]?\d+)?(?![A-Za-z])"
)

DATE_RE = re.compile(
    r"\b(?:"
    r"\d{1,4}[/-]\d{1,2}[/-]\d{1,4}|"
    r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|"
    r"\d{4}-\d{1,2}-\d{1,2}"
    r")\b"
)

UNIT_RE = re.compile(
    r"\b(?:mg|g|kg|mcg|µg|ug|mL|ml|L|dL|mmHg|cmH2O|"
    r"mm|cm|m|cm3|mm3|mL/min|mg/dL|g/dL|U/L|IU/L|"
    r"bpm|%|°C|°F|sec|s|min|hr|h|days?|weeks?|months?|years?)\b",
    re.IGNORECASE,
)

MEASUREMENT_RE = re.compile(
    r"([-+]?\d+(?:[.,]\d+)?)\s*"
    r"(mg/dL|g/dL|mmHg|mg|g|kg|mcg|µg|ug|mL|ml|L|U/L|IU/L|"
    r"bpm|mm|cm|%|°C|°F)\b",
    re.IGNORECASE,
)


def normalize_number(x):
    return x.strip().replace(" ", "")


def normalize_date(x):
    return re.sub(r"[^0-9]", "", x)


def ocr_key(name):
    """
    OCR:
      ocr_text/handwriting_template_1_sample_2.txt

    Key:
      handwriting_template_1_sample_2
    """
    return Path(name).stem.lower()


def gt_key_and_subset(name):
    """
    GT:
      ground_truth/handwriting/template_1_sample_2_handwriting.txt

    Key:
      handwriting_template_1_sample_2

    Subset:
      handwriting
    """
    parts = name.replace("\\", "/").split("/")

    if len(parts) < 3:
        return None, None

    subset = parts[1].lower()
    stem = Path(parts[-1]).stem.lower()

    suffix = f"_{subset}"
    if stem.endswith(suffix):
        stem = stem[:-len(suffix)]

    return f"{subset}_{stem}", subset


def extract_items(text):
    return {
        "numbers": [normalize_number(x) for x in NUMBER_RE.findall(text)],
        "dates": [normalize_date(x) for x in DATE_RE.findall(text)],
        "units": [x.lower() for x in UNIT_RE.findall(text)],
    }


def extract_measurements(text):
    return [
        (normalize_number(value), unit.lower())
        for value, unit in MEASUREMENT_RE.findall(text)
    ]


def multiset_match(gt_items, ocr_items):
    gt = Counter(gt_items)
    ocr = Counter(ocr_items)

    matched = sum(min(count, ocr.get(item, 0))
                  for item, count in gt.items())

    total = sum(gt.values())
    recall = matched / total if total else None

    return matched, total, recall


# ---------------------------------------------------------
# Build Ground Truth lookup
# ---------------------------------------------------------

gt_lookup = {}

with zipfile.ZipFile(GT_ZIP) as gz:
    for name in gz.namelist():
        if not name.lower().endswith(".txt"):
            continue

        key, subset = gt_key_and_subset(name)

        if key:
            gt_lookup[key] = {
                "zip_name": name,
                "subset": subset,
            }


# ---------------------------------------------------------
# Process OCR evaluation documents
# ---------------------------------------------------------

rows = []
unmatched = []

with zipfile.ZipFile(OCR_ZIP) as oz, zipfile.ZipFile(GT_ZIP) as gz:

    for name in oz.namelist():

        if not name.lower().endswith(".txt"):
            continue

        key = ocr_key(name)

        if key not in gt_lookup:
            unmatched.append(name)
            continue

        gt_name = gt_lookup[key]["zip_name"]
        subset = gt_lookup[key]["subset"]

        ocr_text = oz.read(name).decode("utf-8", errors="replace")
        gt_text = gz.read(gt_name).decode("utf-8", errors="replace")

        gt_items = extract_items(gt_text)
        ocr_items = extract_items(ocr_text)

        row = {
            "subset": subset,
            "document": key,
            "ocr_file": name,
            "gt_file": gt_name,
            "gt_chars": len(gt_text),
            "ocr_chars": len(ocr_text),
        }

        for category in ["numbers", "dates", "units"]:

            matched, total, preservation = multiset_match(
                gt_items[category],
                ocr_items[category],
            )

            row[f"{category}_gt"] = total
            row[f"{category}_matched"] = matched
            row[f"{category}_preservation"] = preservation

        gt_measurements = Counter(extract_measurements(gt_text))
        ocr_measurements = Counter(extract_measurements(ocr_text))

        matched_measurements = sum(
            min(count, ocr_measurements.get(item, 0))
            for item, count in gt_measurements.items()
        )

        total_measurements = sum(gt_measurements.values())

        row["measurements_gt"] = total_measurements
        row["measurements_matched"] = matched_measurements
        row["measurement_preservation"] = (
            matched_measurements / total_measurements
            if total_measurements else None
        )

        rows.append(row)


# ---------------------------------------------------------
# Save per-document results
# ---------------------------------------------------------

df = pd.DataFrame(rows)

if df.empty:
    raise RuntimeError(
        "No OCR/GT pairs were matched. Check ZIP paths and filename structure."
    )

df.to_csv(
    OUT_DIR / "clinical_info_per_document.csv",
    index=False,
)


# ---------------------------------------------------------
# Subset-level pooled results
# ---------------------------------------------------------

summary_rows = []

for subset, group in df.groupby("subset"):

    row = {
        "subset": subset,
        "documents": len(group),
    }

    for category in [
        "numbers",
        "dates",
        "units",
        "measurements",
    ]:

        total = int(group[f"{category}_gt"].sum())
        matched = int(group[f"{category}_matched"].sum())

        row[f"{category}_gt"] = total
        row[f"{category}_matched"] = matched
        row[f"{category}_preservation"] = (
            matched / total if total else None
        )

    summary_rows.append(row)


summary = pd.DataFrame(summary_rows).sort_values("subset")

summary.to_csv(
    OUT_DIR / "clinical_info_summary_by_subset.csv",
    index=False,
)


# ---------------------------------------------------------
# Overall pooled results
# ---------------------------------------------------------

overall = {}

for category in [
    "numbers",
    "dates",
    "units",
    "measurements",
]:

    total = int(df[f"{category}_gt"].sum())
    matched = int(df[f"{category}_matched"].sum())

    overall[category] = {
        "ground_truth_total": total,
        "matched": matched,
        "preservation": matched / total if total else None,
    }


with open(
    OUT_DIR / "clinical_info_overall.txt",
    "w",
    encoding="utf-8",
) as f:

    f.write(
        "Experiment 2A — Clinical Information Preservation Proxy\n"
    )
    f.write("=" * 60 + "\n")
    f.write(f"Documents analyzed: {len(df)}\n")
    f.write(f"Unmatched OCR files: {len(unmatched)}\n")
    f.write("\n")

    for category, result in overall.items():

        if result["preservation"] is not None:
            f.write(
                f"{category}: "
                f"GT={result['ground_truth_total']}, "
                f"matched={result['matched']}, "
                f"preservation={result['preservation']:.4f}\n"
            )
        else:
            f.write(
                f"{category}: "
                f"GT={result['ground_truth_total']}, "
                f"matched={result['matched']}, "
                "preservation=N/A\n"
            )


# ---------------------------------------------------------
# Console output
# ---------------------------------------------------------

print()
print("=" * 65)
print("Experiment 2A — Clinical Information Preservation Proxy")
print("=" * 65)

print(f"Documents analyzed : {len(df)}")
print(f"Unmatched OCR files: {len(unmatched)}")

if len(unmatched) > 0:
    print("\nUNMATCHED OCR FILES:")
    for item in unmatched[:20]:
        print(" ", item)

print("\nOverall pooled preservation:")

for category, result in overall.items():

    if result["preservation"] is not None:
        print(
            f"  {category:12s}: "
            f"{result['matched']:5d}/"
            f"{result['ground_truth_total']:5d} "
            f"({result['preservation'] * 100:.2f}%)"
        )
    else:
        print(
            f"  {category:12s}: "
            f"{result['ground_truth_total']:5d} GT items "
            "(no measurable items)"
        )

print("\nSubset summary:")
print(summary.to_string(index=False))

print("\nOutputs:")
print(OUT_DIR / "clinical_info_per_document.csv")
print(OUT_DIR / "clinical_info_summary_by_subset.csv")
print(OUT_DIR / "clinical_info_overall.txt")
