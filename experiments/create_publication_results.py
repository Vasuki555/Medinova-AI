from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# MEDINOVA — PUBLICATION RESULTS PACKAGE
# ============================================================

ROOT = Path(__file__).resolve().parent

RESULTS = ROOT / "results"

OCR_FILE = RESULTS / "clinocr_ocr_per_document.csv"

CLINICAL_FILE = (
    RESULTS
    / "clinical_info"
    / "clinical_info_per_document.csv"
)

CONTROLLED_FILE = (
    RESULTS
    / "clinical_info"
    / "experiment_2c_subset_controlled_results.csv"
)

E3B_FILE = (
    RESULTS
    / "experiment_3"
    / "evaluation_3b"
    / "experiment_3b_statistical_results.csv"
)

OUT = RESULTS / "publication"
OUT.mkdir(parents=True, exist_ok=True)


# ============================================================
# LOAD DATA
# ============================================================

ocr = pd.read_csv(OCR_FILE)
clinical = pd.read_csv(CLINICAL_FILE)
controlled = pd.read_csv(CONTROLLED_FILE)
e3b = pd.read_csv(E3B_FILE)

print("=" * 72)
print("MEDINOVA — PUBLICATION RESULTS PACKAGE")
print("=" * 72)

print()
print(f"OCR documents      : {len(ocr)}")
print(f"Clinical documents : {len(clinical)}")
print(f"Controlled rows    : {len(controlled)}")
print(f"E3B metrics        : {len(e3b)}")


# ============================================================
# TABLE 1 — OCR PERFORMANCE BY SUBSET
# ============================================================

table1 = (
    ocr
    .groupby("subset")
    .agg(
        N=("cer", "count"),
        CER=("cer", "mean"),
        WER=("wer", "mean")
    )
    .reset_index()
)

order = [
    "normal",
    "tables",
    "handwriting",
    "poor",
    "rotated",
    "mixed"
]

table1["order"] = table1["subset"].apply(
    lambda x: order.index(x)
    if x in order else 999
)

table1 = (
    table1
    .sort_values("order")
    .drop(columns="order")
)

table1.to_csv(
    OUT / "table_1_ocr_performance.csv",
    index=False
)


# ============================================================
# TABLE 2 — CLINICAL INFORMATION PRESERVATION
# ============================================================

# Pooled preservation by subset:
#
# matched tokens / ground-truth tokens

rows = []

for subset, group in clinical.groupby("subset"):

    def pooled(matched_col, gt_col):
        matched = group[matched_col].sum()
        gt = group[gt_col].sum()

        if gt == 0:
            return np.nan

        return matched / gt

    rows.append({
        "subset": subset,

        "N": len(group),

        "Numbers": pooled(
            "numbers_matched",
            "numbers_gt"
        ),

        "Dates": pooled(
            "dates_matched",
            "dates_gt"
        ),

        "Units": pooled(
            "units_matched",
            "units_gt"
        ),

        "Measurements": pooled(
            "measurements_matched",
            "measurements_gt"
        )
    })

table2 = pd.DataFrame(rows)

table2["order"] = table2["subset"].apply(
    lambda x: order.index(x)
    if x in order else 999
)

table2 = (
    table2
    .sort_values("order")
    .drop(columns="order")
)

table2.to_csv(
    OUT / "table_2_clinical_information_preservation.csv",
    index=False
)


# ============================================================
# TABLE 3 — CONTROLLED CORRELATION
# ============================================================

table3 = controlled[
    [
        "error_metric",
        "clinical_metric",
        "n",
        "ordinary_pearson_r",
        "ordinary_pearson_p",
        "subset_controlled_pearson_r",
        "subset_controlled_pearson_p",
        "subset_controlled_spearman_rho",
"subset_controlled_spearman_p"
    ]
].copy()

table3.to_csv(
    OUT / "table_3_controlled_correlations.csv",
    index=False
)


# ============================================================
# TABLE 4 — DOWNSTREAM LLM STATISTICS
# ============================================================

table4 = e3b.copy()

table4.to_csv(
    OUT / "table_4_llm_statistics.csv",
    index=False
)


# ============================================================
# FIGURE 1 — CER / WER BY SUBSET
# ============================================================

