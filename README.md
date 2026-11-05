# Atividade Redes 02 - Grupo 02 (Agenda)

## Equipe 02
Trabalho da disciplina de Sistemas Distribuídos (Equipe 02).

É a mesma agenda da APS 01, mas agora com socket UDP. O servidor guarda uma agenda de compromissos na memória e vários clientes podem usar ao mesmo tempo, adicionando, listando, atualizando e removendo eventos. A diferença é que o UDP não tem conexão: cada comando que o cliente digita vai em um datagrama separado e o servidor responde com outro datagrama.

**Integrantes:**

- Daniel Acioly
- Pedro Sarmento
- Luís Felipe Londres
- Lucas Cabral
- Matheus Santos
- Pablo Henrique

## Requisitos

Só o Python 3. Não usamos nenhuma biblioteca externa, então não precisa de `pip install`.

Para ver se já está instalado:

```
python --version
```

No Linux e no Mac normalmente o comando é `python3` em vez de `python`.

## Estrutura do repositório

```
redes-aps02/
├── README.md
└── arquivos/
    ├── servidor.py
    ├── cliente.py
```

| Arquivo | O que faz |
|---------|-----------|
| `README.md` | explica o projeto, como rodar, os comandos e as decisões que tomamos |
| `arquivos/servidor.py` | servidor UDP que guarda a agenda na memória e atende cada datagrama que chega em uma thread |
| `arquivos/cliente.py` | cliente de terminal: manda os comandos para o servidor e mostra as respostas |

## Como rodar

**1. Baixar o projeto**

```
git clone https://github.com/LucasCabra7/redes-aps02
cd redes-aps02/arquivos
```

**2. Subir o servidor**

Em um terminal:

```
python servidor.py
```

Se der certo, aparece `servidor UDP ouvindo na porta 5050`. Deixe esse terminal aberto. Cada comando que chegar vai aparecer nele junto com o endereço de quem mandou.

**3. Abrir o cliente**

Em outro terminal, na mesma pasta:

```
python cliente.py
```

Vai aparecer `cliente UDP enviando para 127.0.0.1:5050. digite sair para encerrar`, e aí é só digitar os comandos da próxima seção. Como não tem conexão, se o servidor estiver desligado o cliente só percebe no primeiro comando.

Para testar vários usuários ao mesmo tempo, abra mais terminais e rode `python cliente.py` em cada um. Todos usam a mesma agenda, então se um cliente adicionar um evento o outro já vê quando der `LIST`.

**4. Encerrar**

- Cliente: digite `sair`.
- Servidor: `Ctrl + C` no terminal dele.

### Rodando em computadores diferentes

Por padrão o cliente manda os comandos para `127.0.0.1`, ou seja, para a própria máquina. Para usar o servidor rodando em outro computador da mesma rede:

1. Descubra o IP da máquina do servidor (`ipconfig` no Windows, `ip a` no Linux ou `ifconfig` no Mac).
2. No `cliente.py`, troque a linha `HOST = "127.0.0.1"` pelo IP do servidor.
3. Se só aparecer `sem resposta do servidor`, provavelmente é o firewall bloqueando a porta 5050 (UDP).

### Problemas comuns

- **`sem resposta do servidor, confira se ele esta rodando`**: o cliente esperou 3 segundos e não chegou nada. Quase sempre é porque o servidor não está aberto; suba ele e mande o comando de novo.
- **`nao foi possivel falar com 127.0.0.1:5050`**: aparece no Windows no mesmo caso de cima. A solução é a mesma.
- **`Address already in use`**: já tem outro servidor rodando em algum terminal. Feche ele antes.

## Comandos

Os comandos podem ser digitados em maiúsculo ou minúsculo. As datas usam o formato `AAAA-MM-DD`, as horas `HH:MM` e a duração é em minutos.

**ADD**: adiciona um compromisso. A descrição é opcional e vem depois do `|`.

```
ADD <data> <hora> <duracao> <titulo> | <descricao>

ADD 2026-11-10 14:00 60 Reuniao do grupo | revisar o codigo
ADD 2026-11-10 09:30 30 Aula de SD
```

Resposta: `OK evento 1 criado`. O número é o id do evento, que é usado no UPDATE e no DELETE.

**LIST**: lista os compromissos de um dia, ordenados pela hora. A data é obrigatória.

```
LIST 2026-11-10
```

Resposta: primeiro vem `OK` com a quantidade de eventos e depois um evento por linha:

```
OK 2
2 2026-11-10 09:30 30min Aula de SD
1 2026-11-10 14:00 60min Reuniao do grupo | revisar o codigo
```

**UPDATE**: altera um campo de um compromisso. Os campos são `titulo`, `data`, `hora`, `duracao` e `descricao`.

