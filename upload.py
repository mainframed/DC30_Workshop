#!/usr/bin/env python3

## requires git clone https://github.com/jake-mainframe/ARBAUTH

# This will create DEFCON.* datasets
# Replaced the LOGON clist with motd.txt
# Adds users DC01 through DC30 to RAKF

import sys
import math

# Takes in a CLIST and splits the text on each line

if len(sys.argv) < 2:
    print("Missing argument\n Usage: {} motd.txt".format(sys.argv[0]))
    sys.exit()

MOTDJCL = '''//UPLOAD JOB (JOB),'MOTD',
//         CLASS=A,MSGLEVEL=(1,1),MSGCLASS=A,
//         NOTIFY=IBMUSER,USER=IBMUSER,PASSWORD=SYS1
//*
//* This JCL was generated with upload.py use that dont edit this
//*
//MOTDPROC EXEC PGM=IEBUPDTE,PARM=NEW
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

upload_file = '''//*
//* Adding DEFCON.OVERFLOW({member})
//*
//CRTEOVRF EXEC PGM=IEBGENER
//SYSUT2   DD   DSN=DEFCON.OVERFLOW({member}),DISP=SHR
//SYSPRINT DD   SYSOUT=*
//SYSIN    DD   DUMMY
//SYSUT1   DD   DATA,DLM='{dlm}'
::E {filename}
{dlm}
'''

replace_ispf_clist = '''//*
//* Replace the ISPF clist to get rid of annoying "FREE" messages
//*
//ISPFPROC EXEC PGM=IEBUPDTE,PARM=NEW
//SYSPRINT DD  SYSOUT=*
//SYSUT2   DD  DSN=SYS1.CMDPROC,DISP=SHR
//SYSIN    DD  DATA,DLM='><'
./ ADD NAME=ISPF
PROC  0                                                             
/*     ALLOCATE REQUIRED ISPF DD NAMES     */                       
ALLOC F(ISPCLIB) DA('SYSGEN.ISPF.CLIB','SYSGEN.REVIEW.CLIST') SHR   
ALLOC F(ISPLLIB) DA('SYSGEN.ISPF.LLIB','SYSGEN.REVIEW.LOAD') SHR    
ALLOC F(ISPMLIB) DA('SYSGEN.ISPF.MLIB') SHR                         
ALLOC F(ISPPLIB) DA('SYSGEN.ISPF.PLIB','SYSGEN.ISPF.RFEPLIB') SHR   
ALLOC F(ISPSLIB) DA('SYSGEN.ISPF.SLIB') SHR                         
ALLOC F(ISPTABL) DA('SYSGEN.ISPF.TLIB') SHR                         
ALLOC F(ISPTLIB) DA('SYSGEN.ISPF.TLIB') SHR                         
/* CREATE USERID.ISP.PROF IF IT DOES NOT EXIST  */                  
IF &SYSDSN('&SYSUID..ISP.PROF') NE &STR(OK) THEN DO                 
    /* CREATE THE DCB INFO */                                       
    ATTRIB PROFS BLKSIZE(3120) LRECL(80) DSORG(PO) RECFM(F,B)       
    /* ALLOCATE THE DATASET */                                      
    ALLOC DSNAME('&SYSUID..ISP.PROF') CYLINDERS SPACE(1,0) DIR(10) +
    VOLUME(PUB001) UNIT(3390) USING(PROFS) NEW                      
    /* FREE THE DCB INFO */                                         
    FREE ATTRLIST(PROFS)                                            
