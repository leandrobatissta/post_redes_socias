# Sistema Kiosk Protegido com Operação Autônoma 24/7: Arquitetura, Proteção Multi-Camada e Aceleração por Inteligência Artificial

**Versão:** 1.0.0 — Produção  
**Data de conclusão da fase v1.0:** 16 de abril de 2026  
**Classificação:** Documento público — dados sensíveis de configuração, protocolo e infraestrutura omitidos intencionalmente.

---

## Autores e Créditos

**Cleyton Pedroza**  
Criador dos componentes fundamentais do sistema. Responsável pela concepção da arquitetura base, desenvolvimento do protocolo de comunicação proprietário, criação da infraestrutura de servidores, criptografia e design original dos fluxos de operação. A base técnica sobre a qual todo o sistema foi construído.

**Leandro Batista**  
Responsável pelo aperfeiçoamento, implementação prática e desenvolvimento de hardware. Transformou a base arquitetural em produto funcional em produção — implementando os drivers, o sistema de bloqueio físico multi-camada, a automação de build e processos de recuperação autônoma. A fase v1.0 foi concluída em 7 dias por uma única pessoa, com auxílio de ferramentas de Inteligência Artificial.

---

## Resumo

Este paper descreve a arquitetura, implementação e validação de um sistema completo de Kiosk/Loja virtual desenvolvido para operação autônoma ininterrupta (24/7) sem necessidade de intervenção manual. O sistema integra cinco componentes de software — quatro em produção e um em desenvolvimento — comunicando-se via protocolo serial proprietário. São implementadas quatro camadas de proteção: física, de software, de sistema e operacional. O ambiente de execução é baseado em Linux com gerenciador de janelas minimalista, gerenciamento de serviços via daemon de sistema e binários compilados para distribuição segura. A fase v1.0 foi entregue em 7 dias por um único desenvolvedor, com aceleração significativa proporcionada pelo uso de ferramentas de Inteligência Artificial — uma tarefa que, no modelo tradicional com equipe, demandaria entre 30 e 60 dias.

**Palavras-chave:** Kiosk, Protocolo Serial Proprietário, Bloqueio Físico, Automação, Linux, Python, Inteligência Artificial, Desenvolvimento Acelerado.

---

## 1. Introdução

Sistemas de Kiosk são amplamente utilizados em aplicações comerciais que exigem operação contínua e segura sem supervisão humana direta [1]. O desafio fundamental nesse domínio é garantir que o sistema opere de forma autônoma, resista a tentativas de manipulação física e digital, e se recupere automaticamente de falhas — tudo isso com latência mínima e sem interrupção do serviço.

Este trabalho apresenta a arquitetura e implementação de um sistema Kiosk desenvolvido sobre Linux com interface minimalista (tela preta), protocolo de comunicação serial customizado, sistema de bloqueio físico de dispositivos de entrada e automação completa de boot, atualizações e recuperação.

O sistema foi concebido com uma base técnica sólida pré-existente — arquitetura, protocolos e criptografia desenvolvidos por Cleyton Pedroza — e implementado em sua totalidade funcional por Leandro Batista em 7 dias, com auxílio de ferramentas de IA. Este resultado representa uma redução de 75–90% no tempo de desenvolvimento estimado pelo modelo tradicional (30–60 dias com equipe), ilustrando o impacto concreto da IA no ciclo de desenvolvimento de software embarcado.

> **Nota:** Detalhes de configuração, caminhos de instalação, estrutura de repositórios, mensagens do protocolo e identificadores internos foram omitidos intencionalmente. O sistema encontra-se em fase de stage/teste em campo.

---

## 2. Arquitetura do Sistema

### 2.1 Visão Geral

O sistema é composto por cinco componentes principais organizados em uma arquitetura modular com comunicação via protocolo serial proprietário:

