# Experiment 3B — Pilot Review

This document contains the six pilot cases selected for manual clinical-fact annotation.

The original ClinOCR-Bench ground-truth report is treated as the factual reference. The Gemini outputs are taken directly from the existing Experiment 3A raw output files.

## Scoring Protocol

- **2** = correctly preserved
- **1** = partially preserved / less precise
- **0** = missing or incorrect

**No scores are assigned automatically.**

---

# E3P001

**Subset:** normal  
**Template:** 1  
**Sample:** 2

## 1. Original Ground Truth Report

Patient: John Smith DOB: 05/20/1965 MRN: 789012 
Accession #: A583920-25
SPRINGFIELD GENERAL HOSPITAL
Sunrise Diagnostics Phone: 
North Valley Imaging Center 456 Oak Avenue, Suite 200 Anytown, USA 12345
(555) 123-4567 
Patient: John Smith 
DOB: 05/20/1965 
MRN: 789012
Gender: Male Referring Physician: Dr. Emily White
Visit #: 456-789 Date of Visit: 06/18/2025
Diagnostic Imaging Report - Chest X-ray (2 views)
Procedure: Radiography of the chest, posteroanterior and lateral views.
Clinical Indication: Persistent cough and shortness of breath.
Findings: The lungs are clear without evidence of consolidation, infiltrate, or effusion. The cardiomediastinal silhouette is within normal limits. The osseous structures of the thorax are unremarkable.
Impression: No acute cardiopulmonary process.
Scheduled appointments:
Follow-up appointment with Dr. White scheduled for 06/25/2025 at 11:00 AM to discuss the results and further management.
Date of Dictation: 06/18/2025 Technician: Sarah Jenkins, RT(R)
CONFIDENTIALITY NOTICE: This report contains confidential patient information protected by federal and state law. It is intended only for the use of the individual or entity to whom it is addressed. If you are not the intended recipient, you are hereby notified that any disclosure, copying, distribution, or action taken in reliance on the contents of these documents is strictly prohibited. If you have received this report in error, please notify the sender immediately by telephone at (217) 555-1212 and destroy this document. 
Springfield General Hospital Imaging Department | 123 Health Way, Springfield, IL, 62704

---

## 2. Gemini Output — Ground Truth Condition

Here is an explanation of your medical report based strictly on the provided text:

### 1. Report Summary
* **Patient Name:** John Smith
* **Date of Birth:**

---

## 3. OCR Text

