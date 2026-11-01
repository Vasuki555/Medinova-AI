from pathlib import Path
import json

import pandas as pd
from scipy.stats import pearsonr, spearmanr


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

OCR_CSV = (
    PROJECT_ROOT
    / "experiments"
    / "results"
    / "clinocr_ocr_per_document.csv"
)

CLINICAL_CSV = (
    PROJECT_ROOT
    / "experiments"
    / "results"
    / "clinical_info"
    / "clinical_info_per_document.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "experiments"
    / "results"
    / "clinical_info"
    / "correlation_analysis"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# DOCUMENT KEY
# ============================================================

def make_ocr_document_key(path, subset):
    """
    OCR ground-truth filename examples:

        template_1_sample_2_normal.txt
        template_5_sample_6_handwriting.txt

    Clinical-info document examples:

        normal_template_1_sample_2
        handwriting_template_5_sample_6

    Convert OCR identifier to the exact clinical identifier.
    """

    filename = Path(str(path)).stem
    subset = str(subset).strip().lower()

    suffix = "_" + subset

    if filename.lower().endswith(suffix):
        filename = filename[:-len(suffix)]

    return f"{subset}_{filename}"


# ============================================================
# CORRELATION FUNCTION
# ============================================================

def calculate_correlation(x, y, metric_name, scope):

    data = pd.DataFrame({
        "ocr_metric": pd.to_numeric(
            x,
            errors="coerce"
        ),
        "clinical_metric": pd.to_numeric(
            y,
            errors="coerce"
        )
    }).dropna()

    n = len(data)

    result = {
        "scope": scope,
        "metric": metric_name,
        "n": n,
        "pearson_r": None,
        "pearson_p": None,
        "spearman_rho": None,
        "spearman_p": None,
    }

    if n < 3:
        return result

    if data["ocr_metric"].nunique() < 2:
        return result

    if data["clinical_metric"].nunique() < 2:
        return result

    try:
        r, p = pearsonr(
            data["ocr_metric"],
            data["clinical_metric"]
        )

        result["pearson_r"] = float(r)
        result["pearson_p"] = float(p)

    except Exception:
        pass

    try:
        rho, p = spearmanr(
            data["ocr_metric"],
            data["clinical_metric"]
        )

        result["spearman_rho"] = float(rho)
        result["spearman_p"] = float(p)

    except Exception:
        pass

    return result


# ============================================================
# START
# ============================================================

print("=" * 70)
print("EXPERIMENT 2C — OCR QUALITY vs CLINICAL INFORMATION")
print("CORRELATION ANALYSIS")
print("=" * 70)


# ============================================================
# LOAD
# ============================================================

print()
print("Loading OCR results...")
print(OCR_CSV)

ocr = pd.read_csv(OCR_CSV)

print(
    f"OCR rows loaded: {len(ocr)}"
)


print()
print("Loading clinical information results...")
print(CLINICAL_CSV)

clinical = pd.read_csv(CLINICAL_CSV)

print(
    f"Clinical rows loaded: {len(clinical)}"
)


# ============================================================
# VALIDATE COLUMNS
# ============================================================

required_ocr_columns = [
    "subset",
    "ground_truth_path",
    "cer",
    "wer",
    "status",
]

required_clinical_columns = [
    "subset",
    "document",
    "numbers_preservation",
    "dates_preservation",
    "units_preservation",
    "measurement_preservation",
]

missing_ocr = [
    c
    for c in required_ocr_columns
    if c not in ocr.columns
]

missing_clinical = [
    c
    for c in required_clinical_columns
    if c not in clinical.columns
]

if missing_ocr:

    raise ValueError(
        "Missing OCR columns: "
        + ", ".join(missing_ocr)
    )

if missing_clinical:

    raise ValueError(
        "Missing clinical columns: "
        + ", ".join(missing_clinical)
    )


# ============================================================
# CREATE OCR DOCUMENT COLUMN
# ============================================================

ocr["document"] = ocr.apply(
    lambda row: make_ocr_document_key(
        row["ground_truth_path"],
        row["subset"]
    ),
    axis=1
)


# ============================================================
# NORMALIZE CLINICAL DOCUMENT KEYS
# ============================================================

clinical["document"] = (
    clinical["document"]
    .astype(str)
    .str.strip()
)


ocr["subset"] = (
    ocr["subset"]
    .astype(str)
    .str.strip()
    .str.lower()
)

clinical["subset"] = (
    clinical["subset"]
    .astype(str)
    .str.strip()
    .str.lower()
)


# ============================================================
# DOCUMENT MATCHING
# ============================================================

ocr_keys = set(
    zip(
        ocr["subset"],
        ocr["document"]
    )
)

clinical_keys = set(
    zip(
        clinical["subset"],
        clinical["document"]
    )
)

matched_keys = (
    ocr_keys & clinical_keys
)

print()
print("=" * 70)
print("DOCUMENT MATCHING")
print("=" * 70)

print(
    f"OCR documents      : {len(ocr_keys)}"
)

print(
    f"Clinical documents : {len(clinical_keys)}"
)

print(
    f"Matched documents  : {len(matched_keys)}"
)

print(
    f"Unmatched OCR      : "
    f"{len(ocr_keys - clinical_keys)}"
)

print(
    f"Unmatched Clinical : "
    f"{len(clinical_keys - ocr_keys)}"
)


# ============================================================
# SHOW SAMPLE KEYS
# ============================================================

print()
print("Sample OCR keys:")

for key in sorted(ocr_keys)[:5]:
    print(" ", key)

print()
print("Sample Clinical keys:")

for key in sorted(clinical_keys)[:5]:
    print(" ", key)


# ============================================================
# FILTER SUCCESSFUL OCR
# ============================================================

ocr["status"] = (
    ocr["status"]
    .astype(str)
    .str.lower()
)

ocr_success = ocr[
    ocr["status"] == "success"
].copy()

print()
print(
    f"Successful OCR records: "
    f"{len(ocr_success)}"
)


# ============================================================
# NUMERIC CONVERSION
# ============================================================

ocr_success["cer"] = pd.to_numeric(
    ocr_success["cer"],
    errors="coerce"
)

ocr_success["wer"] = pd.to_numeric(
    ocr_success["wer"],
    errors="coerce"
)

clinical_metric_columns = [
    "numbers_preservation",
    "dates_preservation",
    "units_preservation",
    "measurement_preservation",
]

for column in clinical_metric_columns:

    clinical[column] = pd.to_numeric(
        clinical[column],
        errors="coerce"
    )


# ============================================================
# MERGE
# ============================================================

merged = pd.merge(
    ocr_success,
    clinical,
    on=[
        "subset",
        "document"
    ],
    how="inner",
    suffixes=(
        "_ocr",
        "_clinical"
    )
)


print()
print("=" * 70)
print("MERGED DATASET")
print("=" * 70)

print(
    f"Merged rows: {len(merged)}"
)


# ============================================================
# STOP IF MATCHING FAILED
# ============================================================

if len(merged) == 0:

    print()
    print(
        "ERROR: No documents were merged."
    )

    print(
        "Correlation analysis was NOT performed."
    )

    print(
        "Check the document keys printed above."
    )

    raise SystemExit(1)


# ============================================================
# SAVE MERGED DATA
# ============================================================

merged_path = (
    OUTPUT_DIR
    / "experiment_2c_merged_document_level.csv"
)

merged.to_csv(
    merged_path,
    index=False
)

print()
print(
    f"Merged dataset saved:\n{merged_path}"
)


# ============================================================
# CLINICAL METRICS
# ============================================================

clinical_metrics = {
    "numbers_preservation":
        "Number preservation",

    "dates_preservation":
        "Date preservation",

    "units_preservation":
        "Unit preservation",

    "measurement_preservation":
        "Measurement preservation",
}


results = []


# ============================================================
# OVERALL CORRELATIONS
# ============================================================

for column, label in clinical_metrics.items():

    # CER
    results.append(
        calculate_correlation(
            merged["cer"],
            merged[column],
            f"CER vs {label}",
            "overall"
        )
    )

    # WER
    results.append(
        calculate_correlation(
            merged["wer"],
            merged[column],
            f"WER vs {label}",
            "overall"
        )
    )


# ============================================================
# SUBSET CORRELATIONS
# ============================================================

for subset in sorted(
    merged["subset"].unique()
):

    subset_data = merged[
        merged["subset"] == subset
    ]

    for column, label in clinical_metrics.items():

        results.append(
            calculate_correlation(
                subset_data["cer"],
                subset_data[column],
                f"CER vs {label}",
                subset
            )
        )

        results.append(
            calculate_correlation(
                subset_data["wer"],
                subset_data[column],
                f"WER vs {label}",
                subset
            )
        )


# ============================================================
# RESULTS DATAFRAME
# ============================================================

results_df = pd.DataFrame(results)

results_df = results_df[
    [
        "scope",
        "metric",
        "n",
        "pearson_r",
        "pearson_p",
        "spearman_rho",
        "spearman_p",
    ]
]


# ============================================================
# SAVE CORRELATION RESULTS
# ============================================================

results_csv = (
    OUTPUT_DIR
    / "experiment_2c_correlation_results.csv"
)

results_df.to_csv(
    results_csv,
    index=False
)


# ============================================================
# SUMMARY
# ============================================================

summary = {
    "experiment": "Experiment 2C",
    "ocr_rows": int(len(ocr)),
    "clinical_rows": int(len(clinical)),
    "successful_ocr_rows": int(
        len(ocr_success)
    ),
    "ocr_document_keys": int(
        len(ocr_keys)
    ),
    "clinical_document_keys": int(
        len(clinical_keys)
    ),
    "matched_document_keys": int(
        len(matched_keys)
    ),
    "merged_rows": int(
        len(merged)
    ),
    "correlation_methods": [
        "Pearson",
        "Spearman"
    ],
    "clinical_metrics": list(
        clinical_metrics.keys()
    ),
    "missing_value_policy": (
        "Blank/non-applicable clinical "
        "preservation values remain missing "
        "and are excluded pairwise."
    ),
}


summary_json = (
    OUTPUT_DIR
    / "experiment_2c_summary.json"
)

with open(
    summary_json,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        summary,
        f,
        indent=2
    )


# ============================================================
# HUMAN-READABLE REPORT
# ============================================================

report_path = (
    OUTPUT_DIR
    / "experiment_2c_report.txt"
)

with open(
    report_path,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "EXPERIMENT 2C — CORRELATION ANALYSIS\n"
    )

    f.write(
        "=" * 70 + "\n\n"
    )

    f.write(
        f"OCR rows: {len(ocr)}\n"
    )

    f.write(
        f"Clinical rows: {len(clinical)}\n"
    )

    f.write(
        f"Matched documents: {len(matched_keys)}\n"
    )

    f.write(
        f"Merged rows: {len(merged)}\n\n"
    )

    f.write(
        "CORRELATION RESULTS\n"
    )

    f.write(
        "-" * 70 + "\n"
    )

    for _, row in results_df.iterrows():

        f.write(
            f"\nScope: {row['scope']}\n"
        )

        f.write(
            f"Metric: {row['metric']}\n"
        )

        f.write(
            f"N: {row['n']}\n"
        )

        f.write(
            f"Pearson r: {row['pearson_r']}\n"
        )

        f.write(
            f"Pearson p: {row['pearson_p']}\n"
        )

        f.write(
            f"Spearman rho: {row['spearman_rho']}\n"
        )

        f.write(
            f"Spearman p: {row['spearman_p']}\n"
        )

        f.write(
            "-" * 50 + "\n"
        )


# ============================================================
# CONSOLE OUTPUT
# ============================================================

print()
print("=" * 70)
print("EXPERIMENT 2C COMPLETE")
print("=" * 70)

print(
    f"Merged documents: {len(merged)}"
)

print()
print("OVERALL CORRELATIONS")
print("-" * 70)

overall = results_df[
    results_df["scope"] == "overall"
]

for _, row in overall.iterrows():

    print(
        f"\n{row['metric']}"
    )

    print(
        f"  N = {row['n']}"
    )

    print(
        f"  Pearson r = {row['pearson_r']}, "
        f"p = {row['pearson_p']}"
    )

    print(
        f"  Spearman rho = {row['spearman_rho']}, "
        f"p = {row['spearman_p']}"
    )


print()
print("OUTPUT FILES")
print("-" * 70)

print(merged_path)
print(results_csv)
print(summary_json)
print(report_path)

print()
print("=" * 70)