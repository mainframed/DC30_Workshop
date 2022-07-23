#!/usr/bin/env python3

# This script is for building releases for MVP (MVS/CE Package manager)
# It works by creating an XMI file which contains:
# - Task file(s), JCL files that will be submitted in numbered order and follow
#   a specific naming convention (#nnnJCL where nnn is 001 through 999) Note: the
#   jobname MUST match the filename.
# - XMI file(s) that makes up the release
# MVS/CE is required to use this script
# Author: Soldier of FORTRAN
# License: GPLv3

import os, sys, time, math, ebcdic
from telnetlib import theNULL
import subprocess
import threading
import queue
import socket
from pathlib import Path
import argparse
from datetime import datetime

jobcard = '''//DC30INST JOB (TSO),
//             'DC30 MVSCE',
//             CLASS=A,
//             MSGCLASS=A,
//             MSGLEVEL=(1,1),
//             USER=IBMUSER,PASSWORD=SYS1
//*
//* Install SYS2.MACLIBS
//*
//MVPINST EXEC MVP,INSTALL='MACLIB -D' 
'''

binary_upload = '''//COPY     EXEC PGM=IEBGENER
//SYSUT2   DD   DSN=MVP.STAGING({}),DISP=SHR
//SYSPRINT DD   SYSOUT=*
//SYSIN    DD   DUMMY
//SYSUT1   DD   DATA,DLM='{dlm}'
'''

MOTD = '''//*
//* Replace MOTD used for logons
//*
//MOTD EXEC PGM=IEBUPDTE,PARM=NEW
//SYSPRINT DD  SYSOUT=*
//SYSUT2   DD  DSN=SYS1.CMDPROC,DISP=SHR
//SYSIN    DD  DATA,DLM='><'
./ ADD NAME=STDLOGON
        PROC 0
CONTROL NOMSG,NOLIST,NOSYMLIST,NOCONLIST,NOFLUSH
CLS
{MOTD}
REVINIT
><
'''

create_pds = '''//*
//* Create PDS to hold overflows
//*
//CREATEOF EXEC PGM=IEFBR14                                             
//OVERFLOW DD  DSN=DEFCON.OVERFLOW,DISP=(NEW,CATLG),                     
//             UNIT=SYSDA,VOL=SER=PUB000,                               
//             SPACE=(TRK,(3,3,3),RLSE),                                
//             DCB=(DSORG=PS,RECFM=FB,LRECL=30000,BLKSIZE=30000)
'''

upload_binary = '''//*
//* Adding DEFCON.OVERFLOW({member})
//*
//COPY     EXEC PGM=IEBGENER
//SYSUT2   DD   DSN=DEFCON.OVERFLOW({member}),DISP=SHR
//SYSPRINT DD   SYSOUT=*
//SYSIN    DD   DUMMY
//SYSUT1   DD   DATA,DLM='{dlm}'
'''

upload_file = '''//*
//* Adding DEFCON.OVERFLOW({member})
//*
//COPY     EXEC PGM=IEBGENER
//SYSUT2   DD   DSN=DEFCON.OVERFLOW({member}),DISP=SHR
//SYSPRINT DD   SYSOUT=*
//SYSIN    DD   DUMMY
//SYSUT1   DD   DATA,DLM='{dlm}'
::E {filename}
{dlm}
'''

