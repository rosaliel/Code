import os
import  my_path

def _check_dir(path):
    """creates the directory if doesn't exists"""
    if not os.path.isdir(path):
        os.mkdir(path)

def _check_path(path):
    """checks and creates all needed directories and files"""
    _check_dir(path + '/job')
    _check_dir(path + '/out')
    _check_dir(path + '/err')
    _check_dir(path + '/pdb')
    if not os.path.isfile(path + '/command'):
        open(path + '/command', 'a').close()
        os.chmod(path + '/command', 0774)
        
def create_job(name, path='', queue='new-all.q', rusage='1024', args=list()):
    """creates a job file and add command to the command file"""
    if path == '':
        path = os.getcwd()
    job_path = '{}/job/job.{}'.format(path, name)
    command_path = path + '/command'
    out_path = '{}/out/out.{}'.format(path, name)
    err_path = '{}/err/err.{}'.format(path, name)
    _check_path(path)
    
    job = list()
    job.append('#!/bin/bash')
    job.append('. /usr/share/lsf/conf/profile.lsf')
    job.append('cd ' + path)
    last_line = '/apps/RH6U4/blcr/0.8.5/bin/cr_run ' + my_path.ROSETTA
    if args: 
        vars = ''    
        for var in args:
            vars += var + ' '
        job.append('{} {}'.format(last_line, vars))
    else:
        job.append(last_line)    
    open(job_path, 'w').writelines([line + '\n' for line in job])
    os.chmod(job_path, 0774)
    
    
    command = 'bsub  -C 1024 -u /dev/null '
    command += '-R rusage[mem={}] '.format(rusage)
    command += '-L /bin/bash -G fleishman-wx-grp-lsf '
    command += '-q {} '.format(queue) 
    command += '-o {} '.format(out_path)
    command += '-e {} '.format(err_path)
    command += '/apps/RH6U4/blcr/0.8.5/bin/cr_run ' + job_path
    open(command_path, 'a').write(command + '\n')

    
    
    
    
    
    
