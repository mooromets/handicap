import os
import sys
import time

start = time.time()

dir = "." #default directory - current

if len(sys.argv) == 2: # if directory specified 
	dir = sys.argv[1]

print "reading from directory: ", dir 

lines = []
header = ""

for root, dirs, files in os.walk(dir): # check current dir
	print "directory:", root
	for file in files: # check all files
		if file.endswith('.csv'): # if .csv file
			filename = os.path.join(root, file)
			print "found file: ", filename
			with open(filename) as f:
				header = f.readline() # read first line as table header
				old_length = len(lines)
				lines += f.read().splitlines() # read all other lines
				print "lines read: ", len(lines) - old_length

unique_list = list(set(lines)) # remove duplicates
print "lines removed as duplicates: ", len(lines) - len(unique_list)
print "lines in result: ", len(unique_list)
#print header[:30] 
#print '\n'.join(str(p)[:30]  for p in unique_list)

out_name = "out.txt"
print "writing to ouput file:", out_name
thefile = open(out_name,'w') # resulting file
thefile.write(header) # write table header
for item in unique_list: 
  print>>thefile, item # write list items

thefile.close()

end = time.time()
print "execution time:", end - start, "seconds"