| # | Componente | Função | Status |
|---|---|---|---|
| 1 | Driver Principal | Core do protocolo de comunicação (botões, sensores, periféricos de hardware) | Produção |
| 2 | Updater | Sistema de atualização automática com rollback | Produção |
| 3 | Launcher | Interface Kiosk fullscreen | Produção |
| 4 | System Lock | Bloqueio físico de dispositivos de entrada | Produção |
| 5 | Game Module | Jogos Interativos | Em desenvolvimento |

Todos os componentes se comunicam via protocolo serial proprietário e são orquestrados por um gerenciador de interface gráfica minimalista com inicialização sequencial controlada via daemon de serviços do sistema.

### 2.2 Ambiente de Execução

| Categoria | Tecnologia |
|---|---|
| Sistema Operacional | Linux |
| Gerenciador de Interface Gráfica | Minimalista (sem ambiente de desktop) |
| Gerenciador de Serviços | Daemon de inicialização do sistema |
| Linguagem | Python 3 |
| Compilação/Distribuição | Compilador de binários Python |
| Versionamento | Git |
| Build Automation | Makefile |
| Integridade | Checksum criptográfico |

### 2.3 Ordem de Inicialização

O sistema segue uma sequência de boot determinística com delays controlados entre cada componente para garantir dependências de inicialização:

```
Estágio 1 → Boot do Sistema Linux
Estágio 2 → Gerenciador de Interface Gráfica carrega (ambiente minimalista)
Estágio 3 → Scripts de autostart executam
Estágio 4 → Driver Principal inicia (protocolo de comunicação)
Estágio 5 → Updater inicia (após intervalo controlado)
Estágio 6 → Launcher Kiosk inicia (após intervalo controlado)
Estágio 7 → System Lock inicia via serviço do daemon
Estágio 8 → Monitoramento contínuo ativo em todos os componentes
```

---

## 3. Protocolo de Comunicação Proprietário

### 3.1 Descrição

O protocolo de comunicação é um protocolo serial proprietário desenvolvido por Cleyton Pedroza para padronizar a troca de mensagens entre os componentes do sistema e os periféricos de hardware. Opera sobre interface serial física e define comandos para controle de sensores físicos (botões), periféricos de entrada de valores e iluminação.

> **Nota de segurança:** A estrutura de mensagens, identificadores de comandos, endereçamento e parâmetros do protocolo são informações proprietárias e não são divulgados neste documento.

### 3.2 Características Funcionais

O protocolo implementa as seguintes garantias de comunicação:

- **Integridade:** Validação de checksum por mensagem transmitida
- **Confiabilidade:** Timeout de comunicação com prevenção de deadlocks
- **Resiliência:** Reconexão automática em caso de perda de conexão serial
- **Observabilidade:** Monitoramento contínuo de status de todos os componentes ativos
- **Isolamento:** O protocolo opera de forma independente do sistema de bloqueio, garantindo que os periféricos continuem funcionando mesmo quando dispositivos de entrada externos são bloqueados

---

## 4. Driver Principal

### 4.1 Descrição

O Driver Principal é o núcleo do sistema, responsável pela implementação completa do protocolo de comunicação proprietário. Gerencia a comunicação bidirecional com todos os periféricos de hardware conectados via interface serial.

### 4.2 Responsabilidades Funcionais

- Implementação completa do protocolo proprietário de comunicação
- Gerenciamento de sensores físicos (botões de interação)
- Controle de periférico de entrada de valores
- Controle de sistema de iluminação
- Simulação de eventos de entrada para o sistema de jogos
- Health check contínuo de todos os componentes integrados
- Logging de auditoria completo das operações

### 4.3 Mecanismos de Proteção

- Validação de integridade de cada mensagem recebida
- Timeout com recuperação automática em caso de travamento
- Reconexão automática com o periférico serial
- Monitoramento de status de componentes dependentes
- Logs completos para rastreabilidade e auditoria

### 4.4 Build e Distribuição

O Driver Principal é compilado em binário nativo para Linux via compilador Python, garantindo:
- Código-fonte não exposto no ambiente de produção
- Deploy remoto automatizado via servidor de distribuição
- Versionamento com rollback automático para versão anterior em caso de falha
- Verificação de integridade do binário antes da execução

