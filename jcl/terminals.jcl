//TERMINAL JOB (TSO),
//             'DC30 MVSCE',
//             CLASS=A,
//             MSGCLASS=A,
//             MSGLEVEL=(1,1),
//             USER=IBMUSER,PASSWORD=SYS1
//*
//* Add the extra terminals needed 
//*
//* MAKE SURE YOU ALSO INCREASE USERS IN SYS1.PAMRLIB(IKJTSO00)
//STORE   EXEC PGM=IEBUPDTE,REGION=1024K,PARM=NEW
//SYSPRINT  DD SYSOUT=*
//SYSUT2    DD DSN=SYS1.VTAMLST,DISP=SHR
//* The changes below are based on the KICKS 251 KookBooks
//* http://www.kicksfortso.com/same/KooKbooK/KooKbooK-251project.htm
//* 2. VTAM must know about the terminals.
//SYSIN     DD *
./ ADD NAME=DC30T,LIST=ALL
LCL400   LBUILD SUBAREA=2                                               
CUU400   LOCAL TERM=3277,CUADDR=400,ISTATUS=ACTIVE,                    +
               LOGTAB=LOGTAB01,LOGAPPL=NETSOL,                         +
               FEATUR2=(MODEL2,PFK)                                     
CUU401   LOCAL TERM=3277,CUADDR=401,ISTATUS=ACTIVE,                    +
               LOGTAB=LOGTAB01,LOGAPPL=NETSOL,                         +
               FEATUR2=(MODEL2,PFK)                                     
CUU402   LOCAL TERM=3277,CUADDR=402,ISTATUS=ACTIVE,                    +
               LOGTAB=LOGTAB01,LOGAPPL=NETSOL,                         +
               FEATUR2=(MODEL2,PFK)                                     
CUU403   LOCAL TERM=3277,CUADDR=403,ISTATUS=ACTIVE,                    +
               LOGTAB=LOGTAB01,LOGAPPL=NETSOL,                         +
               FEATUR2=(MODEL2,PFK)                                     
CUU404   LOCAL TERM=3277,CUADDR=404,ISTATUS=ACTIVE,                    +
               LOGTAB=LOGTAB01,LOGAPPL=NETSOL,                         +
               FEATUR2=(MODEL2,PFK)                                     
CUU405   LOCAL TERM=3277,CUADDR=405,ISTATUS=ACTIVE,                    +
               LOGTAB=LOGTAB01,LOGAPPL=NETSOL,                         +
               FEATUR2=(MODEL2,PFK)                                     
CUU406   LOCAL TERM=3277,CUADDR=406,ISTATUS=ACTIVE,                    +
               LOGTAB=LOGTAB01,LOGAPPL=NETSOL,                         +
               FEATUR2=(MODEL2,PFK)                                     
CUU407   LOCAL TERM=3277,CUADDR=407,ISTATUS=ACTIVE,                    +
               LOGTAB=LOGTAB01,LOGAPPL=NETSOL,                         +
               FEATUR2=(MODEL2,PFK)             
CUU408   LOCAL TERM=3277,CUADDR=408,ISTATUS=ACTIVE,                    +
               LOGTAB=LOGTAB01,LOGAPPL=NETSOL,                         +
               FEATUR2=(MODEL2,PFK)             
CUU409   LOCAL TERM=3277,CUADDR=409,ISTATUS=ACTIVE,                    +
               LOGTAB=LOGTAB01,LOGAPPL=NETSOL,                         +
               FEATUR2=(MODEL2,PFK)             
CUU40A   LOCAL TERM=3277,CUADDR=40A,ISTATUS=ACTIVE,                    +
               LOGTAB=LOGTAB01,LOGAPPL=NETSOL,                         +
               FEATUR2=(MODEL2,PFK)             
CUU40B   LOCAL TERM=3277,CUADDR=40B,ISTATUS=ACTIVE,                    +
               LOGTAB=LOGTAB01,LOGAPPL=NETSOL,                         +
               FEATUR2=(MODEL2,PFK)             
CUU40C   LOCAL TERM=3277,CUADDR=40C,ISTATUS=ACTIVE,                    +
               LOGTAB=LOGTAB01,LOGAPPL=NETSOL,                         +
               FEATUR2=(MODEL2,PFK)             
CUU40D   LOCAL TERM=3277,CUADDR=40D,ISTATUS=ACTIVE,                    +
               LOGTAB=LOGTAB01,LOGAPPL=NETSOL,                         +
               FEATUR2=(MODEL2,PFK)             
CUU40E   LOCAL TERM=3277,CUADDR=40E,ISTATUS=ACTIVE,                    +
               LOGTAB=LOGTAB01,LOGAPPL=NETSOL,                         +
               FEATUR2=(MODEL2,PFK)             
