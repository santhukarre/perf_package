echo off
mkdir Screenshots
cd .\BenchMarkApps
call install.bat
cd ..
python .\Perf_Package\XindusAutomation.pyc 1 <emailid> root 3307 .\Screenshots