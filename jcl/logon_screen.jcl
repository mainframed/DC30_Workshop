//AWESOME  JOB  (SETUP),
//             'Build Netsol',
//             CLASS=A,
//             MSGCLASS=A,
//             MSGLEVEL=(1,1),USER=IBMUSER,PASSWORD=SYS1
//********************************************************************
//*
//* Desc: Build new NETSOL logon screen: DC30
//* Date: 04-08-2022
//* Built using Soldier of FORTRANs ANSi to EBCDiC builder
//*
//* Original ANSi File:   vtam_screen.ans
//* Original ANSi Artist: Anonymous
//* Original ANSi Date:   20220804
//*
//* Command Line Args: --sysgen vtam_screen.ans --ROW 23 --COL 19 
//*                    --member DC30 --file jcl/logon_screen.jcl 
//*                    --extended 
//*
//* After submitting run the following to refresh VTAM in hercules
//* console:
//*
//*     /P TSO
//*     /Z NET,QUICK
//*
//* Then the commands to bring the services back is:
//*
//*     /S NET
//*
//********************************************************************
//*
//* First delete the previous version if it exists
//*
//CLEANUP EXEC PGM=IDCAMS
//SYSPRINT DD  SYSOUT=*
//SYSIN    DD  *
 DELETE SYS1.UMODMAC(DC30)
 SET MAXCC=0
 SET LASTCC=0
//*
//* Then we "compress" SYS1.UMODMAC to free up space
//*
//COMP    EXEC COMPRESS,LIB='SYS1.UMODMAC'
//*
//* THEN WE COPY THE ORIGINAL NETSOL SOURCE FROM SYS1.AMACLIB
//* TO SYS1.UMODMAC
//*
//UMODMAC  EXEC PGM=IEBGENER
//SYSIN    DD DUMMY
//SYSPRINT DD SYSOUT=*
//SYSUT1   DD DISP=SHR,DSN=SYS1.AMACLIB(NETSOL)
//SYSUT2   DD DISP=SHR,DSN=SYS1.UMODMAC(NETSOL)
//*
//* THEN WE UPDATE SYS1.UMODMAC(NETSOL) TO DISPLAY OUR CUSTOM 3270
//*
//UPDATE   EXEC PGM=IEBUPDTE
//SYSPRINT DD SYSOUT=*
//SYSUT1   DD DISP=SHR,DSN=SYS1.UMODMAC
//SYSUT2   DD DISP=SHR,DSN=SYS1.UMODMAC
//SYSIN    DD DATA,DLM=$$
./ ADD NAME=DC30
* NETSOL screen created by ANSi2EBCDiC.py
         PUSH  PRINT
         PRINT OFF
EGMSG    DS 0C EGMSG
         $WCC  (RESETKBD,MDT)
         $SBA  (1,1)
* (1,1) Normal Display (FG) White 
         DC    X'2800002842F7'
         $SBA  (1,1)
* (1,1) Bold/Intense (FG) Red 
         DC    X'2842F2'
         DC    C'$'
         $SBA  (1,2)
* (1,2) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    11C'$'
         $SBA  (1,13)
* (1,13) Bold/Intense 
         DC    X'2842F2'
         DC    C'$'
         $SBA  (1,14)
* (1,14) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    12C'$'
         $SBA  (1,26)
* (1,26) Bold/Intense 
         DC    X'2842F2'
         DC    C'$'
         $SBA  (1,27)
* (1,27) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    9C'$'
         $SBA  (1,36)
* (1,36) Bold/Intense 
         DC    X'2842F2'
         DC    C'$'
         $SBA  (1,37)
* (1,37) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    31C'$'
         $SBA  (1,68)
* (1,68) Bold/Intense 
         DC    X'2842F2'
         DC    C'$'
         $SBA  (1,69)
* (1,69) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    13C'$'
         DC    X'7D'
         $SBA  (2,3)
* (2,3) (FG) White 
         DC    X'2842FE'
         DC    49C' '
         $SBA  (2,52)
* (2,52) (FG) Red 
         DC    X'2842F2'
         DC    X'79'
         DC    C'$$'
         $SBA  (2,55)
