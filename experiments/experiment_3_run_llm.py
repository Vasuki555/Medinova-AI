"""
Experiment 3A
============

Controlled evaluation of OCR-induced information loss on
LLM-generated patient-friendly medical report explanations.

Design
------
For every selected document:

Condition A:
    Ground Truth text -> Gemini

Condition B:
    MediNova OCR text -> Gemini

Both conditions use:
    - Same Gemini model
    - Same prompt
    - Same generation configuration
    - Same document
    - Same output structure

Pilot:
    30 documents
    6 subsets x 5 documents

Model:
    gemini-3.6-flash

SDK:
    google-genai

Outputs:
    experiments/results/experiment_3/
        llm_outputs/
            E3P001/
                ground_truth_output.txt
                ocr_output.txt
            ...
        experiment_3_llm_results.csv
        experiment_3_run_metadata.txt
"""

from pathlib import Path
import sys
import time
import json
from datetime import datetime, timezone

import pandas as pd


# ============================================================
# Project paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MANIFEST_PATH = (
    PROJECT_ROOT
    / "experiments"
    / "results"
    / "experiment_3"
    / "experiment_3_pilot_manifest.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "experiments"
    / "results"
    / "experiment_3"
    / "llm_outputs"
)

RESULTS_CSV = (
    PROJECT_ROOT
    / "experiments"
    / "results"
    / "experiment_3"
    / "experiment_3_llm_results.csv"
)

METADATA_FILE = (
    PROJECT_ROOT
    / "experiments"
    / "results"
    / "experiment_3"
    / "experiment_3_run_metadata.txt"
)


# ============================================================
# Experiment configuration
# ============================================================

MODEL_NAME = "gemini-3.6-flash"

TEMPERATURE = 0.0

MAX_OUTPUT_TOKENS = 1024

PROMPT_VERSION = "E3_PROMPT_V1"

MAX_INPUT_CHARACTERS = 8000

# IMPORTANT:
# We deliberately use the same 8000-character limit for both
# GT and OCR conditions so the only intended difference is
# the source text itself.
#
# This matches the current MediNova report-analysis behavior.


# ============================================================
# Locked experiment prompt
# ============================================================

EXPERIMENT_PROMPT = """
You are a medical information assistant helping a patient understand a medical report.

Use ONLY the information contained in the provided report text.

IMPORTANT RULES:
1. Do not invent, infer, or assume medical facts that are not explicitly stated.
2. Preserve diagnoses, findings, medications, numerical values, dates, units,
   measurements, and other clinically important details exactly as provided.
3. Do not change numerical values, medication names, or dosages.
4. If a value or statement is unclear in the provided text, explicitly state
   that it is unclear.
5. Do not provide a definitive diagnosis.
6. Explain the report in simple, patient-friendly language.

Use this structure:

1. Report Summary
2. Key Findings
3. Abnormal or Important Values
4. Plain-Language Explanation
5. Medications / Treatment Information
6. Information That Is Unclear or Missing

REPORT TEXT:
{report_text}
"""


# ============================================================
# Utility functions
# ============================================================

def read_text_file(path: str) -> str:
    """Read a UTF-8 text file safely."""

    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Text file not found: {file_path}"
        )

    return file_path.read_text(
        encoding="utf-8",
        errors="replace"
    )


def prepare_text(text: str) -> tuple[str, bool]:
    """
    Apply the same input character limit to both conditions.

    Returns:
        processed_text
        was_truncated
    """

    text = text.strip()

    if len(text) <= MAX_INPUT_CHARACTERS:
        return text, False

    return (
        text[:MAX_INPUT_CHARACTERS],
        True
    )


def build_prompt(text: str) -> str:
    return EXPERIMENT_PROMPT.format(
        report_text=text
    )


def save_text(path: Path, text: str):
    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    path.write_text(
        text,
        encoding="utf-8"
    )


# ============================================================
# Gemini client
# ============================================================

def initialize_gemini():

    from google import genai
    from google.genai import types
    import os
    from dotenv import load_dotenv

    # Load backend/.env directly.
    # This avoids loading MediNova's full Settings object,
    # which requires MongoDB/JWT configuration.
    backend_env = PROJECT_ROOT / "backend" / ".env"

    if not backend_env.exists():
        raise RuntimeError(
            f"Backend .env file not found:\n{backend_env}"
        )

    load_dotenv(
        dotenv_path=backend_env,
        override=False
    )

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured in backend/.env"
        )

    client = genai.Client(
        api_key=api_key
    )

    return client, types


# ============================================================
# Single Gemini generation
# ============================================================

def generate_explanation(
    client,
    types,
    text: str
):

    prompt = build_prompt(text)

    start = time.perf_counter()

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=TEMPERATURE,
            max_output_tokens=MAX_OUTPUT_TOKENS,
        ),
    )

    elapsed = time.perf_counter() - start

    output_text = response.text or ""

    return (
        output_text,
        elapsed,
        prompt
    )


