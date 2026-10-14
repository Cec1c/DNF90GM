@echo off
setlocal
cd /d "%~dp0"
if not exist "runtime\gm.json" (
  echo Configure runtime\gm.json using config\gm.example.json first.
  exit /b 1
)
"dist\windows-amd64\DNF90GM.exe" --config "runtime\gm.json" %*
exit /b %errorlevel%
