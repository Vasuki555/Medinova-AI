# MediNova Project - Research Audit Summary

**Date**: September 24, 2026  
**Analysis Type**: Complete Repository Inspection for Research Publication  
**Goal**: Evaluate conference paper readiness without code modification

---

## Executive Summary

**Project Status**: 76% feature-complete, 0% experimentally validated  
**Research Readiness**: 4/10 (Strong implementation, zero validation)  
**Time to Publication**: 3-6 months with focused research effort  
**Critical Finding**: Single-LLM architecture despite "multi-agent" claims in documentation

---

## 1. Project Overview

### What MediNova Actually Is
- **Type**: Layered monolithic web application (NOT multi-agent system)
- **Frontend**: React 18.3.1 SPA with 28 pages (Vite, TailwindCSS)
- **Backend**: FastAPI REST API with 15 modules, 13 services
- **Database**: MongoDB Atlas (10 collections)
- **AI Engine**: Google Gemini 3.6 Flash (single LLM only)
- **OCR Pipeline**: EasyOCR + OpenCV preprocessing

### Architecture Mismatch Alert ⚠️
**README Claims**: "Multi-Agent Healthcare Intelligence Platform with LangGraph orchestration"  
**Actual Code**: Single `genai.Client` with Gemini 3.6 Flash  
**Evidence**: `backend/app/services/ai_service.py:82-93`, `backend/app/config.py:18`  
**Impact**: Documentation must be corrected before publication

---

## 2. Features Inventory

### ✅ Fully Working (42 features, 76%)

**Authentication & Authorization**
- JWT-based auth with refresh tokens
- Role-based access (patient/doctor/admin)
- Password hashing (bcrypt)
- Session management

**OCR Pipeline**
- Image preprocessing (CLAHE, Gaussian blur, adaptive threshold)
- EasyOCR text extraction
- Structured data extraction (medicines, diagnoses, instructions)
- Support for: PNG, JPG, JPEG, WEBP

**AI Simplification**
- Medical jargon to plain English
- Structured JSON output
- Context-aware explanations
- Gemini 3.6 Flash integration

**Patient Features**
- Profile management
- Appointment booking
- Health records view
- Medication tracking
- QR health ID generation

**Doctor Features**
- Profile with specialization
- Appointment management
- Patient record access
- Hospital affiliation

**Admin Features**
- User management
- Hospital CRUD
- System monitoring
- Analytics dashboard

### ⚙️ Partially Implemented (8 features, 15%)
- PDF OCR (code exists but fails on Windows - missing Poppler)
- Email verification (mock only, no SMTP)
- Notifications (storage only, no real-time delivery)
- Telemedicine (UI exists, no video integration)
- Analytics (basic queries, no aggregation pipeline)
- Search (exact match only, no fuzzy search)
- Export (download exists, no format options)
- Multilingual (UI ready, no i18n implementation)

### ❌ Missing (5 features, 9%)
- Real-time video calls
- WebSocket notifications
- Payment integration
- Mobile apps
- Offline mode

---

## 3. Technical Implementation Details

### OCR Preprocessing Pipeline
**File**: `backend/app/services/ocr_service.py`

```python
# CLAHE (Contrast Limited Adaptive Histogram Equalization)
clipLimit=2.0
tileGridSize=(8, 8)

# Gaussian Blur
kernel_size=(3, 3)

# Adaptive Threshold
blockSize=11
C=2
method=ADAPTIVE_THRESH_GAUSSIAN_C
```

### AI Service Architecture
**File**: `backend/app/services/ai_service.py:82-93`

```python
MODEL = "gemini-3.6-flash"  # Single LLM
client = genai.Client(api_key=settings.GOOGLE_AI_KEY)
temperature = 0.7
max_tokens = 2048
```

**NOT multi-agent** - No agent coordinator, no LangGraph, no inter-agent communication

### Document Processing
**File**: `backend/app/services/document_processor.py`

Structured extraction:
- Medications (name, dosage, frequency, duration)
- Diagnoses (condition, severity, notes)
- Instructions (category, description, priority)
- Vitals (type, value, unit, normal_range)

---

## 4. Current Results & Data

