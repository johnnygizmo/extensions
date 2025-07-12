@echo off
setlocal enabledelayedexpansion

:: Output file
set "outfile=output.txt"
echo. > "%outfile%"  -----------

:: Loop through all .py files
for %%F in (*.py) do (
    echo ===== FILE: %%F ===== >> "%outfile%"
    type "%%F" >> "%outfile%"
    echo. >> "%outfile%"
    echo. >> "%outfile%"
)

echo All .py files have been written to %outfile%.
pause