add_users = '''// EXEC TSONUSER,ID={usern},
//      PW='{usern}',
//      PR='IKJACCNT',
//      OP='NOOPER',
//      AC='NOACCT',
//      JC='JCL',
//      MT='NOMOUNT'
//*
//* Create {usern} datasets
//*
//STEP01   EXEC PGM=IEFBR14   
//OVERFLOW DD  DSN={usern}.OVERFLOW,DISP=(NEW,CATLG),    
//             UNIT=SYSDA,VOL=SER=PUB000,                          
//             SPACE=(TRK,(3,3,3),RLSE),                              
//             DCB=(DSORG=PO,RECFM=FB,LRECL=30000,BLKSIZE=30000)       
//DUMP001  DD  DSN={usern}.DUMP001,DISP=(NEW,CATLG),    
//             UNIT=SYSDA,VOL=SER=PUB000,                          
//             SPACE=(TRK,(10,5),RLSE),                              
//             DCB=(DSORG=PS,RECFM=FB,LRECL=121,BLKSIZE=400)       
//DUMP002  DD  DSN={usern}.DUMP002,DISP=(NEW,CATLG),    
//             UNIT=SYSDA,VOL=SER=PUB000,                          
//             SPACE=(TRK,(10,5),RLSE),                              
//             DCB=(DSORG=PS,RECFM=FB,LRECL=121,BLKSIZE=400)
//CNTL     DD  DSN={usern}.JCLLIB,DISP=(NEW,CATLG),
//             UNIT=SYSDA,VOL=SER=PUB000,
//             SPACE=(CYL,(1,1,20)),DCB=SYS1.MACLIB
//*
//* COPY ALL MEMBERS FROM ONE PDS TO ANOTHER
//*
//COPYTHEM EXEC PGM=IEBCOPY
//SYSPRINT DD SYSOUT=*
//* SYSUT1 is source SYSUT2 is destination
//SYSUT1 DD DSN=DEFCON.OVERFLOW,DISP=SHR
//SYSUT2 DD DSN={usern}.OVERFLOW,DISP=SHR
//SYSIN DD DUMMY
//*
//* Adds Labs to Users JCLLIB
//*
//STORE   EXEC PGM=IEBUPDTE,REGION=1024K,PARM=NEW
//SYSPRINT  DD SYSOUT=*
//SYSUT2    DD DSN={usern}.JCLLIB,DISP=SHR
//SYSIN     DD DATA,DLM=$$
./ ADD NAME=LAB01,LIST=ALL
//{usern}LAB1 JOB (TSO),
//             'Normal Run',
//             CLASS=A,
//             MSGCLASS=H,
//             MSGLEVEL=(1,1),NOTIFY=&SYSUID
//RUN    EXEC PGM=HELLO,REGION=0M
//SYSPRINT  DD SYSOUT=*
//STDOUT    DD SYSOUT=*
//STDIN     DD *
TESTRUN
//*
//STEPLIB   DD DISP=SHR,DSN={usern}.LOAD
./ ADD NAME=LAB02,LIST=ALL
//{usern}LAB2 JOB (TSO),
//             'Crash Run',
//             CLASS=A,
//             MSGCLASS=H,
//             MSGLEVEL=(1,1),NOTIFY=&SYSUID
//RUN    EXEC PGM=HELLO,REGION=0M
//SYSPRINT  DD SYSOUT=*
//STDOUT    DD SYSOUT=A
//STDIN     DD DISP=SHR,DSN={usern}.OVERFLOW(LGBT400)
//STEPLIB   DD DISP=SHR,DSN={usern}.LOAD
//SYSUDUMP  DD DISP=SHR,DSN={usern}.DUMP001
./ ADD NAME=LAB03,LIST=ALL
//{usern}LAB3 JOB (TSO),
//             'LOCATE Run',
//             CLASS=A,
//             MSGCLASS=H,
//             MSGLEVEL=(1,1),NOTIFY=&SYSUID
//RUN    EXEC PGM=HELLO,REGION=0M
//SYSPRINT  DD SYSOUT=*
//STDOUT    DD SYSOUT=A
//STDIN     DD DISP=SHR,DSN={usern}.OVERFLOW(LOC400)
//STEPLIB   DD DISP=SHR,DSN={usern}.LOAD
//SYSUDUMP  DD DISP=SHR,DSN={usern}.DUMP002
./ ADD NAME=LAB04,LIST=ALL
//{usern}LAB4  JOB (TSO),'EXPLOIT Run',CLASS=A,MSGCLASS=H,
//             MSGLEVEL=(1,1),NOTIFY=&SYSUID
//RUN    EXEC PGM=HELLO,REGION=0M
//SYSPRINT  DD SYSOUT=*
//STDOUT    DD SYSOUT=*
//STDIN     DD DISP=SHR,DSN={usern}.OVERFLOW(WTO400)
//STEPLIB   DD DISP=SHR,DSN={usern}.LOAD
//SYSUDUMP  DD SYSOUT=*
$$
//* 
//* Link Hello.c to {usern}.LOAD(HELLO)
//*
//LINK    EXEC PGM=IEWL,PARM='MAP,LIST,XREF,NORENT',REGION=1024K
//SYSPRINT  DD SYSOUT=A
//SYSLMOD   DD DISP=SHR,DSN={usern}.LOAD(HELLO)
//SYSUT1    DD UNIT=SYSDA,SPACE=(CYL,(5,1))
//SYSLIN    DD DATA,DLM=$$
::E hello.c
$$
'''

