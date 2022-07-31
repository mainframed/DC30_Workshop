This is the vulnerable C program used in the class. Original author Jake Labelle.

To compile it:

```
docker run -it --entrypoint /bin/bash -v $(pwd):/project mainframed767/jcc:wine
cd project/
wine /jcc/jcc.exe -I/jcc/include/ -o hello.c
/jcc/prelink -s /jcc/objs /project/hello.load /project/hello.obj
```