$pycacheDirs = Get-ChildItem -Path . -Recurse -Directory -Force | Where-Object { $_.Name -eq "__pycache__" }

foreach ($dir in $pycacheDirs) {
    Write-Host "Deleting $($dir.FullName)"
    Remove-Item -Path $dir.FullName -Recurse -Force
}

Write-Host "Done deleting all __pycache__ directories."
