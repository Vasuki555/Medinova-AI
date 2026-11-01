from pathlib import Path
import zipfile, re
from collections import Counter
import pandas as pd

RESULTS_CSV=Path(r"experiments/results/clinocr_ocr_per_document.csv")
OCR_ZIP=Path(r"experiments/results/ocr_text.zip")
GT_ZIP=Path(r"experiments/ground_truth.zip")
OUT=Path(r"experiments/results/clinical_info")
OUT.mkdir(parents=True,exist_ok=True)

NUM=re.compile(r"(?<![A-Za-z])[-+]?\d+(?:[.,]\d+)*(?:[eE][-+]?\d+)?(?![A-Za-z])")
DATE=re.compile(r"\b(?:\d{1,4}[/-]\d{1,2}[/-]\d{1,4}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}-\d{1,2}-\d{1,2})\b")
UNIT=re.compile(r"\b(?:mg|g|kg|mcg|µg|ug|mL|ml|L|dL|mmHg|cmH2O|mm|cm|m|cm3|mm3|mL/min|mg/dL|g/dL|U/L|IU/L|bpm|%|°C|°F|sec|s|min|hr|h|days?|weeks?|months?|years?)\b",re.I)
MEAS=re.compile(r"([-+]?\d+(?:[.,]\d+)?)\s*(mg/dL|g/dL|mmHg|mg|g|kg|mcg|µg|ug|mL|ml|L|U/L|IU/L|bpm|mm|cm|%|°C|°F)\b",re.I)

def gtkey(n):
    x=n.replace("\\","/").split("/")
    if len(x)<3 or not n.lower().endswith(".txt"): return None
    sub=x[1].lower(); stem=Path(x[-1]).stem.lower()
    suf="_"+sub
    if stem.endswith(suf): stem=stem[:-len(suf)]
    return f"{sub}_{stem}"

def items(s):
    return {
        "numbers":[x.replace(" ","") for x in NUM.findall(s)],
        "dates":[re.sub(r"[^0-9]","",x) for x in DATE.findall(s)],
        "units":[x.lower() for x in UNIT.findall(s)],
        "measurements":[(v.replace(" ",""),u.lower()) for v,u in MEAS.findall(s)]
    }

def matched(a,b):
    ca,cb=Counter(a),Counter(b)
    return sum(min(n,cb.get(k,0)) for k,n in ca.items())

def lost(a,b):
    ca,cb=Counter(a),Counter(b); out=[]
    for k,n in ca.items():
        out += [k]*max(0,n-cb.get(k,0))
    return out[:20]

def compact(s,n=1400):
    s=re.sub(r"\s+"," ",s).strip()
    return s if len(s)<=n else s[:n]+" ..."

m=pd.read_csv(RESULTS_CSV)
need={"subset","template","sample","cer","wer"}
missing=need-set(m.columns)
if missing: raise RuntimeError(f"Missing columns: {missing}\nAvailable: {list(m.columns)}")
m["document"]=m["subset"].astype(str).str.lower()+"_template_"+m["template"].astype(str)+"_sample_"+m["sample"].astype(str)
m=m[["subset","document","cer","wer"]].rename(columns={"cer":"CER","wer":"WER"})

gt={}
with zipfile.ZipFile(GT_ZIP) as z:
    for n in z.namelist():
        k=gtkey(n)
        if k: gt[k]=n

rows=[]
with zipfile.ZipFile(OCR_ZIP) as oz, zipfile.ZipFile(GT_ZIP) as gz:
    for n in oz.namelist():
        if not n.lower().endswith(".txt"): continue
        k=Path(n).stem.lower()
        if k not in gt: continue
        ot=oz.read(n).decode("utf-8","replace")
        gttext=gz.read(gt[k]).decode("utf-8","replace")
        a=items(gttext); b=items(ot)
        r={"subset":k.split("_",1)[0],"document":k,"gt_text":gttext,"ocr_text":ot}
        for c in a:
            r[c+"_gt"]=len(a[c]); r[c+"_matched"]=matched(a[c],b[c]); r[c+"_lost"]=lost(a[c],b[c])
        rows.append(r)