add_rakf_profile = '''//*
//* ADD RAKF PROFILE
//*
//ADDRAKFP    EXEC PGM=SORT,REGION=512K,PARM='MSG=AP'
//STEPLIB DD   DSN=SYSC.LINKLIB,DISP=SHR
//SYSOUT  DD   SYSOUT=A
//SYSPRINT DD  SYSOUT=A
//SORTLIB DD   DSNAME=SYSC.SORTLIB,DISP=SHR
//SORTOUT DD   DSN=SYS1.SECURE.CNTL(USERS),DISP=SHR
//SORTWK01 DD  UNIT=2314,SPACE=(CYL,(5,5)),VOL=SER=SORTW1
//SORTWK02 DD  UNIT=2314,SPACE=(CYL,(5,5)),VOL=SER=SORTW2
//SORTWK03 DD  UNIT=2314,SPACE=(CYL,(5,5)),VOL=SER=SORTW3
//SORTWK04 DD  UNIT=2314,SPACE=(CYL,(5,5)),VOL=SER=SORTW5
//SORTWK05 DD  UNIT=2314,SPACE=(CYL,(5,5)),VOL=SER=SORTW6
//SYSIN  DD    *
 SORT FIELDS=(1,80,CH,A)
 RECORD TYPE=F,LENGTH=(80)
 END
/*
//SORTIN DD DSN=SYS1.SECURE.CNTL(USERS),DISP=SHR
//       DD DATA,DLM=@@
{users}
@@
'''

error_check = [
                'open error',
                'Creating crash dump',
                'DISASTROUS ERROR',
                'HHC01023W Waiting for port 3270 to become free for console connections',
                'disabled wait state 00020000 80000005'
              ]

quit_herc_event = threading.Event()
kill_hercules = threading.Event()
reset_herc_event = threading.Event()
STDERR_to_logs = threading.Event()
running_folder = os.getcwd()

