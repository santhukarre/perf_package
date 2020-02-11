import subprocess
import io

def get_adb_device_id():
  p = subprocess.Popen("adb devices", stdout=subprocess.PIPE, shell=True)
  (output, err) = p.communicate()
  p_status = p.wait()
  print("Command output : ", output)
  str_output = str(output, 'utf-8')
  print("str_output :", str_output)
  buf = io.StringIO(str_output)
  print("adb devices first line: ", buf.readline())
  adb_devices_id = buf.readline()
  adb_list = adb_devices_id.split('\t')
  print("adb device id:", adb_list[0])
  adb_id = adb_list[0]
  return adb_id
