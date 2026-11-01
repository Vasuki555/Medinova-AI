import csv
import re
from pathlib import Path

ROOT = Path(r"C:\Users\vasuk\Downloads\ClinOCR-Bench-v1.0\ClinOCR-Bench")
SCAN_ROOT = ROOT / "scans"
GT_ROOT = ROOT / "ground_truth"

SUBSETS = [
    "normal",
    "handwriting",
    "poor",
    "rotated",
    "tables",
    "mixed",
]

rows = []

for subset in SUBSETS:

    scan_dir = SCAN_ROOT / subset
    gt_dir = GT_ROOT / subset

    for scan_path in sorted(scan_dir.glob("*.jpg")):

        name = scan_path.stem

        match = re.match(
            r"template_(\d+)_sample_(\d+)_(.+)$",
            name
        )

        if not match:
            print("SKIPPED:", scan_path)
            continue

        template = int(match.group(1))
        sample = int(match.group(2))

        gt_path = gt_dir / f"{name}.txt"

        if not gt_path.exists():
            print("MISSING GT:", gt_path)
            continue

        rows.append({
            "subset": subset,
            "template": template,
            "sample": sample,
            "split": "exemplar" if sample == min(
                int(re.match(r"template_\d+_sample_(\d+)_", p.stem).group(1))
                for p in scan_dir.glob(f"template_{template}_sample_*_{subset}.jpg")
            ) else "eval",
            "scan_path": str(scan_path),
            "ground_truth_path": str(gt_path)
        })

output = Path("experiments")
output.mkdir(exist_ok=True)

manifest = output / "clinocr_bench_manifest.csv"

with manifest.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "subset",
            "template",
            "sample",
            "split",
            "scan_path",
            "ground_truth_path"
        ]
    )
    writer.writeheader()
    writer.writerows(rows)

print()
print("=" * 60)
print("ClinOCR-Bench manifest created")
print("=" * 60)
print("Total documents :", len(rows))
print("Exemplars       :", sum(r["split"] == "exemplar" for r in rows))
print("Evaluation      :", sum(r["split"] == "eval" for r in rows))
print("Manifest        :", manifest)
print()

for subset in SUBSETS:
    subset_rows = [r for r in rows if r["subset"] == subset]
    print(
        f"{subset:12s}: "
        f"total={len(subset_rows):3d}, "
        f"eval={sum(r['split'] == 'eval' for r in subset_rows):3d}"
    )
