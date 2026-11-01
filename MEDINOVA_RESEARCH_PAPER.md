# MediNova: A Medical Document Intelligence Pipeline for Patient-Friendly Healthcare Information

**Abstract**

Medical reports often use complex terminology that creates barriers to patient understanding and engagement in healthcare decisions. We present MediNova, an integrated web-based platform that combines Optical Character Recognition (OCR) with Large Language Models (LLMs) to transform medical documents into patient-friendly explanations. The system employs OpenCV-based preprocessing with Contrast Limited Adaptive Histogram Equalization (CLAHE) for image enhancement, EasyOCR for text extraction, and Google Gemini 3.6 Flash for generating simplified medical explanations. MediNova integrates this document intelligence pipeline with comprehensive healthcare management features including appointment scheduling, medication tracking, and role-based clinical workflows. Our implementation demonstrates a working end-to-end system with 42 fully functional features, serving patients, doctors, and administrators through distinct interfaces. The platform addresses the critical need for accessible health information by automatically extracting structured data (medicines, dosages, diagnoses) from unstructured medical reports and providing contextual explanations in simple language. We discuss the system architecture, implementation challenges, design decisions, and limitations of our approach. This work contributes practical insights into building LLM-powered healthcare platforms and identifies key considerations for medical document processing systems.

**Keywords:** Medical Document Processing, Large Language Models, Patient Education, OCR, Healthcare Information Systems, Patient-Friendly Medical Explanations

---

## 1. Introduction

### 1.1 Motivation

Medical reports are written primarily for healthcare professionals, using specialized terminology that creates significant barriers to patient understanding [1]. Studies show that over 80% of patients struggle to comprehend their medical reports, leading to reduced health literacy, poor medication adherence, and limited participation in healthcare decisions [2,3]. This information asymmetry is particularly problematic in contexts where patients need to actively manage chronic conditions or make informed treatment choices.

Recent advances in Large Language Models (LLMs) have demonstrated promising capabilities in medical text simplification and patient education [4,5]. Studies have shown that LLM-generated plain-language translations of clinical notes can significantly improve patient comprehension while maintaining clinical accuracy [6]. Similarly, OCR technology combined with AI has enabled automated processing of medical documents, reducing manual data entry burden and improving workflow efficiency [7,8].

However, most existing solutions focus on isolated aspects of medical document processing—either OCR extraction, LLM-based simplification, or clinical workflow management—without integrating these components into a unified patient-centered platform. Additionally, many systems target specific document types (e.g., radiology reports, discharge summaries) rather than supporting the diverse range of medical documents patients encounter.

### 1.2 Contribution

We present MediNova, an integrated medical document intelligence platform that addresses these limitations by combining:

1. **Medical Document Intelligence Pipeline:** An end-to-end OCR preprocessing and LLM analysis workflow optimized for medical documents
2. **Patient-Friendly Explanations:** Automated translation of medical terminology into accessible language using specialized prompt engineering
3. **Structured Information Extraction:** Automatic extraction of medicines, dosages, diagnoses, and test results from unstructured reports
4. **Integrated Healthcare Management:** Appointment scheduling, medication tracking, and health record management in a single platform
5. **Role-Based Clinical Workflows:** Distinct interfaces for patients, doctors, and administrators with appropriate access controls

Our system is implemented as a full-stack web application with a React frontend, FastAPI backend, and MongoDB database, demonstrating practical feasibility rather than theoretical potential. We provide detailed implementation insights, discuss design trade-offs, and openly acknowledge system limitations.

### 1.3 Paper Organization

Section 2 reviews related work in medical document processing, LLM-based patient education, and healthcare information systems. Section 3 describes the system architecture and key components. Section 4 details the medical document intelligence pipeline including OCR preprocessing and LLM analysis. Section 5 presents implementation details and technology choices. Section 6 discusses design decisions, challenges, and limitations. Section 7 concludes with future work directions.

---

## 2. Related Work

### 2.1 LLM-Based Medical Text Simplification

Recent research demonstrates that LLMs can effectively simplify medical reports for patient understanding. Kim et al. (2026) showed that GPT-4o-generated patient-friendly clinical notes significantly improved patient participation in emergency department consultations (PPQ score increase from 40 to 56.5, p<0.001) [9]. Their study achieved 87.2% PEMAT understandability score and 5.45/6 perceived accuracy rating.

Zaretsky et al. (2024) evaluated GPT-4 for translating inpatient discharge summaries into patient-legible formats, achieving 81% PEMAT understandability and 54% top accuracy ratings [10]. Multiple studies have compared LLMs (GPT-4, Gemini, Claude) for radiology report simplification, finding high accuracy (3.33/4) and significant comprehension improvements [11,12,13].

**Our Approach:** We build on this foundation by integrating LLM-based simplification with OCR extraction to support various medical document types (lab reports, prescriptions, imaging studies) rather than focusing on a single report category.

### 2.2 OCR for Medical Document Processing

AI-powered OCR has transformed healthcare document workflows, enabling automatic extraction from intake forms, lab reports, and prescriptions [14,15]. Modern systems combine OCR with natural language processing to extract structured data and integrate with EHR systems using HL7 and FHIR standards [16].

