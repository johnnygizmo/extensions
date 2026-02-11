REM @ECHO OFF
IF NOT EXIST "folder.txt" (
    ECHO Error: folder.txt not found.
    EXIT /B 1
)

move *.zip old_builds
del *.zip
del *.json


SET /P MyVar=<folder.txt

@REM -------------------------------------------------------

@REM Loop through extensions list
IF NOT EXIST "extensions_list.txt" (
    ECHO Error: extensions_list.txt not found.
    EXIT /B 1
)

FOR /F "tokens=*" %%E IN (extensions_list.txt) DO (
    cd ..
    cd %%E
    call ..\extensions\build.bat
    cd ..
    cd extensions
)


"%MyVar%\blender.exe" --command extension server-generate --repo-dir=./
REM "%MyVar%\blender.exe" --command extension server-generate --repo-dir=./ --html
cd old_builds
call index.bat
cd ..