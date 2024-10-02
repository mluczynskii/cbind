	.file	"main.c"
	.text
	.p2align 4
	.globl	increment
	.type	increment, @function
increment:
.LFB23:
	.cfi_startproc
	addl	$1, (%rdi)
	ret
	.cfi_endproc
.LFE23:
	.size	increment, .-increment
	.p2align 4
	.globl	decrement
	.type	decrement, @function
decrement:
.LFB24:
	.cfi_startproc
	subl	$1, (%rdi)
	ret
	.cfi_endproc
.LFE24:
	.size	decrement, .-decrement
	.section	.rodata.str1.1,"aMS",@progbits,1
.LC0:
	.string	"CFunction"
.LC1:
	.string	"%s"
	.section	.text.startup,"ax",@progbits
	.p2align 4
	.globl	main
	.type	main, @function
main:
.LFB25:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	leaq	.LC0(%rip), %rdi
	pushq	%rbx
	.cfi_def_cfa_offset 24
	.cfi_offset 3, -24
	subq	$8, %rsp
	.cfi_def_cfa_offset 32
	movq	8(%rsi), %rbp
	call	initLua@PLT
	movq	%rax, %rdi
	movq	%rbp, %rsi
	movq	%rax, %rbx
	call	execScript@PLT
	leaq	.LC1(%rip), %rsi
	movl	$2, %edi
	movq	%rax, %rdx
	xorl	%eax, %eax
	call	__printf_chk@PLT
	movq	%rbx, %rdi
	call	closeLua@PLT
	addq	$8, %rsp
	.cfi_def_cfa_offset 24
	xorl	%eax, %eax
	popq	%rbx
	.cfi_def_cfa_offset 16
	popq	%rbp
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc
.LFE25:
	.size	main, .-main
	.ident	"GCC: (GNU) 13.2.0"
	.section	.note.GNU-stack,"",@progbits
