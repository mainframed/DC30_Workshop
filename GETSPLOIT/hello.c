#include <string.h>
#include <stdlib.h>
#include <stdio.h>

int main (int argc, char ** argv) {
   char buff[150];
   printf("Hi, D3CF0N attendee what is your handle?\n");
   gets(buff);
   printf("Follow the white rabbit, %s", buff);
   return 0;
};