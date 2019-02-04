import subprocess
from sys import argv

workdir = argv[1]

scriptdir = workdir + '/scripts/'

scriptarray = ['runmaps_processes.py',
               'runmenus_processes.py',
               'runcorrmaps_processes.py',
               'runcorrelations_processes.py',
               'runpathways_processes.py',
               'runparallel_processes.py',
               'rungenes_processes.py',
               'runpathparallel_processes.py',
               'runpathgenes_processes.py',
               'navigome_create_genelist_toupdate.py',
               'runprofiles_processes.py'
               ]

for i in scriptarray:
    print('Running ' + i + '...')
    cmd = ['python', scriptdir + i, workdir]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    (output, err) = process.communicate()
    p_status = process.wait()
