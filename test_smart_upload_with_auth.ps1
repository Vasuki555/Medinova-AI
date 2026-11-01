# Complete Smart Upload Test with Authentication
$baseUrl = "http://localhost:8000/api/v1"
$imagePath = "C:\Users\vasuk\OneDrive\Desktop\MediNova\sample_blood_report.png"

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "MediNova Smart Upload Test" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check if test user exists, if not create one
Write-Host "[Step 1] Checking test user..." -ForegroundColor Yellow

$testEmail = "upload.test$(Get-Random)@medinova.com"
$testPassword = "Upload@Test123"

# Try to register (will fail if user exists, which is fine)
$registerBody = @{
    email = $testEmail
    password = $testPassword
    first_name = "Test"
    last_name = "User"
    role = "patient"
    phone = "+1234567890"
    date_of_birth = "1990-01-01"
    gender = "other"
} | ConvertTo-Json

try {
    $regResponse = Invoke-RestMethod -Uri "$baseUrl/auth/register" -Method Post -Body $registerBody -ContentType "application/json"
    Write-Host "Test user created successfully" -ForegroundColor Green
    Write-Host "User ID: $($regResponse.user.id)" -ForegroundColor Gray
} catch {
    $errorMsg = $_.Exception.Message
    if ($errorMsg -like "*409*" -or $errorMsg -like "*already exists*") {
        Write-Host "Test user already exists (using existing account)" -ForegroundColor Yellow
    } else {
        Write-Host "Registration error: $errorMsg" -ForegroundColor Red
        if ($_.Exception.Response) {
            $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
            $reader.BaseStream.Position = 0
            $responseBody = $reader.ReadToEnd()
            Write-Host "Details: $responseBody" -ForegroundColor Gray
        }
    }
}

# Step 2: Login to get token
Write-Host ""
Write-Host "[Step 2] Logging in..." -ForegroundColor Yellow

$loginBody = @{
    email = $testEmail
    password = $testPassword
} | ConvertTo-Json

try {
    $loginResponse = Invoke-RestMethod -Uri "$baseUrl/auth/login" -Method Post -Body $loginBody -ContentType "application/json"
    $token = $loginResponse.access_token
    Write-Host "Login successful" -ForegroundColor Green
} catch {
    Write-Host "Login failed!" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $reader.BaseStream.Position = 0
        $responseBody = $reader.ReadToEnd()
        Write-Host "Server response: $responseBody" -ForegroundColor Gray
    }
    Write-Host ""
    Write-Host "[Debug] Email: $testEmail" -ForegroundColor Gray
    Write-Host "[Debug] Password: $testPassword" -ForegroundColor Gray
    exit 1
}

# Step 3: Upload medical document
Write-Host ""
Write-Host "[Step 3] Uploading medical document..." -ForegroundColor Yellow

if (-not (Test-Path $imagePath)) {
    Write-Host "Image file not found!" -ForegroundColor Red
    exit 1
}

# Read file
$fileBytes = [System.IO.File]::ReadAllBytes($imagePath)
$fileName = [System.IO.Path]::GetFileName($imagePath)

# Create multipart form data
$boundary = [System.Guid]::NewGuid().ToString()
$LF = "`r`n"

[System.Text.StringBuilder]$bodyBuilder = New-Object System.Text.StringBuilder

# Add file field
[void]$bodyBuilder.Append("--$boundary$LF")
[void]$bodyBuilder.Append("Content-Disposition: form-data; name=`"file`"; filename=`"$fileName`"$LF")
[void]$bodyBuilder.Append("Content-Type: image/png$LF$LF")

# Convert to bytes
$bodyBytesStart = [System.Text.Encoding]::UTF8.GetBytes($bodyBuilder.ToString())

# Add remaining fields
[System.Text.StringBuilder]$bodyBuilderEnd = New-Object System.Text.StringBuilder
[void]$bodyBuilderEnd.Append("$LF--$boundary$LF")
[void]$bodyBuilderEnd.Append("Content-Disposition: form-data; name=`"auto_save`"$LF$LF")
[void]$bodyBuilderEnd.Append("false$LF")
[void]$bodyBuilderEnd.Append("--$boundary$LF")
[void]$bodyBuilderEnd.Append("Content-Disposition: form-data; name=`"record_type`"$LF$LF")
[void]$bodyBuilderEnd.Append("lab_report$LF")
[void]$bodyBuilderEnd.Append("--$boundary--$LF")

$bodyBytesEnd = [System.Text.Encoding]::UTF8.GetBytes($bodyBuilderEnd.ToString())

# Combine all parts
$bodyBytes = $bodyBytesStart + $fileBytes + $bodyBytesEnd

# Send request with authentication
$headers = @{
    "Authorization" = "Bearer $token"
}

try {
    Write-Host "Uploading..." -ForegroundColor Gray
    $uploadResponse = Invoke-RestMethod -Uri "$baseUrl/documents/upload-medical-record" -Method Post -Body $bodyBytes -ContentType "multipart/form-data; boundary=$boundary" -Headers $headers -TimeoutSec 90
    
    Write-Host ""
    Write-Host "SUCCESS! Smart Upload is working!" -ForegroundColor Green
    Write-Host ""
    Write-Host "======================================" -ForegroundColor Cyan
    Write-Host "Extracted Information:" -ForegroundColor Cyan
    Write-Host "======================================" -ForegroundColor Cyan
    
    # Display results
    if ($uploadResponse.success) {
        Write-Host ""
        Write-Host "Extracted Text (first 200 chars):" -ForegroundColor Yellow
        $text = $uploadResponse.extracted_text
        if ($text.Length -gt 200) {
            Write-Host $text.Substring(0, 200) + "..." -ForegroundColor White
        } else {
            Write-Host $text -ForegroundColor White
        }
        
        Write-Host ""
        Write-Host "Word Count: $($uploadResponse.word_count)" -ForegroundColor Yellow
        
        if ($uploadResponse.record_info) {
            $info = $uploadResponse.record_info
            Write-Host ""
            Write-Host "Medical Record Information:" -ForegroundColor Yellow
            Write-Host ($info | ConvertTo-Json -Depth 5) -ForegroundColor White
        }
    }
    
    Write-Host ""
    Write-Host "======================================" -ForegroundColor Cyan
    Write-Host "Test completed successfully!" -ForegroundColor Green
    Write-Host "======================================" -ForegroundColor Cyan
    
} catch {
    Write-Host ""
    Write-Host "Upload failed!" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $reader.BaseStream.Position = 0
        $responseBody = $reader.ReadToEnd()
        Write-Host ""
        Write-Host "Server Response:" -ForegroundColor Yellow
        Write-Host $responseBody -ForegroundColor White
    }
    
    Write-Host ""
    Write-Host "[Tip] Check backend logs for more details" -ForegroundColor Gray
    exit 1
}
