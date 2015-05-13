# gcc -O3 -o go hello_world.s && ./go
.global main
message: .ascii "hello world\n"
str_len = . - message
main:
    mov $1, %rax
    mov $1, %rdi
    mov $message, %rsi
    mov $str_len, %rdx
    syscall
