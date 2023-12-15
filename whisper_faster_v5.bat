@echo off

if exist "C:\AI\Whisper\_stateR.txt" EXIT

@echo running > _stateR.txt

for %%a in ("C:\AI\Whisper\wav\*.wav") do ( 
    echo "%%a"
    echo "%%a" > _stateR.txt
    echo "%%a" && "C:\AI\Whisper\whisper-faster.exe" "%%a" --language=Russian --model=large-v3 --output_dir="txt" --output_format=txt --beep_off
    del "%%a"
)

del "C:\AI\Whisper\_stateR.txt"