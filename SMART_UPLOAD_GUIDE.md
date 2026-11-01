# Smart Upload Feature - User Guide

## Overview
The Smart Upload feature uses AI to automatically extract information from your medical documents, making it easy to add medicines and health records without manual typing.

---

## Getting Started

### 1. Access Smart Upload
- Log in to your patient account
- Click **"Smart Upload"** in the left sidebar (between "AI Assistant" and "QR Health ID")

### 2. Choose Document Type
You'll see two options:
- **Prescription** - For medicine prescriptions from your doctor
- **Lab Report** - For blood tests, X-rays, MRI reports, etc.

---

## Uploading a Prescription

### Step 1: Select Prescription Type
Click on the **"Prescription"** card.

### Step 2: Upload Your File
- Click **"Select File"** or drag and drop
- Supported formats: JPEG, PNG, WEBP, PDF
- Maximum size: 10 MB
- Make sure the image is clear and readable

### Step 3: Extract Information
Click the **"Extract Info"** button with the sparkle icon ✨

The system will:
1. Extract text from your document using OCR
2. Use AI to identify medicines and their details
3. Show you the extracted information with confidence levels

### Step 4: Review Extracted Medicines
You'll see each medicine in an expandable card showing:
- **Medicine Name**
- **Dosage** (e.g., 500mg, 5ml)
- **Frequency** (e.g., twice daily)
- **Duration** (number of days)
- **Instructions** (how to take it)
- **Meal Timing** (before/after/with food)
- **Current Stock** (number of pills)
- **Confidence Level** (high/medium/low)

**Confidence Indicators:**
- 🟢 **High confidence** (green) - Information extracted clearly
- 🟡 **Medium confidence** (amber) - Please double-check
- 🔴 **Low confidence** (red) - Likely needs correction

### Step 5: Edit if Needed
- Click on any card to expand it
- Edit any field that looks incorrect
- Change dosage, frequency, or instructions
- Update stock quantity if you know it
- Remove medicines that were extracted incorrectly (click "Remove this medicine")

### Step 6: Save All Medicines
- Click **"Save All"** button at the top
- Medicines will be added to your Medications tracker
- Reminders will be created automatically
- You'll receive a notification confirming the save

### What Happens Next?
- Medicines appear in your **"Medications"** page
- Automatic reminders are set based on schedule
- Stock levels are tracked
- You'll get low-stock alerts when needed

---

## Uploading a Medical Record

### Step 1: Select Lab Report Type
Click on the **"Lab Report"** card.

### Step 2: Upload Your File
- Click **"Select File"** or drag and drop
- Supported formats: JPEG, PNG, WEBP, PDF
- Maximum size: 10 MB
- Works with blood test reports, X-rays, MRI reports, etc.

### Step 3: Extract Information
Click the **"Extract Info"** button ✨

The system will:
1. Extract text using OCR
2. Identify test parameters and values
3. Detect normal/abnormal/critical values
4. Extract diagnosis and summary

### Step 4: Review Extracted Information
You'll see:
- **Report Name** (e.g., "Complete Blood Count")
- **Summary** (brief overview)
- **Key Findings** with color-coded status:
  - 🟢 Normal
  - 🟡 High/Low
  - 🔴 Critical
- **Test Date** (if found)
- **Doctor Name** (if found)

### Step 5: Record Saved Automatically
If everything looks good, the record is automatically saved to your **"Health Record"** page.

You'll see a confirmation message and can view all your records there.

---

## Tips for Best Results

### 📸 Taking Good Photos
1. **Good Lighting** - Use natural light or bright indoor lighting
2. **Flat Surface** - Place document on a flat surface
3. **No Shadows** - Avoid shadows on the document
4. **Sharp Focus** - Make sure text is clear and readable
5. **Complete Document** - Include all pages if multi-page
6. **No Obstructions** - Remove any objects covering text

### ✅ What Works Well
- Printed prescriptions from doctors
- Typed lab reports from hospitals
- Official medical documents
- Clear, high-resolution photos
- PDFs from hospital portals

### ⚠️ What Might Need Manual Review
- Handwritten prescriptions (may have errors)
- Faded or old documents
- Low-quality photocopies
- Documents with stamps or signatures over text
- Very small text

---

## Common Questions