* (2,55) Bold/Intense 
         DC    X'2842F2'
         DC    C'$'
         $SBA  (2,56)
* (2,56) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    6C'$'
         $SBA  (2,62)
* (2,62) Bold/Intense 
         DC    X'2842F2'
         DC    C'$'
         $SBA  (2,63)
* (2,63) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    11C'$'
         $SBA  (2,74)
* (2,74) Bold/Intense 
         DC    X'2842F2'
         DC    C'$'
         $SBA  (2,75)
* (2,75) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    7C'$'
         $SBA  (3,2)
* (3,2) Bold/Intense (FG) White 
         DC    X'2842F7'
         DC    C'  '
         DC    15C'$'
         $SBA  (3,19)
* (3,19) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C' '
         $SBA  (3,20)
* (3,20) Bold/Intense 
         DC    X'2842F7'
         DC    15C'$'
         $SBA  (3,35)
* (3,35) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C' '
         $SBA  (3,36)
* (3,36) Bold/Intense 
         DC    X'2842F7'
         DC    15C'$'
         $SBA  (3,51)
* (3,51) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C'  '
         $SBA  (3,53)
* (3,53) (FG) Red 
         DC    X'2842F2'
         DC    C'$$$'
         $SBA  (3,56)
* (3,56) (FG) Green 
         DC    X'2842F4'
         DC    22C' '
         $SBA  (3,78)
* (3,78) (FG) Red 
         DC    X'2842F2'
         DC    C'$$$$'
         $SBA  (4,2)
* (4,2) Bold/Intense (FG) White 
         DC    X'2842F7'
         DC    C'  '
         DC    12X'EA'
         DC    C'$$$'
         $SBA  (4,19)
* (4,19) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C' '
         $SBA  (4,20)
* (4,20) Bold/Intense 
         DC    X'2842F7'
         DC    X'EA'
         DC    C'$$$$'
         DC    10X'EA'
         $SBA  (4,35)
* (4,35) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C' '
         $SBA  (4,36)
* (4,36) Bold/Intense 
         DC    X'2842F7'
         DC    X'EAEAEA'
         DC    C'$$$$'
         DC    8X'EA'
         DC    C'  '
         $SBA  (4,53)
* (4,53) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    C'$$$'
         $SBA  (4,56)
* (4,56) (FG) White 
         DC    X'2842FE'
         DC    C' '
         $SBA  (4,57)
* (4,57) Bold/Intense (FG) Light Turquoise 
         DC    X'2842FD'
         DC    C'Welcome to the DC30'
         $SBA  (4,76)
* (4,76) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C'  '
         $SBA  (4,78)
* (4,78) (FG) Red 
         DC    X'2842F2'
         DC    C'$$$'
         $SBA  (5,1)
* (5,1) Bold/Intense 
         DC    X'2842F2'
         DC    C'$'
         $SBA  (5,2)
* (5,2) (FG) White 
         DC    X'2842F7'
         DC    C'  $$$$'
         DC    7C' '
         DC    C'.$$$'
         $SBA  (5,19)
* (5,19) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C' '
         $SBA  (5,20)
* (5,20) Bold/Intense 
         DC    X'2842F7'
         DC    15C'$'
         $SBA  (5,35)
* (5,35) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C' '
         $SBA  (5,36)
* (5,36) Bold/Intense 
         DC    X'2842F7'
         DC    15C'$'
         $SBA  (5,51)
* (5,51) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C'  '
         $SBA  (5,53)
* (5,53) (FG) Red 
         DC    X'2842F2'
         DC    C'$$$'
         $SBA  (5,56)
* (5,56) (FG) White 
         DC    X'2842FE'
         DC    C' '
         $SBA  (5,57)
* (5,57) Bold/Intense (FG) Light Turquoise 
         DC    X'2842FD'
         DC    C'Mainframe Buffer'
         DC    5C' '
         $SBA  (5,78)
* (5,78) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    C'$$$$'
         $SBA  (6,2)
* (6,2) Bold/Intense (FG) White 
         DC    X'2842F7'
         DC    C'  $$$$'
         $SBA  (6,8)
* (6,8) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    5C' '
         $SBA  (6,13)
