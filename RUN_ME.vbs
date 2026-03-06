' ============================================================
'  NetAudit Pro — Silent Launcher (No black CMD window)
'  Double-click this for a cleaner launch experience.
'  Works on Windows 7 / 8 / 10 / 11
' ============================================================

Set objShell = CreateObject("Shell.Application")
Set objFSO   = CreateObject("Scripting.FileSystemObject")

' Get the folder where this .vbs file lives
strFolder = objFSO.GetParentFolderName(WScript.ScriptFullName)

' Check if Python is available
Set objWsh = CreateObject("WScript.Shell")
strPython = ""

On Error Resume Next
objWsh.Run "py --version", 0, True
If Err.Number = 0 Then strPython = "py"
Err.Clear

If strPython = "" Then
    objWsh.Run "python --version", 0, True
    If Err.Number = 0 Then strPython = "python"
    Err.Clear
End If

If strPython = "" Then
    objWsh.Run "python3 --version", 0, True
    If Err.Number = 0 Then strPython = "python3"
    Err.Clear
End If
On Error GoTo 0

If strPython = "" Then
    MsgBox "Python not found!" & vbCrLf & vbCrLf & _
           "Please install Python from https://python.org" & vbCrLf & _
           "Make sure to check 'Add Python to PATH' during install.", _
           vbCritical, "NetAudit Pro"
    WScript.Quit
End If

' Re-launch with admin rights via UAC prompt
strCmd = strPython & " """ & strFolder & "\launch.py"""
objShell.ShellExecute strPython, """" & strFolder & "\launch.py""", strFolder, "runas", 1

WScript.Quit
