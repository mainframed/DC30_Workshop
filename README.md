# DEF CON 30 Workshop Mainframe Container

![DEFCON MAINFRAME](/screenshot.png?raw=true "DEF CON 30")

The scripts here are used to build the MVS 3.8j virtual mainframe for the DEFCON 30 workshop. 

## Use docker

You can use docker instead of building from scratch: https://hub.docker.com/r/mainframed767/defcon30

To run the container use the below commands, make sure to change `$(pwd)/docker` to a folder for your system. 
The `$(pwd)` puts the docker volumes in your current working folder. 

### Minimal Container
Use this command if you just want to run it self contained. :warning: If you remove and relaunch the container
you will lose any and all changes you made to the mainframe environment.

```bash
docker run -d \
  --name=defcon30 \
  -p 21021:2121 \
  -p 8443:8443 \
  -p 8080:8080 \
  -p 2323:3223 \
  -p 31337-32337:31337-32337 \
  --restart unless-stopped \
  mainframed767/defcon30:prerelease
```

| Port         | Description                                                                       |
|--------------|-----------------------------------------------------------------------------------|
| 21021        | Vulnerable FTP Server Port                                                        |
| 8443         | Web based 3270 client which auto connects to lab mainframe                        |
| 8080         | The class Wiki                                                                    |
| 2323         | Encrypted TN3270 server if you want to use your own emulator like x3270 or PW3270 |
| 31337-32337  | FTP Server passive port range                                                     |

### Expert Container

This exposes more ports and allows you to have volumes with permanence. Gives access to the 
hercules and MVS consoles, the card readers/writers.

```bash
docker run -d \
  --name=defcon30 \
  -e HUSER=docker \
  -e HPASS=docker \
  -p 3221:3221 \
  -p 2323:3223 \
  -p 3270:3270 \
  -p 3505:3505 \
  -p 3506:3506 \
  -p 8888:8888 \
  -p 2121:2121 \
  -p 8443:8443 \
  -p 8080:8080 \
  -p 31337-32337:31337-32337 \
  -v $(pwd)/docker/config:/config \
  -v $(pwd)/docker/printers:/printers \
  -v $(pwd)/docker/punchcards:/punchcards \
  -v $(pwd)/docker/logs:/logs \
  -v $(pwd)/docker/dasd:/dasd \
  -v $(pwd)/docker/certs:/certs \
  --restart unless-stopped \
  mainframed767/defcon30:prerelease
```

**Ports**

| Port         | Description                                                                         |
|--------------|-------------------------------------------------------------------------------------|
| 2323         | TLS Encrypted TN3270 Server Port                                                    |
| 3270         | Unencrypted TN3270 Server Port                                                      |
| 3221         | Encrypted FTPD server                                                               |
| 2121         | Unencrypted FTP Server Port                                                         |
| 8443         | Web based 3270 client which auto connects to lab mainframe https://localhost:8443   |
| 8080         | The class Wiki https://localhost:8080                                               |
| 8888         | Hercules Web Server/MVS Console. User/pass = docker                                 |
| 3505         | Punch card reader. Converts ASCII to EBCDIC.                                        |
| 3506         | Punch card reader. Only accepts EBCDIC files.                                       |
| 31337-32337  | FTP Server passive port range                                                       |

**Volumes**

| Folder      | Description                                            |
|-------------|--------------------------------------------------------|
| /config     | Contains the Hercules and web3270 config files         |
| /printers   | Contains the output of the printers on `CLASS=A`       |
| /punchcards | Contains the output of the puncard writer on `CLASS=B` |
| /logs       | Contains Hercules logs                                 |
| /dasd       | Contains the MVS/CE disk images                        |
| /certs      | Contains the certificates used for TLS encryption      |

### Users

