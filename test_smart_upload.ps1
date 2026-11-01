# Test Smart Upload API endpoint
$apiUrl = "http://localhost:8000/api/v1/documents/upload-medical-record"
$imagePath = "C:\Users\vasuk\OneDrive\Desktop\MediNova\sample_blood_report.png"

Write-Host "Testing Smart Upload API..." -ForegroundColor Cyan
Write-Host "Endpoint: $apiUrl" -ForegroundColor Yellow
Write-Host "Image: $imagePath" -ForegroundColor Yellow

# Check if file exists
if (-not (Test-Path $imagePath)) {
    Write-Host "ERROR: Image file not found!" -ForegroundColor Red
    exit 1
}

# Create multipart form data
$boundary = [System.Guid]::NewGuid().ToString()
$fileBytes = [System.IO.File]::ReadAllBytes($imagePath)
$fileName = [System.IO.Path]::GetFileName($imagePath)

# Build multipart body
$bodyLines = @(
    "--$boundary",
    "Content-Disposition: form-data; name=`"file`"; filename=`"$fileName`"",
    "Content-Type: image/png",
    "",
    [System.Text.Encoding]::GetEncoding("iso-8859-1").GetString($fileBytes),
    "--$boundary",
    "Content-Disposition: form-data; name=`"auto_save`"",
    "",
    "false",
    "--$boundary",
    "Content-Disposition: form-data; name=`"record_type`"",
    "",
    "lab_report",
    "--$boundary--"
)

$body = $bodyLines -join "`r`n"

# Send POST request
try {
    Write-Host "`nSending request to API..." -ForegroundColor Cyan
    $response = Invoke-RestMethod -Uri $apiUrl -Method Post -Body $body -ContentType "multipart/form-data; boundary=$boundary" -TimeoutSec 60
    
    Write-Host "`n✅ SUCCESS! Smart Upload is working!" -ForegroundColor Green
    Write-Host "`nExtracted Data:" -ForegroundColor Cyan
    $response | ConvertTo-Json -Depth 10
    
} catch {
    Write-Host "`n❌ FAILED! Error occurred:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $reader.BaseStream.Position = 0
        $responseBody = $reader.ReadToEnd()
        Write-Host "`nServer Response:" -ForegroundColor Yellow
        Write-Host $responseBody
    }
}