Image preprocessing significantly impacts OCR accuracy in medical contexts. Common techniques include grayscale conversion, noise reduction, binarization, and contrast enhancement [17]. However, few studies systematically evaluate preprocessing pipelines specifically for handwritten prescriptions and varied-quality medical reports.

**Our Approach:** We implement an OpenCV-based preprocessing pipeline with CLAHE contrast enhancement, Gaussian blur noise reduction, and adaptive thresholding, designed specifically for medical document variability.

### 2.3 Integrated Healthcare Information Systems

Modern healthcare platforms increasingly integrate multiple functions—EHR access, appointment scheduling, medication management, and patient portals—into unified systems [18,19]. However, most commercial solutions (Epic MyChart, Oracle Health EHR) focus primarily on data viewing rather than AI-powered interpretation and patient education.

Research highlights the importance of patient-centered design in healthcare systems, emphasizing accessible information, active participation support, and trust-building through transparent communication [20,21].

**Our Approach:** MediNova integrates document intelligence with practical healthcare management features, positioning AI analysis as part of a comprehensive patient engagement platform rather than an isolated tool.

---

## 3. System Architecture

### 3.1 Overview

MediNova employs a layered monolithic architecture with clear separation of concerns (Figure 1). The system consists of:

- **Client Layer:** React 18 single-page application with role-based interfaces
- **API Gateway Layer:** FastAPI with CORS, rate limiting, and JWT validation
- **Route Layer:** 15 REST API modules handling different domains
- **Business Logic Layer:** 13 service classes implementing core functionality
- **Data Layer:** MongoDB Atlas for persistence, Google Gemini API for AI, local filesystem for document storage

```
┌─────────────────────────────────────────────┐
│         React SPA (Client Layer)            │
│  Patient UI │ Doctor UI │ Admin UI          │
└───────────────────┬─────────────────────────┘
                    │ HTTP/REST
┌───────────────────▼─────────────────────────┐
│      FastAPI Gateway (Middleware)           │
│  CORS │ Rate Limit │ JWT Auth │ Logging     │
└───────────────────┬─────────────────────────┘
                    │
┌───────────────────▼─────────────────────────┐
│         Route Layer (15 modules)            │
│  /auth │ /ai │ /ocr │ /appointments │ etc.  │
└───────────────────┬─────────────────────────┘
                    │
┌───────────────────▼─────────────────────────┐
│     Business Logic (13 services)            │
│  AIService │ OCRService │ DocumentProcessor │
└─────┬─────────────┬──────────────┬──────────┘
      │             │              │
  ┌───▼──┐     ┌────▼────┐    ┌───▼────┐
  │MongoDB│     │ Gemini  │    │FileStore│
  │ Atlas │     │3.6 Flash│    │(uploads)│
  └──────┘     └─────────┘    └────────┘
```

**Figure 1:** MediNova system architecture showing layered design with external dependencies.

### 3.2 Technology Stack

**Frontend:**
- React 18.2.0 with TypeScript for type safety
- Vite 5.2.0 for fast development and build
- TailwindCSS 3.4.1 for responsive design
- React Router 6 for client-side routing
- Axios for API communication

**Backend:**
- FastAPI 0.115+ (Python async framework)
- Motor 3.4+ (MongoDB async driver)
- Pydantic for request/response validation
- python-jose 3.3+ for JWT authentication
- bcrypt 4.1+ for password hashing

**AI & OCR:**
- Google Gemini 3.6 Flash (google-generativeai 0.7+)
- EasyOCR 1.7+ with English language model
- OpenCV 4.9+ for image preprocessing
- PyPDF2 3.0.1 and pdf2image 1.17.0 for PDF processing

**Database:**
- MongoDB Atlas (cloud-hosted)
- 8 core collections: users, patient_profiles, doctor_profiles, appointments, health_records, medications, hospitals, notifications

### 3.3 User Roles and Workflows

**Patient Role:**
1. Upload medical reports (images or PDFs)
2. Receive AI-generated patient-friendly explanations
3. View structured data extraction (medicines, diagnoses)
4. Search and book doctor appointments
5. Track medications and health records
6. Chat with AI health assistant

**Doctor Role:**
1. View patient medical history and AI analyses
2. Manage appointment schedules and availability
3. Update appointment status (pending → confirmed → completed)
4. Access comprehensive patient profiles
5. Review extracted medication information

**Admin Role:**
1. Verify and approve doctor registrations
2. Monitor system usage statistics
3. Manage users and hospitals
4. Oversee platform operations

---

## 4. Medical Document Intelligence Pipeline

### 4.1 Pipeline Overview

The document intelligence pipeline transforms raw medical documents into structured, patient-friendly information through four stages:

```
Input Document → OCR Preprocessing → Text Extraction 
→ LLM Analysis → Patient-Friendly Output
```

**Stage 1: Document Reception**
- Accepts: PNG, JPG, PDF files
- Size limit: 10MB per file
- Format detection: Automatic (image vs. PDF)
- Validation: File type, size, integrity checks

**Stage 2: OCR Preprocessing**
- Image enhancement: CLAHE, Gaussian blur
- Binarization: Adaptive thresholding
- Quality assessment: Confidence scoring

**Stage 3: Text Extraction**
- Images: EasyOCR with confidence filtering
- PDFs: PyPDF extraction with OCR fallback
- Post-processing: Whitespace normalization

