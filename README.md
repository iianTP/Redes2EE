# Sistema de Monitoramento Remoto

Aplicação distribuída em Python baseada na arquitetura **Cliente-Servidor**, que permite a um cliente monitorar remotamente informações de hardware, sistema operacional e processos de uma ou mais máquinas conectadas a um servidor de monitoramento.

Projeto desenvolvido para a disciplina **Redes de Computadores 1** — UPE/POLI.

**Autores:** Alice Galvão Vasconcelos, Ian Teixeira Pimentel e Juliana Danzi D'Amorim Ferreira
**Professor:** Edison Albuquerque
**Semestre:** 2026.1 | **Turma:** RA

---

## Sobre o projeto

O sistema permite que um computador (cliente) envie requisições a um servidor de monitoramento, que pode se comunicar com uma ou mais máquinas monitoradas. O servidor é responsável por aguardar conexões, receber comandos, interpretar solicitações e retornar ao cliente as informações correspondentes. O cliente fornece a interface de comunicação para o usuário enviar comandos e visualizar as respostas.

É possível:
- Conectar e listar máquinas monitoradas;
- Consultar processos em execução;
- Verificar o estado atual (uso de CPU, RAM e disco) de uma máquina;
- Obter informações gerais da máquina (sistema operacional, arquitetura, processador, armazenamento);
- Consultar o histórico de uso de recursos (logs).

---

## Tecnologias e bibliotecas

- **Python**
- **Sockets TCP** — comunicação cliente-servidor via `socket.AF_INET`, `socket.SOCK_STREAM`
- **TCP/IP** — TCP garante entrega confiável e ordenada dos dados (handshake de três vias); IP é responsável pelo endereçamento e roteamento dos pacotes
- **psutil** — coleta de dados de uso de RAM, disco e CPU
- **tabulate** — formatação de dados em tabelas
- **py-cpuinfo** — informações do processador (`cpuinfo.get_cpu_info()['brand_raw']`)
- **platform** — informações gerais da máquina (sistema operacional, versão, arquitetura)

---

## Arquitetura

O sistema é dividido em servidores, cliente, controllers e parsers.

### Controllers (lógica de processamento)
| Arquivo | Função |
|---|---|
| `display_controller.py` | Formata dados para exibição (tabelas, listas, barras de porcentagem, ajuda) |
| `machine_controller.py` | Coleta dados de hardware/sistema (SO, versão, arquitetura, CPU, núcleos, RAM, armazenamento, processos) |
| `monitor_controller.py` | Gerencia a lista de máquinas conectadas: conectar, renomear, coletar uso de CPU/disco/RAM, salvar e consultar logs |

### Parsers (traduzem comandos em ações)
`servidor → parser → controller → servidor`

| Arquivo | Função |
|---|---|
| `display_parser.py` | Associa comandos de exibição ao `display_controller.py` |
| `machine_parser.py` | Associa comandos de máquina ao `machine_controller.py` |
| `monitor_parser.py` | Associa comandos de monitoramento ao `monitor_controller.py` |

### Demais arquivos
- **`server.py`** — classe base que inicia o servidor (socket, bind, listen, accept)
- **`monitor.py`** — servidor de monitoramento, herda de `server.py`, usa `monitor_parser.py`, porta padrão `2222`
- **`machine.py`** — servidor da máquina monitorada, herda de `server.py`, usa `machine_parser.py`, porta `2223`
- **`client.py`** — interface de comunicação com o usuário: envia comandos e exibe respostas
- **`logs/`** — armazena o histórico de utilização (data, CPU, disco, RAM) de cada máquina
- **`requirements.txt`** — dependências do projeto

---

## Fluxo geral do sistema

1. O cliente (`client.py`) solicita o IP do servidor, cria um socket TCP e conecta-se ao servidor de monitoramento (porta `2222`).
2. O servidor aguarda conexões e passa a receber comandos do cliente.
3. O usuário digita um comando (ex.: `STATUS:MAQUINA1`), que é enviado via `sendall`.
4. O servidor recebe a requisição (`conn.recv`) e a repassa ao parser, que identifica comando e parâmetros.
5. O parser localiza o comando correspondente em seu dicionário de comandos e chama a função associada no controller.
6. Se o comando for direcionado a uma máquina monitorada, o `monitor_controller.py` localiza o ID informado e abre conexão com o servidor daquela máquina (`machine.py`, porta `2223`).
7. O `machine_parser.py` identifica o comando (ex.: `M_STATUS`) e chama a função correspondente no `machine_controller.py`.
8. O controller da máquina coleta os dados via `psutil` e monta a resposta.
9. A resposta trafega de volta: máquina → servidor de monitoramento → cliente.
10. O cliente converte a resposta em um dicionário e, conforme o tipo de exibição (`DISPLAY`), aciona o `display_parser.py` para formatar a saída, ou imprime os dados sem alteração (`DISPLAY:NONE`).

---

## Protocolo

**Requisição:**
```
(comando):(parâmetro-1);(parâmetro-2);(parâmetro-3);...
```

**Múltiplas requisições:**
```
(requisição-1)|(requisição-2)|(requisição-3)|...
```

**Resposta bem-sucedida:**
```
RES:OK|DISPLAY:(tipo-de-exibição)|DATA:(dados)
```

**Resposta mal-sucedida:**
```
RES:ERROR|MSG:(mensagem)
```

### Formato dos dados por tipo de exibição

| Tipo | Formato |
|---|---|
| Listagem (`LIST`/`HELP`) | `DATA:(label)_(dado);(label)_(dado);...` |
| Tabela (`TABLE`) | `DATA:(coluna-1)_(coluna-2)_...;(dado)_(dado)_...;...` |
| Consumo (`USAGE`) | `DATA:(label)_(uso-%);(label)_(uso-%);...` |

---

## Comandos disponíveis

### Ajuda
- `HELP` — lista todos os comandos disponíveis com descrições e parâmetros.

### Conexão / identificação
- `LINK:(ip-1);(ip-2);...` — conecta/salva uma ou mais máquinas ao servidor de monitoramento.
- `LIST` — lista os IDs das máquinas conectadas.
- `RENAME:(id)` — renomeia o identificador de uma máquina.
- `REMOVE:(id)` — remove a conexão de uma máquina.

### Dados das máquinas
- `INFO:(id)` — exibe sistema operacional, edição e versão do SO, arquitetura, processador, núcleos físicos/lógicos, RAM total e armazenamento total.
- `STATUS:(id)` — informa o consumo atual de memória, processamento e armazenamento.
- `PROCS:(id);(limite);(ordenação)` — lista os N processos que mais consomem memória ou processamento.
- `LOG:(id)` — exibe o histórico de consumo de recursos da máquina.

---

## Como executar

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Em cada máquina a ser monitorada, execute:
   ```bash
   python machine.py
   ```
3. Inicie o servidor de monitoramento:
   ```bash
   python monitor.py
   ```
4. Em outra máquina (ou na mesma), inicie o cliente e informe o IP do servidor de monitoramento quando solicitado:
   ```bash
   python client.py
   ```
5. Utilize os comandos listados na seção [Comandos disponíveis] para interagir com o sistema (ex.: `LINK:192.168.0.10`, `LIST`, `STATUS:MAQUINA1`).
