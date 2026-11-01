import asyncio
import csv
import json
import sys
import time
from pathlib import Path
from collections import defaultdict

# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

MANIFEST_PATH = PROJECT_ROOT / "experiments" / "clinocr_bench_manifest.csv"

OUTPUT_DIR = PROJECT_ROOT / "experiments" / "results"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PER_DOCUMENT_CSV = OUTPUT_DIR / "clinocr_ocr_per_document.csv"
SUMMARY_JSON = OUTPUT_DIR / "clinocr_ocr_summary.json"
OCR_TEXT_DIR = OUTPUT_DIR / "ocr_text"
OCR_TEXT_DIR.mkdir(parents=True, exist_ok=True)

# ClinOCR-Bench root
DATASET_ROOT = Path(
    r"C:\Users\vasuk\Downloads\ClinOCR-Bench-v1.0\ClinOCR-Bench"
)

# ---------------------------------------------------------
# Import MediNova OCR service
# ---------------------------------------------------------

BACKEND_DIR = PROJECT_ROOT / "backend"
OCR_SERVICE_FILE = (
    BACKEND_DIR
    / "app"
    / "services"
    / "ocr_service.py"
)

import importlib.util

spec = importlib.util.spec_from_file_location(
    "medinova_ocr_service",
    OCR_SERVICE_FILE
)

if spec is None or spec.loader is None:
    raise ImportError(
        f"Could not load OCR service from: {OCR_SERVICE_FILE}"
    )

ocr_module = importlib.util.module_from_spec(spec)

spec.loader.exec_module(ocr_module)

OCRService = ocr_module.OCRService


# ---------------------------------------------------------
# Text normalization
# ---------------------------------------------------------

def normalize_for_metric(text: str) -> str:
    """
    Minimal normalization used only for the secondary metric.

    Primary CER/WER will use raw text after normalizing
    line endings to avoid Windows CRLF differences.
    """
    return text.replace("\r\n", "\n").replace("\r", "\n")