* (6,13) Bold/Intense 
         DC    X'2842F7'
         DC    C'.$$$$'
         DC    X'7D'
         $SBA  (6,19)
* (6,19) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C' '
         $SBA  (6,20)
* (6,20) Bold/Intense 
         DC    X'2842F7'
         DC    X'EA'
         DC    C'$$$'
         DC    X'50'
         DC    10X'EA'
         $SBA  (6,35)
* (6,35) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C' '
         $SBA  (6,36)
* (6,36) Bold/Intense 
         DC    X'2842F7'
         DC    X'EAEAEA'
         DC    C'Y$$$'
         DC    8X'EA'
         $SBA  (6,51)
* (6,51) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C'  '
         $SBA  (6,53)
* (6,53) (FG) Red 
         DC    X'2842F2'
         DC    C'$$$'
         $SBA  (6,56)
* (6,56) (FG) White 
         DC    X'2842FE'
         DC    C' '
         $SBA  (6,57)
* (6,57) Bold/Intense (FG) Light Turquoise 
         DC    X'2842FD'
         DC    C'Overflow Workshop!'
         $SBA  (6,75)
* (6,75) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C'   '
         $SBA  (6,78)
* (6,78) (FG) Red 
         DC    X'2842F2'
         DC    C'$$$$'
         $SBA  (7,2)
* (7,2) Bold/Intense (FG) White 
         DC    X'2842F7'
         DC    C'  '
         DC    11C'$'
         DC    C'Y'
         DC    X'7D'
         $SBA  (7,17)
* (7,17) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C'  '
         $SBA  (7,19)
* (7,19) (FG) Red 
         DC    X'2842F2'
         DC    C'.'
         $SBA  (7,20)
* (7,20) (FG) White 
         DC    X'2842FE'
         DC    C' '
         $SBA  (7,21)
* (7,21) Bold/Intense 
         DC    X'2842F7'
         DC    14C'$'
         $SBA  (7,35)
* (7,35) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C' '
         $SBA  (7,36)
* (7,36) Bold/Intense 
         DC    X'2842F7'
         DC    7C'$'
         $SBA  (7,43)
* (7,43) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    9C' '
         $SBA  (7,52)
* (7,52) (FG) Red 
         DC    X'2842F2'
         DC    C'.$$$'
         $SBA  (7,56)
* (7,56) (FG) White 
         DC    X'2842FE'
         DC    22C' '
         $SBA  (7,78)
* (7,78) Bold/Intense (FG) Red 
         DC    X'2842F2'
         DC    C'$'
         $SBA  (7,79)
* (7,79) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    C'$$$'
         $SBA  (8,2)
* (8,2) Bold/Intense (FG) White 
         DC    X'2842F7'
         DC    C'  '
         DC    9C'$'
         DC    C'Y'
         DC    X'7D'
         $SBA  (8,15)
* (8,15) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C'  '
         $SBA  (8,17)
* (8,17) (FG) Red 
         DC    X'2842F2'
         DC    C's'
         $SBA  (8,18)
* (8,18) Bold/Intense 
         DC    X'2842F2'
         DC    C'S'
         $SBA  (8,19)
* (8,19) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    C'S'
         $SBA  (8,20)
* (8,20) Bold/Intense (FG) White 
         DC    X'2842F7'
         DC    C' '
         DC    X'79'
         DC    C'Y'
         DC    12C'$'
         $SBA  (8,35)
* (8,35) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C' '
         $SBA  (8,36)
* (8,36) Bold/Intense 
         DC    X'2842F7'
         DC    5C'$'
         DC    C'Y'
         DC    X'7D'
         $SBA  (8,43)
* (8,43) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C'  '
         $SBA  (8,45)
* (8,45) (FG) Red 
         DC    X'2842F2'
         DC    C'.S'
         DC    9C'$'
         $SBA  (8,56)
* (8,56) Bold/Intense 
         DC    X'2842F2'
         DC    C'$'
         $SBA  (8,57)
* (8,57) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    17C'$'
         $SBA  (8,74)
* (8,74) Bold/Intense 
         DC    X'2842F2'
         DC    C'$'
         $SBA  (8,75)
* (8,75) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    7C'$'
         DC    C','
         $SBA  (9,3)