---

## 5. Sistema de Bloqueio Físico (System Lock)

### 5.1 Motivação

Em sistemas Kiosk de uso público, um vetor de ataque comum é a inserção de dispositivos de entrada externos — teclados USB, dongles wireless, adaptadores Bluetooth — para obter acesso ao sistema operacional subjacente. O System Lock foi desenvolvido especificamente para mitigar esse vetor, implementando bloqueio em múltiplas camadas do kernel Linux.

### 5.2 Arquitetura de Bloqueio em 6 Camadas

O sistema implementa seis métodos independentes e complementares de bloqueio, garantindo que mesmo que uma camada seja contornada, as demais continuem ativas:

**Camada 1 — Bloqueio Direto via Sistema de Arquivos (Prioridade Máxima)**

Remoção completa de permissões de acesso ao dispositivo no sistema de arquivos Linux, combinada com desabilitamento via interface sysfs no nível do kernel. Esta é a camada de maior prioridade e menor latência.

**Camada 2 — Bloqueio via Camada Gráfica**

Desabilitamento do dispositivo na camada de servidor gráfico do sistema. Garante que mesmo dispositivos com permissões de sistema não possam enviar eventos para aplicações gráficas.

**Camada 3 — Remoção de Módulos do Kernel**

Descarregamento dos módulos do kernel responsáveis pelo suporte a dispositivos de interface humana. Atua na raiz do suporte ao hardware, impedindo que o kernel processe eventos do dispositivo. Aplicado seletivamente para não afetar periféricos legítimos do sistema.

**Camada 4 — Bloqueio de Interface de Dispositivo (Wireless/Bluetooth)**

Bloqueio específico para dispositivos que comunicam via interface de entrada de baixo nível, cobrindo teclados wireless RF, dongles 2.4GHz e dispositivos Bluetooth. Aplica remoção de permissões nos nós de dispositivo correspondentes.

**Camada 5 — Captura Exclusiva via Chamada de Sistema**

Utilização de chamada de sistema específica para captura exclusiva do dispositivo. Neste modo, apenas o processo que detém o grab recebe os eventos, impedindo que qualquer outra aplicação processe entradas do dispositivo bloqueado.

**Camada 6 — Regras Persistentes de Gerenciamento de Dispositivos**

Criação de regras no sistema de gerenciamento de dispositivos para garantir que o bloqueio persista após reinicializações e seja aplicado automaticamente a qualquer novo dispositivo do mesmo tipo que seja conectado. Esta camada garante a persistência de todas as demais.

### 5.3 Dispositivos Cobertos

| Tipo | Tecnologia | Status |
|---|---|---|
| Teclados USB | Todos os tipos e fabricantes | Bloqueado |
| Teclados PS2 | Portas legadas | Bloqueado |
| Teclados Wireless RF | 2.4GHz, proprietários | Bloqueado |
| Teclados Bluetooth | Todos os profiles | Bloqueado |
| Receptores Universais | Multi-dispositivo | Bloqueado e validado |
| Dispositivos de interface humana genéricos | Interface humana | Bloqueado |

### 5.4 Monitoramento Contínuo e Hotplug

O System Lock implementa um loop de monitoramento com verificação em intervalo de 1 segundo, detectando a inserção de novos dispositivos via análise de timestamps do sistema de arquivos. Ao detectar um novo dispositivo de entrada, todas as 6 camadas de bloqueio são aplicadas imediatamente.

- **Latência máxima de detecção:** 1 segundo
- **Latência de bloqueio após detecção:** imediata (síncrona)
- **Cobertura:** qualquer dispositivo de entrada conectado após o boot

### 5.5 Serviço de Sistema (Daemon)

O System Lock é registrado como serviço do daemon de inicialização do sistema com as seguintes características:

- **Inicialização automática** após carregamento da interface gráfica
- **Restart automático** em caso de falha, com intervalo mínimo entre reinicializações
- **Execução privilegiada** para acesso às interfaces do kernel
- **Dependência** de estar ativo antes que o Launcher Kiosk esteja acessível ao usuário

