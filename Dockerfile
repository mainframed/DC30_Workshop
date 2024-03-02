

FROM mainframed767/jcc:wine as getsploit_builder
# First compile and link hello.c to hello.load
WORKDIR /
COPY GETSPLOIT/hello.c hello.c
RUN wine /jcc/jcc.exe -I/jcc/include/ -o hello.c
RUN /jcc/prelink -s /jcc/objs /hello.load /hello.obj

FROM mainframed767/mvsce:2.0.3 as MVSCE_builder
# Install rdrprep
RUN unset LD_LIBRARY_PATH && apt-get update && apt-get install -yq git build-essential python3-pip lftp
RUN pip3 install ebcdic
WORKDIR /
RUN git clone --depth 1 https://github.com/mvslovers/rdrprep.git
WORKDIR /rdrprep
ENV HOST_ARCH=NOT_PENTIUM
RUN make && make install
# Copy compiled hello.load
WORKDIR /builder
ADD ./ /builder/
COPY --from=getsploit_builder /hello.load /builder/GETSPLOIT/hello.load
RUN git clone --depth 1 https://github.com/jake-mainframe/ARBAUTH
# Build the JCL
RUN ./upload.py motd.txt
RUN mkdir ./users && ./usersjcl.py
RUN for i in users/*.jcl; do rdrprep $i; mv reader.jcl $i.ebcdic; ls $i.ebcdic; done
COPY extra/FTPD.MVP /MVSCE/MVP/packages/FTPD
# Submit the JCL to MVS/CE
# until ./sysgen.py --timeout 3600 --version ${RELEASE_VERSION} --CONTINUE; do echo "Failed, rerunning"; done
RUN until python3 -u automation.py --mvsce /MVSCE --initial; do echo "Failed, trying again"; done
RUN until python3 -u automation.py --mvsce /MVSCE --ftp; do echo "Failed, trying again"; done
RUN until python3 -u automation.py --mvsce /MVSCE --users; do echo "Failed, trying again"; done
# Install web3270 and its requirements
WORKDIR /
RUN git clone --depth 1 https://github.com/MVS-sysgen/web3270.git
WORKDIR /web3270
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --user -r requirements.txt 


# Final Build
FROM mainframed767/mvsce:2.0.3
COPY --from=MVSCE_builder /MVSCE /MVSCE
COPY --from=MVSCE_builder /root/.local /root/.local
COPY --from=MVSCE_builder /web3270 /web3270
ADD web3270.ini /web3270/
ADD mvs.sh /
RUN unset LD_LIBRARY_PATH && apt-get update && apt-get install --no-install-recommends -yq c3270 nodejs npm &&\
    sed -i "s/0400.8/0400.32/g" /MVSCE/conf/local.cnf &&\
    npm install -g tiddlywiki@5.2.0
COPY wiki/users.txt /auth/users.txt
WORKDIR /var/lib/tiddlywiki
COPY wiki/tiddlywiki/ /var/lib/tiddlywiki/
# Add init-and-run script
ADD wiki/start_tiddlywiki.sh /usr/local/bin/start_tiddlywiki
WORKDIR /
VOLUME ["/config","/dasd","/printers","/punchcards","/logs", "/certs"]
EXPOSE 3221 3223 3270 3505 3506 8888 8443 2121 2323 
ENTRYPOINT ["./mvs.sh"]


