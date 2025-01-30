@echo off
:: Edit this batch file with your username and password
set username=
set password=
cd /d R:
:: The file path in this batch script has been edited to remove personal identifying information. The username, password, and absolute file path to the python script below must be correct in order for this cmd line script to function properly.
python "C:\Users\<REDACTED>\Desktop\Metric-Script.py" %username% %password%
pause