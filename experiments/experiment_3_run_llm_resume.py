import os
import csv
import time
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv
from google import genai
from google.genai import types


# ============================================================
# CONFIG
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

MANIFEST_PATH = (
    PROJECT_ROOT
    / "experiments"
    / "results"
    / "experiment_3"
    / "experiment_3_pilot_manifest.csv"
)

RESULTS_DIR = (
    PROJECT_ROOT
    / "experiments"
    / "results"
    / "experiment_3"
)

RESULTS_CSV = RESULTS_DIR / "experiment_3_llm_results.csv"

RAW_DIR = RESULTS_DIR / "raw_outputs"

MODEL = "gemini-3.6-flash"

TEMPERATURE = 0.0
MAX_OUTPUT_TOKENS = 1024
INPUT_CHAR_LIMIT = 8000

PROMPT_VERSION = "E3_PROMPT_V1"

# Delay between requests
REQUEST_DELAY_SECONDS = 1.0

# Retry transient 503 errors
MAX_503_RETRIES = 2

# Retry empty model responses
MAX_EMPTY_RETRIES = 2


CSV_COLUMNS = [
    "pilot_id",
    "subset",
    "template",
    "sample",
    "condition",
    "model",
    "temperature",
    "max_output_tokens",
    "prompt_version",
    "input_char_limit",
    "input_characters",
    "status",
    "error",
    "output_path",
    "timestamp",
]


# ============================================================
# PROMPT
# ============================================================

