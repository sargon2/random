int main() {
    int q=34;
    int n=10;
    char *p="int main() {%c    int q=%d;%c    int n=%d;%c    char *p=%c%s%c;%c    printf(p,n,q,n,n,n,q,p,q,n,n,n);%c}%c";
    printf(p,n,q,n,n,n,q,p,q,n,n,n);
}
