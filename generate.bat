@ECHO OFF
IF NOT EXIST "folder.txt" (
    ECHO Error: folder.txt not found.
    EXIT /B 1
)

del *.zip
del *.json
del *.html

SET /P MyVar=<folder.txt


cd create_empty_vertex_child
call build.bat
cd ..
cd quick_cloth_tool
call build.bat
cd ..



"c:\blender\%MyVar%\blender.exe" --command extension server-generate --repo-dir=./
"c:\blender\%MyVar%\blender.exe" --command extension server-generate --repo-dir=./ --html