### Sample Data Found
**Location**: Project root directory
- `sample_blood_report.png`
- `sample_lipid_profile.png`
- `sample_prescription.png`
- `backend/uploads/` (1 uploaded file)

**Total**: 3-4 medical report images

### Evaluation Results
❌ **NOT FOUND**

No files containing:
- OCR accuracy measurements (CER, WER, accuracy %)
- LLM quality scores (PEMAT, readability, clinical accuracy)
- Baseline comparisons (Tesseract, GPT-4o, Claude)
- Performance benchmarks (latency, throughput, cost)
- User study results
- Clinical validation data
- Automated test execution reports

---

## 5. Dataset Analysis

### Current State
| Component | Count | Ground Truth | Annotations | Adequate for Research? |
|-----------|-------|--------------|-------------|----------------------|
| Medical Reports (Images) | 3-4 | ❌ No | ❌ No | ❌ No (need 100-150) |
| OCR Transcriptions | 0 | ❌ No | - | ❌ No |
| LLM Simplifications | 0 | - | ❌ No expert ratings | ❌ No |
| Patient Feedback | 0 | - | - | ❌ No (need IRB) |
| Baseline Comparisons | 0 | - | - | ❌ No |

### Missing for Publication
1. **OCR Ground Truth**: Manual transcriptions of 100+ reports
2. **LLM Evaluation Set**: 50+ doctor-rated simplifications
3. **Baseline Data**: Tesseract OCR outputs, GPT-4o comparisons
4. **Patient Comprehension**: IRB-approved study with 30+ participants
5. **Performance Logs**: Latency, throughput, cost metrics

---

## 6. Research Readiness Assessment

### Overall Score: 4/10

| Dimension | Score | Status | Evidence |
|-----------|-------|--------|----------|
| **Implementation** | 8/10 | ✅ Strong | 42/55 features working, clean architecture |
| **Dataset** | 1/10 | ❌ Critical | Only 3-4 samples, no ground truth |
| **Evaluation** | 0/10 | ❌ Blocker | Zero experimental results |
| **Baselines** | 2/10 | ❌ Critical | No Tesseract, no GPT-4o, no comparison |
| **Documentation** | 7/10 | ⚠️ Good | README exists but has architecture mismatch |
| **Reproducibility** | 5/10 | ⚠️ Medium | Docker setup exists, but no evaluation scripts |

### Publication Readiness by Component

#### Can Publish Now ✅
- System architecture diagrams
- Feature descriptions
- Technology stack choices
- Implementation decisions

#### Cannot Publish Yet ❌
- OCR accuracy claims (no measurements)
- LLM quality assertions (no validation)
- "Better than baseline" statements (no baselines)
- Patient comprehension improvements (no study)
- Performance characteristics (no benchmarks)

---

## 7. Critical Technical Limitations

1. **PDF OCR Failure**: Requires Poppler binaries not installed on Windows
2. **No Accuracy Measurement**: Zero CER/WER calculations in codebase
3. **Single LLM Only**: No comparison to GPT-4o, Claude, or other models
4. **No Clinical Validation**: No doctor ratings of AI-generated explanations
5. **Mock Email Only**: `email_service.py:13` prints instead of sending
6. **QR Security Vulnerability**: `/api/v1/qr/{user_id}` has no authentication
7. **No Real-time Notifications**: Storage only, no WebSocket/push
8. **No Hallucination Detection**: No fact-checking against source documents
9. **No Automated Testing**: Test files exist but no execution reports
10. **Development-Only Deployment**: No production configuration

---

## 8. Research Gap Identification

### High-Potential Research Components

#### 1. OCR Preprocessing Optimization (HIGH Priority)
**Research Question**: Does CLAHE preprocessing improve medical document OCR accuracy?

**Why It Matters**: 
- Handwritten prescriptions have high error rates (Kim et al. 2026: 87.2% after GPT-4o correction)
- Your specific preprocessing pipeline (CLAHE clipLimit=2.0, Gaussian 3×3, adaptive threshold) is not benchmarked in literature

**What You Have**:
- ✅ Working preprocessing pipeline (`ocr_service.py`)
- ✅ 3-4 sample images

**What You Need**:
- ❌ 100+ manually transcribed reports (ground truth)
- ❌ Preprocessing ON vs OFF comparison
- ❌ CER/WER measurements
- ❌ Tesseract baseline