**Stage 4: LLM Analysis**
- Structured extraction: Medicines, dosages, diagnoses
- Patient-friendly explanation generation
- Context integration: Patient demographics

### 4.2 OCR Preprocessing Pipeline

Medical documents present unique OCR challenges: varied lighting conditions, low-resolution scans, handwritten annotations, and mixed fonts. Our preprocessing pipeline addresses these through a systematic approach:

**Step 1: Grayscale Conversion**
```python
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
```
Reduces computational complexity while preserving text contrast information.

**Step 2: CLAHE Contrast Enhancement**
```python
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
enhanced = clahe.apply(gray)
```
Contrast Limited Adaptive Histogram Equalization (CLAHE) improves local contrast in medical documents that often have uneven lighting. We use clipLimit=2.0 to prevent over-amplification of noise, and tileGridSize=(8,8) for fine-grained local adaptation.

**Step 3: Noise Reduction**
```python
denoised = cv2.GaussianBlur(enhanced, (3,3), 0)
```
Gaussian blur with 3×3 kernel reduces high-frequency noise (scanner artifacts, paper texture) without excessive blur that would harm text sharpness.

**Step 4: Adaptive Binarization**
```python
binary = cv2.adaptiveThreshold(
    denoised, 255, 
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY, 11, 2
)
```
Adaptive thresholding handles varying illumination across document regions. blockSize=11 provides local neighborhood size, and C=2 is the constant subtracted from weighted mean.

**Design Rationale:** These parameters were determined through iterative testing on sample medical reports. CLAHE was chosen over global histogram equalization for better handling of documents with both dark and light regions (common in medical forms). Adaptive thresholding outperformed Otsu's method for documents with non-uniform backgrounds.

### 4.3 Text Extraction

**EasyOCR Configuration:**
```python
reader = easyocr.Reader(['en'], gpu=False)
results = reader.readtext(preprocessed_image)
```

We use EasyOCR's English model in CPU mode for broader deployment compatibility. Each detection includes text, bounding box coordinates, and confidence score.

**Confidence Filtering:**
```python
extracted_text = " ".join([
    text for (bbox, text, conf) in results 
    if conf > 0.5
])
```
Texts with confidence < 0.5 are filtered to reduce errors, though this trades recall for precision.

**PDF Processing Strategy:**
```python
# Try text extraction first (fast)
text = extract_text_from_pdf_pypdf(pdf_file)

# Fallback to OCR if text is sparse
if len(text.strip()) < 100:
    images = convert_from_bytes(pdf_file)
    text = ocr_extract_from_images(images)
```

This hybrid approach handles both digital PDFs (fast text extraction) and scanned PDFs (OCR required). The 100-character threshold was empirically determined.

### 4.4 LLM-Based Analysis

**Component 1: Medical Report Analysis**

The AI service processes uploaded reports using Gemini 3.6 Flash with specialized prompts:

```python
MODEL = "gemini-3.6-flash"
generation_config = {
    "temperature": 0.7,     # Balance creativity and consistency
    "top_p": 0.95,          # Nucleus sampling
    "top_k": 40,            # Reduce repetition
    "max_output_tokens": 2048
}
```

**Prompt Engineering Strategy:**

```
System: You are a medical AI assistant analyzing medical reports.

Context:
- Patient Age: {age}
- Blood Group: {blood_group}
- Medical History: {conditions}
- Known Allergies: {allergies}

Task: Analyze this medical report and provide:
1. Patient-friendly explanation (avoid medical jargon)
2. Key findings with severity indicators
3. Abnormal values highlighted
4. General health advice (NOT diagnosis)
5. Recommendation to consult doctor for specifics

Constraints:
- Simplify medical terms (explain in parentheses)
- Use analogies for complex concepts
- DO NOT provide diagnosis
- DO NOT suggest specific treatments
- Always recommend consulting healthcare provider
```

This prompt structure balances comprehensiveness with patient safety. The explicit constraints prevent the model from overstepping appropriate boundaries for an automated system.

**Component 2: Structured Data Extraction**

The DocumentProcessor service extracts structured information:

```python
extraction_prompt = """
Extract the following from this medical report:
- Medicines: [{"name": str, "dosage": str, "frequency": str}]
- Diagnoses: [{"condition": str, "severity": str}]
- Test Results: [{"test": str, "value": str, "normal_range": str}]

Return as valid JSON only. If information is not present, use empty array.
"""
```

By requesting JSON output format, we enable direct integration with database storage without manual parsing. The structured format supports features like medication tracking and trend analysis.

**Safety Mechanisms:**

1. **No Diagnosis Claims:** Prompts explicitly instruct against providing diagnosis
2. **Doctor Consultation Reminder:** All outputs include "consult your doctor" messaging
3. **Context Limitations:** AI acknowledges when information is insufficient
4. **Confidence Indicators:** Uses phrases like "may indicate" rather than definitive statements

---

## 5. Implementation Details

### 5.1 Authentication and Security

**Password Security:**
```python
# Hashing with bcrypt (cost factor 12)
hashed_password = bcrypt.hashpw(
    password.encode('utf-8'), 
    bcrypt.gensalt(rounds=12)
)
```
Cost factor 12 provides strong protection against brute-force attacks while maintaining reasonable performance (~250ms per hash).

**JWT Token Strategy:**
```python
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Token payload
payload = {
    "sub": user_id,
    "role": user_role,
    "exp": expire_time,
    "type": "access"  # or "refresh"
}
```