PROMPT_TEMPLATE = """You are a medical information assistant helping a patient understand a medical report.

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
# ENVIRONMENT
# ============================================================

def initialize_gemini():

    env_path = PROJECT_ROOT / "backend" / ".env"

    if env_path.exists():
        load_dotenv(env_path)

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY not found in backend/.env"
        )

    return genai.Client(api_key=api_key)


# ============================================================
# FILE HELPERS
# ============================================================

def read_text(path):

    path = Path(path)

    with open(
        path,
        "r",
        encoding="utf-8",
        errors="replace"
    ) as f:
        return f.read()


def ensure_directories():

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    RAW_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


# ============================================================
# EXISTING RESULT HANDLING
# ============================================================

def load_existing_results():

    existing = {}

    if not RESULTS_CSV.exists():
        return existing

    print()
    print("Existing results found:")
    print(RESULTS_CSV)

    with open(
        RESULTS_CSV,
        "r",
        encoding="utf-8",
        newline=""
    ) as f:

        reader = csv.DictReader(f)

        for row in reader:

            pilot_id = row.get(
                "pilot_id",
                ""
            ).strip()

            condition = row.get(
                "condition",
                ""
            ).strip()

            if pilot_id and condition:

                key = (
                    pilot_id,
                    condition
                )

                # Keep latest row if duplicates exist
                existing[key] = row

    print(
        f"Loaded {len(existing)} existing condition results."
    )

    return existing


def save_results(existing):

    rows = list(existing.values())

    # Stable ordering
    rows.sort(
        key=lambda r: (
            r.get("pilot_id", ""),
            r.get("condition", "")
        )
    )

    temp_path = RESULTS_CSV.with_suffix(".tmp")

    with open(
        temp_path,
        "w",
        encoding="utf-8",
        newline=""
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=CSV_COLUMNS
        )

        writer.writeheader()

        for row in rows:

            clean_row = {
                column: row.get(column, "")
                for column in CSV_COLUMNS
            }

            writer.writerow(clean_row)

    # Atomic replacement
    temp_path.replace(RESULTS_CSV)


# ============================================================
# MANIFEST
# ============================================================

def load_manifest():

    if not MANIFEST_PATH.exists():

        raise FileNotFoundError(
            f"Manifest not found:\n{MANIFEST_PATH}"
        )

    with open(
        MANIFEST_PATH,
        "r",
        encoding="utf-8",
        newline=""
    ) as f:

        return list(csv.DictReader(f))


# ============================================================
# GEMINI REQUEST
# ============================================================

def generate_output(
    client,
    report_text
):

    prompt = PROMPT_TEMPLATE.format(
        report_text=report_text
    )

    config = types.GenerateContentConfig(
        temperature=TEMPERATURE,
        max_output_tokens=MAX_OUTPUT_TOKENS,
    )

    empty_attempts = 0

    for attempt in range(MAX_503_RETRIES + 1):

        try:

            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=config,
            )

            output = getattr(
                response,
                "text",
                None
            )

            # ====================================================
            # VALID NON-EMPTY RESPONSE
            # ====================================================

            if output is not None and output.strip():

                return {
                    "status": "success",
                    "output": output,
                    "error": "",
                }

            # ====================================================
            # EMPTY RESPONSE
            # ====================================================

            empty_attempts += 1

            if empty_attempts <= MAX_EMPTY_RETRIES:

                wait_seconds = 2 * empty_attempts

                print(
                    f"      Empty Gemini response. "
                    f"Retrying in {wait_seconds}s "
                    f"({empty_attempts}/{MAX_EMPTY_RETRIES})..."
                )

                time.sleep(wait_seconds)

                continue

            return {
                "status": "empty_output",
                "output": "",
                "error": (
                    "Gemini returned an empty response "
                    f"after {MAX_EMPTY_RETRIES + 1} attempts"
                ),
            }

        except Exception as e:

            error_text = str(e)

            # ====================================================
            # QUOTA / RATE LIMIT
            # ====================================================

            if (
                "429" in error_text
                or "RESOURCE_EXHAUSTED" in error_text
            ):

                return {
                    "status": "quota_exceeded",
                    "output": "",
                    "error": error_text,
                }

            # ====================================================
            # TEMPORARY SERVER ERROR
            # ====================================================

            if (
                "503" in error_text
                or "UNAVAILABLE" in error_text
            ):

                if attempt < MAX_503_RETRIES:

                    wait_seconds = (
                        5 * (2 ** attempt)
                    )

                    print(
                        f"      503 temporary error. "
                        f"Retrying in {wait_seconds}s..."
                    )

                    time.sleep(wait_seconds)

                    continue

                return {
                    "status": "api_error",
                    "output": "",
                    "error": error_text,
                }

            # ====================================================
            # OTHER API ERROR
            # ====================================================

            return {
                "status": "api_error",
                "output": "",
                "error": error_text,
            }

    return {
        "status": "api_error",
        "output": "",
        "error": "Unknown API error",
    }


# ============================================================
# CHECK EXISTING OUTPUT
# ============================================================

def existing_output_is_valid(previous):

    if not previous:
        return False

    previous_status = (
        previous.get(
            "status",
            ""
        )
        .strip()
        .lower()
    )

    previous_output_path = (
        previous.get(
            "output_path",
            ""
        )
        .strip()
    )

    # Must be marked success
    if previous_status != "success":
        return False

    # Must have an output path
    if not previous_output_path:
        return False

    output_file = Path(
        previous_output_path
    )

    # File must exist
    if not output_file.exists():
        return False

    # File must not be empty
    if output_file.stat().st_size <= 0:
        return False

    try:

        output_text = read_text(
            output_file
        )

    except Exception:
        return False

    # File must contain actual text
    if not output_text.strip():
        return False

    return True


# ============================================================
# PROCESS ONE CONDITION
# ============================================================

def process_condition(
    client,
    row,
    condition,
    input_path,
    existing,
):

    pilot_id = row["pilot_id"]

    key = (
        pilot_id,
        condition
    )

    # --------------------------------------------------------
    # RESUME CHECK
    # --------------------------------------------------------

    previous = existing.get(key)

    if previous:

        if existing_output_is_valid(previous):

            print(
                f"    SKIP {condition.upper()} "
                f"(already successful)"
            )

            return "skipped"

        else:

            print(
                f"    RETRY {condition.upper()} "
                f"(previous output missing, empty, "
                f"or invalid)"
            )

    # --------------------------------------------------------
    # READ INPUT
    # --------------------------------------------------------

    try:

        report_text = read_text(
            input_path
        )

    except Exception as e:

        result = {
            "pilot_id": pilot_id,
            "subset": row.get(
                "subset",
                ""
            ),
            "template": row.get(
                "template",
                ""
            ),
            "sample": row.get(
                "sample",
                ""
            ),
            "condition": condition,
            "model": MODEL,
            "temperature": TEMPERATURE,
            "max_output_tokens": MAX_OUTPUT_TOKENS,
            "prompt_version": PROMPT_VERSION,
            "input_char_limit": INPUT_CHAR_LIMIT,
            "input_characters": "",
            "status": "input_error",
            "error": str(e),
            "output_path": "",
            "timestamp": datetime.now().isoformat(),
        }

        existing[key] = result

        save_results(existing)

        return "input_error"

    # --------------------------------------------------------
    # INPUT CHARACTER LIMIT
    # --------------------------------------------------------

    report_text = report_text[
        :INPUT_CHAR_LIMIT
    ]

    print(
        f"    Running {condition.upper()} "
        f"({len(report_text)} chars)..."
    )

    # --------------------------------------------------------
    # API REQUEST
    # --------------------------------------------------------

    result = generate_output(
        client,
        report_text
    )

    timestamp = datetime.now().isoformat()

    # --------------------------------------------------------
    # QUOTA EXCEEDED
    # --------------------------------------------------------

    if result["status"] == "quota_exceeded":

        print()
        print("=" * 70)
        print("GEMINI QUOTA EXCEEDED")
        print("=" * 70)
        print(
            "The experiment will STOP immediately."
        )
        print(
            "Existing successful results have been preserved."
        )
        print("=" * 70)

        return "quota_exceeded"

    # --------------------------------------------------------
    # SAVE RAW OUTPUT
    # --------------------------------------------------------

    output_path = ""

    if result["status"] == "success":

        output_filename = (
            f"{pilot_id}_{condition}_gemini.txt"
        )

        output_file = (
            RAW_DIR / output_filename
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                result["output"]
            )

        output_path = str(
            output_file
        )

        print(
            f"      SUCCESS "
            f"({len(result['output'])} chars)"
        )

    elif result["status"] == "empty_output":

        print(
            f"      EMPTY OUTPUT: "
            f"{result['error']}"
        )

    else:

        print(
            f"      ERROR: "
            f"{result['error'][:300]}"
        )

    # --------------------------------------------------------
    # SAVE RESULT
    # --------------------------------------------------------

    result_row = {
        "pilot_id": pilot_id,
        "subset": row.get(
            "subset",
            ""
        ),
        "template": row.get(
            "template",
            ""
        ),
        "sample": row.get(
            "sample",
            ""
        ),
        "condition": condition,
        "model": MODEL,
        "temperature": TEMPERATURE,
        "max_output_tokens": MAX_OUTPUT_TOKENS,
        "prompt_version": PROMPT_VERSION,
        "input_char_limit": INPUT_CHAR_LIMIT,
        "input_characters": len(
            report_text
        ),
        "status": result["status"],
        "error": result["error"],
        "output_path": output_path,
        "timestamp": timestamp,
    }

    existing[key] = result_row

    # Save after every request
    save_results(existing)

    return result["status"]


# ============================================================
# COUNT RESULTS
# ============================================================

def count_statuses(existing):

    counts = {
        "gt_success": 0,
        "ocr_success": 0,
        "gt_empty": 0,
        "ocr_empty": 0,
        "gt_error": 0,
        "ocr_error": 0,
    }

    for row in existing.values():

        condition = (
            row.get(
                "condition",
                ""
            )
            .strip()
            .lower()
        )

        status = (
            row.get(
                "status",
                ""
            )
            .strip()
            .lower()
        )

        if condition == "gt":

            if status == "success":
                counts["gt_success"] += 1

            elif status == "empty_output":
                counts["gt_empty"] += 1

            else:
                counts["gt_error"] += 1

        elif condition == "ocr":

            if status == "success":
                counts["ocr_success"] += 1

            elif status == "empty_output":
                counts["ocr_empty"] += 1

            else:
                counts["ocr_error"] += 1

    return counts


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("EXPERIMENT 3A — RESUME LLM EVALUATION")
    print("=" * 70)

    print(f"Model: {MODEL}")
    print(f"Temperature: {TEMPERATURE}")
    print(
        f"Max output tokens: "
        f"{MAX_OUTPUT_TOKENS}"
    )
    print(
        f"Prompt version: "
        f"{PROMPT_VERSION}"
    )
    print(
        f"Input char limit: "
        f"{INPUT_CHAR_LIMIT}"
    )

    print()

    ensure_directories()

    manifest = load_manifest()

    print(
        f"Manifest rows: "
        f"{len(manifest)}"
    )

    existing = load_existing_results()

    # --------------------------------------------------------
    # COUNTS BEFORE
    # --------------------------------------------------------

    before = count_statuses(
        existing
    )

    print()

    print(
        "Current stored status:"
    )

    print(
        f"GT  : success={before['gt_success']}, "
        f"empty={before['gt_empty']}, "
        f"error={before['gt_error']}"
    )

    print(
        f"OCR : success={before['ocr_success']}, "
        f"empty={before['ocr_empty']}, "
        f"error={before['ocr_error']}"
    )

    print()

    client = initialize_gemini()

    # --------------------------------------------------------
    # PROCESS DOCUMENTS
    # --------------------------------------------------------

    for index, row in enumerate(
        manifest,
        start=1
    ):

        pilot_id = row["pilot_id"]

        print(
            f"[{index}/{len(manifest)}] "
            f"{pilot_id}"
        )

        gt_path = row[
            "ground_truth_path"
        ]

        ocr_path = row[
            "ocr_output_path"
        ]

        # ====================================================
        # GT
        # ====================================================

        status = process_condition(
            client=client,
            row=row,
            condition="gt",
            input_path=gt_path,
            existing=existing,
        )

        if status == "quota_exceeded":

            print()
            print(
                "Experiment paused because "
                "quota was exceeded."
            )

            print(
                f"Progress saved to:\n"
                f"{RESULTS_CSV}"
            )

            return

        if status != "skipped":

            time.sleep(
                REQUEST_DELAY_SECONDS
            )

        # ====================================================
        # OCR
        # ====================================================

        status = process_condition(
            client=client,
            row=row,
            condition="ocr",
            input_path=ocr_path,
            existing=existing,
        )

        if status == "quota_exceeded":

            print()
            print(
                "Experiment paused because "
                "quota was exceeded."
            )

            print(
                f"Progress saved to:\n"
                f"{RESULTS_CSV}"
            )

            return

        if status != "skipped":

            time.sleep(
                REQUEST_DELAY_SECONDS
            )

    # --------------------------------------------------------
    # FINAL SUMMARY
    # --------------------------------------------------------

    final = count_statuses(
        existing
    )

    print()
    print("=" * 70)
    print("EXPERIMENT 3A RUN COMPLETE")
    print("=" * 70)

    print()
    print(
        f"GT successful : "
        f"{final['gt_success']}/{len(manifest)}"
    )

    print(
        f"OCR successful: "
        f"{final['ocr_success']}/{len(manifest)}"
    )

    print()
    print(
        f"GT empty outputs : "
        f"{final['gt_empty']}"
    )

    print(
        f"OCR empty outputs: "
        f"{final['ocr_empty']}"
    )

    print()
    print(
        f"GT errors : "
        f"{final['gt_error']}"
    )

    print(
        f"OCR errors: "
        f"{final['ocr_error']}"
    )

    total_success = (
        final["gt_success"]
        + final["ocr_success"]
    )

    total_expected = (
        len(manifest) * 2
    )

    print()
    print(
        f"Total valid non-empty outputs: "
        f"{total_success}/{total_expected}"
    )

    print()
    print(
        "Results CSV:"
    )

    print(
        RESULTS_CSV
    )

    print()
    print(
        "Raw outputs:"
    )

    print(
        RAW_DIR
    )

    print("=" * 70)

    # --------------------------------------------------------
    # FINAL VALIDATION
    # --------------------------------------------------------

    if (
        final["gt_success"]
        == len(manifest)
        and
        final["ocr_success"]
        == len(manifest)
        and
        final["gt_empty"] == 0
        and
        final["ocr_empty"] == 0
        and
        final["gt_error"] == 0
        and
        final["ocr_error"] == 0
    ):

        print()
        print(
            "FINAL VALIDATION: "
            "60/60 VALID NON-EMPTY OUTPUTS"
        )
        print(
            "Experiment 3A is ready for analysis."
        )
        print()

    else:

        incomplete = (
            total_expected
            - total_success
        )

        print()
        print(
            f"FINAL VALIDATION: "
            f"{total_success}/{total_expected} "
            f"valid outputs"
        )

        print(
            f"Remaining incomplete/error "
            f"conditions: {incomplete}"
        )

        print(
            "Run this script again after "
            "resolving the remaining API issues."
        )

        print()


if __name__ == "__main__":
    main()