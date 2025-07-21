REM @ECHO OFF
IF NOT EXIST "folder.txt" (
    ECHO Error: folder.txt not found.
    EXIT /B 1
)

move *.zip old_builds
del *.zip
del *.json


SET /P MyVar=<folder.txt


cd create_empty_vertex_child
call build.bat
cd ..
cd quick_cloth_tool
call build.bat
cd ..
cd vertex_bone_picker
call build.bat
cd ..
cd johnnygizmo_rigging_tools
call build.bat
cd ..
cd harmony
call build.bat
cd ..

cd modifier_node_edit_panel
call build.bat
cd ..





"%MyVar%\blender.exe" --command extension server-generate --repo-dir=./
REM "%MyVar%\blender.exe" --command extension server-generate --repo-dir=./ --html
cd old_builds
call index.bat
cd ..