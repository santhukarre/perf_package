echo off

cd .\BenchMarkApps
echo "Installing Antutu 3D Bench"
adb shell "mkdir /sdcard/Android/obb/com.antutu.benchmark.full"
REM cd .\Antutu\Android\obb\com.antutu.benchmark.full
adb push .\Antutu\Android\obb\com.antutu.benchmark.full\main.8010000.com.antutu.benchmark.full.obb /sdcard/Android/obb/com.antutu.benchmark.full
adb install .\Antutu\antutu_3dbench.apk
echo "Installing Antutu"
adb install .\Antutu\antutu.apk

echo "Installing Androbench"
adb install androbench.apk

echo "Installing Gfxbench"
adb install gfxbench.apk

REM CALL :InstallLMBench

echo "Installing 3DMark"
adb install 3dmark.apk

echo "Installing Geekbench"
adb install Geekbench.apk

EXIT /B 0

echo "Pushing LMBench"
adb root 
adb disable-verity
adb remount
adb shell "mkdir /data/lmbench"
adb push "./lmbench/* /data/lmbench"
adb shell "mkdir /data/xindus"
adb push "./xindus_app /data/xindus"
cd ..