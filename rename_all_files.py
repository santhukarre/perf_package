
# Pythono3 code to rename multiple  
# files in a directory or folder 
  
# importing os module 
import os 
  
# Function to rename multiple files 
def main(): 
    i = 0      
    for filename in os.listdir('.\\Release\\Perf_Package\\'): 
        only_file_name = filename.split('.')
        dest = '.\\Release\\Perf_Package\\' + only_file_name[0] + '.pyc'
        src = '.\\Release\\Perf_Package\\' + filename
        print("only_file_name = ", only_file_name[0])
        os.rename(src, dest)
        # Driver Code 
if __name__ == '__main__': 
      
    # Calling main() function 
    main() 
