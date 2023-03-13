#include <stdio.h>

void vuln(){
    char buf[16];
    gets(buf);
    return;
}

void main(){
    printf("getc @ %p\n", getc);
    vuln();
    return;
}