CUU40F   LOCAL TERM=3277,CUADDR=40F,ISTATUS=ACTIVE,                    +
               LOGTAB=LOGTAB01,LOGAPPL=NETSOL,                         +
               FEATUR2=(MODEL2,PFK)             
CUU410   LOCAL TERM=3277,CUADDR=410,ISTATUS=ACTIVE,                    +
               LOGTAB=LOGTAB01,LOGAPPL=NETSOL,                         +
               FEATUR2=(MODEL2,PFK)             
CUU411   LOCAL TERM=3277,CUADDR=411,ISTATUS=ACTIVE,                    +
               LOGTAB=LOGTAB01,LOGAPPL=NETSOL,                         +
               FEATUR2=(MODEL2,PFK)             
CUU412   LOCAL TERM=3277,CUADDR=412,ISTATUS=ACTIVE,                    +
               LOGTAB=LOGTAB01,LOGAPPL=NETSOL,                         +
               FEATUR2=(MODEL2,PFK)             
CUU413   LOCAL TERM=3277,CUADDR=413,ISTATUS=ACTIVE,                    +
               LOGTAB=LOGTAB01,LOGAPPL=NETSOL,                         +
               FEATUR2=(MODEL2,PFK)             
CUU414   LOCAL TERM=3277,CUADDR=414,ISTATUS=ACTIVE,                    +
               LOGTAB=LOGTAB01,LOGAPPL=NETSOL,                         +
               FEATUR2=(MODEL2,PFK)             
CUU415   LOCAL TERM=3277,CUADDR=415,ISTATUS=ACTIVE,                    +
               LOGTAB=LOGTAB01,LOGAPPL=NETSOL,                         +
               FEATUR2=(MODEL2,PFK)             
CUU416   LOCAL TERM=3277,CUADDR=416,ISTATUS=ACTIVE,                    +
               LOGTAB=LOGTAB01,LOGAPPL=NETSOL,                         +
               FEATUR2=(MODEL2,PFK)             
CUU417   LOCAL TERM=3277,CUADDR=417,ISTATUS=ACTIVE,                    +
               LOGTAB=LOGTAB01,LOGAPPL=NETSOL,                         +
               FEATUR2=(MODEL2,PFK)             
CUU418   LOCAL TERM=3277,CUADDR=418,ISTATUS=ACTIVE,                    +
               LOGTAB=LOGTAB01,LOGAPPL=NETSOL,                         +
               FEATUR2=(MODEL2,PFK)             
CUU419   LOCAL TERM=3277,CUADDR=419,ISTATUS=ACTIVE,                    +
               LOGTAB=LOGTAB01,LOGAPPL=NETSOL,                         +
               FEATUR2=(MODEL2,PFK)             
CUU41A   LOCAL TERM=3277,CUADDR=41A,ISTATUS=ACTIVE,                    +
               LOGTAB=LOGTAB01,LOGAPPL=NETSOL,                         +
               FEATUR2=(MODEL2,PFK)             
CUU41B   LOCAL TERM=3277,CUADDR=41B,ISTATUS=ACTIVE,                    +
               LOGTAB=LOGTAB01,LOGAPPL=NETSOL,                         +
               FEATUR2=(MODEL2,PFK)             
CUU41C   LOCAL TERM=3277,CUADDR=41C,ISTATUS=ACTIVE,                    +
               LOGTAB=LOGTAB01,LOGAPPL=NETSOL,                         +
               FEATUR2=(MODEL2,PFK)             
CUU41D   LOCAL TERM=3277,CUADDR=41D,ISTATUS=ACTIVE,                    +
               LOGTAB=LOGTAB01,LOGAPPL=NETSOL,                         +
               FEATUR2=(MODEL2,PFK)             
CUU41E   LOCAL TERM=3277,CUADDR=41E,ISTATUS=ACTIVE,                    +
               LOGTAB=LOGTAB01,LOGAPPL=NETSOL,                         +
               FEATUR2=(MODEL2,PFK)
