from pathlib import Path
import csv
import json
import zipfile


# ============================================================
# EXPERIMENT 3B — PREPARE LLM EVALUATION DATASET
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RESULTS_DIR = (
    PROJECT_ROOT
    / "experiments"
    / "results"
    / "experiment_3"
)

RAW_DIR = RESULTS_DIR / "raw_outputs"

LLM_CSV = RESULTS_DIR / "experiment_3_llm_results.csv"

GROUND_TRUTH_ZIP = (
    PROJECT_ROOT
    / "experiments"
    / "ground_truth.zip"
)

OCR_TEXT_ZIP = (
    PROJECT_ROOT
    / "experiments"
    / "results"
    / "ocr_text.zip"
)

OUTPUT_DIR = RESULTS_DIR / "evaluation_3b"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_JSON = (
    OUTPUT_DIR
    / "experiment_3b_evaluation_dataset.json"
)

OUTPUT_CSV = (
    OUTPUT_DIR
    / "experiment_3b_evaluation_dataset.csv"
)


# ============================================================
# HELPERS
# ============================================================

def read_text_file(path: Path) -> str:
    if not path.exists():
        return ""

    return path.read_text(
        encoding="utf-8",
        errors="replace"
    ).strip()


def read_zip_text(zip_file, member_name):
    """
    Read a UTF-8 text file directly from a ZIP archive.
    """
    try:
        with zip_file.open(member_name) as f:
            return f.read().decode(
                "utf-8",
                errors="replace"
            ).strip()
    except KeyError:
        return ""


def build_zip_index(zip_file):
    """
    Create basename -> full ZIP member mapping.
    """
    index = {}

    for name in zip_file.namelist():

        if not name.lower().endswith(".txt"):
            continue

        basename = Path(name).name.lower()

        index[basename] = name

    return index


def find_gt_filename(subset, template, sample):
    """
    ClinOCR-Bench GT naming convention:

    ground_truth/<subset>/
        template_X_sample_Y_<subset>.txt
    """

    filename = (
        f"template_{template}"
        f"_sample_{sample}"
        f"_{subset}.txt"
    ).lower()

    return filename


def find_ocr_filename(subset, template, sample):
    """
    OCR naming convention:

    ocr_text/
        <subset>_template_X_sample_Y.txt
    """

    filename = (
        f"{subset}"
        f"_template_{template}"
        f"_sample_{sample}.txt"
    ).lower()

    return filename


# ============================================================
# VALIDATE INPUT FILES
# ============================================================

print("=" * 70)
print("EXPERIMENT 3B — DATASET PREPARATION")
print("=" * 70)

if not LLM_CSV.exists():
    raise FileNotFoundError(
        f"Missing Experiment 3A CSV:\n{LLM_CSV}"
    )

if not GROUND_TRUTH_ZIP.exists():
    raise FileNotFoundError(
        f"Missing ground-truth ZIP:\n{GROUND_TRUTH_ZIP}"
    )

if not OCR_TEXT_ZIP.exists():
    raise FileNotFoundError(
        f"Missing OCR ZIP:\n{OCR_TEXT_ZIP}"
    )


# ============================================================
# LOAD EXPERIMENT 3A CSV
# ============================================================

with LLM_CSV.open(
    "r",
    encoding="utf-8-sig",
    newline=""
) as f:

    rows = list(csv.DictReader(f))


print(f"Experiment 3A rows: {len(rows)}")


# ============================================================
# GROUP GT / OCR CONDITIONS
# ============================================================

pairs = {}

for row in rows:

    pilot_id = row["pilot_id"]

    if pilot_id not in pairs:

        pairs[pilot_id] = {
            "pilot_id": pilot_id,
            "subset": row["subset"],
            "template": row["template"],
            "sample": row["sample"],
            "gt": None,
            "ocr": None,
        }

    condition = row["condition"].strip().lower()

    if condition == "gt":
        pairs[pilot_id]["gt"] = row

    elif condition == "ocr":
        pairs[pilot_id]["ocr"] = row


# ============================================================
# OPEN ZIP FILES
# ============================================================

gt_zip = zipfile.ZipFile(
    GROUND_TRUTH_ZIP,
    "r"
)

ocr_zip = zipfile.ZipFile(
    OCR_TEXT_ZIP,
    "r"
)

gt_index = build_zip_index(gt_zip)
ocr_index = build_zip_index(ocr_zip)


print(f"GT text files in ZIP: {len(gt_index)}")
print(f"OCR text files in ZIP: {len(ocr_index)}")


# ============================================================
# BUILD EVALUATION DATASET
# ============================================================

records = []