fig, ax = plt.subplots(
    figsize=(10, 6)
)

x = np.arange(len(table1))
width = 0.36

ax.bar(
    x - width / 2,
    table1["CER"],
    width,
    label="CER"
)

ax.bar(
    x + width / 2,
    table1["WER"],
    width,
    label="WER"
)

ax.set_xticks(x)
ax.set_xticklabels(
    table1["subset"],
    rotation=25,
    ha="right"
)

ax.set_ylabel("Error rate")
ax.set_xlabel("Document subset")

ax.set_title(
    "OCR Error Rates Across Clinical Document Subsets"
)

ax.legend()

fig.tight_layout()

fig.savefig(
    OUT / "figure_1_ocr_error_by_subset.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)


# ============================================================
# FIGURE 2 — CLINICAL INFORMATION PRESERVATION
# ============================================================

fig, ax = plt.subplots(
    figsize=(11, 6)
)

metrics = [
    "Numbers",
    "Dates",
    "Units",
    "Measurements"
]

x = np.arange(len(table2))
width = 0.18

for i, metric in enumerate(metrics):

    ax.bar(
        x + (i - 1.5) * width,
        table2[metric],
        width,
        label=metric
    )

ax.set_xticks(x)
ax.set_xticklabels(
    table2["subset"],
    rotation=25,
    ha="right"
)

ax.set_ylabel("Preservation ratio")
ax.set_xlabel("Document subset")

ax.set_title(
    "Clinical Information Preservation After OCR"
)

ax.legend()

fig.tight_layout()

fig.savefig(
    OUT / "figure_2_clinical_information_preservation.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)


# ============================================================
# FIGURE 3 — CER VS NUMBER PRESERVATION
# ============================================================

fig, ax = plt.subplots(
    figsize=(8, 6)
)

# ------------------------------------------------------------
# Explicit document-level matching
# OCR ground_truth_path <-> clinical gt_file
# Match using subset + ground-truth filename
# ------------------------------------------------------------

ocr_plot = ocr[
    ["subset", "ground_truth_path", "cer"]
].copy()

clinical_plot = clinical[
    ["subset", "gt_file", "numbers_preservation"]
].copy()

# Extract only the ground-truth filename so that differences
# in absolute/relative directory paths do not affect matching.
ocr_plot["match_file"] = (
    ocr_plot["ground_truth_path"]
    .astype(str)
    .str.replace("\\", "/", regex=False)
    .str.strip()
    .str.split("/")
    .str[-1]
)

clinical_plot["match_file"] = (
    clinical_plot["gt_file"]
    .astype(str)
    .str.replace("\\", "/", regex=False)
    .str.strip()
    .str.split("/")
    .str[-1]
)

# Check that each subset + filename identifies one document.
if ocr_plot.duplicated(
    ["subset", "match_file"]
).any():
    raise ValueError(
        "Duplicate OCR document keys found for "
        "['subset', 'match_file']."
    )

if clinical_plot.duplicated(
    ["subset", "match_file"]
).any():
    raise ValueError(
        "Duplicate clinical document keys found for "
        "['subset', 'match_file']."
    )

# Explicit one-to-one document matching.
merged_plot = pd.merge(
    ocr_plot,
    clinical_plot,
    on=["subset", "match_file"],
    how="inner",
    validate="one_to_one"
)

# ------------------------------------------------------------
# Safety checks
# ------------------------------------------------------------

print()
print(
    f"Figure 3 document matching : "
    f"{len(merged_plot)}/{len(ocr_plot)}"
)

if len(merged_plot) != len(ocr_plot):
    missing_ocr = (
        ocr_plot[
            ~ocr_plot.set_index(
                ["subset", "match_file"]
            ).index.isin(
                merged_plot.set_index(
                    ["subset", "match_file"]
                ).index
            )
        ]
    )

    print("Unmatched OCR documents:")
    print(
        missing_ocr[
            ["subset", "ground_truth_path"]
        ].to_string(index=False)
    )

    raise ValueError(
        "Figure 3 matching failed: "
        "not all OCR documents were matched."
    )

if len(merged_plot) != len(clinical_plot):
    raise ValueError(
        "Figure 3 matching failed: "
        "not all clinical documents were matched."
    )

# ------------------------------------------------------------
# Scatter plot
# ------------------------------------------------------------

ax.scatter(
    merged_plot["cer"],
    merged_plot["numbers_preservation"],
    alpha=0.65
)

ax.set_xlabel("Character Error Rate (CER)")
ax.set_ylabel("Number preservation")

ax.set_title(
    "Association Between OCR Error and Number Preservation"
)

fig.tight_layout()

fig.savefig(
    OUT / "figure_3_cer_vs_number_preservation.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)


# ============================================================
# FIGURE 4 — LLM GT VS OCR
# ============================================================

metrics_e3 = [
    "Numeric preservation",
    "Lexical overlap",
    "Section completion"
]

gt_values = [
    float(
        e3b.loc[
            e3b["metric"] == "Numeric preservation",
            "gt_mean"
        ].iloc[0]
    ),
    float(
        e3b.loc[
            e3b["metric"] == "Lexical overlap",
            "gt_mean"
        ].iloc[0]
    ),
    float(
        e3b.loc[
            e3b["metric"] == "Section completion",
            "gt_mean"
        ].iloc[0]
    )
]

ocr_values = [
    float(
        e3b.loc[
            e3b["metric"] == "Numeric preservation",
            "ocr_mean"
        ].iloc[0]
    ),
    float(
        e3b.loc[
            e3b["metric"] == "Lexical overlap",
            "ocr_mean"
        ].iloc[0]
    ),
    float(
        e3b.loc[
            e3b["metric"] == "Section completion",
            "ocr_mean"
        ].iloc[0]
    )
]

fig, ax = plt.subplots(
    figsize=(9, 6)
)

x = np.arange(len(metrics_e3))
width = 0.36

ax.bar(
    x - width / 2,
    gt_values,
    width,
    label="GT condition"
)

ax.bar(
    x + width / 2,
    ocr_values,
    width,
    label="OCR condition"
)

ax.set_xticks(x)
ax.set_xticklabels(
    metrics_e3,
    rotation=15
)

ax.set_ylabel("Score")
ax.set_title(
    "Downstream LLM Automatic Proxy Metrics"
)

ax.legend()

fig.tight_layout()

fig.savefig(
    OUT / "figure_4_llm_gt_vs_ocr.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)


# ============================================================
# MASTER RESULTS TEXT
# ============================================================

with (
    OUT / "publication_results_summary.txt"
).open(
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "MEDINOVA AI — PUBLICATION RESULTS PACKAGE\n"
    )

    f.write("=" * 72 + "\n\n")

    f.write(
        "TABLE 1 — OCR PERFORMANCE\n\n"
    )

    f.write(
        table1.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}"
        )
    )

    f.write("\n\n")

    f.write(
        "TABLE 2 — CLINICAL INFORMATION PRESERVATION\n\n"
    )

    f.write(
        table2.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}"
        )
    )

    f.write("\n\n")

    f.write(
        "TABLE 3 — SUBSET-CONTROLLED CORRELATIONS\n\n"
    )

    f.write(
        table3.to_string(
            index=False,
            float_format=lambda x: f"{x:.6f}"
        )
    )

    f.write("\n\n")

    f.write(
        "TABLE 4 — DOWNSTREAM LLM STATISTICS\n\n"
    )

    f.write(
        table4.to_string(
            index=False,
            float_format=lambda x: f"{x:.6f}"
        )
    )


# ============================================================
# OUTPUT
# ============================================================

print()
print("=" * 72)
print("PUBLICATION RESULTS CREATED")
print("=" * 72)

print()
print("Tables:")

print(
    OUT / "table_1_ocr_performance.csv"
)

print(
    OUT / "table_2_clinical_information_preservation.csv"
)

print(
    OUT / "table_3_controlled_correlations.csv"
)

print(
    OUT / "table_4_llm_statistics.csv"
)

print()
print("Figures:")

print(
    OUT / "figure_1_ocr_error_by_subset.png"
)

print(
    OUT / "figure_2_clinical_information_preservation.png"
)

print(
    OUT / "figure_3_cer_vs_number_preservation.png"
)

print(
    OUT / "figure_4_llm_gt_vs_ocr.png"
)

print()
print(
    OUT / "publication_results_summary.txt"
)

print()
print("=" * 72)