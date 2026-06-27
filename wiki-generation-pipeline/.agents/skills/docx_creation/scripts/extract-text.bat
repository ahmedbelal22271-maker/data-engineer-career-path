@echo off
REM extract-text.bat — Extract text from .docx as markdown via pandoc
REM Usage: extract-text document.docx

if "%1"=="" (
    echo Usage: extract-text document.docx
    exit /b 1
)

pandoc "%1" -t markdown --wrap=none 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: pandoc not found or conversion failed. Install pandoc from https://pandoc.org/
    exit /b 1
)