class herc_automation:

    def __init__(self,
                config="conf/local.cnf",
                rc="conf/mvsce.rc"
                ):

        self.config = config
        self.rc = rc
        self.hercproc = False
        self.stderr_q = queue.Queue()
        self.stdout_q = queue.Queue()

    def kill(self):
        self.hercproc.kill()

    def start_threads(self):
        # start a pair of threads to read output from hercules
        self.stdout_thread = threading.Thread(target=self.queue_stdout, args=(self.hercproc.stdout,self.stdout_q))
        self.stderr_thread = threading.Thread(target=self.queue_stderr, args=(self.hercproc.stderr,self.stderr_q))
        self.check_hercules_thread = threading.Thread(target=self.check_hercules, args=[self.hercproc])
        # self.queue_printer_thread = threading.Thread(target=self.queue_printer, args=('prt00e.txt',printer_q))
        self.stdout_thread.daemon = True
        self.stderr_thread.daemon = True
        # self.queue_printer_thread.daemon = True
        self.check_hercules_thread.daemon = True
        self.stdout_thread.start()
        self.stderr_thread.start()
        self.check_hercules_thread.start()
        # self.queue_printer_thread.start()

    def queue_stdout(self, pipe, q):
        ''' queue the stdout in a non blocking way'''
        global reply_num
        while True:

            l = pipe.readline()
            if len(l.strip()) > 0:
                if len(l.strip()) > 3 and l[0:2] == '/*' and l[2:4].isnumeric():
                    reply_num = l[2:4]
                    print("Reply number set to {}".format(reply_num))
                if  "HHC90020W" not in l and "HHC00007I" not in l and "HHC00107I" not in l and "HHC00100I" not in l:
                    # ignore these messages, they're just noise
                    # HHC90020W 'hthread_setschedparam()' failed at loc=timer.c:193: rc=22: Invalid argument
                    # HHC00007I Previous message from function 'hthread_set_thread_prio' at hthreads.c(1170)
                    print("[HERCLOG] {}".format(l.strip()))
                    q.put(l)
                    for errors in error_check:
                        if errors in l:
                            print("Quiting! Irrecoverable Hercules error: {}".format(l.strip()))
                            kill_hercules.set()
            if reset_herc_event.is_set():
                break

    def queue_stderr(self, pipe, q):
        ''' queue the stderr in a non blocking way'''
        while True:
            l = pipe.readline()
            if len(l.strip()) > 0:
                if STDERR_to_logs.is_set():
                    print("[DIAG] {}".format(l.strip()))
                if 'MIPS' in l:
                    print("[DIAG] {}".format(l.strip()))
                q.put(l)

                for errors in error_check:
                    if errors in l:
                        print("Quiting! Irrecoverable Hercules error: {}".format(l.strip()))
                        kill_hercules.set()
            if reset_herc_event.is_set():
                break

    def check_hercules(self, hercproc):
        ''' check to make sure hercules is still running '''
        while hercproc.poll() is None:
            if quit_herc_event.is_set() or reset_herc_event.is_set():
                print("Quit Event enabled exiting hercproc monitoring")
                return
            if kill_hercules.is_set():
                hercproc.kill()
                break
            continue

        print("ERROR - Hercules Exited Unexpectedly")
        os._exit(1)

    def check_maxcc(self, jobname, steps_cc={}, printer_file='printers/prt00e.txt'):
      '''Checks job and steps results, raises error
          If the step is in steps_cc, check the step vs the cc in the dictionary
          otherwise checks if step is zero
      '''
      print("Checking {} job results".format(jobname))

      found_job = False
      failed_step = False

      logmsg = '[MAXCC] Jobname: {:<8} Procname: {:<8} Stepname: {:<8} Exit Code: {:<8}'

      with open(printer_file, 'r', errors='ignore') as f:
          for line in f.readlines():
              if 'IEF142I' in line and jobname in line:

                  found_job = True

                  x = line.strip().split()
                  y = x.index('IEF142I')
                  j = x[y:]

                  log = logmsg.format(j[1],'',j[2],j[10])
                  maxcc=j[10]
                  stepname = j[2]

                  if j[3] != "-":
                      log = logmsg.format(j[1],j[2],j[3],j[11])
                      stepname = j[3]
                      maxcc=j[11]

                  print(log)

                  if stepname in steps_cc:
                      expected_cc = steps_cc[stepname]
                  else:
                      expected_cc = '0000'

                  if maxcc != expected_cc:
                      error = "Step {} Condition Code does not match expected condition code: {} vs {} review prt00e.txt for errors".format(stepname,j[-1],expected_cc)
                      print(error)
                      failed_step = True

      if not found_job:
          raise ValueError("Job {} not found in printer output {}".format(jobname, printer_file))
      if failed_step:
          raise ValueError(error)


    def reset_hercules(self):
        print('Restarting hercules')
        self.quit_hercules(msg=False)

        # drain STDERR and STDOUT
        while True:
            try:
                line = self.stdout_q.get(False).strip()
            except queue.Empty:
                break

        while True:
            try:
                line = self.stderr_q.get(False).strip()
            except queue.Empty:
                break

        reset_herc_event.set()

        try:
            self.hercmd = subprocess.check_output(["which", "hercules"]).strip()
        except:
            raise Exception('hercules not found')

        print("Launching hercules")

        h = ["hercules", '--externalgui', '-f',self.config, '-r', self.rc]
        print(h)

        self.hercproc = subprocess.Popen(h,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True)
        reset_herc_event.clear()
        quit_herc_event.clear()
        self.start_threads()

        self.rc = self.hercproc.poll()
        if self.rc is not None:
            raise("Unable to start hercules")
        print("Hercules launched")
        #self.write_logs()
        print("Hercules Re-initialization Complete")


    def quit_hercules(self, msg=True):
        if msg:
            print("Shutting down hercules")
        if not self.hercproc or self.hercproc.poll() is not None:
            print("Hercules already shutdown")
            return
        quit_herc_event.set()
        self.send_herc('quit')
        self.wait_for_string('Hercules shutdown complete', stderr=True)
        if msg:
            print('Hercules has exited')

    def wait_for_string(self, string_to_waitfor, stderr=False, timeout=False):
        '''
           Reads stdout queue waiting for expected response, default is
           to check STDOUT queue, set stderr=True to check stderr queue instead
           default timeout is 30 minutes
        '''
        time_started = time.time()

        if not timeout:
            timeout = 1800

        if not timeout and self.timeout:
            timeout=self.timeout

        print("Waiting for string to appear in hercules log: {}".format(string_to_waitfor))

        while True:
            if time.time() > time_started + timeout:
                if self.substep:
                    exception = "Step: {} Substep: {} took too long".format(self.step, self.substep)
                    log = "Step: {} Substep: {} Timeout Exceeded {} seconds".format(self.step, self.substep, timeout)
                else:
                    exception = "Step: {} Timeout".format(self.step, self.substep)
                    log = "Step: {} Timeout Exceeded {} seconds".format(self.step, self.substep, timeout)
                print(log)
                raise Exception(exception)

            try:
                if stderr:
                    line = self.stderr_q.get(False).strip()
                else:
                    line = self.stdout_q.get(False).strip()

                while string_to_waitfor not in line:
                    if stderr:
                        line = self.stderr_q.get(False).strip()
                    else:
                        line = self.stdout_q.get(False).strip()
                    continue
                return

            except queue.Empty:
                continue

    def ipl(self, step_text='', clpa=False):
        print(step_text)
        self.reset_hercules()
        #self.wait_for_string("0:0151 CKD")
        self.wait_for_string("IKT005I TCAS IS INITIALIZED")

    def shutdown_mvs(self, cust=False):
        self.send_oper('$p jes2')
        if cust:
            self.wait_for_string('IEF404I JES2 - ENDED - ')
        else:
            self.wait_for_string('IEF196I IEF285I   VOL SER NOS= SPOOL0.')
        self.send_oper('z eod')
        self.wait_for_string('IEE334I HALT     EOD SUCCESSFUL')
        self.send_oper('quiesce')
        self.wait_for_string("disabled wait state")
        self.send_herc('stop')

    def send_herc(self, command=''):
        ''' Sends hercules commands '''
        print("Sending Hercules Command: {}".format(command))
        self.hercproc.stdin.write(command+"\n")
        self.hercproc.stdin.flush()

    def send_oper(self, command=''):
        ''' Sends operator/console commands (i.e. prepends /) '''
        self.send_herc("/{}".format(command))

    def send_reply(self, command=''):
        ''' Sends operator/console commands with automated number '''
        self.send_herc("/r {},{}".format(reply_num,command))

    def submit(self,jcl, host='127.0.0.1',port=3505, ebcdic=False):
        '''submits a job (in ASCII) to hercules listener'''

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to server and send data
            sock.connect((host, port))
            if ebcdic:
              sock.send(jcl)
            else:
              sock.send(jcl.encode())

        finally:
            sock.close()


