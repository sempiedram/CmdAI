
@echo off
if "%~1"=="run" if "%~2"=="" (
    echo RUN
    set "original_dir=%cd%"
    pushd %~dp0
    call .\venv\Scripts\activate.bat
    call key_gemini_env.bat
    popd
    python cai_script.py "%original_dir%" %*
    call deactivate.bat
    exit /b
)
if "%~1"=="run" if not "%~2"=="" if "%~3"=="" (
    echo RUN %~2
    set "original_dir=%cd%"
    pushd "%~dp0"
    echo dp0: "%~dp0"
    call .\venv\Scripts\activate.bat
    call key_gemini_env.bat
    popd
    echo python "%~dp0\saved_scripts\%~2.cai_script.py" "%original_dir%" %*
    python "%~dp0\saved_scripts\%~2.cai_script.py" "%original_dir%" %*
    call deactivate.bat
    exit /b
)
if "%~1"=="save" if not "%~2"=="" if "%~3"=="" (
    echo Saving cai_script.py as %~2
    set "original_dir=%cd%"
    pushd %~dp0
    copy "%original_dir%\cai_script.py" ".\saved_scripts\%~2.cai_script.py"
    popd
    exit /b
)
if "%~1"=="clean" if "%~2"=="" (
    echo CLEAN
    del cai_script.py
    exit /b
)
if "%~1"=="install" if "%~2"=="" (
    echo "Install command requires library name to be installed:"
    echo "cai install <library name>"
    exit /b
)
if "%~1"=="install" if not "%~2"=="" (
    echo Installing library "%~2"...
    set "original_dir=%cd%"
    pushd %~dp0
    call .\venv\Scripts\activate.bat
    python -m pip install %~2
    call deactivate.bat
    popd
    exit /b
)

set "original_dir=%cd%"
pushd %~dp0
call .\venv\Scripts\activate.bat
call key_gemini_env.bat
python cai.py "%original_dir%" %*
call deactivate.bat
popd