### 5.6 Compatibilidade com Periféricos Legítimos

O sistema de bloqueio é implementado com lista de exceções para garantir que os periféricos legítimos do sistema — utilizados pelo protocolo de comunicação proprietário — nunca sejam bloqueados. A simulação de eventos de teclado via software (utilizada pelo Driver Principal) é preservada em todas as camadas.

---

## 6. Interface Kiosk (Launcher)

### 6.1 Design da Interface

A interface Kiosk implementa o princípio de mínima exposição ao sistema operacional:

- **Tela preta fullscreen** — sem elementos visuais do sistema operacional
- **Sem barra de tarefas, menus ou botões de sistema**
- **Cursor invisível** — experiência Kiosk pura
- **Sem opção de saída** acessível ao usuário
- **Reinicialização automática** em caso de qualquer falha

### 6.2 Sistemas Integrados

O Launcher integra os seguintes subsistemas:

**Detecção e Gerenciamento de Display**
- Identificação automática de monitores conectados
- Configuração automática de resolução por display
- Suporte a múltiplos monitores
- Fallback para display alternativo em caso de falha

**Gerenciamento de Rede**
- Monitoramento contínuo de conectividade
- Reconexão automática em caso de perda de rede
- Monitoramento de qualidade de conexão
- Proteção contra acessos externos não autorizados

**Monitoramento de Processos**
- Detecção de processos em execução no sistema
- Controle de aplicações via lista de permissões e bloqueios
- Monitoramento de consumo de recursos (CPU, memória)
- Validação de integridade de aplicações autorizadas

**Motor de Análise Preditiva**
- Reconhecimento de padrões de uso do sistema
- Análise preditiva de falhas antes que ocorram
- Otimização automática de performance em tempo de execução
- Análise de comportamento para detecção de anomalias

### 6.3 Proteções da Interface

| Proteção | Mecanismo |
|---|---|
| Fullscreen lock | Não pode ser minimizado ou redimensionado |
| No system access | Sem acesso ao sistema operacional subjacente |
| Process protection | Processo não pode ser encerrado por usuário |
| Auto-restart | Recuperação automática em menos de 3 segundos |
| Input validation | Apenas entradas autorizadas pelo protocolo são processadas |
| Display monitoring | Verificação contínua do estado da tela |

---

## 7. Sistema de Atualização Automática (Updater)

### 7.1 Visão Geral

O Updater é responsável por manter todos os componentes do sistema atualizados de forma silenciosa, sem interromper a operação. Opera em segundo plano e implementa um ciclo completo de atualização segura com verificação de integridade e rollback automático.

### 7.2 Fluxo de Atualização

```
Passo 1 — Verificação de versão
         Comparação entre versão local instalada e versão disponível
         no servidor de distribuição remoto.

Passo 2 — Download seguro
         Transferência da nova versão via canal criptografado
         com verificação de autenticidade.

Passo 3 — Backup da versão atual
         Preservação completa da versão em execução antes
         de qualquer modificação.

Passo 4 — Validação de integridade
         Verificação de checksum criptográfico do artefato
         baixado antes da instalação.

Passo 5 — Instalação silenciosa
         Aplicação da nova versão sem interação do usuário
         e sem interrupção do serviço.

Passo 6 — Teste pós-instalação
         Verificação de funcionamento do componente atualizado.

Passo 7 — Limpeza
         Remoção de arquivos temporários do processo de atualização.

Passo 8 — Rollback automático (se necessário)
         Em caso de falha em qualquer passo, restauração automática
         da versão anterior a partir do backup.
```

### 7.3 Segurança do Processo

- Checksum criptográfico verificado antes e após instalação
- Assinatura digital dos artefatos distribuídos
- Comunicação exclusivamente via canal criptografado
- Permissões de acesso restritas ao processo de atualização
- Registro completo de auditoria de cada atualização realizada
- Janelas de atualização configuradas para períodos de menor atividade