**Publication Potential**: IEEE EMBC, SPIE Medical Imaging

---

#### 2. Multi-LLM Comparison for Medical Simplification (HIGH Priority)
**Research Question**: How do different LLMs compare for medical jargon simplification?

**Why It Matters**:
- Kim et al. 2026 showed GPT-4o improved patient comprehension 40→56.5 (PPQ scale)
- No published comparison of Gemini vs GPT-4o vs Claude for this specific task

**What You Have**:
- ✅ Working Gemini 3.6 Flash integration
- ✅ Structured simplification prompts

**What You Need**:
- ❌ GPT-4o API integration
- ❌ Claude API integration
- ❌ 50+ doctor ratings (PEMAT scale)
- ❌ Patient comprehension testing
- ❌ Hallucination rate measurement

**Publication Potential**: AMIA, ACM CHASE, JAMIA

---

#### 3. End-to-End Pipeline Benchmark (HIGH Priority)
**Research Question**: What is the accuracy, latency, and cost of the integrated OCR-to-LLM pipeline?

**Why It Matters**:
- No published work evaluates full medical document → simplified explanation pipeline
- Trade-offs between preprocessing, OCR engine, and LLM choice are unexplored

**What You Have**:
- ✅ Complete pipeline implementation
- ✅ EasyOCR + Gemini integration

**What You Need**:
- ❌ End-to-end accuracy measurements
- ❌ Latency profiling (OCR time, LLM time, total time)
- ❌ Cost analysis (API calls × volume)
- ❌ Comparison to Tesseract + GPT-4o baseline

**Publication Potential**: IEEE EMBC, ACM CHASE

---

#### 4. Patient Comprehension Validation (MEDIUM Priority)
**Research Question**: Does AI-simplified medical text improve patient understanding?

**Why It Matters**:
- Kim et al. 2026 showed 40% comprehension improvement
- Your system needs user validation to claim benefit

**What You Have**:
- ✅ Working simplification feature

**What You Need**:
- ❌ IRB approval (human subjects research)
- ❌ 30+ patient participants
- ❌ Pre-post comprehension testing
- ❌ Control group (original text)
- ❌ Statistical analysis

**Publication Potential**: AMIA, Journal of Medical Internet Research

**Timeline**: 4-6 months (IRB approval is slow)

---

## 9. Research Questions (Prioritized)

### RQ1: OCR Preprocessing Impact (Can start immediately)
**Does CLAHE preprocessing (clipLimit=2.0, tileGridSize=8×8) + Gaussian blur (3×3) + adaptive thresholding improve OCR accuracy on medical documents compared to no preprocessing?**

**Metrics**: CER, WER, extraction accuracy  
**Dataset**: 100 manually transcribed reports  
**Baseline**: EasyOCR without preprocessing  
**Time**: 2-3 weeks

---

### RQ2: LLM Comparison (Needs API access)
**How do Gemini 3.6 Flash, GPT-4o, and Claude 3.5 Sonnet compare for medical jargon simplification in terms of readability, clinical accuracy, and hallucination rate?**

**Metrics**: PEMAT score, clinical accuracy (doctor ratings), hallucination rate, Flesch-Kincaid grade  
**Dataset**: 50 medical reports with doctor-rated simplifications  
**Baseline**: Original medical text  
**Time**: 4-6 weeks

---

### RQ3: Patient Comprehension (Requires IRB)
**Does AI-simplified medical text improve patient comprehension compared to original medical documents?**

**Metrics**: PPQ (Patient Preparation Questionnaire), comprehension score, confidence rating  
**Dataset**: 30+ patients, IRB-approved study  
**Baseline**: Control group with original text  
**Time**: 3-4 months (including IRB approval)

---

### RQ4: Latency-Accuracy-Cost Trade-offs
**What are the trade-offs between OCR engine, preprocessing intensity, and LLM choice in terms of accuracy, latency, and API cost?**

**Metrics**: End-to-end latency, cost per document, accuracy (CER + clinical accuracy)  
**Conditions**: 4 OCR engines × 3 preprocessing levels × 3 LLMs = 36 configurations  
**Time**: 2-3 weeks

---

