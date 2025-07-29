.section .text
.globl _start
_start:
mov $2, %rax
push %rax
mov $19, %rax
pop %rbx
add %rbx, %rax

push %rax
mov $8, %rax
push %rax
mov $12, %rax
pop %rbx
mul %rbx, %rax

pop %rbx
add %rbx, %rax
call imprime_num

mov $245678, %rax
push %rax
mov $14569, %rax
pop %rbx
add %rbx, %rax

push %rax
mov $4578, %rax
push %rax
mov $25, %rax
pop %rbx
sub %rbx, %rax

pop %rbx
div %rbx, %rax
call imprime_num

call sair
.include "runtime.s"