---

## 8. Camadas de Proteção — Visão Consolidada

```
┌──────────────────────────────────────────────────────┐
│              CAMADA 4: OPERACIONAL                   │
│  Monitoramento contínuo · Recuperação automática     │
│  Logs de auditoria · Health check · Alertas          │
├──────────────────────────────────────────────────────┤
│              CAMADA 3: SISTEMA                       │
│  Boot seguro · Atualizações automáticas              │
│  Rollback · Validação de integridade · Daemon        │
├──────────────────────────────────────────────────────┤
│              CAMADA 2: SOFTWARE                      │
│  Tela preta Kiosk · Sem terminal acessível           │
│  Cursor invisível · Restart automático               │
├──────────────────────────────────────────────────────┤
│              CAMADA 1: FÍSICA                        │
│  Bloqueio USB · PS2 · Wireless · Bluetooth           │
│  6 métodos independentes · Detecção hotplug          │
└──────────────────────────────────────────────────────┘
```

### 8.1 Proteções por Categoria

| Categoria | Proteção | Mecanismo |
|---|---|---|
| Física | Bloqueio de teclados USB | 6 camadas independentes no kernel |
| Física | Bloqueio de teclados wireless | Interface de dispositivo + persistência + módulos de kernel |
| Física | Proteção contra hotplug | Monitoramento com latência de 1s |
| Software | Ambiente Kiosk isolado | Sem acesso ao SO subjacente |
| Software | Sem interface de linha de comando | Gerenciador de interface gráfica minimalista |
| Sistema | Boot sem interação manual | Daemon de inicialização automática |
| Sistema | Atualizações sem interrupção | Updater com rollback |
| Operacional | Recuperação de falhas | Restart automático todos os serviços |
| Operacional | Rastreabilidade | Logs de auditoria completos |

---

## 9. O Papel da Inteligência Artificial no Desenvolvimento

A fase v1.0 deste sistema foi concluída em **7 dias por um único desenvolvedor**, com auxílio ativo de ferramentas de IA no processo de desenvolvimento.

### 9.1 Comparativo de Tempo

| Modelo de Desenvolvimento | Equipe | Tempo Estimado |
|---|---|---|
| Tradicional (sem IA) | 3–5 pessoas | 30–60 dias |
| Com IA como parceira | 1 pessoa | 7 dias |

### 9.2 Como a IA foi Utilizada

| Área | Contribuição da IA |
|---|---|
| Implementação de drivers | Estrutura base gerada e validada iterativamente |
| Debug | Identificação e resolução de problemas em tempo real |
| Padronização | Consistência entre os 5 componentes mantida automaticamente |
| Documentação | Geração e organização da documentação técnica |
| Arquitetura | Validação de decisões e sugestão de padrões |
| Testes | Geração de casos de teste e análise de cobertura |

### 9.3 Considerações sobre Engineering Amplification

O uso de IA não substitui o conhecimento técnico — ele amplifica a capacidade de execução. A base técnica sólida pré-existente (protocolo proprietário, arquitetura, criptografia) foi o fator habilitador fundamental. Sem esse conhecimento de domínio profundo, a IA não teria sido capaz de contribuir com a mesma efetividade.

Este caso ilustra o que a literatura recente denomina de *engineering amplification* [2]: quando a IA é usada como parceira de desenvolvimento por engenheiros com conhecimento profundo do domínio, o resultado é uma compressão significativa do ciclo de desenvolvimento sem perda de qualidade técnica.

A profissão não foi substituída — ela foi comprimida e amplificada.

---

## 10. Validação e Status em Produção

### 10.1 Componentes Validados

| Componente | Status | Resultado dos Testes |
|---|---|---|
| Driver Principal | ✅ Produção | Comunicação serial e periféricos validados |
| Updater | ✅ Produção | Boot automático e rollback confirmados |
| Launcher Kiosk | ✅ Produção | Interface fullscreen e auto-restart confirmados |
| System Lock | ✅ Produção | Bloqueio de receptores universais validado em campo |
| Protocolo Proprietário | ✅ Produção | Comunicação bidirecional e checksum confirmados |

