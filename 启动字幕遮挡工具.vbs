Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\mutia\Desktop\subtitle_masker"
WshShell.Run """C:\Users\mutia\Desktop\subtitle_masker\.venv\Scripts\pythonw.exe"" ""C:\Users\mutia\Desktop\subtitle_masker\main.py""", 0, False
