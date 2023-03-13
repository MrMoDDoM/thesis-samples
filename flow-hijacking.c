#include <stdio.h>

// This function is never called.
void win(){
    system("/bin/sh");
}

void vuln(){
    char buf[16];
    gets(buf);
    return;
}


void main(){
    vuln();
    return;
}