def to_ebcdic(string='',codepage='cp1047'):
    '''
       takes a string and converts it to ebcdic for use in card reader
       lines longer tha 80 chars will be truncated
    '''
    temp = b''
    line = "{:80}"
    for l in string.splitlines():
        t = line.format(l)
        temp += t.encode('cp1047')
    return temp

def read_ascii(filename):
    '''takes a string filename/path returns the file as ebcdic'''
    with open(filename,"r") as infile:
        return to_ebcdic(infile.read())

def read_binary(filename):
    '''Reads a file and returns binary JCL'''
    with open(filename,"rb") as infile:
        return infile.read()

def upload_binary_file(filename,member=False,dlm="><"):
    '''Uses JCL to upload a Binary file'''
    if not member:
        member = filename.split(".")[0].upper()
    upload_file_jcl_ebcdic =  to_ebcdic(upload_binary.format(member=member,dlm=dlm))
    upload_file_jcl_ebcdic += read_binary(filename)
    upload_file_jcl_ebcdic += dlm.encode('cp1047')
    return upload_file_jcl_ebcdic

def upload_rdrprep_file(filename,member=False,dlm="><"):
    '''Uses JCL to upload a Binary file'''
    if not member:
        member = filename.split(".")[0].upper()
        if "/" in member:
            member = member.split("/")[-1]
    upload_file_jcl =  upload_file.format(filename=filename,member=member,dlm=dlm)
    return upload_file_jcl

def read_file(filename):
    with open(filename, "r") as infile:
        return infile.read()

################ Script begins here

# First we add the jobcard

ebcdic_jcl_to_upload = b''
jcl_to_upload = ''
print("* Adding jobcard")
ebcdic_jcl_to_upload=to_ebcdic(jobcard)
jcl_to_upload += jobcard

# Then we add the motd
print("* Adding motd")

motd = ''
with open("motd.txt",'r') as motd_text_file:
    for line in motd_text_file:
        l = len(line.rstrip())
        if l >= 80:
            # the line is too long, truncating
            l = 79
            line = line.rstrip()[:l]
        first_half = line.rstrip()[:math.floor(l/2)]
        second_half = line.rstrip()[math.floor(l/2):]
        motd += "WRITE {first}-\n{second}\n".format(first=first_half,second=second_half)

final_motd = MOTD.format(MOTD=motd)

ebcdic_jcl_to_upload+=to_ebcdic(final_motd)
jcl_to_upload += final_motd