* (9,3) (FG) White 
         DC    X'2842FE'
         DC    12C' '
         $SBA  (9,15)
* (9,15) (FG) Red 
         DC    X'2842F2'
         DC    C's$$$$'
         $SBA  (9,20)
* (9,20) Bold/Intense 
         DC    X'2842F2'
         DC    C'$'
         $SBA  (9,21)
* (9,21) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    C's'
         $SBA  (9,22)
* (9,22) (FG) White 
         DC    X'2842FE'
         DC    21C' '
         $SBA  (9,43)
* (9,43) (FG) Red 
         DC    X'2842F2'
         DC    C'sS'
         DC    18C'$'
         DC    X'EAEAEA'
         $SBA  (9,66)
* (9,66) Bold/Intense 
         DC    X'2842F2'
         DC    X'EA'
         $SBA  (9,67)
* (9,67) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    X'EAEAEAEA'
         DC    23C'$'
         $SBA  (10,14)
* (10,14) Bold/Intense 
         DC    X'2842F2'
         DC    C'$'
         $SBA  (10,15)
* (10,15) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    11C'$'
         DC    C'Ss'
         $SBA  (10,28)
* (10,28) (FG) White 
         DC    X'2842FE'
         DC    C'   '
         $SBA  (10,31)
* (10,31) Bold/Intense 
         DC    X'2842F7'
         DC    C'nnnn'
         $SBA  (10,35)
* (10,35) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    30C' '
         $SBA  (10,65)
* (10,65) Bold/Intense 
         DC    X'2842F7'
         DC    C'nnnn'
         $SBA  (10,69)
* (10,69) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    10C' '
         $SBA  (10,79)
* (10,79) (FG) Red 
         DC    X'2842F2'
         DC    X'79'
         DC    7C'$'
         $SBA  (11,7)
* (11,7) Bold/Intense 
         DC    X'2842F2'
         DC    C'$'
         $SBA  (11,8)
* (11,8) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    20C'$'
         $SBA  (11,28)
* (11,28) (FG) White 
         DC    X'2842FE'
         DC    C'  '
         $SBA  (11,30)
* (11,30) Bold/Intense 
         DC    X'2842F7'
         DC    15C'$'
         $SBA  (11,45)
* (11,45) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C' '
         $SBA  (11,46)
* (11,46) Bold/Intense 
         DC    X'2842F7'
         DC    16C'$'
         $SBA  (11,62)
* (11,62) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C' '
         $SBA  (11,63)
* (11,63) Bold/Intense 
         DC    X'2842F7'
         DC    13C'$'
         DC    C'Ss'
         $SBA  (11,78)
* (11,78) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C'  '
         $SBA  (11,80)
* (11,80) (FG) Red 
         DC    X'2842F2'
         DC    C'$$$$'
         $SBA  (12,4)
* (12,4) Bold/Intense 
         DC    X'2842F2'
         DC    C'$'
         $SBA  (12,5)
* (12,5) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    17C'$'
         $SBA  (12,22)
* (12,22) Bold/Intense 
         DC    X'2842F2'
         DC    C'$'
         $SBA  (12,23)
* (12,23) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    5C'$'
         $SBA  (12,28)
* (12,28) Bold/Intense (FG) White 
         DC    X'2842F7'
         DC    C'  '
         DC    X'EA'
         DC    C'$$$$'
         DC    6X'EA'
         DC    C'$$$$'
         $SBA  (12,45)
* (12,45) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C' '
         $SBA  (12,46)
* (12,46) Bold/Intense 
         DC    X'2842F7'
         DC    C'$$$$'
         DC    8X'EA'
         DC    C'$$$$'
         $SBA  (12,62)
* (12,62) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C' '
         $SBA  (12,63)
* (12,63) Bold/Intense 
         DC    X'2842F7'
         DC    X'EAEA'
         DC    C'$$$$'
         DC    X'EAEAEAEA79'
         DC    C'$$$$'
         $SBA  (12,78)
* (12,78) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C'  '
         $SBA  (12,80)
* (12,80) (FG) Red 
         DC    X'2842F2'
         DC    10C'$'
         $SBA  (13,10)
* (13,10) Bold/Intense 
         DC    X'2842F2'
         DC    C'$'
         $SBA  (13,11)
