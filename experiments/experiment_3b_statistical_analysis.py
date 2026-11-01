from pathlib import Path
import csv
import math
import statistics

try:
    from scipy.stats import wilcoxon
except ImportError:
    raise SystemExit(
        "scipy is required. Install with:\n"
        "pip install scipy"
    )


# ============================================================
# MEDINOVA — EXPERIMENT 3B STATISTICAL ANALYSIS
# ============================================================

ROOT = Path(__file__).resolve().parent

INPUT = (
    ROOT
    / "results"
    / "experiment_3"
    / "evaluation_3b"
    / "experiment_3b_final_results.csv"
)

OUTPUT_DIR = (
    ROOT
    / "results"
    / "experiment_3"
    / "evaluation_3b"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_CSV = (
    OUTPUT_DIR
    / "experiment_3b_statistical_results.csv"
)

OUTPUT_SUBSET_CSV = (
    OUTPUT_DIR
    / "experiment_3b_subset_statistics.csv"
)

OUTPUT_TXT = (
    OUTPUT_DIR
    / "experiment_3b_statistical_summary.txt"
)


# ============================================================
# HELPERS
# ============================================================

def read_csv(path):
    with path.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as f:
        return list(csv.DictReader(f))


def number(value):
    if value is None:
        return None

    value = str(value).strip()

    if not value:
        return None

    try:
        return float(value)
    except ValueError:
        return None


def clean_pairs(rows, gt_col, ocr_col):
    pairs = []

    for row in rows:
        gt = number(row.get(gt_col))
        ocr = number(row.get(ocr_col))

        if gt is not None and ocr is not None:
            pairs.append((gt, ocr))

    return pairs


def mean(values):
    return statistics.mean(values) if values else None


def median(values):
    return statistics.median(values) if values else None


def std(values):
    if len(values) < 2:
        return None
    return statistics.stdev(values)


def fmt(value, digits=6):
    if value is None:
        return "N/A"
    return f"{value:.{digits}f}"


# ============================================================
# LOAD
# ============================================================

rows = read_csv(INPUT)

print("=" * 70)
print("EXPERIMENT 3B — STATISTICAL ANALYSIS")
print("=" * 70)

print()
print(f"Input rows: {len(rows)}")


# ============================================================
# METRICS
# ============================================================

metrics = [
    (
        "Numeric preservation",
        "gt_numeric_preservation",
        "ocr_numeric_preservation",
    ),
    (
        "Lexical overlap",
        "gt_lexical_overlap",
        "ocr_lexical_overlap",
    ),
    (
        "Section completion",
        "gt_section_completion_rate",
        "ocr_section_completion_rate",
    ),
]


results = []


# ============================================================
# WILCOXON ANALYSIS
# ============================================================

for metric_name, gt_col, ocr_col in metrics:

    pairs = clean_pairs(
        rows,
        gt_col,
        ocr_col
    )

    gt = [p[0] for p in pairs]
    ocr = [p[1] for p in pairs]

    differences = [
        a - b
        for a, b in pairs
    ]

    nonzero = [
        d
        for d in differences
        if d != 0
    ]

    n = len(pairs)
    n_nonzero = len(nonzero)

    if n_nonzero == 0:

        statistic = 0.0
        p_value = 1.0

    else:

        test = wilcoxon(
            gt,
            ocr,
            alternative="two-sided",
            zero_method="wilcox",
            method="auto"
        )

        statistic = float(
            test.statistic
        )

        p_value = float(
            test.pvalue
        )

    mean_gt = mean(gt)
    mean_ocr = mean(ocr)

    median_gt = median(gt)
    median_ocr = median(ocr)

    mean_diff = mean(differences)
    median_diff = median(differences)

    sd_diff = std(differences)

    # Rank-biserial effect size
    #
    # r_rb = (W_plus - W_minus) / total_rank_sum
    #
    # Calculate using absolute ranks with average ranks for ties.

    if n_nonzero == 0:

        rank_biserial = 0.0

    else:

        abs_diffs = [
            abs(d)
            for d in nonzero
        ]

        indexed = sorted(
            enumerate(abs_diffs),
            key=lambda x: x[1]
        )

        ranks = [0.0] * len(
            indexed
        )

        i = 0

        while i < len(indexed):

            j = i

            while (
                j + 1 < len(indexed)
                and indexed[j + 1][1]
                == indexed[i][1]
            ):
                j += 1

            average_rank = (
                (i + 1) + (j + 1)
            ) / 2.0

            for k in range(i, j + 1):
                original_index = indexed[k][0]
                ranks[original_index] = (
                    average_rank
                )

            i = j + 1

        positive_rank_sum = sum(
            rank
            for rank, diff in zip(
                ranks,
                nonzero
            )
            if diff > 0
        )

        negative_rank_sum = sum(
            rank
            for rank, diff in zip(
                ranks,
                nonzero
            )
            if diff < 0
        )

        denominator = (
            positive_rank_sum
            + negative_rank_sum
        )

        if denominator == 0:
            rank_biserial = 0.0
        else:
            rank_biserial = (
                positive_rank_sum
                - negative_rank_sum
            ) / denominator

    significant = (
        p_value < 0.05
    )

    results.append({

        "metric": metric_name,

        "n": n,

        "n_nonzero_difference":
            n_nonzero,

        "gt_mean":
            mean_gt,

        "ocr_mean":
            mean_ocr,

        "gt_median":
            median_gt,

        "ocr_median":
            median_ocr,

        "mean_difference_gt_minus_ocr":
            mean_diff,

        "median_difference_gt_minus_ocr":
            median_diff,

        "difference_sd":
            sd_diff,

        "wilcoxon_statistic":
            statistic,

        "wilcoxon_p_value":
            p_value,

        "rank_biserial_effect_size":
            rank_biserial,

        "significant_at_0_05":
            significant,
    })


# ============================================================
# SUBSET ANALYSIS
# ============================================================

subset_results = []

subsets = sorted(
    set(
        str(r.get("subset", "")).strip()
        for r in rows
        if r.get("subset")
    )
)


for subset in subsets:

    subset_rows = [
        r for r in rows
        if str(r.get("subset", "")).strip()
        == subset
    ]

    for metric_name, gt_col, ocr_col in metrics:

        pairs = clean_pairs(
            subset_rows,
            gt_col,
            ocr_col
        )

        if not pairs:
            continue

        gt = [p[0] for p in pairs]
        ocr = [p[1] for p in pairs]

        differences = [
            a - b
            for a, b in pairs
        ]

        nonzero = [
            d for d in differences
            if d != 0
        ]

        if len(nonzero) == 0:

            statistic = 0.0
            p_value = 1.0

        else:

            test = wilcoxon(
                gt,
                ocr,
                alternative="two-sided",
                zero_method="wilcox",
                method="auto"
            )

            statistic = float(
                test.statistic
            )

            p_value = float(
                test.pvalue
            )

        subset_results.append({

            "subset": subset,

            "metric": metric_name,

            "n": len(pairs),

            "gt_mean":
                mean(gt),

            "ocr_mean":
                mean(ocr),

            "mean_difference":
                mean(differences),

            "gt_median":
                median(gt),

            "ocr_median":
                median(ocr),

            "median_difference":
                median(differences),

            "wilcoxon_statistic":
                statistic,

            "wilcoxon_p_value":
                p_value,

            "significant_at_0_05":
                p_value < 0.05,
        })


# ============================================================
# WRITE OVERALL CSV
# ============================================================

with OUTPUT_CSV.open(
    "w",
    encoding="utf-8",
    newline=""
) as f:

    fieldnames = list(
        results[0].keys()
    )

    writer = csv.DictWriter(
        f,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(results)


# ============================================================
# WRITE SUBSET CSV
# ============================================================

with OUTPUT_SUBSET_CSV.open(
    "w",
    encoding="utf-8",
    newline=""
) as f:

    fieldnames = list(
        subset_results[0].keys()
    )

    writer = csv.DictWriter(
        f,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(subset_results)


# ============================================================
# WRITE TEXT SUMMARY
# ============================================================

with OUTPUT_TXT.open(
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "MEDINOVA AI — EXPERIMENT 3B "
        "STATISTICAL ANALYSIS\n"
    )

    f.write("=" * 72 + "\n\n")

    f.write(
        "Design: paired comparison of GT-text and OCR-text "
        "conditions for the same documents.\n"
    )

    f.write(
        "Test: two-sided Wilcoxon signed-rank test.\n"
    )

    f.write(
        "Significance threshold: alpha = 0.05.\n"
    )

    f.write(
        "Effect size: rank-biserial correlation.\n\n"
    )

    for result in results:

        f.write(
            f"METRIC: {result['metric']}\n"
        )

        f.write("-" * 72 + "\n")

        f.write(
            f"N: {result['n']}\n"
        )

        f.write(
            f"Non-zero paired differences: "
            f"{result['n_nonzero_difference']}\n"
        )

        f.write(
            f"GT mean: "
            f"{fmt(result['gt_mean'])}\n"
        )

        f.write(
            f"OCR mean: "
            f"{fmt(result['ocr_mean'])}\n"
        )

        f.write(
            f"GT median: "
            f"{fmt(result['gt_median'])}\n"
        )

        f.write(
            f"OCR median: "
            f"{fmt(result['ocr_median'])}\n"
        )

        f.write(
            f"Mean difference (GT - OCR): "
            f"{fmt(result['mean_difference_gt_minus_ocr'])}\n"
        )

        f.write(
            f"Median difference (GT - OCR): "
            f"{fmt(result['median_difference_gt_minus_ocr'])}\n"
        )

        f.write(
            f"Difference SD: "
            f"{fmt(result['difference_sd'])}\n"
        )

        f.write(
            f"Wilcoxon statistic: "
            f"{fmt(result['wilcoxon_statistic'])}\n"
        )

        f.write(
            f"Wilcoxon p-value: "
            f"{fmt(result['wilcoxon_p_value'])}\n"
        )

        f.write(
            f"Rank-biserial effect size: "
            f"{fmt(result['rank_biserial_effect_size'])}\n"
        )

        f.write(
            f"Significant at alpha=0.05: "
            f"{result['significant_at_0_05']}\n\n"
        )


    f.write(
        "IMPORTANT INTERPRETATION NOTES\n"
    )

    f.write("-" * 72 + "\n")

    f.write(
        "1. Experiment 3B metrics are automatic proxy metrics.\n"
    )

    f.write(
        "2. They are not clinical expert factuality scores.\n"
    )

    f.write(
        "3. Statistical significance does not establish causality.\n"
    )

    f.write(
        "4. Section completion measures structural output behaviour, "
        "not clinical correctness.\n"
    )

    f.write(
        "5. Results should be interpreted together with the OCR "
        "and clinical-information experiments.\n"
    )


# ============================================================
# TERMINAL OUTPUT
# ============================================================

print()
print("=" * 70)
print("OVERALL STATISTICAL RESULTS")
print("=" * 70)

for result in results:

    print()
    print(
        f"{result['metric']}"
    )

    print(
        f"  N                    : "
        f"{result['n']}"
    )

    print(
        f"  GT mean              : "
        f"{fmt(result['gt_mean'])}"
    )

    print(
        f"  OCR mean             : "
        f"{fmt(result['ocr_mean'])}"
    )

    print(
        f"  Mean difference      : "
        f"{fmt(result['mean_difference_gt_minus_ocr'])}"
    )

    print(
        f"  Wilcoxon statistic   : "
        f"{fmt(result['wilcoxon_statistic'])}"
    )

    print(
        f"  Wilcoxon p-value     : "
        f"{fmt(result['wilcoxon_p_value'])}"
    )

    print(
        f"  Rank-biserial effect : "
        f"{fmt(result['rank_biserial_effect_size'])}"
    )

    print(
        f"  Significant (0.05)   : "
        f"{result['significant_at_0_05']}"
    )


print()
print("=" * 70)
print("FILES CREATED")
print("=" * 70)

print()
print(OUTPUT_CSV)
print(OUTPUT_SUBSET_CSV)
print(OUTPUT_TXT)

print()
print("=" * 70)