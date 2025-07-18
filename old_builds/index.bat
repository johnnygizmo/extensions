@echo off
setlocal enabledelayedexpansion

:: File to write
set "indexFile=index.html"

:: Write HTML header
(
echo ^<!DOCTYPE html^>
echo ^<html^>
echo ^<head^>
echo     ^<meta charset="UTF-8"^>
echo     ^<title^>Old Extension Builds</title^>
echo     ^<style^>
echo         body { font-family: monospace; padding: 20px; }
echo         a { text-decoration: none; color: #00f; }
echo     ^</style^>
echo ^</head^>
echo ^<body^>
echo     ^<h2^>Previous Builds^</h2^>
echo     ^<hr^>
echo     ^<pre^>
) > index.html

:: List all .zip files
for %%F in (*.zip) do (
    set "filename=%%F"
    set "filesize=%%~zF"
    set "datetime=%%~tF"
    echo     ^<a href="!filename!"^>!filename!^</a^>  >> index.html
)

:: Close HTML
(
echo     ^</pre^>
echo     ^<hr^>
echo ^</body^>
echo ^</html^>
) >> index.html

echo index.html created successfully.
