# run.ps1
$venvPython = ".\venv\Scripts\python.exe"

$versionOutput = & $venvPython --version
if ($versionOutput -notmatch "Python 3\.13\.7") {
    Write-Error "Warning Python version deprecated. Expected Python 3.13.7, but got: $versionOutput"
}

if (-not (Test-Path $venvPython)) {
    Write-Warning "Virtual environment not found. Please run install.ps1 first."
}

# Ensure project root is on PYTHONPATH so `import src` works
$projectRoot = (Get-Location).Path
$env:PYTHONPATH = $projectRoot

# Run the application module so imports resolve consistently
& $venvPython -m src.main @args
