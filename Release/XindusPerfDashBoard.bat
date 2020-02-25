echo off
mkdir Screenshots
cd .\BenchMarkApps
call install.bat
cd ..
python .\Perf_Package\XindusAutomation.pyc 1 santhu.karre@gmail.com root 3307 .\Screenshots