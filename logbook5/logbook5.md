# Guião Semana #5 (Buffer-Overflow Attack Lab - Set-UID Version)

## Configuração do ambiente
Começamos por desativar as contramedidas indicadas no guião.

![pre tasks](logbook5/pre_task.png)

## Questão 1
### Task 1
Compilamos o código disponível em callshellcode.c utilizando o comando *make* e observamos que foram gerados os binários para as shellcodes, criando dois ficheiros - a32.out e a64.out. Corremos e foram abertas duas *shells*, uma de 32 bits e outra de 64 bits.

![task 1](logbook5/task_1.png)


### Task 2
Depois de alterarmos o valor da variável L1 da Makefile disponível na pasta Labsetup/code para o valor 100+8*7, compilamos e verificamos que ocorreu segmentation fault, pois apesar de no programa stack.c ser definido um BUF_SIZE igual a 100 bytes, a função *strcpy* tenta copiar um array com até 517 bytes (mais do que o buffer pode suportar) sem verificar os seus limites e causando assim assim **buffer overflow**.


![task 2](logbook5/task_2.png)

Para isto desativamos também o *StackGuard* e as proteções contra a execução de código invocado desde a stack, mudamos o owner do programa para `root` e ativamos o `Set-UID` utilizando os seguintes comandos:

```bash
$ gcc -DBUF_SIZE=100 -m32 -o stack -z execstack -fno-stack-protector stack.c
$ sudo chown root stack
$ sudo chmod 4755 stack
```


### Task 3
Para podermos fazer uso da vulnerabilidade buffer overflow deste programa começamos por criar o ficheiro badfile vazio, executamos o código vulnerável e utilizamos depois o debugger gdb para executar o código vulnerável e descobrir o endereço inicial do buffer e a posição do return address. Para isso corremos os seguites comandos:

```bash
$ touch badfile
$ gdb stack-L1-dbg
gdb-peda$ b bof
gdb-peda$ run
gdb-peda$ next
gdb-peda$ p $ebp
gdb-peda$ p &buffer
```

![task 3](logbook5/task_3-2.png)

Após obtermos os endereços necessários, fizemos as seguintes alterações no ficheiro badfile:
- na variável shellcode inserimos o shellcode em 32-bits que executa uma shell
- alteramos o valor de start
- colocamos o novo endereço de retorno
- calculamos o offset

![task 3](logbook5/task_3-5.png)

Por fim, executamos o programa vulnerável o que provocou novamente buffer overflow, contudo desta vez foi lançada uma shell com permissões root tal como esperado.

![task 3](logbook5/task_3-4.png)