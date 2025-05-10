
# Trabalho realizado nas Semanas #2 e #3

# CVE-2022-27254

## Identificação

- Ataque que afeta o sistema sem chave (RKE) do Honda Civic 2018.

- Esta vulnerabilidade em sistemas de controlo de acesso físico consiste na reutilização de sinais RF para abrir portas sem criptografia dinâmica.

- Isto facilita ataques de replay de sinal para desbloquear o veículo.

- Permite acesso completo e ilimitado para trancar, destrancar, controlar as janelas, abrir o porta-malas e arrancar com o motor do veículo alvo.



## Catalogação

- Este potencial ataque foi reportado pelo cientista de computação Blake Berry e o pesquisador Ayyappam Rajesh em fevereiro de 2022.

- Este CVE foi atribuído e divulgado em março de 2022 pela NVD e os veículos afetados confirmados.

- Quanto a Bug bounty, nenhuma recompensa pública foi mencionada para este CVE.

- Foi classificado como CVSS 5.3 (médio), impacto moderado, mas risco físico elevado.

## Exploit

- É um ataque de replay que se deve à captura de sinais RF (radio frequency) do key fob.

- São utilizadas ferramentas de captura RF para gravar e reproduzir sinais tais como HackRF One, GNURadio , FCCID.io e  Gqrx.


## Ataques

- Relatos de pesquisadores que conseguiram abrir e ligar veículos usando estes ataques foram depois demonstrados em conferências de segurança como Black Hat e DEF CON.

- Apesar dos ataques terem todos sidos feitos em contexto de teste, alguns dos veículos afetados são o 2018 Honda Civic Hatchback e o 2020 Honda Civic LX.

- Este ataque já vem relacionado com o CVE-2019-20626, onde a vulnerabilidade em questão foi encontrada mas a Honda ignorou e continuou sem implementar medidas de segurança.

- Este ataque potencializa o roubo de veículos sem partir janelas ou usar força física.
