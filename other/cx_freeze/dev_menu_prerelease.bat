@ECHO OFF
SET releaseoption=0
SET checkoption=0
SET cleanupval=0
:MENU
CLS
ECHO -----------------------------------------------
ECHO Dungeonblade Pre-Release Release Utility
ECHO -----------------------------------------------
ECHO.
ECHO 1 - Release
ECHO 2 - Validate manifest
ECHO 3 - itch.io build status.
ECHO 4 - Push File List.
ECHO 5 - EXIT
ECHO.
SET /P M=Option:
IF %M%==1 SET releaseoption=1
IF %M%==1 GOTO CLEANUP
IF %M%==2 GOTO VALIDATE
IF %M%==3 GOTO STATUS
IF %M%==4 GOTO PUSHFILELISTMENU
IF %M%==5 EXIT

:PUSHFILELISTMENU
CLS
ECHO -----------------------------------------------
ECHO Push File List for:
ECHO -----------------------------------------------
ECHO.
ECHO 1 - Release
ECHO 2 - Back
ECHO.
SET /P M=Option:
IF %M%==1 SET checkoption=1
IF %M%==1 GOTO CLEANUP_DRY
IF %M%==2 GOTO MENU

:CLEANJUNK
CLS
copy ".itch.toml" "build\.itch.toml"

echo Build files generated.
IF %cleanupval%==1 GOTO POSTCLEANUP
IF %cleanupval%==2 GOTO POSTCLEANUP_DRY

:CLEANUP
CLS
SET cleanupval==1
GOTO CLEANJUNK

:POSTCLEANUP
IF %releaseoption%==1 echo Press any key to push Release build
pause
IF %releaseoption%==1 GOTO RELEASE

:CLEANUP_DRY
CLS
SET cleanupval==2
GOTO CLEANJUNK

:POSTCLEANUP_DRY
IF %checkoption%==1 echo Press any key to check Release build
pause
IF %checkoption%==1 GOTO RELEASE_DRY

:RELEASE
CLS
butler push build bitl/dungeonblade-hk:windows-beta --if-changed --userversion-file betaversion.txt
pause
rmdir /Q /S build
GOTO MENU

:RELEASE_DRY
CLS
butler push build bitl/dungeonblade-hk:windows-beta --if-changed --dry-run --userversion-file betaversion.txt
pause
rmdir /Q /S build
GOTO MENU

:VALIDATE
CLS
butler validate build
pause
GOTO MENU

:STATUS
CLS
echo RELEASE
butler status bitl/dungeonblade-hk:windows-beta
pause
GOTO MENU