./ ADD NAME=APPLTSO,LIST=ALL
TSO      APPL AUTH=(PASS,NVPACE,TSO),BUFFACT=5                          
TSO0001  APPL AUTH=(PASS,NVPACE,TSO),BUFFACT=5                          
TSO0002  APPL AUTH=(PASS,NVPACE,TSO),BUFFACT=5                          
TSO0003  APPL AUTH=(PASS,NVPACE,TSO),BUFFACT=5                          
TSO0004  APPL AUTH=(PASS,NVPACE,TSO),BUFFACT=5                          
TSO0005  APPL AUTH=(PASS,NVPACE,TSO),BUFFACT=5                          
TSO0006  APPL AUTH=(PASS,NVPACE,TSO),BUFFACT=5                          
TSO0007  APPL AUTH=(PASS,NVPACE,TSO),BUFFACT=5                          
TSO0008  APPL AUTH=(PASS,NVPACE,TSO),BUFFACT=5                          
TSO0009  APPL AUTH=(PASS,NVPACE,TSO),BUFFACT=5                          
TSO0010  APPL AUTH=(PASS,NVPACE,TSO),BUFFACT=5                          
TSO0011  APPL AUTH=(PASS,NVPACE,TSO),BUFFACT=5                          
TSO0012  APPL AUTH=(PASS,NVPACE,TSO),BUFFACT=5                          
TSO0013  APPL AUTH=(PASS,NVPACE,TSO),BUFFACT=5                          
TSO0014  APPL AUTH=(PASS,NVPACE,TSO),BUFFACT=5                          
TSO0015  APPL AUTH=(PASS,NVPACE,TSO),BUFFACT=5                          
TSO0016  APPL AUTH=(PASS,NVPACE,TSO),BUFFACT=5                          
TSO0017  APPL AUTH=(PASS,NVPACE,TSO),BUFFACT=5                          
TSO0018  APPL AUTH=(PASS,NVPACE,TSO),BUFFACT=5                          
TSO0019  APPL AUTH=(PASS,NVPACE,TSO),BUFFACT=5                          
TSO0020  APPL AUTH=(PASS,NVPACE,TSO),BUFFACT=5                          
TSO0021  APPL AUTH=(PASS,NVPACE,TSO),BUFFACT=5                          
TSO0022  APPL AUTH=(PASS,NVPACE,TSO),BUFFACT=5                          
TSO0023  APPL AUTH=(PASS,NVPACE,TSO),BUFFACT=5                          
TSO0024  APPL AUTH=(PASS,NVPACE,TSO),BUFFACT=5                          
TSO0025  APPL AUTH=(PASS,NVPACE,TSO),BUFFACT=5                          
TSO0026  APPL AUTH=(PASS,NVPACE,TSO),BUFFACT=5                          
TSO0027  APPL AUTH=(PASS,NVPACE,TSO),BUFFACT=5                          
TSO0028  APPL AUTH=(PASS,NVPACE,TSO),BUFFACT=5                          
TSO0029  APPL AUTH=(PASS,NVPACE,TSO),BUFFACT=5                          
TSO0030  APPL AUTH=(PASS,NVPACE,TSO),BUFFACT=5 
TSO0031  APPL AUTH=(PASS,NVPACE,TSO),BUFFACT=5
./ ADD NAME=ATCSTR00,LIST=ALL
CONFIG=00,                         /*CONFIG LIST SUFFIX              */+
SSCPID=01,                         /*THIS VTAMS ID IN NETWORK        */+
NETSOL=YES,                        /*NETWORK SOLICITOR OPTION        */+
MAXSUBA=31,                        /*MAXIMUM SUBAREAS IN NETWORK     */+
NOPROMPT,                          /*OPERATOR PROMPT OPTION          */+
SUPP=NOSUP,                        /*MESSAGE SUPPRESSION OPTION      */+
COLD,                              /*RESTART OPTION   - COLD/WARM    */+
APBUF=(192,,128),                  /*ACE STORAGE POOL                */+
CRPLBUF=(281,,181),                /*RPL COPY POOL                   */+
IOBUF=(128,512,104,F),             /*FIXED IO (GP-5/2009)            */+
LFBUF=(32,,32,F),                  /*LARGE FIXED BUFFER POOL         */+
LPBUF=(146,,146),                  /*LARGE PAGEBLE BUFFER POOL       */+
NPBUF=(134,,70,F),                 /*NON WS FMCB                     */+
PPBUF=(20,3992,10,F),              /*PAGEBLE IO (GP-5/2009)          */+
SFBUF=(140,,76,F),                 /*SMALL FIXED BUFFER POOL         */+
SPBUF=(032,,32,F),                 /*SMALL PGBL BUFFER POOL          */+
UECBUF=(128,,108,F),               /*USER EXIT CB                    */+
WPBUF=(64,,64,F)                   /*MESSAGE CONTROL BUFFER POOL     */
/*
//*
//* This step changes USERMAX to 32 in SYS1.PARMLIB(IKJTSO00)
//*
//ADDAPF   EXEC PGM=IKJEFT01,REGION=1024K,DYNAMNBR=50
//SYSPRINT DD  SYSOUT=*
//SYSTSPRT DD  SYSOUT=*
//SYSTERM  DD  SYSOUT=*
//SYSTSIN  DD  *
 EDIT 'SYS1.PARMLIB(IKJTSO00)' DATA
 LIST
 TOP
 CHANGE /USERMAX=8, /USERMAX=32,/
 LIST
 SAVE
 END
 EDIT 'SYS1.VTAMLST(ATCCON00)' DATA
 LIST
 CHANGE /LCL400/DC30T /
 LIST
 SAVE
 END
