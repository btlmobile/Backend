Write-Host "Exporting Swagger documentation..." -ForegroundColor Green

$pythonPath = "..\..\venv\Scripts\python.exe"
if (-not (Test-Path $pythonPath)) {
    Write-Host "Python virtual environment not found. Please run install.ps1 first." -ForegroundColor Red
    exit 1
}

& $pythonPath export_swagger.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "Swagger documentation exported successfully!" -ForegroundColor Green
    Write-Host "Open swagger/index.html in your browser to view the documentation." -ForegroundColor Yellow
} else {
    Write-Host "Failed to export Swagger documentation." -ForegroundColor Red
    exit 1
}