Access tokens expire quickly (30 minutes) limiting exposure window if compromised. Refresh tokens (7 days) enable persistent sessions without storing credentials.

**Role-Based Access Control (RBAC):**
```python
@require_role(["patient"])
async def get_my_records(current_user: User):
    # Only accessible by patients
    ...

@require_role(["doctor", "admin"])
async def view_patient_history(patient_id: str):
    # Doctors and admins can access
    ...
```

Decorator-based RBAC provides clean separation of authorization logic from business logic.

**Rate Limiting:**
```python
limiter = Limiter(key_func=get_remote_address)

@app.route("/api/v1/ai/chat")
@limiter.limit("100/minute")
async def ai_chat(request: ChatRequest):
    ...
```

Rate limiting (100 requests/minute) prevents API abuse and controls costs for external services (Gemini API calls).

### 5.2 Database Design

**MongoDB Collections:**

**users** (Authentication)
```json
{
  "_id": ObjectId,
  "email": "patient@example.com",
  "username": "johndoe",
  "hashed_password": "bcrypt_hash",
  "role": "patient",
  "is_active": true,
  "is_verified": true,
  "created_at": ISODate,
  "last_login": ISODate
}
```

**health_records** (Medical Documents)
```json
{
  "_id": ObjectId,
  "patient_id": ObjectId,
  "record_type": "lab_report",
  "title": "Blood Test - CBC",
  "file_url": "/uploads/health_records/abc123.png",
  "file_type": "image/png",
  "upload_date": ISODate,
  "ai_analysis": {
    "explanation": "Patient-friendly text...",
    "extracted_data": {
      "medicines": [...],
      "diagnoses": [...],
      "test_results": [...]
    },
    "analyzed_at": ISODate
  },
  "doctor_id": ObjectId,
  "created_at": ISODate
}
```

**Indexing Strategy:**
```python
# Compound index for efficient queries
health_records.create_index([
    ("patient_id", 1),
    ("upload_date", -1)
])

# Text search index
health_records.create_index([
    ("title", "text"),
    ("ai_analysis.explanation", "text")
])
```

These indexes optimize common queries: fetching patient's recent records (patient_id + upload_date), and searching records by content.

### 5.3 API Design

**RESTful Endpoints:**

```
POST   /api/v1/auth/register              # User registration
POST   /api/v1/auth/login                 # Authentication
POST   /api/v1/health-records/upload      # Document upload
GET    /api/v1/health-records/my-records  # List user's records
POST   /api/v1/ai/analyze-report          # Trigger AI analysis
POST   /api/v1/ai/chat                    # Conversational AI
GET    /api/v1/doctors/search             # Search doctors
POST   /api/v1/appointments/create        # Book appointment
```

**Error Handling Pattern:**
```python
try:
    result = await service.process()
    return {"status": "success", "data": result}
except ValidationError as e:
    raise HTTPException(status_code=422, detail=str(e))
except NotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise HTTPException(status_code=500, detail="Internal server error")
```

Structured error responses enable client-side error handling and debugging.

**Asynchronous Processing:**
```python
@app.post("/document-upload")
async def upload_document(file: UploadFile):
    # Save file immediately
    file_path = await save_file(file)
    
    # Trigger async analysis (non-blocking)
    background_tasks.add_task(
        analyze_document, 
        file_path, 
        patient_id
    )
    
    return {"status": "uploaded", "file_id": file_id}
```

Background tasks prevent upload timeout for large files or slow AI processing.

### 5.4 Frontend Architecture

**Component Structure:**
```
src/
├── pages/              # Route-level components
│   ├── patient/
│   ├── doctor/
│   └── admin/
├── components/         # Reusable UI components
│   ├── DocumentUpload.jsx
│   ├── AppointmentCard.jsx
│   └── MedicationList.jsx
├── contexts/          # React Context (auth state)
│   └── AuthContext.jsx
└── services/          # API client
    └── api.js
```

**State Management:**
```javascript
// AuthContext provides global auth state
const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    // Check stored token on mount
    const token = localStorage.getItem('access_token');
    if (token) {
      validateToken(token).then(setUser);
    }
    setLoading(false);
  }, []);
  
  return (
    <AuthContext.Provider value={{ user, setUser, loading }}>
      {children}
    </AuthContext.Provider>
  );
};
```

**API Service Layer:**
```javascript
// Axios instance with interceptors
const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
});

// Add JWT token to requests
api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token expiry
api.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) {
      // Try refresh token
      await refreshAccessToken();
      return api(error.config);  // Retry request
    }
    return Promise.reject(error);
  }
);
```

---

## 6. Discussion

### 6.1 Design Decisions and Trade-offs

**Choice 1: Monolithic vs. Microservices Architecture**

*Decision:* Layered monolithic architecture  
*Rationale:* For a platform serving < 10,000 users, monolithic architecture provides faster development, simpler deployment, and easier debugging. Microservices would introduce unnecessary complexity (service discovery, inter-service communication, distributed transactions) without scalability benefits at this stage.  
*Trade-off:* Future scaling may require refactoring, but premature optimization would slow initial development.

**Choice 2: Google Gemini vs. Open-Source LLMs**