## 10. Missing Evaluation Metrics

### OCR Accuracy
- ❌ **Character Error Rate (CER)**: Characters wrong / total characters
- ❌ **Word Error Rate (WER)**: Words wrong / total words
- ❌ **Extraction Accuracy**: % of medications/diagnoses correctly extracted
- ❌ **Preprocessing Impact**: Accuracy with vs without CLAHE/blur/threshold

### LLM Quality
- ❌ **PEMAT Score**: Patient Education Materials Assessment Tool (0-100)
- ❌ **Flesch-Kincaid Grade Level**: Target = 6th-8th grade
- ❌ **Clinical Accuracy**: % of medical facts preserved correctly
- ❌ **Hallucination Rate**: % of added facts not in source
- ❌ **Factual Consistency**: BERT-Score or NLI-based verification

### Patient Comprehension
- ❌ **PPQ Score**: Patient Preparation Questionnaire (Kim et al. 2026)
- ❌ **Comprehension Test**: Multiple choice questions about report
- ❌ **Confidence Rating**: Patient's confidence in understanding (1-5 scale)
- ❌ **Actionability**: Can patient explain next steps?

### System Performance
- ❌ **OCR Latency**: Time to extract text from image
- ❌ **LLM Latency**: Time to generate simplification
- ❌ **End-to-End Latency**: Total time per document
- ❌ **Throughput**: Documents processed per hour
- ❌ **Cost**: API cost per document

### Security & Privacy
- ❌ **Authentication Coverage**: % of endpoints requiring auth
- ❌ **Data Encryption**: At-rest and in-transit verification
- ❌ **HIPAA Compliance**: Audit trail, access logs
- ❌ **Penetration Testing**: Security audit results

### Usability
- ❌ **Task Completion Rate**: % of users who successfully upload & view report
- ❌ **Time on Task**: Seconds to complete key workflows
- ❌ **Error Rate**: User errors per session
- ❌ **Satisfaction**: System Usability Scale (SUS) score

---

## 11. Required Datasets for Publication

### Dataset 1: OCR Evaluation (100-150 medical reports)
**Purpose**: Measure CER, WER, extraction accuracy  
**Format**: Image + manual transcription + structured data ground truth  
**Sources**: Public (MIMIC-III) or collect from hospitals (requires IRB)  
**Annotations Needed**: 
- Full text transcription
- Bounding boxes for key entities (medications, diagnoses)
- Structured JSON (medicines, dosages, frequencies)

### Dataset 2: LLM Evaluation (50+ simplification pairs)
**Purpose**: Measure PEMAT, clinical accuracy, hallucination rate  
**Format**: Original medical text + AI simplification + doctor ratings  
**Experts Needed**: 5-10 licensed physicians  
**Rating Criteria**:
- PEMAT score (14 items, yes/no/N/A)
- Clinical accuracy (5-point Likert scale)
- Hallucination presence (binary + severity)
- Overall quality (1-5 scale)

### Dataset 3: Patient Comprehension (30+ participants)
**Purpose**: Measure PPQ, comprehension improvement  
**Format**: Pre-post testing with control group  
**Requirements**: IRB approval, informed consent  
**Protocol**:
- Randomized assignment (AI-simplified vs original)
- Pre-test (baseline comprehension)
- Intervention (read medical report)
- Post-test (comprehension questions, PPQ)
- Follow-up (optional, 1 week later)

### Dataset 4: Baseline Comparison
**Purpose**: Compare to Tesseract OCR, GPT-4o, Claude  
**Format**: Same 100 reports processed by all systems  
**Outputs**:
- Tesseract OCR transcriptions
- GPT-4o simplifications
- Claude 3.5 Sonnet simplifications
- Cost logs (API usage)
- Latency logs (processing time)

---

## 12. Recommended Next Actions

### Immediate (Week 1-2)

1. **Fix Documentation**
   - Remove "multi-agent" claims from README
   - Clarify architecture: "Medical Document Intelligence Pipeline with OCR & LLM"
   - Update system diagram to show actual architecture

2. **Decide Research Focus**
   - Choose 1-2 research components from RQ1-RQ4
   - Prioritize based on: novelty, feasibility, publication venue

