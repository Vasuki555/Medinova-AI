"""
Experiment 3 - Pilot Dataset Selection

Purpose:
    Select a reproducible, stratified 30-document pilot set
    for the downstream LLM evaluation.

Design:
    6 document subsets x 5 documents = 30 documents

Subsets:
    normal
    handwriting
    poor
    rotated
    tables
    mixed

Selection:
    - eval split only
    - fixed random seed
    - random selection within each subset
    - preserves GT/OCR pairing
    - does not select based on CER/WER

Input:
    experiments/results/clinocr_ocr_per_document.csv

Output:
    experiments/results/experiment_3/
        experiment_3_pilot_manifest.csv
        experiment_3_pilot_summary.csv
"""

from pathlib import Path
import pandas as pd


# ============================================================
# Configuration
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_CSV = (
    PROJECT_ROOT
    / "experiments"
    / "results"
    / "clinocr_ocr_per_document.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "experiments"
    / "results"
    / "experiment_3"
)

SEED = 42
DOCUMENTS_PER_SUBSET = 5

SUBSETS = [
    "normal",
    "handwriting",
    "poor",
    "rotated",
    "tables",
    "mixed",
]


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 70)
    print("Experiment 3 - Pilot Dataset Selection")
    print("=" * 70)

    # --------------------------------------------------------
    # Check input
    # --------------------------------------------------------

    if not INPUT_CSV.exists():
        raise FileNotFoundError(
            f"Input CSV not found:\n{INPUT_CSV}"
        )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Load dataset
    # --------------------------------------------------------

    df = pd.read_csv(INPUT_CSV)

    print(f"\nInput file:")
    print(INPUT_CSV)

    print(f"\nTotal rows: {len(df)}")

    # --------------------------------------------------------
    # Validate required columns
    # --------------------------------------------------------

    required_columns = [
        "subset",
        "template",
        "sample",
        "split",
        "image_path",
        "ground_truth_path",
        "ocr_output_path",
        "status",
        "cer",
        "wer",
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing required columns:\n"
            + "\n".join(missing_columns)
        )

    # --------------------------------------------------------
    # Keep evaluation split only
    # --------------------------------------------------------

    eval_df = df[
        df["split"].astype(str).str.lower() == "eval"
    ].copy()

    print(f"Evaluation documents: {len(eval_df)}")

    # --------------------------------------------------------
    # Keep successful OCR results only
    # --------------------------------------------------------

    before_status_filter = len(eval_df)

    eval_df = eval_df[
        eval_df["status"].astype(str).str.lower() == "success"
    ].copy()

    print(
        f"Successful OCR documents: "
        f"{len(eval_df)} "
        f"(removed {before_status_filter - len(eval_df)})"
    )

    # --------------------------------------------------------
    # Validate subsets
    # --------------------------------------------------------

    available_subsets = sorted(
        eval_df["subset"].astype(str).str.lower().unique()
    )

    print("\nAvailable subsets:")
    for subset in available_subsets:
        count = (
            eval_df["subset"]
            .astype(str)
            .str.lower()
            .eq(subset)
            .sum()
        )
        print(f"  {subset:12s}: {count}")

    # --------------------------------------------------------
    # Stratified random sampling
    # --------------------------------------------------------

    selected_parts = []

    for subset in SUBSETS:

        subset_df = eval_df[
            eval_df["subset"]
            .astype(str)
            .str.lower()
            .eq(subset)
        ].copy()

        if len(subset_df) < DOCUMENTS_PER_SUBSET:
            raise ValueError(
                f"Subset '{subset}' has only "
                f"{len(subset_df)} documents, but "
                f"{DOCUMENTS_PER_SUBSET} are required."
            )

        selected = subset_df.sample(
            n=DOCUMENTS_PER_SUBSET,
            random_state=SEED
        ).copy()

        selected_parts.append(selected)

        print(
            f"\nSelected {DOCUMENTS_PER_SUBSET} "
            f"documents from '{subset}':"
        )

        for _, row in selected.iterrows():
            print(
                f"  template={int(row['template'])}, "
                f"sample={int(row['sample'])}, "
                f"CER={row['cer']:.6f}, "
                f"WER={row['wer']:.6f}"
            )

    # --------------------------------------------------------
    # Combine selected documents
    # --------------------------------------------------------

    pilot_df = pd.concat(
        selected_parts,
        ignore_index=True
    )

    # --------------------------------------------------------
    # Sort deterministically
    # --------------------------------------------------------

    subset_order = {
        subset: index
        for index, subset in enumerate(SUBSETS)
    }

    pilot_df["_subset_order"] = (
        pilot_df["subset"]
        .astype(str)
        .str.lower()
        .map(subset_order)
    )

    pilot_df = (
        pilot_df
        .sort_values(
            ["_subset_order", "template", "sample"]
        )
        .drop(columns=["_subset_order"])
        .reset_index(drop=True)
    )

    # --------------------------------------------------------
    # Add pilot identifiers
    # --------------------------------------------------------

    pilot_df.insert(
        0,
        "pilot_id",
        [
            f"E3P{i:03d}"
            for i in range(1, len(pilot_df) + 1)
        ]
    )

    pilot_df.insert(
        1,
        "selection_seed",
        SEED
    )

    # --------------------------------------------------------
    # Add explicit experiment condition information
    # --------------------------------------------------------

    pilot_df["condition_gt"] = "ground_truth_text"
    pilot_df["condition_ocr"] = "mediNova_ocr_text"

    # --------------------------------------------------------
    # Save manifest
    # --------------------------------------------------------

    manifest_path = (
        OUTPUT_DIR
        / "experiment_3_pilot_manifest.csv"
    )

    pilot_df.to_csv(
        manifest_path,
        index=False
    )

    # --------------------------------------------------------
    # Create summary
    # --------------------------------------------------------

    summary_rows = []

    for subset in SUBSETS:

        subset_selected = pilot_df[
            pilot_df["subset"]
            .astype(str)
            .str.lower()
            .eq(subset)
        ]

        summary_rows.append({
            "subset": subset,
            "selected_documents": len(subset_selected),
            "mean_cer": subset_selected["cer"].mean(),
            "mean_wer": subset_selected["wer"].mean(),
            "min_cer": subset_selected["cer"].min(),
            "max_cer": subset_selected["cer"].max(),
            "min_wer": subset_selected["wer"].min(),
            "max_wer": subset_selected["wer"].max(),
        })

    summary_df = pd.DataFrame(summary_rows)

    overall_row = pd.DataFrame([{
        "subset": "ALL",
        "selected_documents": len(pilot_df),
        "mean_cer": pilot_df["cer"].mean(),
        "mean_wer": pilot_df["wer"].mean(),
        "min_cer": pilot_df["cer"].min(),
        "max_cer": pilot_df["cer"].max(),
        "min_wer": pilot_df["wer"].min(),
        "max_wer": pilot_df["wer"].max(),
    }])

    summary_df = pd.concat(
        [summary_df, overall_row],
        ignore_index=True
    )

    summary_path = (
        OUTPUT_DIR
        / "experiment_3_pilot_summary.csv"
    )

    summary_df.to_csv(
        summary_path,
        index=False
    )

    # --------------------------------------------------------
    # Final validation
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("FINAL VALIDATION")
    print("=" * 70)

    print(f"Total pilot documents: {len(pilot_df)}")

    counts = (
        pilot_df["subset"]
        .value_counts()
        .reindex(SUBSETS)
    )

    print("\nDocuments per subset:")

    for subset, count in counts.items():
        print(f"  {subset:12s}: {count}")

    expected_total = (
        len(SUBSETS) * DOCUMENTS_PER_SUBSET
    )

    if len(pilot_df) != expected_total:
        raise RuntimeError(
            f"Expected {expected_total} documents, "
            f"but selected {len(pilot_df)}."
        )

    if counts.isna().any():
        raise RuntimeError(
            "One or more subsets are missing."
        )

    if (counts != DOCUMENTS_PER_SUBSET).any():
        raise RuntimeError(
            "Incorrect number of documents in one or more subsets."
        )

    # Check duplicate document identifiers
    duplicate_mask = pilot_df.duplicated(
        subset=["subset", "template", "sample"],
        keep=False
    )

    if duplicate_mask.any():
        print("\nWARNING: Duplicate document identifiers found:")
        print(
            pilot_df.loc[
                duplicate_mask,
                ["subset", "template", "sample"]
            ].to_string(index=False)
        )
        raise RuntimeError(
            "Duplicate documents detected."
        )

    print("\nNo duplicate documents detected.")

    # Check paired paths
    missing_gt = (
        pilot_df["ground_truth_path"]
        .isna()
        .sum()
    )

    missing_ocr = (
        pilot_df["ocr_output_path"]
        .isna()
        .sum()
    )

    print(f"Missing GT paths:  {missing_gt}")
    print(f"Missing OCR paths: {missing_ocr}")

    if missing_gt > 0 or missing_ocr > 0:
        raise RuntimeError(
            "Some selected documents are missing GT/OCR paths."
        )

    # --------------------------------------------------------
    # Print output locations
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("PILOT DATASET CREATED")
    print("=" * 70)

    print(f"\nManifest:")
    print(manifest_path)

    print(f"\nSummary:")
    print(summary_path)

    print("\nExperiment design:")
    print("  6 subsets")
    print("  5 documents per subset")
    print("  30 documents total")
    print("  Evaluation split only")
    print(f"  Random seed: {SEED}")
    print("  Selection based on random sampling, not CER/WER")

    print("\nNext step:")
    print(
        "Use experiment_3_pilot_manifest.csv "
        "to run the paired GT-vs-OCR Gemini experiment."
    )


if __name__ == "__main__":
    main()