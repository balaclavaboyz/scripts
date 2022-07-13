import subprocess
import os
import re
local_files=[]
list_files_to_compress=[]

for path in os.listdir('./'):
    if os.path.isfile(os.path.join('./',path)):
        local_files.append(path)
for i in range(len(local_files)):
    if re.search(r'.tar$',local_files[i]):
        list_files_to_compress.append(local_files[i])

list_commands=[]
for i in list_files_to_compress:
    list_commands.append(f"gzip -9 -v './{i}'")

if __name__=='__main__':
    procs=[subprocess.Popen(i) for i in list_commands]
    for p in procs:
        p.wait()
        print('spawned process\n')