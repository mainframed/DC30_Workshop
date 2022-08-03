

FROM mainframed767/jcc:wine as getsploit_builder
# First compile and link hello.c to hello.load
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
# Build the JCL
RUN ./upload.py motd.txt
RUN ./usersjcl.py
RUN for i in users/*.jcl; do rdrprep $i; mv reader.jcl $i.ebcdic; ls $i.ebcdic; done
COPY extra/FTPD.MVP /MVSCE/MVP/packages/FTPD
# Submit the JCL to MVS/CE
RUN python3 -u automation.py --mvsce /MVSCE --initial
RUN python3 -u automation.py --mvsce /MVSCE --ftp
RUN python3 -u automation.py --mvsce /MVSCE --users

# Final Build
FROM mainframed767/mvsce:latest
COPY --from=MVSCE_builder /MVSCE /MVSCE
COPY mvs.sh /
RUN unset LD_LIBRARY_PATH && apt-get update && apt-get install -yq python3-pip c3270 &&\
    git clone --depth 1 https://github.com/MVS-sysgen/web3270.git &&\
    cd web3270 &&\
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    openssl req -x509 -nodes -days 365 \
    -subj  "/C=CA/ST=QC/O=web3270 Inc/CN=3270.web" \
    -newkey rsa:2048 -keyout ca.key \
    -out ca.csr &&\
    cd / &&\
    sed -i "s/0400.8/0400.32/g" /MVSCE/conf/local.cnf &&\
    chmod +x /mvs.sh
ADD web3270.ini /web3270/
WORKDIR /
VOLUME ["/config","/dasd","/printers","/punchcards","/logs", "/certs"]
EXPOSE 3221 3223 3270 3505 3506 8888 8443 2121 2323 
ENTRYPOINT ["./mvs.sh"]