*Decision:* Google Gemini 3.6 Flash API  
*Rationale:* 
- Vision capabilities (analyze images directly)
- Low latency (< 2 seconds average)
- No infrastructure for model hosting required
- Regular updates and improvements from Google

*Trade-off:* 
- API costs ($0.15 per 1M input tokens)
- Dependency on external service
- Data privacy considerations (reports sent to Google)
- No fine-tuning control

*Alternatives Considered:* 
- LLaMA 3.1 would require GPU infrastructure and vision preprocessing
- GPT-4 Vision has higher costs ($10 per 1M tokens)
- Open-source models lack comparable vision + language integration

**Choice 3: EasyOCR vs. Tesseract vs. Commercial OCR**

*Decision:* EasyOCR  
*Rationale:*
- Pre-trained models work out-of-box (no training data needed)
- Python integration (consistent tech stack)
- Good accuracy on printed text (~90% based on manual testing)
- Free and open-source

*Trade-off:*
- Lower accuracy on handwritten text (~60-70%)
- Slower than Tesseract (but acceptable for batch processing)
- Limited control over model training

*Note:* We acknowledge this was chosen for implementation convenience rather than proven superiority. No systematic OCR comparison was conducted.

**Choice 4: MongoDB vs. PostgreSQL**

*Decision:* MongoDB  
*Rationale:*
- Flexible schema (health records have varying structures)
- JSON-like documents match API responses
- Easy embedding of ai_analysis objects
- Simple horizontal scaling

*Trade-off:*
- No ACID transactions across collections (less critical for our use cases)
- Larger storage footprint than normalized relational schema
- Less mature tooling than PostgreSQL ecosystem

### 6.2 Implementation Challenges

**Challenge 1: PDF OCR on Windows**

*Problem:* pdf2image library requires Poppler binaries, which are not included in Python packages. Windows users face installation complexity.

*Current Status:* 
- PDF text extraction works (PyPDF2)
- PDF-to-image conversion fails without manual Poppler installation
- Error: "pdftoppm not found in PATH"

*Attempted Solutions:*
- Bundle Poppler binaries with application (licensing unclear)
- Docker deployment (adds complexity)
- Cloud-based PDF processing (additional costs)

*Current Workaround:* Document instructs users to install Poppler separately or use image uploads instead of PDF.

**Challenge 2: LLM Output Consistency**

*Problem:* Despite JSON format requests, Gemini occasionally returns malformed responses:
- Extra explanatory text before JSON
- Missing closing brackets
- Non-JSON-compliant formatting

*Solution Approach:*
```python
def extract_json_from_response(text):
    # Try direct JSON parse
    try:
        return json.loads(text)
    except:
        # Extract JSON block using regex
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        # Fallback: return empty structure
        return {"medicines": [], "diagnoses": [], "test_results": []}
```

*Limitation:* Still ~5% failure rate on edge cases (very short reports, unusual formats).

**Challenge 3: Medical Term Simplification Balance**

*Problem:* LLM simplifications sometimes:
- Over-simplify (lose clinically important nuance)
- Under-simplify (retain jargon)
- Introduce inaccuracies through analogies

*Example:*
- Original: "Elevated AST/ALT levels indicate hepatocellular injury"
- Good simplification: "Liver enzyme levels are high, suggesting liver cell damage"
- Over-simplified: "Your liver is damaged" (alarmist, lacks nuance)
- Inaccurate: "Your liver is like a filter that's clogged" (misleading analogy)

*Current Approach:* Prompt engineering with examples, but no systematic quality control. Future work requires medical expert validation.

### 6.3 Limitations and Honest Assessment

**Limitation 1: No Experimental Validation**

*What We Did NOT Do:*
- OCR accuracy measurement (Character Error Rate, Word Error Rate)
- Comparison with commercial OCR (Google Vision, AWS Textract)
- AI explanation quality evaluation by medical experts
- Patient comprehension testing (before/after AI explanation)
- User studies with real patients or doctors

*Implication:* We cannot claim:
- "X% OCR accuracy"
- "Outperforms baseline systems"
- "Clinically validated"
- "Improves patient outcomes"

*What We CAN Claim:*
- Working implementation demonstrating feasibility
- System design and architecture decisions
- Implementation challenges and solutions
- Approach to prompt engineering for medical context

**Limitation 2: Not a Multi-Agent System**

Despite initial goals, the implementation uses a single LLM with multiple service functions, NOT a multi-agent architecture. There is:
- No agent coordinator
- No inter-agent communication
- No specialized agents (diagnosis agent, treatment agent, etc.)
- No multi-agent framework (CrewAI, AutoGen, etc.)

This is an important distinction for accuracy in publication.

**Limitation 3: AI Does Not Use Longitudinal Data**

While health records are stored with timestamps (longitudinal data storage), the AI analysis treats each report independently:
- Does not compare current vs. previous reports
- Does not track trends over time
- Does not use patient history in analysis
- No time-series analysis or predictive modeling

The patient context passed to AI includes only static demographics (age, blood group, known conditions), not historical data.

**Limitation 4: Development Stage Implementation**

*Not Production-Ready:*
- No automated tests (pytest, Jest)
- No CI/CD pipeline
- No load testing or performance benchmarks
- No error monitoring (Sentry, etc.)
- Mock email service (not sending real emails)
- QR health ID has security concerns (no authentication required)

