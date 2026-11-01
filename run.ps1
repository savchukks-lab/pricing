$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$taskPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $taskPython)) {
    $taskPython = Join-Path $env:LOCALAPPDATA 'Python\pythoncore-3.14-64\python.exe'
}
if (-not (Test-Path -LiteralPath $taskPython)) {
    throw 'Python was not found. Create .venv and install requirements.txt first.'
}
& $taskPython -m streamlit run app.py --server.port 8502 @args
