#!/usr/bin/env python3
# This script was built for the DEFCON Class
# Use the JCL below to provision staging dataset
# Then upload LGBT400, LOC400, WTO400 to IT.
# The JCL generated expects to use rdrprep to generate EBCDIC
# JCL for upload and it expects `hello.load` to be in the subfolder
# `users`. See README.MD for how to compile.
# Once you've compiled and prelinked hello.c run this script
# convert the output jcl to ebcdic jcl with rdrprep and submit
# then one at a time to the EBCDIC reader on port 3506:
# for i in *.jcl; do echo $i;rdrprep $i;cat reader.jcl|ncat --send-only -w1 172.17.0.3 3506; read; done

## JCL to build staging PDS for overflows.
# //MAKEPDS JOB (JOB),'JOB',CLASS=A,MSGCLASS=H,MSGLEVEL=(1,1),            
# //          NOTIFY=&SYSUID                                              
# //STEP01   EXEC PGM=IEFBR14                                             
# //OVERFLOW DD  DSN=DEFCON.OVERFLOW,DISP=(NEW,CATLG),                     
# //             UNIT=SYSDA,VOL=SER=PUB000,                               
# //             SPACE=(TRK,(3,3,3),RLSE),                                
# //             DCB=(DSORG=PO,RECFM=FB,LRECL=400,BLKSIZE=400)


from pathlib import Path


# This job does all the magic
USERJOB = ('''//{usern} JOB (1),'ADD {usern}',CLASS=S,MSGLEVEL=(1,1),
//             MSGCLASS=A,USER=IBMUSER,PASSWORD=SYS1,NOTIFY=IBMUSER
// EXEC TSONUSER,ID={usern},
//      PW='{usern}',
//      PR='IKJACCNT',
//      OP='NOOPER',
//      AC='NOACCT',
//      JC='JCL',
//      MT='NOMOUNT'
//STEP01   EXEC PGM=IEFBR14   
//OVERFLOW DD  DSN={usern}.OVERFLOW,DISP=(NEW,CATLG),    
//             UNIT=SYSDA,VOL=SER=PUB000,                          
//             SPACE=(TRK,(3,3,3),RLSE),                              
//             DCB=DEFCON.OVERFLOW     
//OVERFLOW DD  DSN={usern}.OVERFLOW.ARBAUTH,DISP=(NEW,CATLG),    
//             UNIT=SYSDA,VOL=SER=PUB000,                          
//             SPACE=(TRK,(3,3,3),RLSE),                              
//             DCB=DEFCON.OVERFLOW.ARBAUTH      
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
//* COPY ALL MEMBERS FROM ONE PDS TO ANOTHER
//COPYTHEM EXEC PGM=IEBCOPY
//SYSPRINT DD SYSOUT=*
//* SYSUT1 is source SYSUT2 is destination
//SYSUT1 DD DSN=DEFCON.OVERFLOW,DISP=SHR
//SYSUT2 DD DSN={usern}.OVERFLOW,DISP=SHR
//SYSIN DD DUMMY
//* 
//* COPY ALL MEMBERS FROM ONE PDS TO ANOTHER
//*
//COPYOVRF EXEC PGM=IEBCOPY
//SYSPRINT DD SYSOUT=*
//* SYSUT1 is source SYSUT2 is destination
//SYSUT1 DD DSN=DEFCON.OVERFLOW,DISP=SHR
//SYSUT2 DD DSN={usern}.OVERFLOW,DISP=SHR
//SYSIN DD DUMMY
//*
//* 
//* COPY ALL MEMBERS FROM ONE PDS TO ANOTHER
//*
//COPYOVRF EXEC PGM=IEBCOPY
//SYSPRINT DD SYSOUT=*
//* SYSUT1 is source SYSUT2 is destination
//SYSUT1 DD DSN=DEFCON.OVERFLOW.ARBAUTH,DISP=SHR
//SYSUT2 DD DSN={usern}.OVERFLOW.ARBAUTH,DISP=SHR
//SYSIN DD DUMMY
//*
//COPYSRC  EXEC PGM=IEBCOPY
//SYSPRINT DD SYSOUT=*
//* SYSUT1 is source SYSUT2 is destination
//SYSUT1 DD DSN=DEFCON.SOURCE,DISP=SHR
//SYSUT2 DD DSN={usern}.SOURCE,DISP=SHR
//SYSIN DD DUMMY
//* 
//LINK    EXEC PGM=IEWL,PARM='MAP,LIST,XREF,NORENT',REGION=1024K
//SYSPRINT  DD SYSOUT=A
//SYSLMOD   DD DISP=SHR,DSN={usern}.LOAD(HELLO)
//SYSUT1    DD UNIT=SYSDA,SPACE=(CYL,(5,1))
//SYSLIN    DD DATA,DLM=$$
::E GETSPLOIT/hello.load
$$
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
./ ADD NAME=FIXHAPPY,LIST=ALL
//FIXHAPPY  JOB (TSO),
//             'RUN FIXDSCB HAPPY',
//             CLASS=A,
//             MSGCLASS=A,
//             MSGLEVEL=(1,1),
//             REGION=0K
//FIXDSCB    EXEC PGM=FIXDSCB
//SYSPRINT DD   SYSOUT=A
//STEPLIB  DD   DISP=SHR,DSN=SYSC.LINKLIB
//SYSIN    DD   *
EXTEND  VOLUME=MVSRES,DSNAME=SYS1.LINKLIB
//*
''')

for x in range(0,30):
    with open("users/DC{}.jcl".format(str(x).zfill(2)), 'w') as jclfile:
        print("*** Writting users/DC{}.jcl".format(str(x).zfill(2)))
        jclfile.write(USERJOB.format(usern="DC{}".format(str(x).zfill(2))))

