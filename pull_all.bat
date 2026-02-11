
@REM Loop through extensions list
IF NOT EXIST "extensions_list.txt" (
    ECHO Error: extensions_list.txt not found.
    EXIT /B 1
)

FOR /F "tokens=*" %%E IN (extensions_list.txt) DO (
    cd ..
    cd %%E
    git pull
    cd ..
    cd extensions
)

