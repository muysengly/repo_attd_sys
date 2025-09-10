Set oWS = WScript.CreateObject("WScript.Shell") 
sLinkFile = "C:\Users\muysengly\Desktop\Attendance System.lnk" 
Set oLink = oWS.CreateShortcut(sLinkFile) 
oLink.TargetPath = "C:\Users\muysengly\Desktop\repo_attendance_system\venv\Scripts\python.exe" 
oLink.Arguments = "C:\Users\muysengly\Desktop\repo_attendance_system\main.py"  
oLink.WorkingDirectory = "C:\Users\muysengly\Desktop\repo_attendance_system" 
oLink.WindowStyle = 1 
oLink.IconLocation = "C:\Users\muysengly\Desktop\repo_attendance_system\icon.ico" 
oLink.Description = "Attendance System Application" 
oLink.Save 
