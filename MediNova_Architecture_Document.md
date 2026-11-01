# MediNova AI: Software Architecture Document
## Comprehensive System Architecture & Design Specifications

---

**Document Version:** 1.0  
**Date:** July 2, 2026  
**Project:** MediNova AI - Multi-Agent Healthcare Intelligence Platform  
**Document Type:** Software Architecture Document (SAD)  
**Prepared By:** Senior Software Architecture Team  

---

## Table of Contents

1. [System Architecture Diagram](#1-system-architecture-diagram)
2. [Multi-Agent Architecture](#2-multi-agent-architecture)
3. [Database Architecture](#3-database-architecture)
4. [API Architecture](#4-api-architecture)
5. [Frontend Architecture](#5-frontend-architecture)
6. [Backend Architecture](#6-backend-architecture)
7. [Authentication Flow](#7-authentication-flow)
8. [Folder Structure](#8-folder-structure)
9. [Database Collections](#9-database-collections)
10. [Sequence Diagrams](#10-sequence-diagrams)
11. [User Flow](#11-user-flow)
12. [Admin Flow](#12-admin-flow)
13. [Doctor Flow](#13-doctor-flow)
14. [Patient Flow](#14-patient-flow)
15. [AI Agent Workflow](#15-ai-agent-workflow)
16. [OCR Workflow](#16-ocr-workflow)
17. [Medical Report Analysis Flow](#17-medical-report-analysis-flow)
18. [Appointment Booking Flow](#18-appointment-booking-flow)
19. [Reminder Flow](#19-reminder-flow)
20. [Deployment Architecture](#20-deployment-architecture)

---

## 1. System Architecture Diagram

### 1.1 High-Level System Architecture (C4 Model - Level 1)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          EXTERNAL USERS & SYSTEMS                        │
│                                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────────────┐       │
│  │ Patient  │  │  Doctor  │  │  Admin   │  │ Wearable Devices│       │
│  │ (Web/    │  │ (Web/    │  │ (Web)    │  │ (Fitbit, Apple  │       │
│  │ Mobile)  │  │ Mobile)  │  │          │  │  Health, etc.)  │       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────────┬────────┘       │
│       │             │             │                   │                 │
└───────┼─────────────┼─────────────┼───────────────────┼─────────────────┘
        │             │             │                   │
        │             │             │                   │
        ▼             ▼             ▼                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         CDN & EDGE LAYER                                 │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │  CloudFlare / AWS CloudFront                                   │    │
│  │  - Static Content Delivery                                     │    │
│  │  - DDoS Protection                                             │    │
│  │  - SSL/TLS Termination                                         │    │
│  │  - WAF (Web Application Firewall)                              │    │
│  └────────────────────────────────────────────────────────────────┘    │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
                                ▼

┌─────────────────────────────────────────────────────────────────────────┐
│                      LOAD BALANCER & API GATEWAY                         │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │  Kong API Gateway / AWS API Gateway                             │    │
│  │  - Request Routing                                              │    │
│  │  - Rate Limiting                                                │    │
│  │  - Authentication/Authorization                                 │    │
│  │  - Request/Response Transformation                              │    │
│  │  - API Versioning                                               │    │
│  │  - Monitoring & Analytics                                       │    │
│  └────────────────────────────────────────────────────────────────┘    │
└───────────────┬───────────────┬───────────────┬─────────────────────────┘
                │               │               │
        ────────┴───────   ────┴─────   ───────┴────────
        │              │   │         │   │              │
        ▼              ▼   ▼         ▼   ▼              ▼
┌───────────────┐ ┌──────────────────────────┐ ┌───────────────────┐
│  APPLICATION  │ │    AI AGENT LAYER        │ │   INTEGRATION     │
│  SERVICES     │ │                          │ │   SERVICES        │
│               │ │                          │ │                   │
│ • Auth        │ │ • Symptom Analyzer      │ │ • FHIR Gateway    │
│ • User Mgmt   │ │ • Diagnostic Assistant  │ │ • Wearable APIs   │
│ • Appointment │ │ • Treatment Planner     │ │ • Video Call SDK  │
│ • EHR         │ │ • Medication Manager    │ │ • Email/SMS       │
│ • Consultation│ │ • Health Monitor        │ │ • Payment Gateway │
│ • Notification│ │ • Predictive Analytics  │ │ • Cloud Storage   │
│ • Analytics   │ │ • Care Coordinator      │ │ • External EHR    │
│               │ │                          │ │                   │
└───────┬───────┘ └────────────┬─────────────┘ └─────────┬─────────┘
        │                      │                          │
        └──────────────────────┼──────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    MESSAGE BROKER & EVENT BUS                            │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │  RabbitMQ / Apache Kafka                                        │    │
│  │  - Inter-Service Communication                                  │    │
│  │  - Event-Driven Architecture                                    │    │
│  │  - Pub/Sub Pattern                                              │    │
│  │  - Message Queuing                                              │    │
│  └────────────────────────────────────────────────────────────────┘    │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          DATA LAYER                                      │
│                                                                          │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │
│  │ PostgreSQL   │ │  MongoDB     │ │  InfluxDB    │ │   Redis      │ │
│  │              │ │              │ │              │ │              │ │
│  │• Users       │ │• Symptoms    │ │• Vitals      │ │• Sessions    │ │
│  │• Patients    │ │• Diagnoses   │ │• Activities  │ │• Cache       │ │
│  │• Doctors     │ │• Reports     │ │• Health      │ │• Rate Limit  │ │
│  │• Appointments│ │• Agent Logs  │ │  Scores      │ │• Pub/Sub     │ │
│  │• Medications │ │• Notifications│ │              │ │              │ │
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ │
│                                                                          │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                  │
│  │   AWS S3     │ │  Pinecone    │ │Elasticsearch │                  │
│  │              │ │              │ │              │                  │
│  │• Images      │ │• Embeddings  │ │• Full-text   │                  │
│  │• Documents   │ │• Vectors     │ │  Search      │                  │
│  │• Reports     │ │• Similarity  │ │• Logs        │                  │
│  │• Backups     │ │  Search      │ │• Analytics   │                  │
│  └──────────────┘ └──────────────┘ └──────────────┘                  │
└─────────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    MONITORING & OBSERVABILITY                            │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │  Prometheus + Grafana + ELK Stack + Jaeger                      │    │
│  │  - Metrics Collection & Visualization                           │    │
│  │  - Centralized Logging                                          │    │
│  │  - Distributed Tracing                                          │    │
│  │  - Alerting & Notifications                                     │    │
│  └────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Architecture Principles


**1. Microservices Architecture**
- Each service is independently deployable and scalable
- Services communicate via REST APIs and message queues
- Loose coupling through event-driven architecture
- Single Responsibility Principle per service

**2. Cloud-Native Design**
- Containerized services (Docker)
- Orchestrated by Kubernetes
- Horizontal auto-scaling based on metrics
- Multi-region deployment capability

**3. Security by Design**
- Zero-trust security model
- End-to-end encryption (TLS 1.3)
- Defense in depth strategy
- HIPAA-compliant architecture

**4. Event-Driven Architecture**
- Asynchronous communication for non-critical operations
- Message broker for inter-service events
- Pub/Sub pattern for broadcasting
- Event sourcing for audit trail

**5. Domain-Driven Design (DDD)**
- Bounded contexts per domain (User, Health, AI, etc.)
- Aggregate roots for data consistency
- Domain events for cross-context communication
- Ubiquitous language

**6. API-First Design**
- RESTful APIs with OpenAPI specification
- API versioning (v1, v2)
- GraphQL for complex queries (optional)
- Comprehensive API documentation

**7. Scalability & Performance**
- Horizontal scaling for all services
- Caching strategy at multiple layers
- CDN for static content
- Database read replicas
- Connection pooling

**8. Resilience & Fault Tolerance**
- Circuit breakers for external dependencies
- Retry mechanisms with exponential backoff
- Graceful degradation
- Health checks and self-healing

### 1.3 Technology Stack Summary

| Layer | Technology | Justification |
|-------|------------|---------------|
| **Frontend Web** | React 18 + TypeScript | Component-based, type-safe, large ecosystem |
| **Frontend Mobile** | React Native | Cross-platform, code sharing with web |
| **API Gateway** | Kong / AWS API Gateway | Enterprise-grade, plugin ecosystem |
| **Backend Services** | Node.js (Nest.js) | Async I/O, TypeScript support, scalable |
| **AI Services** | Python (FastAPI) | ML ecosystem, high performance |
| **Message Broker** | RabbitMQ | Reliable messaging, easy to setup |
| **Databases** | PostgreSQL, MongoDB, InfluxDB, Redis | Polyglot persistence for different needs |
| **Object Storage** | AWS S3 / MinIO | Scalable, HIPAA-eligible |
| **Container** | Docker | Standard containerization |
| **Orchestration** | Kubernetes | Industry standard, auto-scaling |
| **CI/CD** | GitHub Actions / GitLab CI | Git-integrated, easy pipelines |
| **Monitoring** | Prometheus + Grafana | Open-source, powerful visualization |
| **Logging** | ELK Stack | Centralized logging, search capabilities |
| **Tracing** | Jaeger | Distributed tracing for microservices |

---

## 2. Multi-Agent Architecture

### 2.1 Agent System Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      MULTI-AGENT SYSTEM ARCHITECTURE                     │
│                                                                          │
│                    ┌──────────────────────────┐                         │
│                    │   Care Coordinator       │                         │
│                    │        Agent             │                         │
│                    │  (Orchestrator/Router)   │                         │
│                    └────────────┬─────────────┘                         │
│                                 │                                        │
│                    ┌────────────┴─────────────┐                         │
│                    │   Agent Message Bus      │                         │
│                    │   (RabbitMQ Exchange)    │                         │
│                    └────────────┬─────────────┘                         │
│                                 │                                        │
│     ┌───────────┬───────────┬──┴──┬───────────┬───────────┬──────────┐│
│     │           │           │     │           │           │          ││
│     ▼           ▼           ▼     ▼           ▼           ▼          ▼│
│ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐   │
│ │Symptom │ │Diagnos-│ │Treat-  │ │Medica- │ │Health  │ │Predict-│   │
│ │Analyzer│ │tic     │ │ment    │ │tion    │ │Monitor │ │ive     │   │
│ │ Agent  │ │Assist- │ │Planner │ │Manager │ │ Agent  │ │Analyt- │   │
│ │        │ │ant     │ │ Agent  │ │ Agent  │ │        │ │ics     │   │
│ │        │ │ Agent  │ │        │ │        │ │        │ │ Agent  │   │
│ └────┬───┘ └────┬───┘ └────┬───┘ └────┬───┘ └────┬───┘ └────┬───┘   │
│      │          │          │          │          │          │        │
│      ▼          ▼          ▼          ▼          ▼          ▼        │
│ ┌────────────────────────────────────────────────────────────────┐   │
│ │              Agent Knowledge Base & Shared Memory              │   │
│ │  • Medical Knowledge Graph                                     │   │
│ │  • Patient Context Store (Redis)                               │   │
│ │  • Interaction History (MongoDB)                               │   │
│ │  • Model Registry (MLflow)                                     │   │
│ └────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Agent Specifications


#### Agent 1: Symptom Analyzer Agent

**Purpose:** Natural language understanding of patient symptoms

**Architecture:**
```
┌─────────────────────────────────────────────┐
│     Symptom Analyzer Agent                  │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │    Input Layer                      │   │
│  │  • REST API Endpoint                │   │
│  │  • WebSocket for Real-time Chat     │   │
│  │  • Message Queue Consumer           │   │
│  └──────────────┬──────────────────────┘   │
│                 ▼                           │
│  ┌─────────────────────────────────────┐   │
│  │    NLP Processing Pipeline          │   │
│  │                                     │   │
│  │  1. Text Preprocessing              │   │
│  │     • Tokenization                  │   │
│  │     • Normalization                 │   │
│  │     • Spell Correction              │   │
│  │                                     │   │
│  │  2. Medical NER                     │   │
│  │     • BioBERT / ClinicalBERT       │   │
│  │     • Entity Extraction             │   │
│  │     • Symptom Identification        │   │
│  │                                     │   │
│  │  3. Context Understanding           │   │
│  │     • Conversation History          │   │
│  │     • Patient Demographics          │   │
│  │     • Medical History               │   │
│  │                                     │   │
│  │  4. Clarification Generator         │   │
│  │     • Question Generation           │   │
│  │     • Follow-up Logic               │   │
│  └──────────────┬──────────────────────┘   │
│                 ▼                           │
│  ┌─────────────────────────────────────┐   │
│  │    Symptom Structuring              │   │
│  │  • SNOMED CT Mapping                │   │
│  │  • Severity Assessment              │   │
│  │  • Duration Extraction              │   │
│  │  • Location Identification          │   │
│  └──────────────┬──────────────────────┘   │
│                 ▼                           │
│  ┌─────────────────────────────────────┐   │
│  │    Urgency Triage                   │   │
│  │  • Emergency Detection              │   │
│  │  • Urgency Scoring                  │   │
│  │  • Red Flag Identification          │   │
│  └──────────────┬──────────────────────┘   │
│                 ▼                           │
│  ┌─────────────────────────────────────┐   │
│  │    Output Layer                     │   │
│  │  • Structured Symptom Data          │   │
│  │  • Urgency Level                    │   │
│  │  • Recommendations                  │   │
│  │  • Event Publishing                 │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  Technology Stack:                          │
│  • Python 3.10+                            │
│  • FastAPI                                 │
│  • Transformers (Hugging Face)             │
│  • spaCy for NLP                           │
│  • PyTorch                                 │
│  • Redis for context                       │
└─────────────────────────────────────────────┘
```

**Data Flow:**
1. **Input:** Patient symptom text → "I have a severe headache for 3 days with fever"
2. **Processing:** 
   - Extract entities: [headache (severe, 3 days), fever]
   - Map to SNOMED: [25064002 (headache), 386661006 (fever)]
   - Assess urgency: Routine (no red flags)
3. **Output:** Structured symptom object + follow-up questions
4. **Event:** Publish `symptom_analysis_complete` event to message bus

---

#### Agent 2: Diagnostic Assistant Agent

**Purpose:** Generate differential diagnoses and analyze medical data

**Architecture:**
```
┌─────────────────────────────────────────────────────────────────┐
│         Diagnostic Assistant Agent                              │
│                                                                 │
│  ┌───────────────────────────────────────────────────────┐     │
│  │    Input Processing                                   │     │
│  │  • Symptom Data (from Symptom Analyzer)              │     │
│  │  • Medical Images (DICOM)                            │     │
│  │  • Lab Results (HL7/FHIR)                            │     │
│  │  • Patient History                                    │     │
│  └────────────────────┬──────────────────────────────────┘     │
│                       │                                         │
│         ┌─────────────┴─────────────┬─────────────────┐       │
│         ▼                           ▼                 ▼       │
│  ┌──────────────┐          ┌──────────────┐   ┌──────────────┐│
│  │   Symptom    │          │   Medical    │   │  Lab Test    ││
│  │   Pattern    │          │    Image     │   │ Interpreter  ││
│  │  Recognizer  │          │   Analyzer   │   │              ││
│  │              │          │              │   │              ││
│  │ • ML Model   │          │ • CNN Models │   │ • Rule-Based ││
│  │ • Rule-Based │          │ • ResNet-50  │   │ • ML Models  ││
│  │ • Fuzzy      │          │ • EfficientN │   │ • Threshold  ││
│  │   Logic      │          │ • Grad-CAM   │   │   Detection  ││
│  └──────┬───────┘          └──────┬───────┘   └──────┬───────┘│
│         │                         │                   │        │
│         └─────────────┬───────────┴───────────────────┘        │
│                       ▼                                         │
│  ┌───────────────────────────────────────────────────────┐     │
│  │    Diagnosis Generation Engine                        │     │
│  │                                                       │     │
│  │  1. Knowledge Graph Traversal                        │     │
│  │     • Disease-Symptom Relationships                  │     │
│  │     • Probabilistic Inference                        │     │
│  │                                                       │     │
│  │  2. Differential Diagnosis                           │     │
│  │     • Bayesian Network                               │     │
│  │     • Confidence Scoring                             │     │
│  │     • Ranked List Generation                         │     │
│  │                                                       │     │
│  │  3. Evidence Collection                              │     │
│  │     • Supporting Findings                            │     │
│  │     • Contradicting Findings                         │     │
│  │                                                       │     │
│  │  4. Recommendation Engine                            │     │
│  │     • Additional Tests Needed                        │     │
│  │     • Specialist Referral                            │     │
│  └────────────────────┬──────────────────────────────────┘     │
│                       ▼                                         │
│  ┌───────────────────────────────────────────────────────┐     │
│  │    Explainability Layer (XAI)                         │     │
│  │  • SHAP Values                                        │     │
│  │  • Feature Importance                                 │     │
│  │  • Natural Language Explanation Generation            │     │
│  │  • Evidence Retrieval from Medical Literature         │     │
│  └────────────────────┬──────────────────────────────────┘     │
│                       ▼                                         │
│  ┌───────────────────────────────────────────────────────┐     │
│  │    Output                                             │     │
│  │  • Differential Diagnoses (ranked)                    │     │
│  │  • Confidence Scores                                  │     │
│  │  • Explanations                                       │     │
│  │  • Recommended Actions                                │     │
│  └───────────────────────────────────────────────────────┘     │
│                                                                 │
│  Technology Stack:                                              │
│  • Python 3.10+ / FastAPI                                      │
│  • PyTorch / TensorFlow                                        │
│  • OpenCV for image processing                                 │
│  • Neo4j for knowledge graph                                   │
│  • SHAP for explainability                                     │
└─────────────────────────────────────────────────────────────────┘
```


**Medical Image Analysis Pipeline:**
```
DICOM Image → Preprocessing → Model Inference → Post-processing → Report
     │             │                │                 │              │
     │             │                │                 │              │
     ▼             ▼                ▼                 ▼              ▼
• Format      • Resize        • CNN Forward    • Threshold    • Structured
• Metadata    • Normalize     • Feature        • Segment      • Annotation
• Validation  • Augment       • Extract        • Classify     • Confidence
              • Denoise       • Ensemble       • Heatmap      • Explanation
```

---

#### Agent 3: Treatment Planner Agent

**Purpose:** Generate personalized, evidence-based treatment recommendations

**Architecture:**
```
┌─────────────────────────────────────────────────────────────┐
│         Treatment Planner Agent                             │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Input Layer                                      │   │
│  │  • Confirmed Diagnosis                              │   │
│  │  • Patient Profile (age, gender, weight, etc.)     │   │
│  │  • Medical History & Comorbidities                 │   │
│  │  • Current Medications                              │   │
│  │  • Allergies                                        │   │
│  │  • Patient Preferences                              │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Clinical Guidelines Engine                       │   │
│  │  • Load Evidence-Based Guidelines                   │   │
│  │  • Filter by Diagnosis                              │   │
│  │  • Rank by Evidence Level                           │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Personalization Engine                           │   │
│  │                                                     │   │
│  │  1. Patient Stratification                         │   │
│  │     • Age Group                                    │   │
│  │     • Comorbidity Score                            │   │
│  │     • Contraindications Check                      │   │
│  │                                                     │   │
│  │  2. Treatment Filtering                            │   │
│  │     • Remove Contraindicated Options              │   │
│  │     • Adjust for Kidney/Liver Function            │   │
│  │     • Consider Drug Interactions                   │   │
│  │                                                     │   │
│  │  3. Preference Integration                         │   │
│  │     • Cost Considerations                          │   │
│  │     • Lifestyle Factors                            │   │
│  │     • Patient-Reported Priorities                  │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Treatment Options Generator                      │   │
│  │                                                     │   │
│  │  Option 1 (Primary Recommendation)                 │   │
│  │  • Medication Regimen                              │   │
│  │  • Dosage & Frequency                              │   │
│  │  • Duration                                        │   │
│  │  • Expected Outcome                                │   │
│  │  • Side Effects                                    │   │
│  │  • Cost Estimate                                   │   │
│  │                                                     │   │
│  │  Option 2, 3... (Alternatives)                     │   │
│  │  • Pros/Cons Comparison                            │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Lifestyle & Non-Pharmacological                 │   │
│  │  • Diet Recommendations                            │   │
│  │  • Exercise Plans                                  │   │
│  │  • Sleep Hygiene                                   │   │
│  │  • Stress Management                               │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Outcome Prediction                               │   │
│  │  • ML Model for Success Probability                │   │
│  │  • Time to Recovery Estimate                       │   │
│  │  • Risk of Complications                           │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Output                                           │   │
│  │  • Comprehensive Treatment Plan                     │   │
│  │  • Multiple Options Ranked                          │   │
│  │  • Explanation & Rationale                          │   │
│  │  • Follow-up Schedule                               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Data Sources:                                              │
│  • Clinical Guidelines Database                             │
│  • Medical Literature (PubMed)                              │
│  • Drug Database (DrugBank)                                 │
│  • Treatment Outcomes (Historical Data)                     │
└─────────────────────────────────────────────────────────────┘
```

---

#### Agent 4: Medication Manager Agent

**Purpose:** Drug interaction checking and prescription management

**Architecture:**
```
┌─────────────────────────────────────────────────────────────┐
│         Medication Manager Agent                            │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Input Processing                                 │   │
│  │  • Prescription Data                                │   │
│  │  • Current Medications List                         │   │
│  │  • Patient Allergies                                │   │
│  │  • Patient Demographics                             │   │
│  │  • Lab Values (Kidney/Liver Function)              │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Drug Interaction Checker                         │   │
│  │                                                     │   │
│  │  ┌──────────────────────────────────────────┐      │   │
│  │  │ Graph Neural Network                     │      │   │
│  │  │ • Drug-Drug Interaction Graph            │      │   │
│  │  │ • Severity Scoring                       │      │   │
│  │  │ • Mechanism Identification               │      │   │
│  │  └──────────────────────────────────────────┘      │   │
│  │                                                     │   │
│  │  Check Types:                                       │   │
│  │  • Drug-Drug Interactions                           │   │
│  │  • Drug-Food Interactions                           │   │
│  │  • Drug-Disease Contraindications                   │   │
│  │  • Drug-Allergy Cross-reactions                     │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Dosage Validator                                 │   │
│  │  • Age-Based Dosing                                │   │
│  │  • Weight-Based Calculation                         │   │
│  │  • Renal Dose Adjustment                           │   │
│  │  • Hepatic Dose Adjustment                         │   │
│  │  • Maximum Daily Dose Check                        │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Alternative Medication Suggester                 │   │
│  │  • Generic Alternatives                             │   │
│  │  • Therapeutic Equivalents                          │   │
│  │  • Cost-Effective Options                           │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Medication Schedule Generator                    │   │
│  │  • Optimal Timing                                   │   │
│  │  • Food Requirements                                │   │
│  │  • Reminder Schedule                                │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Adherence Predictor                              │   │
│  │  • ML Model for Non-Adherence Risk                 │   │
│  │  • Intervention Suggestions                         │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Output                                           │   │
│  │  • Validated Prescription                           │   │
│  │  • Interaction Warnings                             │   │
│  │  • Dosage Recommendations                           │   │
│  │  • Medication Schedule                              │   │
│  │  • Patient Instructions                             │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```


---

#### Agent 5: Health Monitor Agent

**Purpose:** Real-time health data monitoring and anomaly detection

**Architecture:**
```
┌─────────────────────────────────────────────────────────────┐
│         Health Monitor Agent (Golang/Python)                │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Data Ingestion Layer                             │   │
│  │  • WebSocket Connections (Real-time)                │   │
│  │  • REST API (Manual Entry)                          │   │
│  │  • Wearable Device APIs                             │   │
│  │  • IoT Device Streams                               │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Stream Processing Pipeline                       │   │
│  │                                                     │   │
│  │  1. Data Validation                                │   │
│  │     • Range Check                                  │   │
│  │     • Format Validation                            │   │
│  │     • Timestamp Verification                       │   │
│  │                                                     │   │
│  │  2. Data Normalization                             │   │
│  │     • Unit Conversion                              │   │
│  │     • Standardization                              │   │
│  │                                                     │   │
│  │  3. Data Enrichment                                │   │
│  │     • Patient Context                              │   │
│  │     • Historical Baseline                          │   │
│  │     • Medication Context                           │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Time-Series Storage (InfluxDB)                   │   │
│  │  • Write-Optimized                                  │   │
│  │  • Downsampling Policies                            │   │
│  │  • Retention Policies                               │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Anomaly Detection Engine                         │   │
│  │                                                     │   │
│  │  ┌──────────────────────────────────────────┐      │   │
│  │  │ Statistical Methods                      │      │   │
│  │  │ • Z-Score                                │      │   │
│  │  │ • IQR (Interquartile Range)             │      │   │
│  │  │ • Moving Average                         │      │   │
│  │  └──────────────────────────────────────────┘      │   │
│  │                                                     │   │
│  │  ┌──────────────────────────────────────────┐      │   │
│  │  │ Machine Learning Models                  │      │   │
│  │  │ • LSTM Autoencoder                       │      │   │
│  │  │ • Isolation Forest                       │      │   │
│  │  │ • One-Class SVM                          │      │   │
│  │  └──────────────────────────────────────────┘      │   │
│  │                                                     │   │
│  │  Detection Rules:                                   │   │
│  │  • Threshold Violations                             │   │
│  │  • Trend Changes                                    │   │
│  │  • Pattern Deviations                               │   │
│  │  • Multi-variate Correlations                       │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Alert Classification                             │   │
│  │  • Priority Scoring (0-100)                         │   │
│  │  • Severity Level (Info/Warning/Critical)          │   │
│  │  • Actionability Assessment                         │   │
│  │  • De-duplication                                   │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Alert Router                                     │   │
│  │                                                     │   │
│  │  Critical → Immediate Notification                  │   │
│  │           → Doctor Alert                            │   │
│  │           → Emergency Contact                       │   │
│  │                                                     │   │
│  │  Warning  → Patient Notification                    │   │
│  │           → Health Tips                             │   │
│  │                                                     │   │
│  │  Info     → Dashboard Update                        │   │
│  │           → Trend Visualization                     │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Health Score Calculator                          │   │
│  │  • Cardiovascular Score                             │   │
│  │  • Metabolic Score                                  │   │
│  │  • Activity Score                                   │   │
│  │  • Sleep Quality Score                              │   │
│  │  • Overall Health Score (0-100)                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Technology Stack:                                          │
│  • Golang (for high-performance streaming)                  │
│  • Python (for ML models)                                   │
│  • InfluxDB (time-series storage)                          │
│  • Redis (real-time state)                                 │
│  • WebSocket for real-time communication                   │
└─────────────────────────────────────────────────────────────┘
```

---

#### Agent 6: Predictive Analytics Agent

**Purpose:** Risk assessment and outcome forecasting

**Architecture:**
```
┌─────────────────────────────────────────────────────────────┐
│         Predictive Analytics Agent                          │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Data Aggregation Layer                           │   │
│  │  • Patient Demographics                             │   │
│  │  • Medical History                                  │   │
│  │  • Lab Results (longitudinal)                       │   │
│  │  • Vital Signs Trends                               │   │
│  │  • Medication History                               │   │
│  │  • Lifestyle Data                                   │   │
│  │  • Social Determinants of Health                    │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Feature Engineering Pipeline                     │   │
│  │  • Missing Value Imputation                         │   │
│  │  • Feature Scaling                                  │   │
│  │  • Derived Features (BMI, eGFR, etc.)              │   │
│  │  • Time-Based Features                              │   │
│  │  • Interaction Features                             │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Risk Prediction Models                           │   │
│  │                                                     │   │
│  │  ┌──────────────────────────────────────────┐      │   │
│  │  │ Diabetes Risk Predictor                  │      │   │
│  │  │ • XGBoost Model                          │      │   │
│  │  │ • Features: HbA1c, FBG, BMI, Age, etc.  │      │   │
│  │  │ • Output: 5-year risk probability        │      │   │
│  │  └──────────────────────────────────────────┘      │   │
│  │                                                     │   │
│  │  ┌──────────────────────────────────────────┐      │   │
│  │  │ Cardiovascular Disease Risk              │      │   │
│  │  │ • Framingham Enhanced with ML            │      │   │
│  │  │ • Features: BP, Cholesterol, Smoking     │      │   │
│  │  │ • Output: 10-year CVD risk               │      │   │
│  │  └──────────────────────────────────────────┘      │   │
│  │                                                     │   │
│  │  ┌──────────────────────────────────────────┐      │   │
│  │  │ Hospital Readmission Predictor           │      │   │
│  │  │ • Random Forest Model                    │      │   │
│  │  │ • Features: Diagnosis, Length of Stay    │      │   │
│  │  │ • Output: 30-day readmission probability │      │   │
│  │  └──────────────────────────────────────────┘      │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Disease Progression Models                       │   │
│  │  • LSTM for Time-Series Forecasting                │   │
│  │  • Survival Analysis (Cox Regression)              │   │
│  │  • Trajectory Prediction                            │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Treatment Outcome Predictor                      │   │
│  │  • ML Models for Success Probability               │   │
│  │  • Side Effect Prediction                           │   │
│  │  • Time to Recovery                                 │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Preventive Care Recommendation Engine           │   │
│  │  • High-Risk Patient Identification                │   │
│  │  • Intervention Suggestions                         │   │
│  │  • Personalized Prevention Plans                    │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Population Health Analytics                      │   │
│  │  • Cohort Analysis                                  │   │
│  │  • Trend Identification                             │   │
│  │  • Epidemiological Insights                         │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```


---

#### Agent 7: Care Coordinator Agent

**Purpose:** Orchestrate multi-agent collaboration and manage patient care journey

**Architecture:**
```
┌─────────────────────────────────────────────────────────────┐
│         Care Coordinator Agent (Orchestrator)               │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Request Router                                   │   │
│  │  • Identify Request Type                            │   │
│  │  • Determine Required Agents                        │   │
│  │  • Priority Assignment                              │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Context Manager                                  │   │
│  │  • Patient Context Retrieval (Redis)                │   │
│  │  • Session State Management                         │   │
│  │  • Conversation History                             │   │
│  │  • Agent Interaction History                        │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Workflow Orchestration Engine                    │   │
│  │                                                     │   │
│  │  Workflow Types:                                    │   │
│  │                                                     │   │
│  │  1. Symptom-to-Diagnosis                           │   │
│  │     Step 1: Invoke Symptom Analyzer                │   │
│  │     Step 2: Wait for structured symptoms           │   │
│  │     Step 3: Invoke Diagnostic Assistant            │   │
│  │     Step 4: Wait for diagnosis                     │   │
│  │     Step 5: Return to user/doctor                  │   │
│  │                                                     │   │
│  │  2. Complete Care Journey                          │   │
│  │     Step 1: Symptom Analysis                       │   │
│  │     Step 2: Diagnosis                              │   │
│  │     Step 3: Treatment Planning                     │   │
│  │     Step 4: Medication Management                  │   │
│  │     Step 5: Monitoring Setup                       │   │
│  │                                                     │   │
│  │  3. Emergency Escalation                           │   │
│  │     Step 1: Detect emergency                       │   │
│  │     Step 2: Notify on-call doctor                  │   │
│  │     Step 3: Alert emergency contacts               │   │
│  │     Step 4: Provide location info                  │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Agent Communication Manager                      │   │
│  │  • Message Publishing                               │   │
│  │  • Message Subscription                             │   │
│  │  • Request-Reply Pattern                            │   │
│  │  • Timeout Handling                                 │   │
│  │  • Retry Logic                                      │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Response Aggregator                              │   │
│  │  • Collect Responses from Multiple Agents          │   │
│  │  • Merge and De-duplicate                          │   │
│  │  • Prioritize Information                           │   │
│  │  • Format for Presentation                          │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Human-in-the-Loop Decider                        │   │
│  │  • Identify Decisions Requiring Human Input        │   │
│  │  • Escalate to Doctor When Necessary               │   │
│  │  • Confidence Threshold Checks                      │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    Care Journey Tracker                             │   │
│  │  • Track Patient Progress                           │   │
│  │  • Update Care Plan Status                          │   │
│  │  • Generate Care Summary                            │   │
│  │  • Identify Care Gaps                               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  State Machine for Care Journey:                            │
│                                                             │
│  [Initial] → [Symptoms Reported] → [Preliminary Diagnosis]  │
│     → [Doctor Review] → [Treatment Plan] → [Monitoring]     │
│     → [Follow-up] → [Outcome Tracking] → [Complete]         │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 Inter-Agent Communication Protocol

**Message Format (JSON):**
```json
{
  "message_id": "uuid-v4",
  "correlation_id": "uuid-v4",
  "timestamp": "2026-07-02T10:30:00Z",
  "sender": {
    "agent_id": "symptom-analyzer-01",
    "agent_type": "symptom_analyzer",
    "version": "v2.1.0"
  },
  "receiver": {
    "agent_id": "diagnostic-assistant-01",
    "agent_type": "diagnostic_assistant"
  },
  "message_type": "symptom_analysis_complete",
  "priority": "high",
  "payload": {
    "patient_id": "uuid",
    "session_id": "uuid",
    "structured_symptoms": [...],
    "urgency_level": "routine",
    "confidence_score": 0.92
  },
  "context": {
    "workflow_id": "uuid",
    "step": 2,
    "total_steps": 5
  },
  "metadata": {
    "processing_time_ms": 234,
    "model_version": "symptom-nlp-v2.1",
    "data_sources": ["conversation", "medical_history"]
  }
}
```

**Communication Patterns:**

1. **Request-Reply Pattern:**
```
Agent A → Request → Message Broker → Agent B
Agent A ← Reply ← Message Broker ← Agent B
```

2. **Pub-Sub Pattern:**
```
Agent A → Publish Event → Message Broker → Multiple Subscribers
```

3. **Choreography Pattern:**
```
Event 1 → Agent A → Event 2 → Agent B → Event 3 → Agent C
(Each agent knows what to do when it sees an event)
```

4. **Orchestration Pattern:**
```
Care Coordinator → Command → Agent A
Care Coordinator → Command → Agent B (after A completes)
Care Coordinator → Command → Agent C (after B completes)
```

### 2.4 Agent Deployment Model

**Kubernetes Deployment:**
```yaml
# Each agent is deployed as a Deployment with:
# - Horizontal Pod Autoscaler (HPA)
# - Resource limits
# - Health checks
# - Multiple replicas for high availability

Agent Instance → Pod → ReplicaSet → Deployment → Service → Ingress
```

**Scaling Strategy:**
- **CPU-based:** Scale when CPU > 70%
- **Memory-based:** Scale when Memory > 80%
- **Custom metrics:** Scale based on queue depth
- **Min replicas:** 2 (for HA)
- **Max replicas:** 10

---

## 3. Database Architecture

### 3.1 Polyglot Persistence Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│              DATABASE ARCHITECTURE OVERVIEW                     │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐    │
│  │          Application Services Layer                    │    │
│  └─────────┬──────────┬──────────┬──────────┬─────────────┘    │
│            │          │          │          │                   │
│            ▼          ▼          ▼          ▼                   │
│  ┌─────────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐        │
│  │ PostgreSQL  │ │ MongoDB │ │InfluxDB │ │  Redis   │        │
│  │             │ │         │ │         │ │          │        │
│  │ OLTP Data   │ │Document │ │Time-    │ │ Cache &  │        │
│  │ (Relational)│ │ Store   │ │Series   │ │ Session  │        │
│  └─────────────┘ └─────────┘ └─────────┘ └──────────┘        │
│                                                                 │
│  ┌─────────────┐ ┌─────────┐ ┌──────────────┐                │
│  │   AWS S3    │ │Pinecone │ │Elasticsearch │                │
│  │             │ │         │ │              │                │
│  │ Object      │ │Vector   │ │ Full-Text    │                │
│  │ Storage     │ │Database │ │ Search       │                │
│  └─────────────┘ └─────────┘ └──────────────┘                │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 PostgreSQL Schema Design

**Database:** `medinova_db`

**Schema Organization:**
```
medinova_db/
├── auth_schema/          # Authentication & Authorization
│   ├── users
│   ├── roles
│   ├── permissions
│   └── user_sessions
│
├── healthcare_schema/    # Core Healthcare Data
│   ├── patient_profiles
│   ├── doctor_profiles
│   ├── medical_history
│   ├── allergies
│   ├── medications
│   └── immunizations
│
├── clinical_schema/      # Clinical Operations
│   ├── appointments
│   ├── consultations
│   ├── prescriptions
│   ├── lab_tests
│   └── medical_images
│
└── audit_schema/         # Auditing & Compliance
    ├── audit_logs
    ├── data_access_logs
    └── consent_records
```


**Entity Relationship Design:**
```
users (1) ──────── (0..1) patient_profiles
  │                           │
  │                           │
  │                      (1) ─┴─ (0..*) medical_history
  │                           │
  │                      (1) ─┴─ (0..*) allergies
  │                           │
  │                      (1) ─┴─ (0..*) medications
  │
  │
  ├─ (1) ────── (0..1) doctor_profiles
  │                           │
  │                      (1) ─┴─ (0..*) appointments
  │
  │
  └─ (1) ────── (0..*) consultations
                              │
                         (1) ─┴─ (0..*) prescriptions
                              │
                         (1) ─┴─ (0..*) lab_tests
```

**Key Tables with Indexes:**
```sql
-- users table
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_created_at ON users(created_at);

-- appointments table  
CREATE INDEX idx_appointments_patient ON appointments(patient_id);
CREATE INDEX idx_appointments_doctor ON appointments(doctor_id);
CREATE INDEX idx_appointments_date ON appointments(appointment_date);
CREATE INDEX idx_appointments_status ON appointments(status);

-- medications table
CREATE INDEX idx_medications_patient ON medications(patient_id);
CREATE INDEX idx_medications_status ON medications(status);
CREATE INDEX idx_medications_dates ON medications(start_date, end_date);
```

**Data Partitioning Strategy:**
```
-- Partition audit_logs by month for performance
CREATE TABLE audit_logs (
    log_id UUID,
    timestamp TIMESTAMP,
    ...
) PARTITION BY RANGE (timestamp);

CREATE TABLE audit_logs_2026_07 PARTITION OF audit_logs
    FOR VALUES FROM ('2026-07-01') TO ('2026-08-01');
```

### 3.3 MongoDB Collections Design

**Database:** `medinova_documents`

**Collections:**

1. **symptom_reports** - Conversational symptom data
2. **ai_diagnoses** - AI-generated diagnostic reports
3. **treatment_plans** - Treatment recommendations
4. **agent_communications** - Inter-agent messages
5. **notifications** - User notifications
6. **medical_documents** - Scanned documents (metadata)

**Indexing Strategy:**
```javascript
// symptom_reports
db.symptom_reports.createIndex({ "patient_id": 1, "created_at": -1 })
db.symptom_reports.createIndex({ "session_id": 1 })
db.symptom_reports.createIndex({ "urgency_level": 1, "created_at": -1 })

// ai_diagnoses
db.ai_diagnoses.createIndex({ "patient_id": 1 })
db.ai_diagnoses.createIndex({ "consultation_id": 1 })
db.ai_diagnoses.createIndex({ "created_at": -1 })

// For text search
db.symptom_reports.createIndex({ "conversation.message": "text" })
```

**Sharding Strategy:**
```
// Shard by patient_id for horizontal scaling
sh.shardCollection("medinova_documents.symptom_reports", { "patient_id": 1 })
```

### 3.4 InfluxDB Time-Series Design

**Database:** `medinova_timeseries`

**Measurements:**

```
vital_signs
  tags: patient_id, device_id, source
  fields: heart_rate, bp_systolic, bp_diastolic, temperature, spo2
  timestamp: nanosecond precision

activity_data
  tags: patient_id, device_id
  fields: steps, distance_meters, calories_burned, active_minutes
  timestamp: nanosecond precision

health_scores
  tags: patient_id
  fields: overall_score, cardiovascular_score, metabolic_score
  timestamp: nanosecond precision
```

**Retention Policies:**
```
// Keep raw data for 90 days
CREATE RETENTION POLICY "raw_data" ON "medinova_timeseries" 
  DURATION 90d REPLICATION 1 DEFAULT

// Downsample to hourly aggregates, keep for 1 year
CREATE RETENTION POLICY "hourly" ON "medinova_timeseries" 
  DURATION 365d REPLICATION 1

// Downsample to daily aggregates, keep forever
CREATE RETENTION POLICY "daily" ON "medinova_timeseries" 
  DURATION INF REPLICATION 1
```

**Continuous Queries:**
```sql
// Downsample to hourly averages
CREATE CONTINUOUS QUERY "cq_vitals_hourly" ON "medinova_timeseries"
BEGIN
  SELECT mean(heart_rate) AS heart_rate, 
         mean(bp_systolic) AS bp_systolic
  INTO "hourly"."vital_signs_hourly"
  FROM "vital_signs"
  GROUP BY time(1h), patient_id
END
```

### 3.5 Redis Data Structures

**Key Patterns:**

```
// Session storage
session:{session_id} → Hash
  {user_id, role, exp, mfa_verified, ...}
  TTL: 1800 seconds (30 min)

// User cache
cache:user:{user_id} → String (JSON)
  {profile data}
  TTL: 900 seconds (15 min)

// Rate limiting
rate_limit:{user_id}:{endpoint} → String (counter)
  TTL: 60 seconds

// Real-time health alerts
alert:{patient_id} → List
  [alert1, alert2, ...]
  TTL: Based on alert type

// Agent context
agent:context:{session_id} → Hash
  {patient_id, current_step, conversation_state, ...}
  TTL: 3600 seconds

// Pub/Sub channels
channel:notifications:{user_id}
channel:health_alerts:{patient_id}
channel:agent_events
```

### 3.6 Data Access Patterns

**1. Write Path:**
```
Application → Write to Primary DB → Async Replication to Replicas
           → Publish Event to Message Broker
           → Invalidate Cache (if exists)
```

**2. Read Path (Hot Path):**
```
Application → Check Redis Cache
  ├─ Cache Hit → Return Data
  └─ Cache Miss → Query Database
                → Store in Cache
                → Return Data
```

**3. Analytics Query Path:**
```
Application → Read Replica / Data Warehouse
           → Aggregate
           → Cache Results
           → Return
```

### 3.7 Data Security

**Encryption:**
```
┌─────────────────────────────────────────────┐
│ Application Layer                           │
│ • Field-level encryption for PHI            │
│ • Encryption keys from KMS                  │
└──────────────────┬──────────────────────────┘
                   ▼
┌─────────────────────────────────────────────┐
│ Database Layer                              │
│ • TLS 1.3 for connections                   │
│ • Transparent Data Encryption (TDE)         │
│ • Encrypted backups                         │
└─────────────────────────────────────────────┘
```

**Access Control:**
- **Row-Level Security (RLS)** in PostgreSQL
- **Attribute-Based Access Control** at application layer
- **Audit logging** for all PHI access
- **Connection pooling** with dedicated service accounts

---

## 4. API Architecture

### 4.1 API Gateway Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                    API GATEWAY (Kong)                       │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Request Pipeline                                   │   │
│  │                                                     │   │
│  │  1. Rate Limiting                                  │   │
│  │     ↓                                              │   │
│  │  2. Authentication (JWT Validation)                │   │
│  │     ↓                                              │   │
│  │  3. Authorization (RBAC/ABAC)                      │   │
│  │     ↓                                              │   │
│  │  4. Request Transformation                         │   │
│  │     ↓                                              │   │
│  │  5. Routing to Backend Service                     │   │
│  │     ↓                                              │   │
│  │  6. Response Transformation                        │   │
│  │     ↓                                              │   │
│  │  7. Response Caching (if applicable)               │   │
│  │     ↓                                              │   │
│  │  8. Metrics & Logging                              │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 API Versioning Strategy

**URL-Based Versioning:**
```
https://api.medinova.ai/v1/users
https://api.medinova.ai/v2/users

Benefits:
- Clear and explicit
- Easy to route
- Browser-friendly
```

**Version Deprecation Policy:**
```
v1 Released → v2 Released (v1 maintained) → 
6 months → v1 deprecated warning → 
6 months → v1 sunset
```

### 4.3 RESTful API Design

**Resource Naming Convention:**
```
GET    /api/v1/users               # List users
POST   /api/v1/users               # Create user
GET    /api/v1/users/{id}          # Get user
PUT    /api/v1/users/{id}          # Update user
DELETE /api/v1/users/{id}          # Delete user

GET    /api/v1/patients/{id}/appointments
POST   /api/v1/patients/{id}/medical-history
GET    /api/v1/doctors/{id}/availability
```

**HTTP Status Codes:**
```
200 OK - Successful GET, PUT, PATCH
201 Created - Successful POST
204 No Content - Successful DELETE
400 Bad Request - Invalid input
401 Unauthorized - Authentication required
403 Forbidden - No permission
404 Not Found - Resource doesn't exist
409 Conflict - Resource conflict
422 Unprocessable Entity - Validation error
429 Too Many Requests - Rate limit exceeded
500 Internal Server Error - Server error
503 Service Unavailable - Service down
```

**Standard Response Format:**
```json
{
  "success": true,
  "data": {
    // Response data
  },
  "meta": {
    "timestamp": "2026-07-02T10:30:00Z",
    "request_id": "uuid",
    "version": "v1"
  },
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

**Error Response Format:**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  },
  "meta": {
    "timestamp": "2026-07-02T10:30:00Z",
    "request_id": "uuid"
  }
}
```

### 4.4 API Security

**Authentication Flow:**
```
Client → POST /auth/login {email, password}
  ↓
Server validates credentials
  ↓
Server generates JWT access token (15 min) + refresh token
  ↓
Client stores tokens (httpOnly cookie or secure storage)
  ↓
Client → GET /api/v1/resource with Bearer token
  ↓
API Gateway validates JWT
  ↓
Route to backend service
```

**JWT Token Structure:**
```json
{
  "header": {
    "alg": "RS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user_id",
    "role": "patient",
    "permissions": ["read:own_profile", "write:symptoms"],
    "iat": 1656756000,
    "exp": 1656756900
  },
  "signature": "..."
}
```

### 4.5 Rate Limiting

**Tiers:**
```
Patient:  100 requests/minute, 5000 requests/day
Doctor:   500 requests/minute, 25000 requests/day
Admin:    1000 requests/minute, 50000 requests/day
Anonymous: 20 requests/minute, 500 requests/day
```

**Implementation (Redis):**
```
Key: rate_limit:{user_id}:{minute}
Value: request_count
TTL: 60 seconds

If request_count >= limit:
  Return 429 Too Many Requests
Else:
  Increment request_count
  Process request
```

---

## 5. Frontend Architecture

### 5.1 Web Application Architecture (React)

```
┌─────────────────────────────────────────────────────────────┐
│                  FRONTEND ARCHITECTURE                      │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │            Presentation Layer                       │   │
│  │                                                     │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────┐  │   │
│  │  │   Pages      │  │  Components  │  │ Layouts │  │   │
│  │  │              │  │              │  │         │  │   │
│  │  │ • Dashboard  │  │ • Common     │  │ • Auth  │  │   │
│  │  │ • Profile    │  │ • Patient    │  │ • Main  │  │   │
│  │  │ • Symptom    │  │ • Doctor     │  │ • Admin │  │   │
│  │  │   Checker    │  │ • Admin      │  │         │  │   │
│  │  └──────────────┘  └──────────────┘  └─────────┘  │   │
│  └──────────────────────────┬──────────────────────────┘   │
│                             ▼                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │            State Management Layer                   │   │
│  │                                                     │   │
│  │  ┌──────────────────────────────────────────┐      │   │
│  │  │  Redux Store / Zustand                   │      │   │
│  │  │                                          │      │   │
│  │  │  • authSlice (user, tokens, session)    │      │   │
│  │  │  • patientSlice (profile, history)      │      │   │
│  │  │  • symptomSlice (reports, analysis)     │      │   │
│  │  │  • appointmentSlice (bookings)          │      │   │
│  │  │  • notificationSlice (alerts)           │      │   │
│  │  │  • uiSlice (modals, toasts, loading)    │      │   │
│  │  └──────────────────────────────────────────┘      │   │
│  └──────────────────────────┬──────────────────────────┘   │
│                             ▼                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │            Business Logic Layer                     │   │
│  │                                                     │   │
│  │  • Custom Hooks (useAuth, useSymptoms, etc.)      │   │
│  │  • Utility Functions                               │   │
│  │  • Validators                                      │   │
│  │  • Formatters                                      │   │
│  └──────────────────────────┬──────────────────────────┘   │
│                             ▼                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │            Data Access Layer (Services)             │   │
│  │                                                     │   │
│  │  • API Client (axios/fetch)                        │   │
│  │  • authService.ts                                  │   │
│  │  • userService.ts                                  │   │
│  │  • symptomService.ts                               │   │
│  │  • appointmentService.ts                           │   │
│  │  • WebSocket Client                                │   │
│  └──────────────────────────┬──────────────────────────┘   │
│                             ▼                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │            API Gateway                              │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Component Architecture

**Atomic Design Pattern:**
```
Atoms (Basic building blocks)
  ├─ Button
  ├─ Input
  ├─ Label
  ├─ Icon
  └─ Avatar

Molecules (Simple combinations)
  ├─ FormField (Label + Input + Error)
  ├─ SearchBar (Input + Icon + Button)
  └─ Card

Organisms (Complex components)
  ├─ Header (Logo + Navigation + User Menu)
  ├─ SymptomForm (Multiple FormFields + Logic)
  └─ AppointmentCard (Card + Multiple Molecules)

Templates (Page layouts)
  ├─ DashboardTemplate
  ├─ AuthTemplate
  └─ TwoColumnTemplate

Pages (Specific instances)
  ├─ PatientDashboard
  ├─ Login
  └─ SymptomChecker
```

### 5.3 Routing Strategy

```typescript
// Route Structure
/                           # Landing page
/login                      # Login
/register                   # Registration
/dashboard                  # Role-based dashboard redirect
  ├─ /patient              # Patient dashboard
  │   ├─ /symptoms          # Symptom checker
  │   ├─ /appointments      # Appointments
  │   ├─ /medications       # Medications
  │   ├─ /health-monitor    # Health monitoring
  │   └─ /profile           # Profile
  ├─ /doctor               # Doctor dashboard
  │   ├─ /patients          # Patient list
  │   ├─ /consultations     # Consultations
  │   ├─ /schedule          # Schedule management
  │   └─ /analytics         # Analytics
  └─ /admin                # Admin dashboard
      ├─ /users             # User management
      ├─ /system            # System settings
      └─ /reports           # Reports
```

**Route Protection:**
```typescript
// Protected Route Component
<ProtectedRoute 
  path="/dashboard/patient" 
  allowedRoles={['patient']}
  requireMFA={false}
>
  <PatientDashboard />
</ProtectedRoute>
```

### 5.4 State Management Pattern

**Redux Store Structure:**
```
store/
├─ auth/
│   ├─ auth.slice.ts
│   ├─ auth.selectors.ts
│   └─ auth.thunks.ts
├─ patient/
│   ├─ patient.slice.ts
│   └─ patient.thunks.ts
├─ symptom/
├─ appointment/
└─ store.ts (root)
```

**Data Flow:**
```
User Action → Component → dispatch(action)
  → Redux Middleware (thunk/saga)
  → API Call
  → dispatch(success/error action)
  → Reducer updates state
  → Component re-renders with new state
```

### 5.5 Performance Optimization

**Code Splitting:**
```typescript
// Lazy load routes
const PatientDashboard = lazy(() => import('./pages/PatientDashboard'));
const DoctorDashboard = lazy(() => import('./pages/DoctorDashboard'));

// Split by route
<Suspense fallback={<LoadingSpinner />}>
  <Routes>
    <Route path="/patient/*" element={<PatientDashboard />} />
    <Route path="/doctor/*" element={<DoctorDashboard />} />
  </Routes>
</Suspense>
```

**Caching Strategy:**
```
1. Browser Cache (static assets) - 1 year
2. Service Worker Cache (offline support)
3. React Query for API response caching
4. Memoization (useMemo, React.memo)
```

**Bundle Optimization:**
```
- Tree shaking (remove unused code)
- Minification
- Compression (gzip/brotli)
- Image optimization (WebP, lazy loading)
- Font subsetting
```

---

