from pathlib import Path
import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr, t


# ============================================================
# MEDINOVA — EXPERIMENT 2C SUBSET-CONTROLLED ANALYSIS
# ============================================================

ROOT = Path(__file__).resolve().parent

OCR_FILE = (
    ROOT
    / "results"
    / "clinocr_ocr_per_document.csv"
)

CLINICAL_FILE = (
    ROOT
    / "results"
    / "clinical_info"
    / "clinical_info_per_document.csv"
)

OUTPUT_DIR = (
    ROOT
    / "results"
    / "clinical_info"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_CSV = (
    OUTPUT_DIR
    / "experiment_2c_subset_controlled_results.csv"
)

OUTPUT_TXT = (
    OUTPUT_DIR
    / "experiment_2c_subset_controlled_summary.txt"
)


# ============================================================
# LOAD
# ============================================================

ocr = pd.read_csv(OCR_FILE)
clinical = pd.read_csv(CLINICAL_FILE)

print("=" * 72)
print("EXPERIMENT 2C — SUBSET-CONTROLLED ANALYSIS")
print("=" * 72)

print()
print(f"OCR rows      : {len(ocr)}")
print(f"Clinical rows : {len(clinical)}")


# ============================================================
# CREATE MATCHING KEY
# ============================================================

def normalize_name(value):

    if pd.isna(value):
        return ""

    value = str(value).strip()

    # Remove common path extensions
    value = value.replace(".txt", "")
    value = value.replace(".png", "")
    value = value.replace(".jpg", "")
    value = value.replace(".jpeg", "")

    return value.lower()


def clinical_key(row):

    document = normalize_name(
        row.get("document", "")
    )

    subset = str(
        row.get("subset", "")
    ).strip().lower()

    return (
        subset,
        document
    )


def ocr_key(row):

    subset = str(
        row.get("subset", "")
    ).strip().lower()

    template = str(
        row.get("template", "")
    ).strip()

    sample = str(
        row.get("sample", "")
    ).strip()

    # Expected OCR naming:
    # subset_template_X_sample_Y
    document = (
        f"{subset}_"
        f"template_{template}_"
        f"sample_{sample}"
    )

    return (
        subset,
        normalize_name(document)
    )


clinical["_match_key"] = clinical.apply(
    clinical_key,
    axis=1
)

ocr["_match_key"] = ocr.apply(
    ocr_key,
    axis=1
)


# ============================================================
# MATCH
# ============================================================

merged = pd.merge(
    ocr,
    clinical,
    on="_match_key",
    how="inner",
    suffixes=("_ocr", "_clinical")
)

print()
print(f"Matched documents: {len(merged)}")


if len(merged) == 0:

    print()
    print("ERROR: No documents matched.")
    print("Inspect the document naming convention.")

    raise SystemExit(1)


# ============================================================
# PREPARE VARIABLES
# ============================================================

merged["subset"] = (
    merged["subset_ocr"]
    .astype(str)
    .str.lower()
    .str.strip()
)

variables = {

    "number_preservation":
        "numbers_preservation",

    "date_preservation":
        "dates_preservation",

    "unit_preservation":
        "units_preservation",

    "measurement_preservation":
        "measurement_preservation",
}


# ============================================================
# RESIDUALIZATION
# ============================================================

def residualize(values, subsets):

    values = np.asarray(
        values,
        dtype=float
    )

    subset_series = pd.Series(
        subsets
    ).astype(str)

    # Intercept + subset dummy variables
    dummies = pd.get_dummies(
        subset_series,
        drop_first=True
    ).astype(float)

    X = np.column_stack([
        np.ones(len(values)),
        dummies.values
    ])

    beta = np.linalg.lstsq(
        X,
        values,
        rcond=None
    )[0]

    predicted = X @ beta

    residuals = (
        values - predicted
    )

    return residuals


# ============================================================
# SUBSET-CONTROLLED PEARSON
# ============================================================

def partial_pearson(
    x,
    y,
    subsets
):

    x_res = residualize(
        x,
        subsets
    )

    y_res = residualize(
        y,
        subsets
    )

    if (
        np.std(x_res) == 0
        or np.std(y_res) == 0
    ):
        return np.nan, np.nan

    # Pearson correlation between residualized variables.
    # The correlation coefficient itself is unchanged from
    # the original residualization procedure.
    r, _ = pearsonr(
        x_res,
        y_res
    )

    # --------------------------------------------------------
    # Number of independent control variables
    # --------------------------------------------------------
    #
    # Six subsets are represented using drop_first=True:
    #
    #   5 independent dummy variables
    #
    # Therefore:
    #
    #   df = N - k - 2
    #
    # where:
    #   N = number of observations
    #   k = number of control variables
    #
    # --------------------------------------------------------

    subset_series = pd.Series(
        subsets
    ).astype(str)

    dummies = pd.get_dummies(
        subset_series,
        drop_first=True
    ).astype(float)

    k = dummies.shape[1]
    n = len(x)

    df = n - k - 2

    if df <= 0:
        return r, np.nan

    # t statistic for partial correlation
    t_stat = (
        r
        * np.sqrt(
            df / (1.0 - r ** 2)
        )
    )

    # Two-sided p-value
    p = 2.0 * t.sf(
        abs(t_stat),
        df
    )

    return r, p


# ============================================================
# SUBSET-CONTROLLED SPEARMAN
# ============================================================

def partial_spearman(
    x,
    y,
    subsets
):

    # Rank first, then residualize ranks
    x_rank = pd.Series(
        x
    ).rank(
        method="average"
    ).to_numpy()

    y_rank = pd.Series(
        y
    ).rank(
        method="average"
    ).to_numpy()

    x_res = residualize(
        x_rank,
        subsets
    )

    y_res = residualize(
        y_rank,
        subsets
    )

    if (
        np.std(x_res) == 0
        or np.std(y_res) == 0
    ):
        return np.nan, np.nan

    # Pearson correlation between residualized ranks.
    # This is the subset-controlled Spearman-style
    # partial rank correlation used by the experiment.
    rho, _ = pearsonr(
        x_res,
        y_res
    )

    # --------------------------------------------------------
    # Number of independent control variables
    # --------------------------------------------------------

    subset_series = pd.Series(
        subsets
    ).astype(str)

    dummies = pd.get_dummies(
        subset_series,
        drop_first=True
    ).astype(float)

    k = dummies.shape[1]
    n = len(x)

    df = n - k - 2

    if df <= 0:
        return rho, np.nan

    # t approximation for partial rank correlation
    t_stat = (
        rho
        * np.sqrt(
            df / (1.0 - rho ** 2)
        )
    )

    # Two-sided p-value
    p = 2.0 * t.sf(
        abs(t_stat),
        df
    )

    return rho, p


# ============================================================
# ANALYSE
# ============================================================

correlation_results = []


for error_metric in [
    "cer",
    "wer"
]:

    if error_metric not in merged.columns:

        print(
            f"WARNING: missing {error_metric}"
        )

        continue

    for preservation_name, preservation_col in variables.items():

        if preservation_col not in merged.columns:

            print(
                f"WARNING: missing "
                f"{preservation_col}"
            )

            continue

        data = merged[
            [
                error_metric,
                preservation_col,
                "subset"
            ]
        ].copy()

        data = data.dropna()

        if len(data) < 10:
            continue

        x = data[
            error_metric
        ].astype(float).to_numpy()

        y = data[
            preservation_col
        ].astype(float).to_numpy()

        subsets = data[
            "subset"
        ].astype(str).to_numpy()


        # ====================================================
        # ORDINARY CORRELATIONS
        # ====================================================

        pearson_r, pearson_p = pearsonr(
            x,
            y
        )

        spearman_rho, spearman_p = spearmanr(
            x,
            y
        )


        # ====================================================
        # SUBSET-CONTROLLED CORRELATIONS
        # ====================================================

        partial_r, partial_p = partial_pearson(
            x,
            y,
            subsets
        )

        partial_rho, partial_rho_p = partial_spearman(
            x,
            y,
            subsets
        )


        # ====================================================
        # SAVE RESULT
        # ====================================================

        correlation_results.append({

            "error_metric":
                error_metric,

            "clinical_metric":
                preservation_name,

            "n":
                len(data),

            "ordinary_pearson_r":
                pearson_r,

            "ordinary_pearson_p":
                pearson_p,

            "ordinary_spearman_rho":
                spearman_rho,

            "ordinary_spearman_p":
                spearman_p,

            "subset_controlled_pearson_r":
                partial_r,

            "subset_controlled_pearson_p":
                partial_p,

            "subset_controlled_spearman_rho":
                partial_rho,

            "subset_controlled_spearman_p":
                partial_rho_p,
        })


results_df = pd.DataFrame(
    correlation_results
)


# ============================================================
# SAVE CSV
# ============================================================

results_df.to_csv(
    OUTPUT_CSV,
    index=False
)


# ============================================================
# WRITE SUMMARY
# ============================================================

with OUTPUT_TXT.open(
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "MEDINOVA AI — EXPERIMENT 2C "
        "SUBSET-CONTROLLED ANALYSIS\n"
    )

    f.write("=" * 72 + "\n\n")

    f.write(
        f"Matched documents: {len(merged)}\n"
    )

    f.write(
        "Control variable: document subset\n"
    )

    f.write(
        "Subsets: handwriting, mixed, normal, "
        "poor, rotated, tables\n\n"
    )

    f.write(
        "Subset-controlled Pearson correlations "
        "were calculated by residualizing both "
        "variables against subset dummy variables.\n"
    )

    f.write(
        "Subset-controlled Spearman correlations "
        "were calculated by ranking both variables "
        "first and then residualizing the ranks "
        "against subset dummy variables.\n"
    )

    f.write(
        "For controlled correlation p-values, "
        "the residual degrees of freedom were "
        "calculated as N - k - 2, where k is the "
        "number of independent subset dummy "
        "variables.\n\n"
    )

    f.write(
        "The analysis tests whether the observed "
        "association between OCR error and clinical "
        "information preservation remains after "
        "accounting for document subset.\n"
    )

    f.write(
        "It does not establish causality.\n\n"
    )

    for _, row in results_df.iterrows():

        f.write(
            f"{row['error_metric'].upper()} vs "
            f"{row['clinical_metric']}\n"
        )

        f.write("-" * 72 + "\n")

        f.write(
            f"N: {int(row['n'])}\n"
        )

        f.write(
            f"Ordinary Pearson r: "
            f"{row['ordinary_pearson_r']:.6f}\n"
        )

        f.write(
            f"Ordinary Pearson p: "
            f"{row['ordinary_pearson_p']:.6e}\n"
        )

        f.write(
            f"Ordinary Spearman rho: "
            f"{row['ordinary_spearman_rho']:.6f}\n"
        )

        f.write(
            f"Ordinary Spearman p: "
            f"{row['ordinary_spearman_p']:.6e}\n"
        )

        f.write(
            f"Subset-controlled Pearson r: "
            f"{row['subset_controlled_pearson_r']:.6f}\n"
        )

        f.write(
            f"Subset-controlled Pearson p: "
            f"{row['subset_controlled_pearson_p']:.6e}\n"
        )

        f.write(
            f"Subset-controlled Spearman rho: "
            f"{row['subset_controlled_spearman_rho']:.6f}\n"
        )

        f.write(
            f"Subset-controlled Spearman p: "
            f"{row['subset_controlled_spearman_p']:.6e}\n\n"
        )


# ============================================================
# TERMINAL OUTPUT
# ============================================================

print()
print("=" * 72)
print("SUBSET-CONTROLLED RESULTS")
print("=" * 72)

for _, row in results_df.iterrows():

    print()
    print(
        f"{row['error_metric'].upper()} vs "
        f"{row['clinical_metric']}"
    )

    print(
        f"  N                         : "
        f"{int(row['n'])}"
    )

    print(
        f"  Ordinary Pearson r        : "
        f"{row['ordinary_pearson_r']:.6f}"
    )

    print(
        f"  Ordinary Pearson p        : "
        f"{row['ordinary_pearson_p']:.6e}"
    )

    print(
        f"  Ordinary Spearman rho     : "
        f"{row['ordinary_spearman_rho']:.6f}"
    )

    print(
        f"  Ordinary Spearman p       : "
        f"{row['ordinary_spearman_p']:.6e}"
    )

    print(
        f"  Controlled Pearson r      : "
        f"{row['subset_controlled_pearson_r']:.6f}"
    )

    print(
        f"  Controlled Pearson p      : "
        f"{row['subset_controlled_pearson_p']:.6e}"
    )

    print(
        f"  Controlled Spearman rho   : "
        f"{row['subset_controlled_spearman_rho']:.6f}"
    )

    print(
        f"  Controlled Spearman p     : "
        f"{row['subset_controlled_spearman_p']:.6e}"
    )


print()
print("=" * 72)
print("FILES CREATED")
print("=" * 72)

print()
print(OUTPUT_CSV)
print(OUTPUT_TXT)

print()
print("=" * 72)