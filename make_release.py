
# Pythono3 code to rename multiple  
# files in a directory or folder 
  
# importing os module 
import os 
import compileall

compileall.compile_dir('.\\Perf_Package_Source\\', force=True)


  
# Function to rename multiple files 
def main(): 
    i = 0      
    for filename in os.listdir('.\\Perf_Package_Source\\__pycache__'): 
        only_file_name = filename.split('.')
        dest = '.\\Release\\Perf_Package\\' + only_file_name[0] + '.pyc'
        src = '.\\Perf_Package_Source\\__pycache__\\' + filename
        print("only_file_name = ", only_file_name[0])
        print("source = ", src, "dest = ", dest)
        os.rename(src, dest)
        # Driver Code 
if __name__ == '__main__': 
      
    # Calling main() function 
    main() 