### Q: Can I upload multiple prescriptions at once?
**A:** Currently, you need to upload one at a time. Each upload is processed individually.

### Q: What if the AI gets something wrong?
**A:** You can edit any field before saving. Just click on the medicine card to expand it and make corrections.

### Q: Will it create duplicate medicines?
**A:** No! The system checks for duplicates and won't add the same medicine twice.

### Q: What if my document doesn't upload?
**A:** Check that:
- File size is under 10 MB
- File format is JPEG, PNG, WEBP, or PDF
- You have a stable internet connection
- Your GEMINI_API_KEY is configured (ask your admin)

### Q: Can I delete medicines after upload?
**A:** Yes! Go to your **"Medications"** page and delete any medicine you don't want.

### Q: What happens to my uploaded documents?
**A:** Documents are processed and then immediately deleted. Only the extracted text information is stored.

### Q: Is my data secure?
**A:** Yes! All data is:
- Encrypted in transit
- Stored securely in the database
- Only accessible to you
- Never shared without permission

### Q: Can I see what text was extracted?
**A:** Yes! The extracted text is shown in the results. You can verify it matches your document.

---

## Troubleshooting

### Upload Failed
**Problem:** "OCR failed" or "Upload failed" error

**Solutions:**
1. Check your internet connection
2. Try a smaller file (compress the image)
3. Make sure the image is clear
4. Try a different file format (PNG instead of JPEG)
5. Refresh the page and try again

### No Medicines Extracted
**Problem:** "No medicines found" or empty results

**Solutions:**
1. Make sure you uploaded a prescription (not a lab report)
2. Check if the document is readable (not too blurry)
3. Try taking a new photo with better lighting
4. If it's handwritten, consider typing it in manually

### Wrong Information Extracted
**Problem:** Medicine names or dosages are incorrect

**Solutions:**
1. Edit the fields before saving
2. Check the confidence level - low confidence means review carefully
3. Compare with your physical prescription
4. Remove incorrect entries and add manually if needed

### Can't Save Medicines
**Problem:** "Failed to save" error

**Solutions:**
1. Check if the medicine already exists (duplicate)
2. Make sure medicine name and dosage are filled
3. Try saving them one at a time
4. Contact support if the issue persists

---

## Advanced Tips

### 🎯 Maximizing Accuracy
- Upload prescriptions soon after receiving them (while they're crisp)
- Use your phone's document scan mode if available
- For PDFs, use the original digital file rather than a scan

### 🔄 Workflow Suggestions
1. **After Doctor Visit:**
   - Take a photo of prescription immediately
   - Upload via Smart Upload
   - Review and save before leaving pharmacy

2. **After Lab Tests:**
   - Get digital copy from hospital portal
   - Upload to Smart Upload
   - Compare with AI analysis in AI Assistant

3. **Stock Management:**
   - Upload new prescriptions each time
   - System tracks remaining quantity
   - Get refill reminders automatically

### 📱 Mobile Tips
- Use portrait mode for better resolution
- Zoom in slightly on the prescription
- Take multiple photos and choose the clearest one

---

## Feature Limits

### Rate Limits
- **10 uploads per minute** per user
- This prevents system abuse and ensures good performance for everyone

If you hit the limit, wait 60 seconds and try again.

### File Limits
- **Maximum file size:** 10 MB
- **Supported formats:** JPEG, PNG, WEBP, BMP, PDF
- **PDF pages:** Up to 10 pages processed

---

## Privacy & Security

### What We Store
- Extracted text from documents (not images)
- Medicine information you confirm
- Medical record summaries and findings

### What We DON'T Store
- Original images or PDFs (deleted immediately after processing)
- Information you don't confirm/save
- Any data you remove or edit out

### Who Can See Your Data
- **Only you** can see your uploaded information
- Doctors you share with (via secure sharing features)
- System admins cannot access your medical data without authorization

---

## Support

### Need Help?
- Check this guide first
- Try the **AI Assistant** for health questions
- Contact support via the Help button
- Report bugs via the Feedback form

### Providing Feedback
We're constantly improving! Let us know:
- What worked well
- What could be better
- Feature suggestions
- Any issues you encountered

---

**Happy Smart Uploading! 🎉**

Your health data, simplified with AI.