# ============================================================
# Main experiment
# ============================================================

def main():

    print("=" * 75)
    print("Experiment 3A - GT vs MediNova OCR LLM Evaluation")
    print("=" * 75)

    # --------------------------------------------------------
    # Check manifest
    # --------------------------------------------------------

    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(
            f"Pilot manifest not found:\n{MANIFEST_PATH}"
        )

    manifest = pd.read_csv(
        MANIFEST_PATH
    )

    print(
        f"\nPilot manifest: {MANIFEST_PATH}"
    )

    print(
        f"Documents loaded: {len(manifest)}"
    )

    if len(manifest) != 30:
        raise ValueError(
            f"Expected 30 pilot documents, "
            f"found {len(manifest)}."
        )

    # --------------------------------------------------------
    # Validate columns
    # --------------------------------------------------------

    required_columns = [
        "pilot_id",
        "subset",
        "template",
        "sample",
        "ground_truth_path",
        "ocr_output_path",
        "cer",
        "wer",
    ]

    missing = [
        col
        for col in required_columns
        if col not in manifest.columns
    ]

    if missing:
        raise ValueError(
            "Manifest missing required columns:\n"
            + "\n".join(missing)
        )

    # --------------------------------------------------------
    # Initialize Gemini
    # --------------------------------------------------------

    print("\nInitializing Gemini client...")

    client, types = initialize_gemini()

    print(
        f"Gemini model: {MODEL_NAME}"
    )

    print(
        f"Temperature: {TEMPERATURE}"
    )

    print(
        f"Max output tokens: {MAX_OUTPUT_TOKENS}"
    )

    print(
        f"Prompt version: {PROMPT_VERSION}"
    )

    print(
        f"Input character limit: {MAX_INPUT_CHARACTERS}"
    )

    # --------------------------------------------------------
    # Prepare output directory
    # --------------------------------------------------------

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Metadata
    # --------------------------------------------------------

    run_start = datetime.now(
        timezone.utc
    ).isoformat()

    results = []

    # --------------------------------------------------------
    # Process documents
    # --------------------------------------------------------

    for index, row in manifest.iterrows():

        pilot_id = str(
            row["pilot_id"]
        )

        subset = str(
            row["subset"]
        )

        print("\n" + "-" * 75)

        print(
            f"[{index + 1}/30] "
            f"{pilot_id} | "
            f"{subset} | "
            f"template={row['template']} "
            f"sample={row['sample']}"
        )

        gt_path = str(
            row["ground_truth_path"]
        )

        ocr_path = str(
            row["ocr_output_path"]
        )

        document_output_dir = (
            OUTPUT_DIR
            / pilot_id
        )

        document_output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        # ----------------------------------------------------
        # Read GT
        # ----------------------------------------------------

        try:

            gt_raw = read_text_file(
                gt_path
            )

            gt_text, gt_truncated = prepare_text(
                gt_raw
            )

        except Exception as e:

            print(
                f"GT read error: {e}"
            )

            results.append({
                "pilot_id": pilot_id,
                "subset": subset,
                "template": row["template"],
                "sample": row["sample"],
                "condition": "ground_truth",
                "status": "input_error",
                "error": str(e),
            })

            continue

        # ----------------------------------------------------
        # Read OCR
        # ----------------------------------------------------

        try:

            ocr_raw = read_text_file(
                ocr_path
            )

            ocr_text, ocr_truncated = prepare_text(
                ocr_raw
            )

        except Exception as e:

            print(
                f"OCR read error: {e}"
            )

            results.append({
                "pilot_id": pilot_id,
                "subset": subset,
                "template": row["template"],
                "sample": row["sample"],
                "condition": "ocr",
                "status": "input_error",
                "error": str(e),
            })

            continue

        # ----------------------------------------------------
        # Save actual experiment inputs
        # ----------------------------------------------------

        save_text(
            document_output_dir
            / "ground_truth_input.txt",
            gt_text
        )

        save_text(
            document_output_dir
            / "ocr_input.txt",
            ocr_text
        )

        # ----------------------------------------------------
        # Ground Truth condition
        # ----------------------------------------------------

        print("  Running GT condition...")

        try:

            (
                gt_output,
                gt_latency,
                gt_prompt
            ) = generate_explanation(
                client,
                types,
                gt_text
            )

            save_text(
                document_output_dir
                / "ground_truth_output.txt",
                gt_output
            )

            save_text(
                document_output_dir
                / "ground_truth_prompt.txt",
                gt_prompt
            )

            print(
                f"  GT completed: "
                f"{gt_latency:.2f} sec"
            )

            gt_status = "success"
            gt_error = ""

        except Exception as e:

            print(
                f"  GT generation error: {e}"
            )

            gt_output = ""
            gt_latency = None
            gt_status = "api_error"
            gt_error = str(e)

        # ----------------------------------------------------
        # Small pause before second request
        # ----------------------------------------------------

        time.sleep(1.0)

        # ----------------------------------------------------
        # OCR condition
        # ----------------------------------------------------

        print("  Running OCR condition...")

        try:

            (
                ocr_output,
                ocr_latency,
                ocr_prompt
            ) = generate_explanation(
                client,
                types,
                ocr_text
            )

            save_text(
                document_output_dir
                / "ocr_output.txt",
                ocr_output
            )

            save_text(
                document_output_dir
                / "ocr_prompt.txt",
                ocr_prompt
            )

            print(
                f"  OCR completed: "
                f"{ocr_latency:.2f} sec"
            )

            ocr_status = "success"
            ocr_error = ""

        except Exception as e:

            print(
                f"  OCR generation error: {e}"
            )

            ocr_output = ""
            ocr_latency = None
            ocr_status = "api_error"
            ocr_error = str(e)

        # ----------------------------------------------------
        # Save paired result
        # ----------------------------------------------------

        results.append({

            "pilot_id": pilot_id,

            "subset": subset,

            "template": int(
                row["template"]
            ),

            "sample": int(
                row["sample"]
            ),

            "cer": float(
                row["cer"]
            ),

            "wer": float(
                row["wer"]
            ),

            "ground_truth_path": gt_path,

            "ocr_output_path": ocr_path,

            "gt_input_characters_raw": len(
                gt_raw
            ),

            "ocr_input_characters_raw": len(
                ocr_raw
            ),

            "gt_input_characters_used": len(
                gt_text
            ),

            "ocr_input_characters_used": len(
                ocr_text
            ),

            "gt_input_truncated": gt_truncated,

            "ocr_input_truncated": ocr_truncated,

            "gt_status": gt_status,

            "ocr_status": ocr_status,

            "gt_latency_seconds": gt_latency,

            "ocr_latency_seconds": ocr_latency,

            "gt_output_characters": len(
                gt_output
            ),

            "ocr_output_characters": len(
                ocr_output
            ),

            "gt_error": gt_error,

            "ocr_error": ocr_error,

            "model": MODEL_NAME,

            "temperature": TEMPERATURE,

            "max_output_tokens": MAX_OUTPUT_TOKENS,

            "prompt_version": PROMPT_VERSION,

            "experiment_timestamp_utc": datetime.now(
                timezone.utc
            ).isoformat(),

        })

        # ----------------------------------------------------
        # Save progress after every document
        # ----------------------------------------------------

        pd.DataFrame(
            results
        ).to_csv(
            RESULTS_CSV,
            index=False
        )

    # --------------------------------------------------------
    # Final metadata
    # --------------------------------------------------------

    run_end = datetime.now(
        timezone.utc
    ).isoformat()

    metadata = {
        "experiment": "Experiment 3A",
        "description": (
            "Controlled comparison of LLM-generated "
            "medical report explanations using "
            "ground-truth text versus MediNova OCR text."
        ),
        "model": MODEL_NAME,
        "temperature": TEMPERATURE,
        "max_output_tokens": MAX_OUTPUT_TOKENS,
        "prompt_version": PROMPT_VERSION,
        "max_input_characters": MAX_INPUT_CHARACTERS,
        "pilot_documents": len(manifest),
        "conditions": [
            "ground_truth",
            "ocr"
        ],
        "manifest": str(
            MANIFEST_PATH
        ),
        "run_start_utc": run_start,
        "run_end_utc": run_end,
        "sdk": "google-genai",
    }

    METADATA_FILE.write_text(
        json.dumps(
            metadata,
            indent=2
        ),
        encoding="utf-8"
    )

    # --------------------------------------------------------
    # Final summary
    # --------------------------------------------------------

    results_df = pd.DataFrame(
        results
    )

    print("\n" + "=" * 75)
    print("EXPERIMENT 3A COMPLETE")
    print("=" * 75)

    print(
        f"\nResult rows: {len(results_df)}"
    )

    if not results_df.empty:

        print("\nStatus summary:")

        if "gt_status" in results_df.columns:
            print(
                results_df[
                    "gt_status"
                ].value_counts()
            )

        if "ocr_status" in results_df.columns:
            print(
                results_df[
                    "ocr_status"
                ].value_counts()
            )

    print(
        f"\nResults CSV:\n{RESULTS_CSV}"
    )

    print(
        f"\nRaw outputs:\n{OUTPUT_DIR}"
    )

    print(
        f"\nMetadata:\n{METADATA_FILE}"
    )


if __name__ == "__main__":
    # Make backend/app importable.
    backend_dir = str(
        PROJECT_ROOT / "backend"
    )

    if backend_dir not in sys.path:
        sys.path.insert(
            0,
            backend_dir
        )

    main()