* (13,11) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    6C'$'
         $SBA  (13,17)
* (13,17) Bold/Intense 
         DC    X'2842F2'
         DC    C'$'
         $SBA  (13,18)
* (13,18) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    10C'$'
         DC    C's'
         $SBA  (13,29)
* (13,29) (FG) White 
         DC    X'2842FE'
         DC    C'  '
         $SBA  (13,31)
* (13,31) Bold/Intense 
         DC    X'2842F7'
         DC    C'$$$$'
         $SBA  (13,35)
* (13,35) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    6C' '
         $SBA  (13,41)
* (13,41) Bold/Intense 
         DC    X'2842F7'
         DC    X'EAEAEAEA'
         $SBA  (13,45)
* (13,45) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C' '
         $SBA  (13,46)
* (13,46) Bold/Intense 
         DC    X'2842F7'
         DC    C'$$$$'
         $SBA  (13,50)
* (13,50) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    8C' '
         $SBA  (13,58)
* (13,58) Bold/Intense 
         DC    X'2842F7'
         DC    C'$$$$'
         $SBA  (13,62)
* (13,62) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C'   '
         $SBA  (13,65)
* (13,65) Bold/Intense 
         DC    X'2842F7'
         DC    C'$$$$'
         $SBA  (13,69)
* (13,69) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    5C' '
         $SBA  (13,74)
* (13,74) Bold/Intense 
         DC    X'2842F7'
         DC    C'$$$$'
         $SBA  (13,78)
* (13,78) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C'  '
         $SBA  (13,80)
* (13,80) Bold/Intense (FG) Red 
         DC    X'2842F2'
         DC    C'$'
         $SBA  (14,1)
* (14,1) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    28C'$'
         $SBA  (14,29)
* (14,29) (FG) White 
         DC    X'2842FE'
         DC    C'  '
         $SBA  (14,31)
* (14,31) Bold/Intense 
         DC    X'2842F7'
         DC    C'$$$$'
         DC    11C' '
         DC    C'$$$$'
         $SBA  (14,50)
* (14,50) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    8C' '
         $SBA  (14,58)
* (14,58) Bold/Intense 
         DC    X'2842F7'
         DC    C'$$$$'
         $SBA  (14,62)
* (14,62) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C'  '
         $SBA  (14,64)
* (14,64) Bold/Intense 
         DC    X'2842F7'
         DC    C'.$$$I'
         $SBA  (14,69)
* (14,69) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C'  '
         $SBA  (14,71)
* (14,71) (FG) Red 
         DC    X'2842F2'
         DC    C'.'
         $SBA  (14,72)
* (14,72) (FG) White 
         DC    X'2842FE'
         DC    C'  '
         $SBA  (14,74)
* (14,74) Bold/Intense 
         DC    X'2842F7'
         DC    C'$$$$'
         $SBA  (14,78)
* (14,78) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C'  '
         $SBA  (14,80)
* (14,80) (FG) Red 
         DC    X'2842F2'
         DC    14C'$'
         $SBA  (15,14)
* (15,14) Bold/Intense 
         DC    X'2842F2'
         DC    C'$'
         $SBA  (15,15)
* (15,15) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    6C'$'
         $SBA  (15,21)
* (15,21) Bold/Intense 
         DC    X'2842F2'
         DC    C'$'
         $SBA  (15,22)
* (15,22) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    7C'$'
         $SBA  (15,29)
* (15,29) (FG) White 
         DC    X'2842FE'
         DC    C'  '
         $SBA  (15,31)
* (15,31) Bold/Intense 
         DC    X'2842F7'
         DC    14C'$'
         $SBA  (15,45)
* (15,45) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C' '
         $SBA  (15,46)
* (15,46) Bold/Intense 
         DC    X'2842F7'
         DC    16C'$'
         $SBA  (15,62)
* (15,62) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C' '
         $SBA  (15,63)
* (15,63) Bold/Intense 
         DC    X'2842F7'
         DC    C'S$$$Y'
         DC    X'7D'
         $SBA  (15,69)
* (15,69) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C' '
         $SBA  (15,70)