```
UPDATE <id> <campo> <novo_valor>

UPDATE 1 hora 15:00
UPDATE 1 titulo Reuniao final do grupo
```

Resposta: `OK evento 1 atualizado`

**DELETE**: remove um compromisso pelo id.

```
DELETE 2
```

Resposta: `OK evento 2 removido`

**sair**: fecha o cliente. Esse comando não vai para o servidor, é tratado no próprio `cliente.py`.

### Quando dá erro

Se algo estiver errado, o servidor responde com uma linha começando com `ERRO` e o cliente pode continuar mandando comandos normalmente. Alguns exemplos:

```
> LIST
ERRO uso: LIST <data>
> ADD 10/11/2026 14:00 60 Teste
ERRO data invalida, use AAAA-MM-DD
> DELETE 99
ERRO evento 99 nao encontrado
> ABC
ERRO comando desconhecido
```

## Protocolo

A comunicação é toda em texto, usando UDP. Não tem conexão: o cliente só manda um datagrama para o endereço do servidor (`127.0.0.1:5050` por padrão) e fica esperando a resposta.

- Cada comando vai em um datagrama só.
- O servidor responde com um datagrama para o mesmo endereço e porta de onde veio o comando. É assim que ele sabe para quem responder, já que não tem conexão aberta.
- A primeira linha da resposta sempre começa com `OK` ou `ERRO`.
- ADD, UPDATE e DELETE respondem com uma linha só.
- O LIST é o único que responde com várias linhas: a primeira é `OK <n>` e depois vêm `n` linhas, uma por evento. Todas vão juntas no mesmo datagrama.

Na APS 01 a gente precisava do `\n` para saber onde terminava cada mensagem, porque o TCP é um fluxo de bytes. No UDP isso não é mais problema, porque cada datagrama já chega separado e inteiro. Mesmo assim mantivemos o mesmo formato de texto (inclusive o `OK <n>` do LIST) para os comandos e as respostas ficarem iguais aos da primeira atividade.

Formato de cada evento na resposta do LIST:

```
<id> <data> <hora> <duracao>min <titulo> | <descricao>
```

A parte do `| <descricao>` só aparece se o evento tiver descrição.

O tamanho máximo de um datagrama UDP é 65507 bytes, e é esse o tamanho que o servidor e o cliente usam no `recvfrom`. Um comando digitado nunca chega perto disso, e a resposta do LIST só passaria do limite com muitos eventos no mesmo dia.

## Decisões de projeto

**Formato do ADD.** O enunciado sugere `ADD <data> <hora> <titulo>`, mas o evento também precisa ter duração e uma descrição opcional, então o comando ficou assim:

```
ADD <data> <hora> <duracao> <titulo> | <descricao>
```

- Data, hora e duração vêm primeiro porque não têm espaço no meio, então dá para separar pelos espaços sem confusão.
- O título vem por último antes do `|` para poder ter espaços (`Reuniao do grupo`). O servidor separa só os 3 primeiros campos e o que sobrar é o título.
- A descrição também pode ter espaços, então precisava de um separador diferente do espaço. Escolhemos o `|`. Se não tiver `|`, o evento fica sem descrição.

**Formato do UPDATE.** O enunciado sugere `UPDATE <id> <novo_valor>`, mas só com isso o servidor não sabe qual campo trocar (o `15:00` é uma hora, mas o `60` pode ser a duração ou o título). Por isso adicionamos o nome do campo:

```
UPDATE <id> <campo> <novo_valor>
```

Cada UPDATE muda um campo só. O novo valor passa pela mesma validação do ADD, então não dá para colocar uma data inválida editando o evento.

**Data e hora.** Usamos `AAAA-MM-DD` e `HH:MM` (24h). O servidor converte com o `datetime`, então datas que não existem, como `2026-02-30`, já dão erro. Ele também guarda sempre no mesmo formato (`9:30` vira `09:30`), e por isso dá para ordenar o LIST comparando a hora como texto.

**LIST por dia.** O LIST pede a data porque o enunciado usa `LIST <data>` e porque, com muitos eventos, listar a agenda inteira ia ficar confuso. No UDP isso ainda ajuda a resposta a caber em um datagrama só.

**Ids.** Cada evento ganha um id que é só um contador que começa em 1. Quando um evento é apagado, o id dele não é reaproveitado. Assim, se um cliente apagar o evento 2 e outro criar um evento logo depois, o novo não vai ser o 2. Isso evita que alguém dê UPDATE ou DELETE no evento errado achando que é o antigo.

**Conflito de horário.** O servidor deixa criar dois eventos no mesmo horário. Como a agenda é compartilhada por várias pessoas, não faz sentido bloquear um compromisso só porque outra pessoa marcou algo na mesma hora.

