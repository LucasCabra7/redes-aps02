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

## Decisões de projeto

## Concorrência e integridade dos dados

## Exemplo