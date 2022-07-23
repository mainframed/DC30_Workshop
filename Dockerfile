# First compile hello world

FROM mainframed767/jcc:wine as getsploit_builder

# compile and link hello.c to hello.load
WORKDIR /
COPY GETSPLOIT/hello.c hello.c
RUN wine /jcc/jcc.exe -I/jcc/include/ -o hello.c
RUN /jcc/prelink -s /jcc/objs /hello.load /hello.obj

FROM mainframed767/mvsce:latest as MVSCE_builder
# Install rdrprep
RUN unset LD_LIBRARY_PATH && apt-get update && apt-get install -yq git build-essential python3-pip lftp
RUN pip3 install ebcdic
WORKDIR /
RUN git clone --depth 1 https://github.com/mvslovers/rdrprep.git
WORKDIR /rdrprep
RUN make && make install
WORKDIR /builder
ADD ./ /builder/
COPY --from=getsploit_builder /hello.load /builder/GETSPLOIT/hello.load
RUN git clone --depth 1 https://github.com/jake-mainframe/ARBAUTH
RUN ./upload.py motd.txt
RUN ./usersjcl.py
RUN for i in users/*.jcl; do rdrprep $i; mv reader.jcl $i.ebcdic; ls $i.ebcdic; done
RUN python3 -u automation.py --mvsce /MVSCE --initial
RUN python3 -u automation.py --mvsce /MVSCE --ftp
RUN python3 -u automation.py --mvsce /MVSCE --users

# Final Build
FROM mainframed767/mvsce:latest
RUN unset LD_LIBRARY_PATH && apt-get update && apt-get install -yq python3-pip c3270
# Install web3270
RUN git clone --depth 1 https://github.com/MVS-sysgen/web3270.git
WORKDIR /web3270
COPY web3270/requirements.txt /web3270
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    openssl req -x509 -nodes -days 365 \
    -subj  "/C=CA/ST=QC/O=web3270 Inc/CN=3270.web" \
    -newkey rsa:2048 -keyout ca.key \
    -out ca.csr
ADD web3270.ini web3270/index.html web3270/server.py web3270/login.html web3270/favicon.ico web3270/3270-Regular.woff /web3270/
COPY --from=MVSCE_builder /MVSCE /MVSCE
COPY mvs.sh /
RUN chmod +x /mvs.sh
VOLUME ["/config","/dasd","/printers","/punchcards","/logs", "/certs"]
EXPOSE 3221 3223 3270 3505 3506 8888 443 21021
ENTRYPOINT ["./mvs.sh"]