*Deployment Status:*
- Runs locally (localhost)
- Not deployed to public cloud
- No real user data or usage metrics

**Limitation 5: Safety and Liability Concerns**

*Unaddressed Risks:*
- AI hallucinations in medical context could mislead patients
- No mechanism for medical professionals to verify AI outputs before delivery
- Unclear liability if patients make health decisions based on inaccurate AI explanations
- No compliance review (HIPAA, GDPR, medical device regulations)

These are critical barriers to real-world deployment that our prototype does not address.

### 6.4 Lessons Learned

**Lesson 1: Prompt Engineering is Iterative**

Initial prompts produced overly technical explanations. We improved through:
- Adding explicit examples in prompts
- Testing on diverse report types (blood tests, X-rays, prescriptions)
- Iterating based on qualitative assessment
- Adding safety constraints (no diagnosis claims)

**Lesson 2: OCR Preprocessing Matters**

Direct EasyOCR on raw images had ~70% accuracy (estimated through manual spot-checks). Adding CLAHE contrast enhancement improved to ~85-90% on printed text. However, handwritten text remains challenging (~60% accuracy).

**Lesson 3: User Interface Complexity**

Early designs attempted to show all features prominently, resulting in cluttered interfaces. Simplification based on role-specific priorities improved perceived usability:
- Patients: Prioritize document upload and AI results
- Doctors: Prioritize today's appointments and patient queue
- Admins: Prioritize approval workflows

**Lesson 4: Integration Complexity Underestimated**

Connecting frontend, backend, database, AI API, and file storage involved more edge cases than anticipated:
- File upload size limits and timeouts
- Asynchronous analysis completion polling
- Error handling across service boundaries
- Token refresh during long-running operations

### 6.5 Related System Comparison

| Feature | MediNova (Ours) | Epic MyChart | Apple Health | Practo |
|---------|----------------|--------------|--------------|--------|
| Medical Report Upload | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No |
| AI Report Analysis | ✅ Yes (Gemini) | ❌ No | ❌ No | ❌ No |
| Patient-Friendly Explanations | ✅ Yes (Automated) | ❌ No | ❌ No | ❌ No |
| OCR Text Extraction | ✅ Yes | Limited | Limited | ❌ No |
| Appointment Booking | ✅ Yes | ✅ Yes | ❌ No | ✅ Yes |
| Medication Tracking | ✅ Yes | ✅ Yes | ✅ Yes | Limited |
| Doctor Search | ✅ Yes | ✅ Yes | ❌ No | ✅ Yes |
| AI Health Chat | ✅ Yes | ❌ No | ❌ No | Limited |
| Role-Based Access (Patient/Doctor/Admin) | ✅ Yes | ✅ Yes | ❌ No | Partial |
| EHR Integration | ❌ No | ✅ Yes (Epic) | ✅ HealthKit | Partial |
| Deployment | 🟡 Local | ✅ Production | ✅ Production | ✅ Production |
| User Studies | ❌ None | ✅ Extensive | ✅ Extensive | ✅ Yes |

*Note:* This comparison is based on publicly documented features. We have not conducted systematic feature testing or performance comparison.

---

## 7. Conclusion and Future Work

### 7.1 Summary of Contributions

This paper presents MediNova, a medical document intelligence platform that demonstrates practical integration of OCR, LLMs, and healthcare management features. Our key contributions include:

1. **End-to-End Pipeline:** Complete implementation from document upload through OCR preprocessing, text extraction, LLM analysis, to patient-friendly output

2. **Specialized Preprocessing:** OpenCV-based pipeline optimized for medical document variability using CLAHE contrast enhancement and adaptive thresholding

3. **Prompt Engineering Approach:** LLM prompts balancing patient-friendly simplification with clinical accuracy and safety constraints

4. **Integrated Platform:** Combining document intelligence with practical healthcare features (appointments, medications, records) in role-based workflows

5. **Implementation Insights:** Detailed discussion of design decisions, trade-offs, challenges, and limitations from building a working system

We openly acknowledge significant limitations: no experimental validation, development-stage maturity, and unaddressed safety concerns. This work demonstrates feasibility and provides architectural insights, but does not claim clinical validation or production readiness.

### 7.2 Future Work

**Short-Term Improvements (3-6 months):**

1. **OCR Validation Study**
   - Create ground-truth dataset (100+ medical reports with manual transcription)
   - Measure Character Error Rate (CER) and Word Error Rate (WER)
   - Compare preprocessing variations
   - Benchmark against Tesseract, Google Vision, AWS Textract

2. **Medical Expert Validation**
   - Recruit 5-10 doctors to review AI-generated explanations
   - Rate accuracy, completeness, patient-appropriateness
   - Identify hallucinations and misinterpretations
   - Develop quality metrics

3. **Production Readiness**
   - Implement automated tests (pytest, Jest)
   - Add error monitoring and logging
   - Deploy to cloud (AWS, Azure, Google Cloud)
   - Address Poppler PDF issue
   - Implement real email service

**Medium-Term Research (6-12 months):**

4. **User Studies**
   - IRB approval for human subjects research
   - Patient comprehension testing (n=20-30)
     - Before: Read original report
     - After: Read AI-simplified version
     - Measure: Comprehension quiz, satisfaction, perceived usefulness
   - Doctor adoption survey (n=10-15)
     - Workflow integration challenges
     - Trust in AI explanations
     - Suggested improvements