for pilot_id in sorted(pairs):

    pair = pairs[pilot_id]

    gt_row = pair["gt"]
    ocr_row = pair["ocr"]

    subset = pair["subset"].strip().lower()

    template = str(pair["template"]).strip()
    sample = str(pair["sample"]).strip()

    # --------------------------------------------------------
    # Ground Truth
    # --------------------------------------------------------

    gt_filename = find_gt_filename(
        subset,
        template,
        sample
    )

    gt_member = gt_index.get(gt_filename)

    ground_truth_text = ""

    if gt_member:
        ground_truth_text = read_zip_text(
            gt_zip,
            gt_member
        )

    # --------------------------------------------------------
    # OCR Text
    # --------------------------------------------------------

    ocr_filename = find_ocr_filename(
        subset,
        template,
        sample
    )

    ocr_member = ocr_index.get(ocr_filename)

    ocr_text = ""

    if ocr_member:
        ocr_text = read_zip_text(
            ocr_zip,
            ocr_member
        )

    # --------------------------------------------------------
    # Gemini GT Output
    # --------------------------------------------------------

    gt_llm_output = ""
    gt_output_path = ""

    if gt_row:

        candidate = Path(
            gt_row["output_path"]
        )

        if not candidate.is_absolute():

            candidate = (
                PROJECT_ROOT
                / candidate
            )

        if candidate.exists():

            gt_llm_output = read_text_file(
                candidate
            )

        else:

            # Fallback to known raw-output location
            fallback = (
                RAW_DIR
                / f"{pilot_id}_gt_gemini.txt"
            )

            gt_llm_output = read_text_file(
                fallback
            )

        gt_output_path = str(candidate)

    # --------------------------------------------------------
    # Gemini OCR Output
    # --------------------------------------------------------

    ocr_llm_output = ""
    ocr_output_path = ""

    if ocr_row:

        candidate = Path(
            ocr_row["output_path"]
        )

        if not candidate.is_absolute():

            candidate = (
                PROJECT_ROOT
                / candidate
            )

        if candidate.exists():

            ocr_llm_output = read_text_file(
                candidate
            )

        else:

            fallback = (
                RAW_DIR
                / f"{pilot_id}_ocr_gemini.txt"
            )

            ocr_llm_output = read_text_file(
                fallback
            )

        ocr_output_path = str(candidate)

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    ready = all([
        bool(ground_truth_text),
        bool(ocr_text),
        bool(gt_llm_output),
        bool(ocr_llm_output),
    ])

    record = {

        "pilot_id": pilot_id,

        "subset": subset,

        "template": template,

        "sample": sample,

        "ground_truth_text":
            ground_truth_text,

        "ocr_text":
            ocr_text,

        "gt_llm_output":
            gt_llm_output,

        "ocr_llm_output":
            ocr_llm_output,

        "ground_truth_member":
            gt_member or "",

        "ocr_text_member":
            ocr_member or "",

        "gt_output_path":
            gt_output_path,

        "ocr_output_path":
            ocr_output_path,

        "gt_status":
            gt_row["status"] if gt_row else "",

        "ocr_status":
            ocr_row["status"] if ocr_row else "",

        "ground_truth_found":
            bool(ground_truth_text),

        "ocr_text_found":
            bool(ocr_text),

        "gt_llm_output_found":
            bool(gt_llm_output),

        "ocr_llm_output_found":
            bool(ocr_llm_output),

        "ready_for_annotation":
            ready,
    }

    records.append(record)


# ============================================================
# CLOSE ZIP FILES
# ============================================================

gt_zip.close()
ocr_zip.close()


# ============================================================
# SAVE JSON
# ============================================================

with OUTPUT_JSON.open(
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        records,
        f,
        ensure_ascii=False,
        indent=2
    )


# ============================================================
# SAVE CSV
# ============================================================

fieldnames = [

    "pilot_id",
    "subset",
    "template",
    "sample",

    "ground_truth_text",
    "ocr_text",

    "gt_llm_output",
    "ocr_llm_output",

    "ground_truth_member",
    "ocr_text_member",

    "gt_output_path",
    "ocr_output_path",

    "gt_status",
    "ocr_status",

    "ground_truth_found",
    "ocr_text_found",

    "gt_llm_output_found",
    "ocr_llm_output_found",

    "ready_for_annotation",
]


with OUTPUT_CSV.open(
    "w",
    encoding="utf-8",
    newline=""
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=fieldnames
    )

    writer.writeheader()

    writer.writerows(records)


# ============================================================
# SUMMARY
# ============================================================

ready_count = sum(
    1
    for r in records
    if r["ready_for_annotation"]
)

not_ready_count = (
    len(records) - ready_count
)


print()
print("=" * 70)
print("DATASET VALIDATION")
print("=" * 70)

print(
    f"Total pilot pairs: {len(records)}"
)

print(
    f"Ready for annotation: {ready_count}"
)

print(
    f"Not ready: {not_ready_count}"
)


# ============================================================
# SUBSET COUNTS
# ============================================================

print()
print("Subset counts:")

subset_counts = {}

for r in records:

    subset = r["subset"]

    subset_counts[subset] = (
        subset_counts.get(subset, 0) + 1
    )

for subset, count in sorted(
    subset_counts.items()
):

    print(
        f"  {subset}: {count}"
    )


# ============================================================
# MISSING DATA
# ============================================================

if not_ready_count > 0:

    print()
    print("Missing-data details:")

    for r in records:

        missing = []

        if not r["ground_truth_found"]:
            missing.append("ground_truth")

        if not r["ocr_text_found"]:
            missing.append("ocr_text")

        if not r["gt_llm_output_found"]:
            missing.append("gt_llm_output")

        if not r["ocr_llm_output_found"]:
            missing.append("ocr_llm_output")

        if missing:

            print(
                f"  {r['pilot_id']}: "
                + ", ".join(missing)
            )


# ============================================================
# OUTPUTS
# ============================================================

print()
print("Output files:")

print(OUTPUT_JSON)
print(OUTPUT_CSV)

print("=" * 70)