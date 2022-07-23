# DEF CON 30 Workshop Mainframe Container

![DEFCON MAINFRAME](/screenshot.png?raw=true "DEF CON 30")

The scripts here are used to build the MVS 3.8j virtual mainframe for the DEFCON 30 workshop. 

## Use docker

You can use docker instead of building from scratch: https://hub.docker.com/r/mainframed767/defcon30

To run the container use the below, make sure to change `/opt/docker/mvsce` to a folder for your system

```
docker run -d \
  --name=defcon30 \
  -e HUSER=docker \
  -e HPASS=docker \
  -p 2121:3221 \
  -p 2323:3223 \
  -p 3270:3270 \
  -p 3505:3505 \
  -p 3506:3506 \
  -p 8888:8888 \
  -p 21021:2121 \
  -v /opt/docker/mvsce:/config \
  -v /opt/docker/mvsce/printers:/printers \
  -v /opt/docker/mvsce/punchcards:/punchcards \
  -v /opt/docker/mvsce/logs:/logs \
  -v /opt/docker/mvsce/dasd:/dasd \
  -v /opt/docker/mvsce/certs:/certs \
  --restart unless-stopped \
  mainframed767/defcon30
```

Ports 2323/3270 are encrypted/unencrypted 3270 servers
Ports 2121/21021 are encrypted/unencrypted FTP servers
Port 8888 is the hercules webserver u/p is docker
Ports 3505/3506 are ebcdic/ascii punch card readers


## Building from scratch

- Download the most recent version of MVSCE from https://github.com/MVS-sysgen/sysgen/releases
- Launch MVSCE
- Submit the job `MACLFTPF.jcl`: `cat jcl/MACLFTPF.jcl|ncat --send-only -w1 127.0.0.1 3505`
- Submit the job `logon_screen.jcl`: `cat jcl/logon_screen.jcl|ncat --send-only -w1 127.0.0.1 3505`
- Submit the job `terminal.jcl`: `cat terminal.jcl|ncat --send-only -w1 127.0.0.1 3505`
- Clone the ARBAUTH repo: `git clone https://github.com/jake-mainframe/ARBAUTH`
- Run the python script `upload.py`: `./upload.py motd.txt`
- Submit the job `upload.jcl`: `cat upload.jcl|ncat --send-only -w1 127.0.0.1 3505`
- Install `https://github.com/mvslovers/rdrprep` on your Linux box
- Clone `https://github.com/mvslovers/jcc` to this folder
- Compile `hello.c`:
    - `./jcc/jcc -I./jcc/include -o hello.c`
    - `./jcc/prelink -s ./jcc/objs hello.load hello.obj`
- Copy `hello.load` to `./GETSPLOIT`: `cp hello.load GETSPLOIT`
- Run usersjcl.py: `./usersjcl.py`
- Convert each job in the users folder with `rdrprep` and submit them one by one:
    - `for i in *.jcl; do echo $i;rdrprep $i;cat reader.jcl|ncat --send-only -w1 172.17.0.3 3506; read; done`
    - You can check the output of MVSCE `printers/prt00e.txt` to see each job completed
- Shutdown MVS/CE
- Re-IPL MVS/CE and enjoy your lab environment

## Files

- `GETSPLOIT/hello.c` vulnerable C program from https://github.com/jake-mainframe/GETSPLOIT
- `ARBAUTH` from https://github.com/jake-mainframe/ARBAUTH
- EBCDIC files `LGBT400`, `LOC400`, `WTO400`
- `Dockerfile` used to build docker image
- `logon_screen.ans`/`logon_screen.jcl`: ANSI/JCL to replace the NETSOL logon screen
- `upload.py` generates JCL used to provision datasets, copy files and get the system ready
- `terminals.jcl` adds 32 new terminal interfaces and updates VTAM config
- `usersjcl.py` creates `DC00.jcl` through `DC30.jcl` in the `./users` folder
- `submit.py` a MVS automation python script used to deploy to docker