3. **Dataset Strategy Decision**
   - Option A: Use public MIMIC-III dataset (faster, no IRB)
   - Option B: Collect hospital data (more realistic, requires IRB + partnerships)

### Short-Term (Month 1)

4. **Implement Baselines**
   - Add Tesseract OCR integration
   - Get GPT-4o API access (OpenAI)
   - Get Claude API access (Anthropic)

5. **Create Ground Truth**
   - Manually transcribe 50 sample reports
   - Create structured JSON annotations
   - Recruit 2-3 medical students to help

6. **Basic Metrics**
   - Implement CER/WER calculation
   - Implement Flesch-Kincaid readability
   - Log latency and cost for all API calls

7. **Expert Recruitment**
   - Recruit 5-10 doctors for LLM rating task
   - Create PEMAT rating interface
   - Pilot test with 5 reports

### Medium-Term (Month 2-3)

8. **Run Experiments**
   - OCR: Preprocessing ON vs OFF (50 reports)
   - LLM: Gemini vs GPT-4o vs Claude (50 reports)
   - End-to-end: Latency and cost profiling

9. **Statistical Analysis**
   - Paired t-tests for OCR accuracy
   - ANOVA for LLM comparison
   - Inter-rater reliability (Krippendorff's alpha)

10. **Patient Comprehension Study** (if choosing RQ3)
    - Submit IRB application
    - Recruit 30+ participants
    - Run pre-post testing
    - Analyze results

### Long-Term (Month 4-6)

11. **Draft Paper**
    - Introduction (problem, gap, contribution)
    - Related work (50+ citations)
    - Methods (system architecture, evaluation protocol)
    - Results (tables, figures, statistical tests)
    - Discussion (limitations, future work)

12. **Target Conferences**
    - **IEEE EMBC** (Engineering in Medicine and Biology Conference) - July deadline
    - **AMIA** (American Medical Informatics Association) - March/August deadlines
    - **ACM CHASE** (Connected Health Applications, Systems, and Engineering) - April deadline
    - **SPIE Medical Imaging** - September deadline

---

## 13. Research Positioning

### What Your System Actually Is
**"An Integrated OCR-to-LLM Pipeline for Medical Document Understanding and Patient Communication"**

**NOT**: Multi-agent system, orchestrated AI, agentic framework  
**IS**: Layered pipeline combining preprocessing, OCR, and LLM simplification

### Novelty Claims (What You Can Defensibly Claim)

✅ **Can Claim**:
- First evaluation of CLAHE preprocessing for medical document OCR
- Comparison of Gemini vs GPT-4o vs Claude for medical simplification
- End-to-end pipeline integrating QR-based health IDs
- Open-source implementation with full reproducibility

❌ **Cannot Claim (Yet)**:
- "Improves OCR accuracy" (no measurements)
- "Better than baseline" (no baselines)
- "Patients understand better" (no user study)
- "Multi-agent coordination" (not implemented)

### Competitive Positioning
**Compared to Kim et al. 2026 (Nature Digital Medicine)**:
- They used: GPT-4o for prescription correction (PPQ: 40→56.5)
- You have: OCR preprocessing + Gemini 3.6 Flash (no evaluation yet)
- Your gap: Preprocessing optimization, multi-LLM comparison

**Compared to Zaretsky et al. 2024 (JAMA)**:
- They used: LLMs to simplify discharge summaries
- You have: Medical reports + prescriptions (broader scope)
- Your gap: Patient comprehension validation

---

## 14. Final Summary Table

| Category | Status | What Exists | What's Missing | Priority |
|----------|--------|-------------|----------------|----------|
| **Implementation** | 76% complete | 42 working features, clean architecture | PDF OCR, real-time notifications, payment | LOW (engineering) |
| **Dataset** | 3-4 samples | Sample medical images | 100+ annotated reports, ground truth transcriptions | HIGH (blocker) |
| **OCR Evaluation** | 0% | Preprocessing pipeline code | CER, WER, extraction accuracy measurements | HIGH (RQ1) |
| **LLM Evaluation** | 0% | Gemini integration | PEMAT scores, doctor ratings, hallucination analysis | HIGH (RQ2) |
| **Baselines** | 0% | EasyOCR + Gemini | Tesseract OCR, GPT-4o, Claude comparisons | HIGH (required) |
| **Patient Study** | 0% | Simplification feature | IRB approval, 30+ participants, PPQ scores | MEDIUM (RQ3) |
| **Performance** | 0% | Working system | Latency logs, throughput benchmarks, cost analysis | MEDIUM (RQ4) |
| **Security Audit** | 0% | JWT auth, bcrypt | Penetration testing, HIPAA compliance verification | LOW (engineering) |
| **Documentation** | 80% | README, comments | Correct architecture description (fix multi-agent claim) | HIGH (critical) |
| **Reproducibility** | 60% | Docker setup | Evaluation scripts, dataset download, baseline implementations | HIGH (required) |

---

## 15. Estimated Timeline to Publication

### Conservative Path (6 months)
- **Month 1**: Fix documentation, implement baselines, create 50-report ground truth
- **Month 2**: Run OCR experiments (RQ1), implement CER/WER metrics
- **Month 3**: Run LLM experiments (RQ2), recruit doctors for ratings
- **Month 4**: Analyze results, statistical testing, write paper draft
- **Month 5**: Patient comprehension study (if time permits)
- **Month 6**: Revisions, submit to IEEE EMBC or AMIA

### Aggressive Path (3 months) - OCR Focus Only
- **Month 1**: Fix documentation, implement Tesseract baseline, 100-report ground truth
- **Month 2**: Run preprocessing ON vs OFF experiments, CER/WER analysis
- **Month 3**: Write paper, submit to SPIE Medical Imaging

### Realistic Recommendation: **4 months**
- Focus on RQ1 (OCR) + RQ2 (LLM) without patient study
- Use public MIMIC-III dataset to avoid IRB delays
- Target IEEE EMBC (July deadline) or ACM CHASE (April deadline)

---

## 16. Conference Target Recommendations

### Tier 1 (Best Fit)
1. **IEEE EMBC** - Engineering focus, OCR + LLM pipeline fits well
2. **AMIA Annual Symposium** - Medical informatics, clinical validation valued
3. **ACM CHASE** - Digital health systems, engineering rigor

### Tier 2 (Good Fit)
4. **SPIE Medical Imaging** - OCR preprocessing focus
5. **IEEE BHI** - Biomedical and Health Informatics
6. **PervasiveHealth** - mHealth applications

### Tier 3 (Possible)
7. **CHI** (ACM Conference on Human Factors) - If patient study is strong
8. **JAMIA** (Journal) - Requires clinical validation
9. **Nature Digital Medicine** (Journal) - High bar, needs all 4 research components

---

## Conclusion

**Your MediNova project is a solid engineering implementation (76% complete) but needs 3-6 months of research work before it's ready for academic publication.**

### Strengths ✅
- Clean, modular architecture
- Working OCR + LLM integration
- Comprehensive feature set
- Open-source and reproducible

### Critical Gaps ❌
- No experimental validation (0% evaluated)
- No ground truth dataset
- No baseline comparisons
- Documentation claims don't match implementation

### Recommended Path Forward
1. **Fix documentation** (remove "multi-agent" claim)
2. **Choose research focus**: OCR preprocessing (RQ1) + LLM comparison (RQ2)
3. **Create 100-report dataset** with manual transcriptions
4. **Implement baselines**: Tesseract, GPT-4o
5. **Run experiments**: Measure CER, WER, PEMAT
6. **Draft paper**: Target IEEE EMBC or AMIA
7. **Submit in 4 months**

### Final Research Readiness Score

```
┌─────────────────────────────────────┐
│  RESEARCH READINESS: 4/10           │
├─────────────────────────────────────┤
│  Implementation:    ████████ 8/10   │
│  Dataset:           █ 1/10          │
│  Evaluation:        ░ 0/10          │
│  Baselines:         ██ 2/10         │
│  Documentation:     ███████ 7/10    │
│  Reproducibility:   █████ 5/10      │
└─────────────────────────────────────┘

STATUS: NOT READY FOR PUBLICATION
ACTION: Complete evaluation pipeline
        before submitting to conferences
```

---

**Next Steps**: Choose your research focus (RQ1-RQ4) and I can help you design the experimental protocol, create evaluation scripts, and plan the paper structure.