def normalize_secondary(text: str) -> str:
    """
    Conservative secondary normalization:
    - normalize line endings
    - collapse repeated whitespace
    - strip leading/trailing whitespace

    This is NOT used for the primary raw CER/WER.
    """
    import re

    text = normalize_for_metric(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ---------------------------------------------------------
# Edit distance
# ---------------------------------------------------------

def levenshtein_distance(a, b):
    """
    Standard Levenshtein edit distance.
    """
    if a == b:
        return 0

    if len(a) < len(b):
        a, b = b, a

    previous = list(range(len(b) + 1))

    for i, char_a in enumerate(a, start=1):
        current = [i]

        for j, char_b in enumerate(b, start=1):
            insert_cost = current[j - 1] + 1
            delete_cost = previous[j] + 1
            substitute_cost = previous[j - 1] + (char_a != char_b)

            current.append(
                min(insert_cost, delete_cost, substitute_cost)
            )

        previous = current

    return previous[-1]


# ---------------------------------------------------------
# CER
# ---------------------------------------------------------

def calculate_cer(reference: str, hypothesis: str):
    """
    Character Error Rate:

        CER = edit_distance / number_of_reference_characters
    """
    reference = normalize_for_metric(reference)
    hypothesis = normalize_for_metric(hypothesis)

    if len(reference) == 0:
        return 0.0 if len(hypothesis) == 0 else None

    distance = levenshtein_distance(reference, hypothesis)

    return distance / len(reference)


# ---------------------------------------------------------
# WER
# ---------------------------------------------------------

def calculate_wer(reference: str, hypothesis: str):
    """
    Word Error Rate:

        WER = edit_distance / number_of_reference_words
    """
    reference = normalize_for_metric(reference)
    hypothesis = normalize_for_metric(hypothesis)

    ref_words = reference.split()
    hyp_words = hypothesis.split()

    if len(ref_words) == 0:
        return 0.0 if len(hyp_words) == 0 else None

    distance = levenshtein_distance(ref_words, hyp_words)

    return distance / len(ref_words)


# ---------------------------------------------------------
# Main evaluation
# ---------------------------------------------------------

async def main():

    print()
    print("=" * 72)
    print("MediNova - ClinOCR-Bench OCR Evaluation")
    print("=" * 72)

    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(
            f"Manifest not found: {MANIFEST_PATH}"
        )

    # -----------------------------------------------------
    # Load evaluation rows
    # -----------------------------------------------------

    rows = []

    with MANIFEST_PATH.open(
        "r",
        encoding="utf-8",
        newline=""
    ) as f:

        reader = csv.DictReader(f)

        for row in reader:
            if row["split"] == "eval":
                rows.append(row)

    print(f"Evaluation documents : {len(rows)}")

    if len(rows) != 328:
        raise RuntimeError(
            f"Expected 328 evaluation documents, found {len(rows)}"
        )

    # -----------------------------------------------------
    # Initialize existing MediNova OCR service
    # -----------------------------------------------------

    ocr_service = OCRService()

    print()
    print("OCR configuration:")
    print("  Engine       : EasyOCR")
    print("  Version      : 1.7.2")
    print("  Language     : English")
    print("  GPU          : False")
    print("  paragraph    : True")
    print("  Preprocessing: OpenCV grayscale + CLAHE + Gaussian")
    print("                 + adaptive Gaussian threshold")
    print()

    print("Starting evaluation...")
    print()

    results = []

    total_start = time.perf_counter()

    # -----------------------------------------------------
    # Process every evaluation document
    # -----------------------------------------------------

    for index, row in enumerate(rows, start=1):

        subset = row["subset"]
        template = int(row["template"])
        sample = int(row["sample"])

        image_path = Path(row["scan_path"])
        gt_path = Path(row["ground_truth_path"])

        # Safety check
        if not image_path.exists():
            print(
                f"[{index:03d}/328] MISSING IMAGE: {image_path}"
            )
            continue

        if not gt_path.exists():
            print(
                f"[{index:03d}/328] MISSING GT: {gt_path}"
            )
            continue

        # -------------------------------------------------
        # Read ground truth
        # -------------------------------------------------

        reference_text = gt_path.read_text(
            encoding="utf-8"
        )

        # -------------------------------------------------
        # Run MediNova OCR
        # -------------------------------------------------

        start = time.perf_counter()

        try:

            ocr_result = await ocr_service.extract_from_image(
                str(image_path)
            )

            elapsed = time.perf_counter() - start

            if ocr_result.get("success"):

                hypothesis_text = ocr_result.get(
                    "text",
                    ""
                )

                status = "success"
                error_message = ""

            else:

                hypothesis_text = ""

                status = "ocr_failed"

                error_message = ocr_result.get(
                    "error",
                    "Unknown OCR error"
                )

        except Exception as exc:

            elapsed = time.perf_counter() - start

            hypothesis_text = ""

            status = "exception"

            error_message = str(exc)

        # -------------------------------------------------
        # Metrics
        # -------------------------------------------------

        raw_cer = calculate_cer(
            reference_text,
            hypothesis_text
        )

        raw_wer = calculate_wer(
            reference_text,
            hypothesis_text
        )

        # Secondary normalized metrics
        normalized_reference = normalize_secondary(
            reference_text
        )

        normalized_hypothesis = normalize_secondary(
            hypothesis_text
        )

        normalized_cer = calculate_cer(
            normalized_reference,
            normalized_hypothesis
        )

        normalized_wer = calculate_wer(
            normalized_reference,
            normalized_hypothesis
        )

        # -------------------------------------------------
        # Save raw OCR output
        # -------------------------------------------------

        output_name = (
            f"{subset}_"
            f"template_{template}_"
            f"sample_{sample}.txt"
        )

        ocr_output_path = OCR_TEXT_DIR / output_name

        ocr_output_path.write_text(
            hypothesis_text,
            encoding="utf-8"
        )

        # -------------------------------------------------
        # Document result
        # -------------------------------------------------

        result = {
            "subset": subset,
            "template": template,
            "sample": sample,
            "split": row["split"],
            "image_path": str(image_path),
            "ground_truth_path": str(gt_path),
            "ocr_output_path": str(ocr_output_path),
            "status": status,
            "error": error_message,
            "runtime_seconds": round(elapsed, 4),
            "reference_characters": len(reference_text),
            "hypothesis_characters": len(hypothesis_text),
            "reference_words": len(reference_text.split()),
            "hypothesis_words": len(hypothesis_text.split()),
            "cer": raw_cer,
            "wer": raw_wer,
            "normalized_cer": normalized_cer,
            "normalized_wer": normalized_wer,
        }

        results.append(result)

        # -------------------------------------------------
        # Progress
        # -------------------------------------------------

        cer_display = (
            f"{raw_cer:.4f}"
            if raw_cer is not None
            else "N/A"
        )

        wer_display = (
            f"{raw_wer:.4f}"
            if raw_wer is not None
            else "N/A"
        )

        print(
            f"[{index:03d}/328] "
            f"{subset:12s} "
            f"T{template:02d} "
            f"S{sample:02d} "
            f"| CER={cer_display:>7} "
            f"| WER={wer_display:>7} "
            f"| {elapsed:6.2f}s "
            f"| {status}"
        )

    # -----------------------------------------------------
    # Total runtime
    # -----------------------------------------------------

    total_runtime = time.perf_counter() - total_start

    # -----------------------------------------------------
    # Save per-document CSV
    # -----------------------------------------------------

    fieldnames = [
        "subset",
        "template",
        "sample",
        "split",
        "image_path",
        "ground_truth_path",
        "ocr_output_path",
        "status",
        "error",
        "runtime_seconds",
        "reference_characters",
        "hypothesis_characters",
        "reference_words",
        "hypothesis_words",
        "cer",
        "wer",
        "normalized_cer",
        "normalized_wer",
    ]

    with PER_DOCUMENT_CSV.open(
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

    # -----------------------------------------------------
    # Aggregate metrics
    # -----------------------------------------------------

    def mean(values):

        values = [
            value
            for value in values
            if value is not None
        ]

        if not values:
            return None

        return sum(values) / len(values)

    # Overall
    successful = [
        r for r in results
        if r["status"] == "success"
    ]

    overall = {
        "documents_processed": len(results),
        "successful": len(successful),
        "failed": len(results) - len(successful),
        "mean_cer": mean(
            [r["cer"] for r in successful]
        ),
        "mean_wer": mean(
            [r["wer"] for r in successful]
        ),
        "mean_normalized_cer": mean(
            [r["normalized_cer"] for r in successful]
        ),
        "mean_normalized_wer": mean(
            [r["normalized_wer"] for r in successful]
        ),
        "mean_runtime_seconds": mean(
            [r["runtime_seconds"] for r in results]
        ),
        "total_runtime_seconds": total_runtime,
    }

    # -----------------------------------------------------
    # Subset metrics
    # -----------------------------------------------------

    subset_summary = {}

    for subset in sorted(
        set(r["subset"] for r in results)
    ):

        subset_results = [
            r for r in results
            if r["subset"] == subset
        ]

        subset_successful = [
            r for r in subset_results
            if r["status"] == "success"
        ]

        subset_summary[subset] = {
            "documents": len(subset_results),
            "successful": len(subset_successful),
            "failed": (
                len(subset_results)
                - len(subset_successful)
            ),
            "mean_cer": mean(
                [r["cer"] for r in subset_successful]
            ),
            "mean_wer": mean(
                [r["wer"] for r in subset_successful]
            ),
            "mean_normalized_cer": mean(
                [
                    r["normalized_cer"]
                    for r in subset_successful
                ]
            ),
            "mean_normalized_wer": mean(
                [
                    r["normalized_wer"]
                    for r in subset_successful
                ]
            ),
            "mean_runtime_seconds": mean(
                [
                    r["runtime_seconds"]
                    for r in subset_results
                ]
            ),
        }

    # -----------------------------------------------------
    # Experiment metadata
    # -----------------------------------------------------

    summary = {
        "experiment": {
            "name": "MediNova ClinOCR-Bench OCR Baseline",
            "dataset": "ClinOCR-Bench",
            "evaluation_documents": 328,
            "exemplars_excluded": 56,
            "total_documents": 384,
        },

        "ocr_configuration": {
            "engine": "EasyOCR",
            "version": "1.7.2",
            "language": ["en"],
            "gpu": False,
            "paragraph": True,
            "preprocessing": {
                "grayscale": True,
                "clahe": {
                    "clipLimit": 2.0,
                    "tileGridSize": [8, 8],
                },
                "gaussian_blur": {
                    "kernel": [3, 3],
                    "sigma": 0,
                },
                "adaptive_threshold": {
                    "method": "ADAPTIVE_THRESH_GAUSSIAN_C",
                    "threshold_type": "THRESH_BINARY",
                    "blockSize": 11,
                    "C": 2,
                },
            },
        },

        "software_environment": {
            "opencv": "5.0.0",
            "numpy": "2.5.1",
        },

        "metrics": {
            "primary": [
                "CER",
                "WER",
            ],
            "secondary": [
                "normalized_CER",
                "normalized_WER",
            ],
        },

        "overall": overall,

        "by_subset": subset_summary,
    }

    with SUMMARY_JSON.open(
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            summary,
            f,
            indent=2,
            ensure_ascii=False
        )

    # -----------------------------------------------------
    # Final console report
    # -----------------------------------------------------

    print()
    print("=" * 72)
    print("EVALUATION COMPLETE")
    print("=" * 72)

    print(
        f"Documents processed : {len(results)}"
    )

    print(
        f"Successful          : {len(successful)}"
    )

    print(
        f"Failed              : "
        f"{len(results) - len(successful)}"
    )

    print()

    print(
        f"Mean CER            : "
        f"{overall['mean_cer']:.6f}"
        if overall["mean_cer"] is not None
        else "Mean CER            : N/A"
    )

    print(
        f"Mean WER            : "
        f"{overall['mean_wer']:.6f}"
        if overall["mean_wer"] is not None
        else "Mean WER            : N/A"
    )

    print()

    print("Subset results:")
    print("-" * 72)

    for subset, data in subset_summary.items():

        cer = data["mean_cer"]
        wer = data["mean_wer"]

        cer_text = (
            f"{cer:.6f}"
            if cer is not None
            else "N/A"
        )

        wer_text = (
            f"{wer:.6f}"
            if wer is not None
            else "N/A"
        )

        print(
            f"{subset:12s} "
            f"| N={data['documents']:3d} "
            f"| CER={cer_text:>10} "
            f"| WER={wer_text:>10}"
        )

    print()
    print(
        f"Total runtime       : "
        f"{total_runtime:.2f} seconds"
    )

    print()
    print(
        f"Per-document CSV    : {PER_DOCUMENT_CSV}"
    )

    print(
        f"Summary JSON         : {SUMMARY_JSON}"
    )

    print(
        f"OCR text directory   : {OCR_TEXT_DIR}"
    )

    print("=" * 72)


if __name__ == "__main__":
    asyncio.run(main())