Patient;John Smith DOB: 05/20/1965,MRN:789012 Accession #; A583920-25 Sunrise Diagnostics Phone: Patient:john Smithi: SPRINGFIELD . North Valley Imaging Center;456; DOB:.05/20/1965 GENERAL Qak Averue;Suite 200 Anytown;; MRN: 789012 HOSPITAL USA 12345 Gender: Male Referring . (555)123-4567; Physician: Dr Emily White Visit#2456,789 Date ot Visitz06118/2025 14 Diagnostic lmaging Report : Chest: X-ray (2views) Procedure: Radiographyofthe chest,posteroanterior and Lateral views: Clinicai indication: Persistentcoughand shortness of breath:
Findings The lungsare clear without evidence of consolidation; infiltrate;or effusion:The cardiomediastinal Silhouette _s within normal limits: The osseous structures of,the thoraxare: junremarkable:
'Impression: No acute cardiopulmonary process-
'Scheduled appointments: 'Follow-up appointmentwith Dr:-White scheduled for 08/25/2025 at [1;0OAMtodiscussthe results and ifurther management: 'Date of Dictation: 06/18/2025,Technician: Sarah Jenkins; RT(R):
'CONFIDENTjALITY NOTICE: This report contains confidential patient information protected byfederal and state law;it is intended onlyfor the use ofthe individual or entity to Whom itis addressed lfyouare; "not the intended recipient; you are herebynotified thatany disclosure; copying distribution; or action taken in relianceon the contents of;,these documents is strictly prohibited Ifyou have received this' reportin error; please notify the sender immediately by telephone at (217) 555-1212 anddestroy this; document:; Springfield General Hospital Imaging Department: | 123 Health Way; Springtield,IL, 62704:

---

## 4. Gemini Output — OCR Condition

Here is a summary and clear breakdown of your chest X-ray report using only the information provided in the text.

---

### 1. Report Summary
* **Patient Name:**

---

## 5. Manual Clinical Fact Annotation

| Fact ID | Category | Reference Fact | GT Score | OCR Score | GT Evidence | OCR Evidence | Notes |
|---|---|---|---:|---:|---|---|---|
| F1 | | | | | | | |
| F2 | | | | | | | |
| F3 | | | | | | | |
| F4 | | | | | | | |
| F5 | | | | | | | |
| F6 | | | | | | | |
| F7 | | | | | | | |
| F8 | | | | | | | |
| F9 | | | | | | | |
| F10 | | | | | | | |
| F11 | | | | | | | |
| F12 | | | | | | | |
| F13 | | | | | | | |
| F14 | | | | | | | |
| F15 | | | | | | | |

### Allowed Categories

- DIAGNOSIS
- FINDING
- NUMERICAL_VALUE
- MEASUREMENT
- UNIT
- DATE
- MEDICATION
- DOSAGE
- CLINICAL_INSTRUCTION
- OTHER_CLINICAL_FACT

### Scoring

**2** = correctly preserved  
**1** = partially preserved / less precise  
**0** = missing or incorrect

---

# E3P006

**Subset:** handwriting  
**Template:** 1  
**Sample:** 2

## 1. Original Ground Truth Report

Patient: John Smith DOB: 05/20/1965 MRN: 789012 
Accession #: A583920-25
SPRINGFIELD GENERAL HOSPITAL
Sunrise Diagnostics Phone: 
North Valley Imaging Center 456 Oak Avenue, Suite 200 Anytown, USA 12345
(555) 123-4567 
Patient: John Smith 
DOB: 05/20/1965 
MRN: 789012
Gender: Male Referring Physician: Dr. Emily White
Visit #: 456-789 Date of Visit: 06/18/2025
Diagnostic Imaging Report - Chest X-ray (2 views)
Procedure: Radiography of the chest, posteroanterior and lateral views.
Clinical Indication: Persistent cough and shortness of breath.
Findings: The lungs are clear without evidence of consolidation, infiltrate, or effusion. The cardiomediastinal silhouette is within normal limits. The osseous structures of the thorax are unremarkable.
Impression: No acute cardiopulmonary process.
Scheduled appointments:
Follow-up appointment with Dr. White scheduled for 06/25/2025 at 11:00 AM to discuss the results and further management.
Date of Dictation: 06/18/2025 Technician: Sarah Jenkins, RT(R)
CONFIDENTIALITY NOTICE: This report contains confidential patient information protected by federal and state law. It is intended only for the use of the individual or entity to whom it is addressed. If you are not the intended recipient, you are hereby notified that any disclosure, copying, distribution, or action taken in reliance on the contents of these documents is strictly prohibited. If you have received this report in error, please notify the sender immediately by telephone at (217) 555-1212 and destroy this document. 
Springfield General Hospital Imaging Department | 123 Health Way, Springfield, IL, 62704

---

## 2. Gemini Output — Ground Truth Condition

Here is an explanation of your medical report based strictly on the text provided:

---

### 1. Report Summary
* **Patient Name:** John Smith
* **Date of Birth:** 05/20/1965
* **Gender:** Male
* **MRN:** 789012
* **Accession #:** A583920-25
* **Visit #:** 456-789
* **Date of Visit / Dictation:** 06/18/

---

## 3. OCR Text

Patient:John Smith DOB;, 05/20/1965 MRN:.789012} 'Accession #:A583920-25 SPRINGFIELD 'Sunrise Diagnostics Phone: Patient: John Smith; North Valley Imaging Center.456 " 'DOB:.05/20/1965} GENERAL 'OakAvenue; Suite 200 Anytown; MRN: 789012 HOSPITAL USA 12345: Gender; Male_Referring; '(555) 123.4567 Physician: Dr; Emily White Visit #3456 789 Date ofVi EE06/1812025 562 Diagnostic liaging Report Chest X-ray (2views)' Procedure: Radiography of the_chest; posteroanterior and lateral views: "Clinical Indication: Persistent cough and shortness ofbreath:
Findings: lings : swcber"fhut-evidhcei%k} censcbdetzhv: "tkete: Iq; dllnsich {s luitte%s idhin; hoskkel bnzts; Teosstouis gtuetisis #te #bicx civ unicnzs
caidionidiesthz
Impression "Irriezte ciabrulninarj_ Ricess:
Scheduled appointments:; 'Fgllow-Up appointment with Dr:White scheduled for06/25/2025at 1.1:00AM to discussthe results and further management: 'Date of Dictation: 06/18/2025 Technician: Sarah Jenkins; RT(R):
CONFIDENTIALITY NOTICE: This report contains confidential patientinformation protected by federal' and state law: it is intended only for the use ofthe individualor entity to whom itis addressed: Ifyou are, notthe intended recipient; you are hereby notified that any disclosure, copying; distribution; or.action;, taken in reliance on the contents of these documentsis strictly prohibited; ifyou_ have received this;: report in error; please notify the sender immediatelyby telephone at (217),555-1212and destroy this document: Springfield General Hospital Imaging Department | 123 Health; Way; Springfield; IL;,62704:

---

## 4. Gemini Output — OCR Condition

**3. Abnormal or Important Values**
        *   No readable or clear numerical values, test results, or measurements are present in the findings or impression sections because the text is garbled.

---

## 5. Manual Clinical Fact Annotation

| Fact ID | Category | Reference Fact | GT Score | OCR Score | GT Evidence | OCR Evidence | Notes |
|---|---|---|---:|---:|---|---|---|
| F1 | | | | | | | |
| F2 | | | | | | | |
| F3 | | | | | | | |
| F4 | | | | | | | |
| F5 | | | | | | | |
| F6 | | | | | | | |
| F7 | | | | | | | |
| F8 | | | | | | | |
| F9 | | | | | | | |
| F10 | | | | | | | |
| F11 | | | | | | | |
| F12 | | | | | | | |
| F13 | | | | | | | |
| F14 | | | | | | | |
| F15 | | | | | | | |

### Allowed Categories

- DIAGNOSIS
- FINDING
- NUMERICAL_VALUE
- MEASUREMENT
- UNIT
- DATE
- MEDICATION
- DOSAGE
- CLINICAL_INSTRUCTION
- OTHER_CLINICAL_FACT

### Scoring

**2** = correctly preserved  
**1** = partially preserved / less precise  
**0** = missing or incorrect

---

# E3P011

**Subset:** poor  
**Template:** 1  
**Sample:** 2

## 1. Original Ground Truth Report

Patient: John Smith DOB: 05/20/1965 MRN: 789012 
Accession #: A583920-25
SPRINGFIELD GENERAL HOSPITAL
Sunrise Diagnostics Phone: 
North Valley Imaging Center 456 Oak Avenue, Suite 200 Anytown, USA 12345
(555) 123-4567 
Patient: John Smith 
DOB: 05/20/1965 
MRN: 789012
Gender: Male Referring Physician: Dr. Emily White
Visit #: 456-789 Date of Visit: 06/18/2025
Diagnostic Imaging Report - Chest X-ray (2 views)
Procedure: Radiography of the chest, posteroanterior and lateral views.
Clinical Indication: Persistent cough and shortness of breath.
Findings: The lungs are clear without evidence of consolidation, infiltrate, or effusion. The cardiomediastinal silhouette is within normal limits. The osseous structures of the thorax are unremarkable.
Impression: No acute cardiopulmonary process.
Scheduled appointments:
Follow-up appointment with Dr. White scheduled for 06/25/2025 at 11:00 AM to discuss the results and further management.
Date of Dictation: 06/18/2025 Technician: Sarah Jenkins, RT(R)
CONFIDENTIALITY NOTICE: This report contains confidential patient information protected by federal and state law. It is intended only for the use of the individual or entity to whom it is addressed. If you are not the intended recipient, you are hereby notified that any disclosure, copying, distribution, or action taken in reliance on the contents of these documents is strictly prohibited. If you have received this report in error, please notify the sender immediately by telephone at (217) 555-1212 and destroy this document. 
Springfield General Hospital Imaging Department | 123 Health Way, Springfield, IL, 62704

---

## 2. Gemini Output — Ground Truth Condition

Translate imaging terms carefully without adding medical facts outside the text:
            *   "Lungs are clear without evidence of consolidation, infiltrate, or effusion": The lungs do not show fluid buildup

---

## 3. OCR Text

Patlent " Jotn= Smith F Accession4:85418202505120/1985 MRNze9012/ DQBES SPRINGEIELD  'Sunise piagnostics Phones '"Patient Jahn Siitn GENERAL North Valley Imaging Center 45e DOB: 05/20/1965 HOSPITAL Oak Avenue;Suite ?00 Anytown MRN;789012 USA 12345, Gender: Mala Referting (555)1 123-45674, Pbysician DrEmily White Aieltk456389 DateDEVIsiE06/18/20252 Diagnostic lmaging Repozte Chest Xiray (2views) Precedure Radlography ofithe chest posteroantarorandTateralvlewz: cimnicallndication: Persistent cough andchortness ofbreath;
"Findings; The lungs are clearwithouf evidence 0f consolidation infiltiate greiusionathe? cardiomediastinalsilhouette swithi normaljimits Jha.osacouastructures etthethoraxaie: @nremarkable;
Ipression Noacute cardiopuimonary proce;e
Sgbeduleda omrnen Wth Pr Whitescheduled ior06/25/2025ar1[ 00 AMito discusstheresuitsand (Eoiew Yp appoinenent furtherimai agement: . pictation; 06/18/2023 echriclen; Sarah Jenkins RTUR) ate of;
Teport "contelig= aordidantlat patient Information protected 2nl the ign3unanacany {Lzceosire? 'antity  ioicaa Jor towhomit "Peotecezesytevozaira notlfiez CoNfipen Jeis irite dyolara heresedo Ocumenti is striciy prohibitea ifyoi distribution; iaw:E Tecipiene;  pf ithese: Or,action . and Fata; itended ; contenis Immediately bytelephone.at ( deEyothave received on.iiie {02 sendaj (2171,55541212.an2 this; {as the ringgance 'plepsenotifyt 1123 destroy; this; faken 'errov;; Vimaging F pepaitment | teporti Health Way, = 'Springiiala; (General Hospiteii 4;62704' document; Springiield

---

## 4. Gemini Output — OCR Condition

**
        *   *Chest X-ray (2 views)*: An imaging test taking pictures of the front and side of the chest.
        *   *Clear lungs without consolidation, infiltrate

---

## 5. Manual Clinical Fact Annotation

| Fact ID | Category | Reference Fact | GT Score | OCR Score | GT Evidence | OCR Evidence | Notes |
|---|---|---|---:|---:|---|---|---|
| F1 | | | | | | | |
| F2 | | | | | | | |
| F3 | | | | | | | |
| F4 | | | | | | | |
| F5 | | | | | | | |
| F6 | | | | | | | |
| F7 | | | | | | | |
| F8 | | | | | | | |
| F9 | | | | | | | |
| F10 | | | | | | | |
| F11 | | | | | | | |
| F12 | | | | | | | |
| F13 | | | | | | | |
| F14 | | | | | | | |
| F15 | | | | | | | |

### Allowed Categories

- DIAGNOSIS
- FINDING
- NUMERICAL_VALUE
- MEASUREMENT
- UNIT
- DATE
- MEDICATION
- DOSAGE
- CLINICAL_INSTRUCTION
- OTHER_CLINICAL_FACT

### Scoring

**2** = correctly preserved  
**1** = partially preserved / less precise  
**0** = missing or incorrect

---

# E3P016

**Subset:** rotated  
**Template:** 1  
**Sample:** 2

## 1. Original Ground Truth Report

Patient: John Smith DOB: 05/20/1965 MRN: 789012 
Accession #: A583920-25
SPRINGFIELD GENERAL HOSPITAL
Sunrise Diagnostics Phone: 
North Valley Imaging Center 456 Oak Avenue, Suite 200 Anytown, USA 12345
(555) 123-4567 
Patient: John Smith 
DOB: 05/20/1965 
MRN: 789012
Gender: Male Referring Physician: Dr. Emily White
Visit #: 456-789 Date of Visit: 06/18/2025
Diagnostic Imaging Report - Chest X-ray (2 views)
Procedure: Radiography of the chest, posteroanterior and lateral views.
Clinical Indication: Persistent cough and shortness of breath.
Findings: The lungs are clear without evidence of consolidation, infiltrate, or effusion. The cardiomediastinal silhouette is within normal limits. The osseous structures of the thorax are unremarkable.
Impression: No acute cardiopulmonary process.
Scheduled appointments:
Follow-up appointment with Dr. White scheduled for 06/25/2025 at 11:00 AM to discuss the results and further management.
Date of Dictation: 06/18/2025 Technician: Sarah Jenkins, RT(R)
CONFIDENTIALITY NOTICE: This report contains confidential patient information protected by federal and state law. It is intended only for the use of the individual or entity to whom it is addressed. If you are not the intended recipient, you are hereby notified that any disclosure, copying, distribution, or action taken in reliance on the contents of these documents is strictly prohibited. If you have received this report in error, please notify the sender immediately by telephone at (217) 555-1212 and destroy this document. 
Springfield General Hospital Imaging Department | 123 Health Way, Springfield, IL, 62704

---

## 2. Gemini Output — Ground Truth Condition

Lungs are clear*: No signs of lung collapse/solid areas (consolidation), fluid buildup or fluid around lungs (infiltrate or effusion).
            *   *Card

---

## 3. OCR Text

23 9 1 82 1 1 # 2 8 | L 1 1 U 1 2 L ] @ 8 H 8  1 H 1 6 [ 1 ] | H 3 [ ] #H 1 2 9 Hi
8 1
K 3 3 0 1 29 Ea 5 I 9 38 | 0 5 1 8 3 ! 8 0 0 X L 0 H 83 1 8 0 1 M 2 L L 8 k H 3 1 g 5 N |
5 8 8 8 1 L 0 H F [ J

---

## 4. Gemini Output — OCR Condition

Based on the text provided, here is an explanation of the medical report using the required structure:

### 1. Report Summary
The provided text does not contain any readable medical summary, medical history, or clinical context. It consists entirely of a series of unformatted numbers, single letters, and symbols.

### 2. Key Findings
There are no identifiable medical findings, physical examination results, or imaging/lab results mentioned in the text.

### 3. Abnormal or Important Values
There are no recognizable lab results, vital signs, reference ranges, or numerical medical values present in the text.

### 4. Plain-Language Explanation
The document provided appears to be corrupted, mistyped, or garbled text (a collection of symbols, single numbers, and letters such as `23 9 1 82...` and `K 3 3 0...`). Because there are no readable words or standard medical terms, it is not possible to explain what this report means for your health.

### 5. Medications / Treatment Information
No medications, dosages, treatments, or medical procedures are listed in the provided text.

### 6. Information That Is Unclear or Missing
* **Unclear / Missing Information:** The entire document is completely unclear and missing legible medical data. 
* **Recommendation:** Please check the document or contact your healthcare provider or medical records department to obtain a clear, readable copy of your actual medical report.

---

## 5. Manual Clinical Fact Annotation

| Fact ID | Category | Reference Fact | GT Score | OCR Score | GT Evidence | OCR Evidence | Notes |
|---|---|---|---:|---:|---|---|---|
| F1 | | | | | | | |
| F2 | | | | | | | |
| F3 | | | | | | | |
| F4 | | | | | | | |
| F5 | | | | | | | |
| F6 | | | | | | | |
| F7 | | | | | | | |
| F8 | | | | | | | |
| F9 | | | | | | | |
| F10 | | | | | | | |
| F11 | | | | | | | |
| F12 | | | | | | | |
| F13 | | | | | | | |
| F14 | | | | | | | |
| F15 | | | | | | | |

### Allowed Categories

- DIAGNOSIS
- FINDING
- NUMERICAL_VALUE
- MEASUREMENT
- UNIT
- DATE
- MEDICATION
- DOSAGE
- CLINICAL_INSTRUCTION
- OTHER_CLINICAL_FACT

### Scoring

**2** = correctly preserved  
**1** = partially preserved / less precise  
**0** = missing or incorrect

---

# E3P021

**Subset:** tables  
**Template:** 10  
**Sample:** 2

## 1. Original Ground Truth Report

LAKEWOOD HOSPITAL
831676002937
Patient: Maria C. Delgado  DOB: 03/28/1972  
MRN: 007-214-55
March 10, 2026
SECTION A: Medical History
Yes
No
Rheumatoid Arthritis (ICD-10: M06.9)
X
Hypothyroidism (ICD-10: E03.9)
X
Major Depressive Disorder (ICD-10: F32.1)
X
Gastroesophageal Reflux Disease (ICD-10: K21.0)
X
Osteoporosis (ICD-10: M81.0)
X
Anemia, Iron Deficiency (ICD-10: D50.9)
X
Fibromyalgia (ICD-10: M79.3)
X
SECTION B: Current Medication
Yes
No
Methotrexate 15 mg — once weekly
X
Folic Acid 1 mg — once daily
X
Levothyroxine 75 mcg — once daily (fasting)
X
Sertraline 50 mg — once daily (AM)
X
Omeprazole 20 mg — once daily before meals
X
Alendronate 70 mg — once weekly
X
Hydroxychloroquine 200 mg — twice daily
X
Maria Delgado  
Patient signature
Maria Delgado  
Print name

---

## 2. Gemini Output — Ground Truth Condition

Here is an explanation of your medical report using only the information provided in the document.

---

### 1. Report Summary
* **Facility:** Lakewood Hospital
* **Patient Name:** Maria

---

## 3. OCR Text

Patient; Maria C: Delgado: DOB: 03/28/1972: MRN:.007-214-55
831676002937
LAKEWOOD; HOSPITAL
March 10,2026-
32Z4SECTION A:MedicalHisto
Yes;
No
Rheumatoid Aithritis (ICD-1O: M06.9)  Hypothyroidism (ICD-10.E03.92 Major Depressive Disorder (ICD-1O:F32.1)_ Gastroesophageal Reflux Disease (ICD:10:K21.0) Osteoporosis (ICD:-1O:M81:O) Anemia;Iron Deficiency (ICD-1OD5O.9) Fibromyalgia (ICD-10:M79.3)
'
SECTION Bcurrent Medication
Yes X; X; X: X X ' X
No'
Methotrexate 15.mg once weekly: Folic Acid:1 ig__once daily_ Levothyroxine;75 _cg once daily(fasting) Sertraline 50.mg_ once daily (AM): Omeprazole 20 ig} once daily before meals;' Alendronate 70ing) Aonce weekly Hydroxychloroquine 2O0mg twice daily
Waria 'Pelgado Patient signature
Maria_ Delgado Print name

---

## 4. Gemini Output — OCR Condition

Here is a clear summary and explanation of your medical report based strictly on the provided text.

### 1. Report Summary
* **Patient Name:** Maria C. Delgado (signed

---

## 5. Manual Clinical Fact Annotation

| Fact ID | Category | Reference Fact | GT Score | OCR Score | GT Evidence | OCR Evidence | Notes |
|---|---|---|---:|---:|---|---|---|
| F1 | | | | | | | |
| F2 | | | | | | | |
| F3 | | | | | | | |
| F4 | | | | | | | |
| F5 | | | | | | | |
| F6 | | | | | | | |
| F7 | | | | | | | |
| F8 | | | | | | | |
| F9 | | | | | | | |
| F10 | | | | | | | |
| F11 | | | | | | | |
| F12 | | | | | | | |
| F13 | | | | | | | |
| F14 | | | | | | | |
| F15 | | | | | | | |

### Allowed Categories

- DIAGNOSIS
- FINDING
- NUMERICAL_VALUE
- MEASUREMENT
- UNIT
- DATE
- MEDICATION
- DOSAGE
- CLINICAL_INSTRUCTION
- OTHER_CLINICAL_FACT

### Scoring

**2** = correctly preserved  
**1** = partially preserved / less precise  
**0** = missing or incorrect

---

# E3P026

**Subset:** mixed  
**Template:** 2  
**Sample:** 2

## 1. Original Ground Truth Report

Patient Name: Jane Doe MRN: 987654321
LAKEWOOD HOSPITAL
PATHOLOGY REPORT
831676002937
Patient Name: Jane Doe
Patient ID: 987654321
Date of Birth: 1970-05-15
Gender: Female
Accession Number: P25-12345
University Medical Center
123 Health Sciences Drive
Metropolis, USA 12345
Phone: (123) 456-7890
Fax: (123) 456-7891
Date of Collection: 2025-06-15 
Time of Collection: 09:30 AM 
Specimen Type: Tissue biopsy, left breast 
Clinical History: Palpable lump in the upper outer quadrant of the left breast. Mammogram and ultrasound findings are suspicious for malignancy.
Ordering Physician: Dr. John Smith, MD Clinical Practice: Metropolis Oncology Associates Address: 456 Cancer Care Plaza, Metropolis, USA 12345 Phone: (123) 555-0123
Gross Description:
The specimen is received in formalin, labeled with the patient's name and medical record number, and designated "left breast core biopsy." It consists of three tan-white, cylindrical tissue fragments, ranging in length from 1.2 cm to 1.5 cm and in diameter from 0.2 cm to 0.3 cm. The entire specimen is submitted in one cassette.
Microscopic Description:
Histologic sections reveal cores of breast tissue with an infiltrative neoplasm. The tumor cells are arranged in irregular nests and single files, infiltrating the fibrous stroma. The neoplastic cells are pleomorphic with enlarged, hyperchromatic nuclei and prominent nucleoli. Mitotic figures are frequently identified. There is associated ductal carcinoma in situ (DCIS), solid type, with high-grade nuclear features. No evidence of lymphovascular invasion is identified in the submitted material.
Diagnosis:
Invasive Ductal Carcinoma, Grade 3 of 3.
Comments:
The histomorphologic features are those of a high-grade invasive ductal carcinoma. Correlation with imaging findings and clinical presentation is recommended. Further evaluation for hormone receptor status and HER2/neu expression is pending and will be reported in an addendum.
Biomarkers:
Page 1 of 1

---

## 2. Gemini Output — Ground Truth Condition

Here is a clear, patient-friendly breakdown of the provided pathology report.

### 1. Report Summary
* **Patient Name:** Jane Doe
* **Patient ID (MR

---

## 3. OCR Text

[upuad Ja #wm 'nauizhak [@upyad (Ua)joxd922y2uon1s 8old  dAS R7 'X F2jupuad {E Quodeoou 4a3q45 Vip2nsoy Joleuigig] 77 JI= Xay_ 95 5i70S NsjoxJeLoi8
"ticxi [ejoiqoiu
487
S)42 1{76
Si
Gialzwr  % iidaSX 500 3140380431W Ti Sit" Ts4 'ZO
djisea,68043
Z1O -55S 194o44.377ET Recouppv_
Notsinezjum? ;odA 204jpode: 2401,281834097 410z7 Zoz :491*221103jo@180 3t4=
248j931g1p
jsjeada 2
68L,99/ (CZH)ED 18823s7(cZL)  [403 Zstcz: VSQi oijio 802449155 4ipoHEzWJ D1uo31*3Ipo1 Mizoilun JV4asoH OOOMBXV; Zeps9L8s Nuwideagu0 'ouot
JV5 NoqLUnM VO 0p5 Ppud'
zai
vypn2d
'LC6zO09L9iEB
4oja8AJ010H

---

## 4. Gemini Output — OCR Condition

1. Report Summary**
The provided report text appears to be heavily corrupted, garbled, or incorrectly scanned (OCR errors). Because the text consists almost entirely of unreadable characters and fragmented letter combinations

---

## 5. Manual Clinical Fact Annotation

| Fact ID | Category | Reference Fact | GT Score | OCR Score | GT Evidence | OCR Evidence | Notes |
|---|---|---|---:|---:|---|---|---|
| F1 | | | | | | | |
| F2 | | | | | | | |
| F3 | | | | | | | |
| F4 | | | | | | | |
| F5 | | | | | | | |
| F6 | | | | | | | |
| F7 | | | | | | | |
| F8 | | | | | | | |
| F9 | | | | | | | |
| F10 | | | | | | | |
| F11 | | | | | | | |
| F12 | | | | | | | |
| F13 | | | | | | | |
| F14 | | | | | | | |
| F15 | | | | | | | |

### Allowed Categories

- DIAGNOSIS
- FINDING
- NUMERICAL_VALUE
- MEASUREMENT
- UNIT
- DATE
- MEDICATION
- DOSAGE
- CLINICAL_INSTRUCTION
- OTHER_CLINICAL_FACT

### Scoring

**2** = correctly preserved  
**1** = partially preserved / less precise  
**0** = missing or incorrect

---