| Username | Password | Description                                  |
|----------|----------|----------------------------------------------|
| IBMUSER  | SYS1     | Adminstrative User with access to everything |
| MVSCE01  | CUL8TR   | Adminstrative User with access to everything |
| MVSCE02  | PASS4U   | Generic User                                 |
| DC0      | DC0      | DEFCON Workshop User                         |
| DC1      | DC1      | DEFCON Workshop User                         |
| DC2      | DC2      | DEFCON Workshop User                         |
| DC3      | DC3      | DEFCON Workshop User                         |
| DC4      | DC4      | DEFCON Workshop User                         |
| DC5      | DC5      | DEFCON Workshop User                         |
| DC6      | DC6      | DEFCON Workshop User                         |
| DC7      | DC7      | DEFCON Workshop User                         |
| DC8      | DC8      | DEFCON Workshop User                         |
| DC9      | DC9      | DEFCON Workshop User                         |
| DC10     | DC10     | DEFCON Workshop User                         |
| DC11     | DC11     | DEFCON Workshop User                         |
| DC12     | DC12     | DEFCON Workshop User                         |
| DC13     | DC13     | DEFCON Workshop User                         |
| DC14     | DC14     | DEFCON Workshop User                         |
| DC15     | DC15     | DEFCON Workshop User                         |
| DC16     | DC16     | DEFCON Workshop User                         |
| DC17     | DC17     | DEFCON Workshop User                         |
| DC18     | DC18     | DEFCON Workshop User                         |
| DC19     | DC19     | DEFCON Workshop User                         |
| DC20     | DC20     | DEFCON Workshop User                         |
| DC21     | DC21     | DEFCON Workshop User                         |
| DC22     | DC22     | DEFCON Workshop User                         |
| DC23     | DC23     | DEFCON Workshop User                         |

:warning: With the current setup the maximum number of concurrent users is 24. If a 25th user logs on you get 
the following error message `IKT00203I ADDRESS SPACE CREATION FAILED`.

## Building from scratch

- Download the most recent version of MVSCE from https://github.com/MVS-sysgen/sysgen/releases
- Copy the vulnerable FTPD server to MVP: `cp extra/FTPD.MVP MVSCE/MVP/packages`
- Launch MVSCE
- Submit the job `MACLFTPF.jcl`: `cat jcl/MACLFTPF.jcl|ncat --send-only -w1 127.0.0.1 3505`
- Submit the job `logon_screen.jcl`: `cat jcl/logon_screen.jcl|ncat --send-only -w1 127.0.0.1 3505`
- Submit the job `terminal.jcl`: `cat terminal.jcl|ncat --send-only -w1 127.0.0.1 3505`
- Clone the ARBAUTH repo: `git clone https://github.com/jake-mainframe/ARBAUTH`
- Run the python script `upload.py`: `./upload.py motd.txt`
- Submit the job `upload.jcl`: `cat upload.jcl|ncat --send-only -w1 127.0.0.1 3505`
- Install `https://github.com/mvslovers/rdrprep` on your Linux box
- Clone `https://github.com/mvslovers/jcc` to this folder
- Install wine and wine 32: `sudo apt install wine wine32`
- Compile `GETSPLOIT/hello.c`:
    - `wine ./jcc/jcc.exe -I./jcc/include -o ./GETSPLOIT/hello.c`
    - `./jcc/prelink -s ./jcc/objs hello.load hello.obj`
- Copy `hello.load` to `./GETSPLOIT`: `cp hello.load GETSPLOIT`
- Run usersjcl.py: `./usersjcl.py`
- Convert each job in the users folder with `rdrprep` and submit them one by one:
    - `for i in *.jcl; do echo $i;rdrprep $i;cat reader.jcl|ncat --send-only -w1 172.17.0.3 3506; read; done`
    - You can check the output of MVSCE `printers/prt00e.txt` to see each job completed
- Shutdown MVS/CE
- Re-IPL MVS/CE and enjoy your lab environment
- Then download web3270 from https://github.com/MVS-sysgen/web3270
- Follow the instructions on how to prepare for web3270
- Edit `web3270.ini` as appropriate
- Launch web3270 with `python3 -u ./server.py --config /path/to/config --certs /path/to/certs`

## Files

- `GETSPLOIT/hello.c` vulnerable C program from https://github.com/jake-mainframe/GETSPLOIT
- `ARBAUTH` from https://github.com/jake-mainframe/ARBAUTH
- EBCDIC files `overflows/LGBT400`, `overflows/LOC400`, `overflows/WTO400`
- `Dockerfile` used to build docker image
- `MACLFTPD.jcl`: JCL file to install MACLIBS and FTPD server using MVP
- `logon_screen.ans`/`jcl/logon_screen.jcl`: ANSI/JCL to replace the NETSOL logon screen
- `upload.py` generates JCL used to provision datasets, copy files and get the system ready
- `jcl/terminals.jcl` adds 32 new terminal interfaces and updates VTAM config
- `usersjcl.py` creates `DC00.jcl` through `DC23.jcl` in the `./users` folder
- `automation.py` a MVS automation python script used to deploy to docker
- `matrix.txt` Follow the white rabbit
- `rexx/DEBRUJIN.rex`: REXX script to generate Debrujin pattern
- `rexx/decodei.rex`: decodes MVS hex instructions to human readeable
- `motd.txt` the CLIST run at logon to TSO
- `mvs.sh` the container run script to launch web3270, hercules