* (15,70) (FG) Red 
         DC    X'2842F2'
         DC    C'sS'
         $SBA  (15,72)
* (15,72) (FG) White 
         DC    X'2842FE'
         DC    C'  '
         $SBA  (15,74)
* (15,74) Bold/Intense 
         DC    X'2842F7'
         DC    C'$$$$'
         $SBA  (15,78)
* (15,78) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C'  '
         $SBA  (15,80)
* (15,80) (FG) Red 
         DC    X'2842F2'
         DC    8C'$'
         $SBA  (16,8)
* (16,8) Bold/Intense 
         DC    X'2842F2'
         DC    C'$'
         $SBA  (16,9)
* (16,9) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    20C'$'
         $SBA  (16,29)
* (16,29) (FG) White 
         DC    X'2842FE'
         DC    C'  '
         $SBA  (16,31)
* (16,31) Bold/Intense 
         DC    X'2842F7'
         DC    X'79'
         DC    C'Y'
         DC    12C'$'
         DC    C' '
         DC    X'79'
         DC    C'Y'
         DC    12C'$'
         DC    C'Y'
         DC    X'7D'
         $SBA  (16,62)
* (16,62) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C' '
         $SBA  (16,63)
* (16,63) Bold/Intense 
         DC    X'2842F7'
         DC    C'$$$Y'
         DC    X'7D'
         $SBA  (16,68)
* (16,68) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C' '
         $SBA  (16,69)
* (16,69) Bold/Intense (FG) Red 
         DC    X'2842F2'
         DC    C's'
         $SBA  (16,70)
* (16,70) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    C'S'
         $SBA  (16,71)
* (16,71) Bold/Intense 
         DC    X'2842F2'
         DC    C'$'
         $SBA  (16,72)
* (16,72) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    C's'
         $SBA  (16,73)
* (16,73) (FG) White 
         DC    X'2842FE'
         DC    C' '
         $SBA  (16,74)
* (16,74) Bold/Intense 
         DC    X'2842F7'
         DC    C'$$$$'
         $SBA  (16,78)
* (16,78) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C'  '
         $SBA  (16,80)
* (16,80) (FG) Red 
         DC    X'2842F2'
         DC    C'$$'
         $SBA  (17,2)
* (17,2) Bold/Intense 
         DC    X'2842F2'
         DC    C'$'
         $SBA  (17,3)
* (17,3) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    C'$$$SoF'
         DC    15C'$'
         $SBA  (17,24)
* (17,24) Bold/Intense 
         DC    X'2842F2'
         DC    C'$'
         $SBA  (17,25)
* (17,25) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    C'$$$$'
         $SBA  (17,29)
* (17,29) Bold/Intense 
         DC    X'2842F2'
         DC    C'S'
         $SBA  (17,30)
* (17,30) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    C's'
         $SBA  (17,31)
* (17,31) (FG) White 
         DC    X'2842FE'
         DC    36C' '
         $SBA  (17,67)
* (17,67) (FG) Red 
         DC    X'2842F2'
         DC    C'sS$$$Ss'
         $SBA  (17,74)
* (17,74) (FG) White 
         DC    X'2842FE'
         DC    5C' '
         $SBA  (17,79)
* (17,79) (FG) Red 
         DC    X'2842F2'
         DC    C'.'
         DC    7C'$'
         $SBA  (18,7)
* (18,7) Bold/Intense 
         DC    X'2842F2'
         DC    C'$'
         $SBA  (18,8)
* (18,8) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    14C'$'
         $SBA  (18,22)
* (18,22) Bold/Intense 
         DC    X'2842F2'
         DC    C'$'
         $SBA  (18,23)
* (18,23) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    10C'$'
         $SBA  (18,33)
* (18,33) Bold/Intense 
         DC    X'2842F2'
         DC    C'$'
         $SBA  (18,34)
* (18,34) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    6C'$'
         $SBA  (18,40)
* (18,40) Bold/Intense 
         DC    X'2842F2'
         DC    C'$'
         $SBA  (18,41)
* (18,41) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    8C'$'
         $SBA  (18,49)
* (18,49) Bold/Intense 
         DC    X'2842F2'
         DC    C'$'
         $SBA  (18,50)
