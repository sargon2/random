# gcc -o retcode retcode.s
.global main
main:
    mov $60, %rax
    mov $6, %rdi # returns 6
    syscall