# Next we add the VTAM/NETSOL DEFCON screen
# This file is generated in the DockerFile
# ANSi2EBCDiC/ansi2ebcdic.py --sysgen logon_screen.ans --ROW 20 --COL 20 --member DC30 --file logon_screen.jcl --extended

print("* Adding NETSOL")
ebcdic_jcl_to_upload += read_ascii("logon_screen.jcl")

with open("logon_screen.jcl", "r") as infile:
    #ebcdic_jcl_to_upload += to_ebcdic(''.join(infile.readlines()[8:]))
    jcl_to_upload += (''.join(infile.readlines()[5:-1]))

# Then the terminals

print("* Adding Terminals")
ebcdic_jcl_to_upload += read_ascii("terminal.jcl")
jcl_to_upload += read_file("terminal.jcl")

# Add the overflows

print("* Adding Overflows")
ebcdic_jcl_to_upload += to_ebcdic(create_pds)
jcl_to_upload += create_pds
ebcdic_jcl_to_upload += upload_binary_file("LGBT400")
ebcdic_jcl_to_upload += upload_binary_file("LOC400")
ebcdic_jcl_to_upload += upload_binary_file("WTO400")
ebcdic_jcl_to_upload += upload_binary_file("ARBAUTH/PATTERN")
jcl_to_upload += upload_rdrprep_file("LGBT400")
jcl_to_upload += upload_rdrprep_file("LOC400")
jcl_to_upload += upload_rdrprep_file("WTO400")
jcl_to_upload += upload_rdrprep_file("ARBAUTH/PATTERN")

if not Path("hello.load").is_file():
    print("hello.load missing. Compile it with JCC: ./jcc/jcc -I./jcc/include -o hello.c && ./jcc/prelink -s ./jcc/objs hello.load hello.obj")
    sys.exit()


with open("hello.c", "r") as infile:
    hellosrc = "./ ADD NAME=HELLO,LIST=ALL\n{}".format( infile.read() )

with open("ARBAUTH/arbauth.jcl", "r") as infile:
    arbauthsrc = "./ ADD NAME=ARBAUTH,LIST=ALL\n{}".format( infile.read() )

with open("hello.load", "rb") as h:
    helloload = h.read()

users = ''

for x in range(0,30):
    ebcdic_jcl_to_upload += to_ebcdic(add_users.format(usern="DC{}".format(str(x).zfill(2)), hello=helloload,sources=hellosrc+arbauthsrc))
    ebcdic_jcl_to_upload += helloload
    ebcdic_jcl_to_upload += to_ebcdic("$$")
    jcl_to_upload += add_users.format(usern="DC{}".format(str(x).zfill(2)), hello="::E hello.load",sources=hellosrc+arbauthsrc)
    users += "{usern}     USER     {usern}     N\n".format(usern="DC{}".format(str(x).zfill(2)))

ebcdic_jcl_to_upload += to_ebcdic(add_rakf_profile.format(users=users))
jcl_to_upload += add_rakf_profile.format(users=users.rstrip())

with open("ARBAUTH/arbauth.jcl", "r") as infile:
    #ebcdic_jcl_to_upload += to_ebcdic(''.join(infile.readlines()[8:]))
    jcl_to_upload += (''.join(infile.readlines()[8:-2]))

with open("output.ebcdic.jcl", "wb") as outfile:
    outfile.write(ebcdic_jcl_to_upload)
with open("output.jcl", "w") as outfile:
    outfile.write(jcl_to_upload)

print(jcl_to_upload)

sys.exit()

print("Changing to MVS/CE Folder {}".format(args.mvsce))
os.chdir(args.mvsce)
try:
    os.remove("punchcards/pch00d.txt")
except:
    print("punchcards/pch00d.txt Already deleted")
build = herc_automation()
try:
  build.ipl()
  build.send_oper("$s punch1")
  build.wait_for_string("$HASP000 OK")
  build.submit(temp,port=3506,ebcdic=True)
  build.wait_for_string("$HASP190 HEADER   SETUP -- PUNCH1")
  build.send_oper("$s punch1")
  build.wait_for_string("HASP250 HEADER   IS PURGED")
  build.check_maxcc("HEADER")
finally:
  build.quit_hercules()

with open("punchcards/pch00d.txt", 'rb') as punchfile:
  punchfile.seek(160)
  no_headers = punchfile.read()
  no_footers = no_headers[:-80]

os.chdir(running_folder)

with open(args.name, 'wb') as review_out:
  review_out.write(no_footers)