* (18,50) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    9C'$'
         $SBA  (18,59)
* (18,59) Bold/Intense 
         DC    X'2842F2'
         DC    C'$'
         $SBA  (18,60)
* (18,60) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    13C'$'
         $SBA  (18,73)
* (18,73) Bold/Intense 
         DC    X'2842F2'
         DC    C'$'
         $SBA  (18,74)
* (18,74) Normal Display (FG) White (FG) Red 
         DC    X'2800002842F72842F2'
         DC    7C'$'
         $SBA  (19,1)
* (19,1) (FG) White 
         DC    X'2842FE'
         DC    23C' '
         $SBA  (20,24)
* (20,24) (FG) Turquoise 
         DC    X'2842F5'
         DC    C'H'
         $SBA  (20,25)
* (20,25) Bold/Intense (FG) Red 
         DC    X'2842F2'
         DC    C' '
         $SBA  (20,26)
* (20,26) Normal Display (FG) White (FG) Turquoise 
         DC    X'2800002842F72842F5'
         DC    C'A'
         $SBA  (20,27)
* (20,27) Bold/Intense (FG) Red 
         DC    X'2842F2'
         DC    C' '
         $SBA  (20,28)
* (20,28) Normal Display (FG) White (FG) Turquoise 
         DC    X'2800002842F72842F5'
         DC    C'C'
         $SBA  (20,29)
* (20,29) Bold/Intense (FG) Red 
         DC    X'2842F2'
         DC    C' '
         $SBA  (20,30)
* (20,30) Normal Display (FG) White (FG) Turquoise 
         DC    X'2800002842F72842F5'
         DC    C'K'
         $SBA  (20,31)
* (20,31) Bold/Intense (FG) Red 
         DC    X'2842F2'
         DC    C' 3 '
         $SBA  (20,34)
* (20,34) Normal Display (FG) White (FG) Turquoise 
         DC    X'2800002842F72842F5'
         DC    C'R'
         $SBA  (20,35)
* (20,35) Bold/Intense (FG) Red 
         DC    X'2842F2'
         DC    C'   '
         $SBA  (20,38)
* (20,38) Normal Display (FG) White (FG) Turquoise 
         DC    X'2800002842F72842F5'
         DC    C'H'
         $SBA  (20,39)
* (20,39) Bold/Intense (FG) Red 
         DC    X'2842F2'
         DC    C' 0 '
         $SBA  (20,42)
* (20,42) Normal Display (FG) White (FG) Turquoise 
         DC    X'2800002842F72842F5'
         DC    C'M'
         $SBA  (20,43)
* (20,43) Bold/Intense (FG) Red 
         DC    X'2842F2'
         DC    C' '
         $SBA  (20,44)
* (20,44) Normal Display (FG) White (FG) Turquoise 
         DC    X'2800002842F72842F5'
         DC    C'E'
         $SBA  (20,45)
* (20,45) Bold/Intense (FG) Red 
         DC    X'2842F2'
         DC    C' '
         $SBA  (20,46)
* (20,46) Normal Display (FG) White (FG) Turquoise 
         DC    X'2800002842F72842F5'
         DC    C'C'
         $SBA  (20,47)
* (20,47) Bold/Intense (FG) Red 
         DC    X'2842F2'
         DC    C' '
         $SBA  (20,48)
* (20,48) Normal Display (FG) White (FG) Turquoise 
         DC    X'2800002842F72842F5'
         DC    C'O'
         $SBA  (20,49)
* (20,49) Bold/Intense (FG) Red 
         DC    X'2842F2'
         DC    C' '
         $SBA  (20,50)
* (20,50) Normal Display (FG) White (FG) Turquoise 
         DC    X'2800002842F72842F5'
         DC    C'M I'
         $SBA  (20,53)
* (20,53) Bold/Intense (FG) Red 
         DC    X'2842F2'
         DC    C' '
         $SBA  (20,54)
* (20,54) Normal Display (FG) White (FG) Turquoise 
         DC    X'2800002842F72842F5'
         DC    C'N'
         $SBA  (20,55)
* (20,55) Bold/Intense (FG) Red 
         DC    X'2842F2'
         DC    C' '
         $SBA  (20,56)