**Sem conexão persistente.** O enunciado da APS 01 pedia conexões persistentes, mas o UDP não tem conexão. No lugar disso, o servidor fica ouvindo na porta 5050 e responde cada datagrama para o endereço de quem mandou. Ele não guarda nenhuma informação sobre os clientes, então qualquer cliente pode mandar comandos a qualquer momento, sem "entrar" nem "sair".

**Perda de pacote.** O UDP não garante que o datagrama chega. O cliente espera a resposta por 3 segundos e, se não chegar nada, mostra `sem resposta do servidor` e volta para o `>`. Não fizemos reenvio automático porque, se o ADD tiver chegado e só a resposta se perdeu, reenviar criaria o evento duas vezes. Nesse caso dá para usar o `LIST` e conferir se o evento entrou antes de mandar de novo.

**Erro de porta no Windows.** No Windows, se o servidor responde para um cliente que já fechou, o próximo `recvfrom` do servidor pode dar `ConnectionResetError`. O servidor ignora esse erro e continua ouvindo, para não cair por causa de um cliente que saiu.

**Agenda só na memória.** Como pede o enunciado, os eventos ficam em um dicionário dentro do servidor. Se o servidor for fechado, a agenda é perdida.

## Concorrência e integridade dos dados

Como não tem conexão, o servidor não cria uma thread por cliente como na APS 01. Ele fica em um laço recebendo datagramas e, para cada um que chega, abre uma thread que processa o comando e manda a resposta. Assim um comando mais demorado não segura os outros, e comandos de clientes diferentes podem estar sendo tratados ao mesmo tempo. Todas as threads usam o mesmo dicionário `agenda` e o mesmo contador `proximo_id`.

Para não dar problema, usamos um `threading.Lock` único:

- **ADD**: ler o `proximo_id`, salvar o evento e somar 1 no contador acontece dentro do lock. Sem isso, dois clientes que dessem ADD ao mesmo tempo podiam ler o mesmo valor do contador e ganhar o mesmo id, e um evento ia sobrescrever o outro.
- **UPDATE e DELETE**: conferir se o id existe e alterar ou apagar o evento é feito dentro do lock. Assim não acontece de um cliente checar que o evento existe, outro apagar ele, e o primeiro tentar alterar algo que já sumiu.
- **LIST**: a busca e a montagem das linhas também ficam dentro do lock, para não ler um evento no meio de uma alteração.

A validação dos dados (data, hora, duração) é feita antes de pegar o lock, porque não mexe na agenda. Assim o lock fica preso o menor tempo possível.

Para testar, mandamos 200 ADD ao mesmo tempo, cada um de uma thread. Todos receberam ids diferentes e o `LIST` daquele dia mostrou `OK 200`, sem nenhum evento perdido.

## Exemplo

Sessão com o servidor rodando e um cliente mandando comandos:

```
> ADD 2026-11-10 14:00 60 Reuniao do grupo | revisar o codigo
OK evento 1 criado
> ADD 2026-11-10 09:30 30 Aula de SD
OK evento 2 criado
> ADD 2026-11-11 08:00 120 Prova de redes
OK evento 3 criado
> LIST 2026-11-10
OK 2
2 2026-11-10 09:30 30min Aula de SD
1 2026-11-10 14:00 60min Reuniao do grupo | revisar o codigo
> UPDATE 1 hora 16:00
OK evento 1 atualizado
> UPDATE 2 descricao levar o notebook
OK evento 2 atualizado
> UPDATE 1 duracao abc
ERRO valor invalido para duracao
> DELETE 2
OK evento 2 removido
> DELETE 2
ERRO evento 2 nao encontrado
> UPDATE 3 local CIn
ERRO campo invalido, use titulo, data, hora, duracao ou descricao
> list 2026-11-11
OK 1
3 2026-11-11 08:00 120min Prova de redes
> sair
```

Enquanto isso, o terminal do servidor mostra cada comando com o endereço de quem mandou:

```
servidor UDP ouvindo na porta 5050
('127.0.0.1', 54012) -> ADD 2026-11-10 14:00 60 Reuniao do grupo | revisar o codigo
('127.0.0.1', 54012) -> ADD 2026-11-10 09:30 30 Aula de SD
('127.0.0.1', 54012) -> ADD 2026-11-11 08:00 120 Prova de redes
...
```

Um segundo cliente, aberto em outro terminal, já vê a agenda com as alterações do primeiro:

```
> LIST 2026-11-10
OK 1
1 2026-11-10 16:00 60min Reuniao do grupo | revisar o codigo
```

E se o servidor for fechado, o cliente continua aberto e só avisa quando manda o próximo comando:

```
> LIST 2026-11-10
sem resposta do servidor, confira se ele esta rodando
```