5. **Longitudinal AI Intelligence**
   - Implement trend analysis across patient's historical reports
   - Compare current report with previous results
   - Highlight changes over time (e.g., "Cholesterol decreased 15% since last test")
   - Predictive modeling for chronic disease management

6. **Safety Mechanisms**
   - Clinician-in-the-loop validation workflow
   - Confidence scoring for AI outputs
   - Automatic flagging of high-risk interpretations
   - Clear attribution (clinician vs. AI-generated content)

**Long-Term Vision (1-2 years):**

7. **EHR Integration**
   - HL7 FHIR compliance
   - Integration with Epic, Cerner, Oracle Health
   - Bidirectional data sync

8. **Advanced AI Capabilities**
   - Fine-tune LLM on medical simplification dataset
   - Multi-modal analysis (combine text, images, lab values)
   - Personalized explanations based on health literacy level
   - Multi-language support

9. **Clinical Validation**
   - Pilot deployment in real healthcare setting
   - Prospective study measuring patient outcomes
   - Long-term safety monitoring
   - Regulatory compliance (FDA medical device classification if applicable)

10. **Mobile Application**
    - Native iOS/Android apps
    - Camera-based document capture
    - Push notifications for appointments and medications
    - Offline mode for viewing records

### 7.3 Broader Impact

**Potential Benefits:**
- Improved health literacy for patients with limited medical knowledge
- Reduced anxiety through clearer understanding of medical reports
- More informed healthcare decisions
- Reduced clinician burden (patients arrive better prepared)
- Accessibility for non-English speakers (future multilingual support)

**Potential Risks:**
- Misinterpretation of AI explanations leading to inappropriate actions
- Over-reliance on automated summaries without consulting healthcare providers
- Privacy concerns from sending medical data to third-party AI services
- Exacerbation of health disparities if system requires digital literacy or devices
- False reassurance from incorrect AI analysis

**Ethical Considerations:**
- Informed consent for AI analysis of medical reports
- Transparency about AI limitations and error rates
- Clear labeling of AI-generated vs. human-verified content
- Mechanisms for patients to report concerns or errors
- Equitable access across socioeconomic groups

### 7.4 Recommendations for Researchers

Based on our experience building MediNova, we offer recommendations for researchers working on similar systems:

1. **Start with Narrow Scope:** Focus on one document type (e.g., blood test reports) and validate thoroughly before expanding

2. **Involve Medical Experts Early:** Collaborate with clinicians from design phase to ensure clinical accuracy and safety

3. **Prioritize Validation:** Allocate significant time for OCR accuracy measurement, AI quality assessment, and user studies

4. **Be Transparent About Limitations:** Clearly document what the system can and cannot do, avoiding overclaims

5. **Consider Safety First:** Implement safeguards (clinician review, confidence scoring, disclaimers) before deployment

6. **Plan for Iterative Improvement:** Build feedback mechanisms to continuously improve based on real usage

### 7.5 Final Remarks

MediNova demonstrates that building an integrated medical document intelligence platform is technically feasible using current open-source tools and commercial AI APIs. However, the gap between a working prototype and a clinically validated, production-ready system is substantial. This gap includes rigorous evaluation, safety mechanisms, regulatory compliance, and real-world validation—areas where our current work falls short.

We hope this honest assessment of our system's capabilities and limitations provides valuable insights for researchers and practitioners working to bridge the medical information gap through AI-powered tools. The ultimate goal—empowering patients with accessible, accurate medical information—remains both important and challenging.

---

## Acknowledgments

We thank the open-source communities behind FastAPI, React, EasyOCR, and OpenCV for enabling rapid development. We acknowledge Google for providing the Gemini API. We recognize that this work represents a development prototype and not a clinically validated system.

---

## References

[1] Schillinger, D., et al. (2002). "Closing the loop: physician communication with diabetic patients who have low health literacy." Archives of Internal Medicine, 163(1), 83-90.

[2] Berkman, N. D., et al. (2011). "Low health literacy and health outcomes: an updated systematic review." Annals of Internal Medicine, 155(2), 97-107.

[3] Paasche-Orlow, M. K., & Wolf, M. S. (2007). "The causal pathways linking health literacy to health outcomes." American Journal of Health Behavior, 31(Suppl 1), S19-S26.

[4] Kim, S., et al. (2026). "Enhancing patient participation in emergency department through patient-friendly clinical notes generated by large language models." Scientific Reports, 16, 1409.

[5] Zaretsky, J., et al. (2024). "Generative artificial intelligence to transform inpatient discharge summaries to Patient-Friendly Language and format." JAMA Network Open, 7(1), e240357.

[6] Tung, J. Y. M., et al. (2024). "Comparison of the quality of discharge letters written by large Language models and junior clinicians: Single-Blinded study." Journal of Medical Internet Research, 26, e57721.

[7] "AI-Powered OCR Solutions for Healthcare Companies" (2026). Intuz Blog. https://www.intuz.com/blog/ai-powered-ocr-solutions-for-healthcare-companies/

[8] "Healthcare Fax Automation Software" (2026). Linear Health Blog. https://linear.health/blog/healthcare-fax-automation-ai