* (20,56) Normal Display (FG) White (FG) Turquoise 
         DC    X'2800002842F72842F5'
         DC    C'G'
         $SBA  (20,57)
* (20,57) (FG) White 
         DC    X'2842FE'
         DC    C' '
         $SBA  (22,2)
* (22,2) Bold/Intense (FG) Light Green 
         DC    X'2842FC'
         DC    C'To login type: DC## where ## is 00 to 22'
         $SBA  (22,42)
* (22,42) Normal Display (FG) White 
         DC    X'2800002842F7'
         DC    C' '
         $SBA  (23,2)
* (23,2) Bold/Intense (FG) Red 
         DC    X'2842F2'
         DC    C'Login Here:'
         $SBA  (23,13)
* (23,13) (FG) Light Green 
         DC    X'2842FC'
         DC    C' '
         $SBA  (23,14)
* (23,14) (FG) Red 
         DC    X'2842F2'
         DC    C'==='
         DC    X'6E'
         $SBA  (23,18)
* (23,18) Normal Display (FG) White 
         DC    X'2800002842F7'
* Insert Cursor and unprotected field
         $SBA  (23,19)
         DC    X'2842F2'  SA COLOR RED
         $SF   (UNPROT,HI)
         $IC
         DC    CL20' '
         DC    X'280000'
         DC    X'1DF8'     SF (PROT,HIGH INTENSITY)
         $SBA  (24,80)
         $SF   (SKIP,HI)
EGMSGLN EQU *-EGMSG
         POP   PRINT
./ CHANGE NAME=NETSOL
         CLI   MSGINDEX,X'0C'                                           23164802
         BNE   EGSKIP                                                   23164804
         LA    R3,EGMSGLN                                               23164808
         L     R4,=A(EGMSG)                                             23164810
*                                                                       23164812
         WRITE RPL=(PTRRPL),                                           X23164814
               OPTCD=(LBT,ERASE),                                      X23164816
               AREA=(R4),                                              X23164818
               RECLEN=(R3),                                            X23164820
               EXIT=WRITEND                                             23164822
*                                                                       23164824
         B EGOK                                                         23164826
*                                                                       23164828
*                                                                       23164830
EGSKIP   DS 0H EGSKIP                                                   23164832
EGOK     DS 0H EGOK                                                     23166010
         COPY DC30                        , logon screen copy book      66810010
$$
//*
//* With that done its time to assemble our new screen
//* We assemble SYS1.UMODMAC(NETSOL) with IFOX00
//*
//ASM     EXEC PGM=IFOX00,REGION=1024K
//SYSLIB   DD  DISP=SHR,DSN=SYS1.UMODMAC,DCB=LRECL=32720
//         DD  DISP=SHR,DSN=SYS2.MACLIB
//         DD  DISP=SHR,DSN=SYS1.MACLIB
//         DD  DISP=SHR,DSN=SYS1.AMODGEN
//SYSUT1   DD  UNIT=VIO,SPACE=(1700,(600,100))
//SYSUT2   DD  UNIT=VIO,SPACE=(1700,(300,50))
//SYSUT3   DD  UNIT=VIO,SPACE=(1700,(300,50))
//SYSPRINT DD  SYSOUT=*,DCB=BLKSIZE=1089
//SYSPUNCH DD  DISP=(NEW,PASS,DELETE),
//             UNIT=VIO,SPACE=(TRK,(2,2)),
//             DCB=(BLKSIZE=80,LRECL=80,RECFM=F)
//SYSIN    DD  *
ISTNSC00 CSECT ,
         NETSOL SYSTEM=VS2
         END   ,
//*
//* Then we link it and put it in SYS1.VTAMLIB(ISTNSC00)
//*
//LKED    EXEC PGM=IEWL,PARM='XREF,LIST,LET,NCAL',REGION=1024K
//SYSPRINT DD  SYSOUT=*
//SYSLIN   DD  DISP=(OLD,DELETE,DELETE),DSN=*.ASM.SYSPUNCH
//SYSLMOD  DD  DISP=SHR,DSN=SYS1.VTAMLIB(ISTNSC00)
//SYSUT1   DD  UNIT=VIO,SPACE=(1024,(200,20))
//*
//