d=pd.DataFrame(rows)
if len(d)!=328: raise RuntimeError(f"Expected 328 matched documents, found {len(d)}")
d=d.merge(m,on=["subset","document"],how="left",validate="one_to_one")
if d.CER.isna().any(): raise RuntimeError("Some documents could not be matched to Experiment 1 CER/WER.")

for c in ["numbers","dates","units","measurements"]:
    d[c+"_loss"]=d.apply(lambda r: 1-r[c+"_matched"]/r[c+"_gt"] if r[c+"_gt"] else 0,axis=1)
d["information_loss_score"]=.40*d.measurements_loss+.30*d.numbers_loss+.15*d.dates_loss+.15*d.units_loss

sel=[]
for sub,g in d.groupby("subset"):
    elig=g[(g.numbers_gt+g.dates_gt+g.units_gt+g.measurements_gt)>0]
    sel.append(elig.sort_values(["information_loss_score","CER"],ascending=False).head(3))
    sel.append(elig.sort_values(["CER","WER"],ascending=False).head(1))
sel=pd.concat(sel).drop_duplicates("document")

out=[]
for _,r in sel.iterrows():
    out.append({
        "subset":r.subset,"document":r.document,"CER":round(float(r.CER),6),"WER":round(float(r.WER),6),
        "numbers":f"{int(r.numbers_matched)}/{int(r.numbers_gt)}",
        "dates":f"{int(r.dates_matched)}/{int(r.dates_gt)}",
        "units":f"{int(r.units_matched)}/{int(r.units_gt)}",
        "measurements":f"{int(r.measurements_matched)}/{int(r.measurements_gt)}",
        "lost_numbers":"; ".join(map(str,r.numbers_lost)),
        "lost_dates":"; ".join(map(str,r.dates_lost)),
        "lost_units":"; ".join(map(str,r.units_lost)),
        "lost_measurements":"; ".join(map(str,r.measurements_lost)),
        "ground_truth":compact(r.gt_text),"ocr_output":compact(r.ocr_text)
    })

rep=pd.DataFrame(out)
rep.to_csv(OUT/"representative_ocr_error_cases.csv",index=False)
d[["subset","document","CER","WER","numbers_gt","numbers_matched","dates_gt","dates_matched","units_gt","units_matched","measurements_gt","measurements_matched","information_loss_score"]].sort_values(["subset","information_loss_score"],ascending=[True,False]).to_csv(OUT/"all_document_information_loss.csv",index=False)

lines=["EXPERIMENT 2B — REPRESENTATIVE OCR ERROR INSPECTION","="*70,"Documents analyzed: 328","CER/WER taken from existing Experiment 1 CSV; OCR not rerun.","information_loss_score is a case-selection heuristic, not a clinical metric.",""]
for _,r in rep.iterrows():
    lines += ["-"*70,f"SUBSET: {r['subset']}",f"DOCUMENT: {r['document']}",f"CER={r['CER']} | WER={r['WER']}",f"Numbers: {r['numbers']} | Dates: {r['dates']} | Units: {r['units']} | Measurements: {r['measurements']}",f"Lost numbers: {r['lost_numbers'] or 'None'}",f"Lost dates: {r['lost_dates'] or 'None'}",f"Lost units: {r['lost_units'] or 'None'}",f"Lost measurements: {r['lost_measurements'] or 'None'}","","GROUND TRUTH:",r["ground_truth"],"","OCR OUTPUT:",r["ocr_output"],""]
(OUT/"representative_ocr_error_cases.txt").write_text("\n".join(lines),encoding="utf-8")
print("="*70)
print("Experiment 2B completed")
print(f"Documents analyzed   : {len(d)}")
print(f"Representative cases : {len(rep)}")
print(rep.groupby("subset").size().to_string())
print("\nOutputs:")
print(OUT/"representative_ocr_error_cases.csv")
print(OUT/"representative_ocr_error_cases.txt")
print(OUT/"all_document_information_loss.csv")