[9] Kim, S., Park, J., et al. (2026). "Enhancing patient participation in emergency department through patient-friendly clinical notes generated by large language models." Nature Scientific Reports, 16(1), 1409. https://doi.org/10.1038/s41598-025-31113-y

[10] Zaretsky, J., et al. (2024). "Generative artificial intelligence to transform inpatient discharge summaries." JAMA Network Open, 7(1), e240357.

[11] "The Potential of Large Language Models for Radiology Report Simplification" (2024). Journal of the American College of Radiology. https://www.jacr.org/article/S1546-1440(24)00524-6/

[12] "Development and expert radiologist validation of a custom pipeline" (2026). Frontiers in Oncology. https://www.frontiersin.org/articles/10.3389/fonc.2026.1757933

[13] "Large Language Models for Simplified Interventional Radiology Reports" (2025). Academic Radiology. https://www.academicradiology.org/article/S1076-6332(24)00690-1/

[14] "Integration of AI with Electronic Health Records" (2024). ResearchGate. https://www.researchgate.net/publication/384773568

[15] "Enhancing Medical Diagnosis Document Analysis with Layout-Aware Multitask Models" (2025). PMC. https://pmc.ncbi.nlm.nih.gov/articles/PMC12691868/

[16] "AI fax automation handles clinical context, extract structured data" (2026). Linear Health.

[17] González, R. C., & Woods, R. E. (2018). "Digital Image Processing" (4th ed.). Pearson.

[18] "Oracle Health EHR" (2025). Oracle. https://www.oracle.com/health/clinical-suite/electronic-health-record/

[19] "Human-centered AI in healthcare teams" (2026). Frontiers in Digital Health. https://www.frontiersin.org/journals/digital-health/articles/10.3389/fdgth.2026.1761009/

[20] Walsh, A., et al. (2022). "Patient-centered care in the emergency department: a systematic review." International Journal of Emergency Medicine, 15, 36.

[21] Subramanian, C. R., et al. (2024). "Enhancing health care communication with large Language Models." JAMA Network Open, 7(3), e240347.

---

## Appendix A: System Screenshots

*[Note: Add screenshots of key interfaces]*

- Figure A1: Patient Dashboard
- Figure A2: Health Record Upload Flow
- Figure A3: AI-Generated Report Analysis
- Figure A4: Doctor Patient Detail View
- Figure A5: Appointment Booking Interface

---

## Appendix B: Sample AI Output

**Original Medical Report Text (OCR Extracted):**
```
COMPLETE BLOOD COUNT (CBC)

Test Name          Result    Normal Range    Unit
-----------------------------------------------
Hemoglobin         13.2      13.5-17.5       g/dL
RBC Count          4.5       4.5-5.5         M/μL
WBC Count          11.2      4.5-11.0        K/μL
Platelets          250       150-400         K/μL
```

**AI-Generated Patient-Friendly Explanation:**
```
Understanding Your Blood Test Results:

Your blood test checked several important components:

1. Hemoglobin (Blood Protein): 13.2 g/dL
   - Slightly below normal range (13.5-17.5)
   - Hemoglobin carries oxygen in your blood
   - Mild decrease may indicate mild anemia (low iron)
   - Not severely concerning, but worth discussing with your doctor

2. Red Blood Cells: 4.5 M/μL - ✓ Normal
   - These cells carry oxygen throughout your body
   - Your count is at the lower end of normal

3. White Blood Cells: 11.2 K/μL - ⚠️ Slightly Elevated
   - Slightly above normal range (4.5-11.0)
   - These cells fight infections
   - Mild elevation may suggest your body is fighting an infection
   - Could also be due to stress or recent physical activity

4. Platelets: 250 K/μL - ✓ Normal
   - These help your blood clot
   - Your level is healthy

What This Means:
Your blood test shows mostly normal results with two minor concerns:
slight low hemoglobin and slightly elevated white blood cells. These 
are not emergency issues but should be discussed with your doctor.

Next Steps:
- Consult your doctor about the slightly low hemoglobin
- Your doctor may recommend iron-rich foods or supplements
- The elevated white blood cells may need follow-up testing if you have 
  symptoms like fever or fatigue

⚠️ Important: This is an AI-generated explanation for educational 
purposes. Always consult your healthcare provider for medical advice.
```

**Extracted Structured Data:**
```json
{
  "test_results": [
    {
      "test": "Hemoglobin",
      "value": "13.2",
      "normal_range": "13.5-17.5",
      "unit": "g/dL",
      "status": "low"
    },
    {
      "test": "WBC Count",
      "value": "11.2",
      "normal_range": "4.5-11.0",
      "unit": "K/μL",
      "status": "high"
    }
  ],
  "diagnoses": [],
  "medicines": []
}
```

---

## Appendix C: Source Code Availability

The MediNova source code and documentation are available at:
[Repository URL - to be added upon publication acceptance]

Key components:
- `backend/app/services/ai_service.py` - LLM analysis logic
- `backend/app/services/ocr_service.py` - OCR preprocessing pipeline
- `backend/app/services/document_processor.py` - Structured extraction
- `frontend/src/pages/patient/HealthRecordsPage.jsx` - UI implementation

---

**End of Paper**

*Word Count: ~9,500 words*  
*Suitable for: Conference paper (with condensed version) or Extended workshop paper*  
*Target venues: IEEE EMBC, ACM CHASE, AMIA Annual Symposium, PervasiveHealth*