END                                                                 
/* ALLOCATE USER PROFILES */                                        
ALLOC F(ISPPROF) DA('&SYSUID..ISP.PROF') SHR                        
ALLOC F(REVPROF) DA('&SYSUID..ISP.PROF') SHR                        
/* LAUNCH ISPF */                                                   
CALL 'SYSGEN.ISPF.LLIB(ISPF)'                                       
FREE  F(ISPCLIB,ISPLLIB,ISPMLIB,ISPPLIB,ISPSLIB,ISPTABL,ISPTLIB)    
FREE  F(ISPPROF,REVPROF)  
><
//*
//* Replace COMMND00 with custom
//*
//NEWCOMND EXEC PGM=IEBUPDTE,PARM=NEW
//SYSUT2   DD  DSN=SYS1.PARMLIB,DISP=OLD
//SYSPRINT DD  SYSOUT=*
//SYSIN    DD  *
./ ADD NAME=COMMND00,LIST=ALL
./ NUMBER NEW1=10,INCR=10
COM='SEND 'AUTO COMMANDS IN COMMND00 BEING PROCESSED',CN=01'
COM='START JES2,,,PARM='WARM,NOREQ''                        
COM='START SETPFKEY,M=00'                                   
COM='START FTPDDC30'                                          
COM='START NET'                                             
./ ENDUP                                     
'''

sources = '''//*
//* Adds sources to DEFCON.source
//*
//SOURCES   EXEC PGM=IEBUPDTE,REGION=1024K,PARM=NEW
//SYSPRINT  DD SYSOUT=*
//SYSUT2    DD DSN=DEFCON.SOURCE,DISP=SHR
//SYSIN     DD DATA,DLM=$$
{sources}
$$
'''

def upload_rdrprep_file(filename,member=False,dlm="><"):
    '''Uses rdrprep to upload a Binary file'''
    if not member:
        member = filename.split(".")[0].upper()
        if "/" in member:
            member = member.split("/")[-1]
    upload_file_jcl =  upload_file.format(filename=filename,member=member,dlm=dlm)
    return upload_file_jcl

# Creates JCL to upload OVERFLOW files
jcl = ''

print("*** Generating MOTD")
motd = ''
with open(sys.argv[1],'r') as motd_text_file:
    for line in motd_text_file:
        l = len(line.rstrip())
        if l >= 80:
            # the line is too long, truncating
            l = 79
            line = line.rstrip()[:l]
        first_half = line.rstrip()[:math.floor(l/2)]
        second_half = line.rstrip()[math.floor(l/2):]
        motd += "WRITE {first}-\n{second}\n".format(first=first_half,second=second_half)

jcl = MOTDJCL.format(MOTD=motd)

create_pds = '''//*
//* Create PDS to hold overflows
//*
//CREATEOF EXEC PGM=IEFBR14
//OVERFLOW DD  DSN=DEFCON.OVERFLOW,DISP=(NEW,CATLG),
//             UNIT=SYSDA,VOL=SER=PUB000,
//             SPACE=(TRK,(3,3,3),RLSE),
//             DCB=(DSORG=PS,RECFM=FB,LRECL=30000,BLKSIZE=30000)
//SOURCE   DD  DSN=DEFCON.SOURCE,DISP=(NEW,CATLG),
//             UNIT=SYSDA,VOL=SER=PUB000,
//             SPACE=(TRK,(3,3,3),RLSE),DCB=SYS1.MACLIB
'''


# These dont work cause cards are max 80 cars, use FTP instead:
# for i in overflows/*; do lftp -e "cd DEFCON.OVERFLOW; put $i; bye" -u ibmuser,sys1 localhost:2121; done
# create_pds += upload_rdrprep_file("overflows/LGBT400")
# create_pds += upload_rdrprep_file("overflows/LOC400")
# create_pds += upload_rdrprep_file("overflows/WTO400")
# create_pds += upload_rdrprep_file("ARBAUTH/PATTERN")

print("*** Creating DEFCON.OVERFLOW and DEFCON.SOURCE")


jcl += create_pds

print("*** Adding Source files ")

with open("GETSPLOIT/hello.c", "r") as infile:
    hellosrc = "./ ADD NAME=HELLO,LIST=ALL\n{}".format( infile.read() )

with open("ARBAUTH/arbauth.jcl", "r") as infile:
    arbauthsrc = "./ ADD NAME=ARBAUTH,LIST=ALL\n{}".format( infile.read() )

jcl += sources.format(sources=hellosrc+arbauthsrc)


add_rakf_profiles = '''//*
//* ADD RAKF PROFILES
//*
//ADDRAKFU EXEC PGM=SORT,REGION=512K,PARM='MSG=AP'
//STEPLIB  DD   DSN=SYSC.LINKLIB,DISP=SHR
//SYSOUT   DD   SYSOUT=A
//SYSPRINT DD   SYSOUT=A
//SORTLIB  DD   DSNAME=SYSC.SORTLIB,DISP=SHR
//SORTOUT  DD   DSN=SYS1.SECURE.CNTL(USERS),DISP=SHR
//SORTWK01 DD   UNIT=2314,SPACE=(CYL,(5,5)),VOL=SER=SORTW1
//SORTWK02 DD   UNIT=2314,SPACE=(CYL,(5,5)),VOL=SER=SORTW2
//SORTWK03 DD   UNIT=2314,SPACE=(CYL,(5,5)),VOL=SER=SORTW3
//SORTWK04 DD   UNIT=2314,SPACE=(CYL,(5,5)),VOL=SER=SORTW5
//SORTWK05 DD   UNIT=2314,SPACE=(CYL,(5,5)),VOL=SER=SORTW6
//SYSIN  DD     *
 SORT FIELDS=(1,80,CH,A)
 RECORD TYPE=F,LENGTH=(80)
 END
/*
//SORTIN DD DSN=SYS1.SECURE.CNTL(USERS),DISP=SHR
//       DD DATA,DLM=@@
{users}
@@
//*
//* Update the RAKF database
//*
//RAKFUPDT EXEC RAKFUSER
'''

print("*** Adding DC00 - DC30 RAKF users ")

rakf_users = ''
for x in range(0,30):
    rakf_users += ("{usern}     USER     {usern}     N\n".format(usern="DC{}".format(str(x).zfill(2))))
jcl += add_rakf_profiles.format(users=rakf_users[:-1])

jcl += replace_ispf_clist


print("*** Adding ARBAUTH/arbauth.jcl ")
with open("ARBAUTH/arbauth.jcl", "r") as infile:
    #ebcdic_jcl_to_upload += to_ebcdic(''.join(infile.readlines()[8:]))
    jcl += (''.join(infile.readlines()[8:]))


print("*** Writting jcl/upload.jcl")
with open("jcl/upload.jcl", "w") as outfile:
    outfile.write(jcl)

