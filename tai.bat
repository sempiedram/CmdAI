
@echo off
pushd %~dp0
call .\venv\Scripts\activate.bat
call key_gemini_env.bat
python tai.py %*
call deactivate.bat
popd