### 10.2 Testes de Campo

O sistema encontra-se em fase de **stage/teste em campo** com cliente. Os seguintes cenários foram validados:

- Boot completo do sistema sem interação manual ✅
- Bloqueio de teclado USB após hotplug ✅
- Bloqueio de receptor wireless universal ✅
- Operação do protocolo de comunicação com System Lock ativo ✅
- Atualização remota sem interrupção do serviço ✅
- Recuperação automática após falha simulada ✅
- Operação contínua em janela de 24 horas ✅

---

## 11. Stack Tecnológico

| Categoria | Tecnologia |
|---|---|
| Linguagem | Python 3 |
| Sistema Operacional | Linux |
| Gerenciador de Interface Gráfica | Minimalista |
| Gerenciador de Serviços | Daemon de Serviços do Sistema |
| Comunicação Serial | Interface serial física (protocolo proprietário) |
| Simulação de Eventos | Simulador de Eventos de Entrada |
| Compilação | Compilador de Binários |
| Versionamento | Git |
| Build Automation | Makefile |
| Criptografia/Integridade | Checksum criptográfico (algoritmo não divulgado) |

---

## 12. Conclusão

Este paper apresentou a arquitetura e implementação de um sistema Kiosk com operação autônoma 24/7, proteção multi-camada e automação completa de ciclo de vida. O sistema demonstra que é possível construir infraestrutura de software embarcado robusta e de produção combinando três elementos fundamentais:

1. **Arquitetura bem definida como fundação** — concepção técnica sólida que define protocolos, fluxos e interfaces (contribuição de Cleyton Pedroza)
2. **Implementação focada com conhecimento de domínio** — transformação da arquitetura em produto funcional, testado e em produção (contribuição de Leandro Batista)
3. **IA como acelerador de execução** — compressão do ciclo de desenvolvimento de 30–60 dias para 7 dias, mantendo qualidade técnica

O resultado é um produto funcional, em fase de validação em campo, com 4 camadas de proteção ativas, 6 métodos de bloqueio físico, operação autônoma validada e documentação completa.

**✅ Fase v1.0 concluída em 16/04/2026.**

---

## Referências

[1] KIOSK INDUSTRY ASSOCIATION. *Best Practices for Unattended Kiosk Deployment and Security*. 2023. Disponível em: https://kioskindustry.org

[2] CHEN, M.; TWOREK, J. et al. *Evaluating Large Language Models Trained on Code*. OpenAI, 2021. arXiv:2107.03374.

[3] LINUX KERNEL DOCUMENTATION. *Input Subsystem — Event Interface*. The Linux Kernel Archives. Disponível em: https://www.kernel.org/doc/html/latest/input/input.html

[4] FREEDESKTOP.ORG. *Dynamic Device Management — Linux Kernel Documentation*. 2024. Disponível em: https://www.kernel.org/doc/html/latest/driver-api/usb/index.html

[5] THE LINUX DOCUMENTATION PROJECT. *Gerenciamento de Interface Gráfica em Ambientes Embarcados*. Disponível em: https://tldp.org

[6] PYTHON SOFTWARE FOUNDATION. *Python Deployment and Distribution*. Disponível em: https://docs.python.org/3/distributing/

[7] PARADOXO DE JEVONS. In: POLIMENI, R.; FABIAN, F. *Microeconomics*. McGraw-Hill, 2019. Cap. 4 — Efficiency Paradox and Resource Consumption.

[8] CORBET, J.; RUBINI, A.; KROAH-HARTMAN, G. *Linux Device Drivers*, 3rd ed. O'Reilly Media, 2005.

---

*Sistema Kiosk Protegido e Automatizado*  
*Versão 1.0.0 — Produção*  
*Fase v1.0 concluída em 16/04/2026*  
*Documento público — informações sensíveis de configuração e protocolo omitidas intencionalmente.*
