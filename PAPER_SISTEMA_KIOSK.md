# Sistema Kiosk Protegido com Operação Autônoma 24/7: Arquitetura, Proteção Multi-Camada e Aceleração por Inteligência Artificial

**Versão:** 1.0.0 — Produção  
**Data de conclusão da fase v1.0:** 16 de abril de 2026

---

## Autores e Créditos

**Cleyton Pedroza**  
Criador dos componentes fundamentais do sistema. Responsável pela concepção da arquitetura base, desenvolvimento do protocolo de comunicação V18F, criação da infraestrutura de servidores, criptografia e design original dos fluxos de operação. A base técnica sobre a qual todo o sistema foi construído.

**Leandro Batista**  
Responsável pelo aperfeiçoamento, implementação prática e desenvolvimento de hardware. Transformou a base arquitetural em produto funcional em produção — implementando os drivers, o sistema de bloqueio físico multi-camada, a automação de deploy e os processos de recuperação autônoma. A fase v1.0 foi concluída em 7 dias por uma única pessoa, com auxílio de ferramentas de Inteligência Artificial.

---

## Resumo

Este paper descreve a arquitetura, implementação e validação de um sistema completo de Kiosk/Loja virtual desenvolvido para operação autônoma ininterrupta (24/7) sem necessidade de intervenção manual. O sistema integra cinco componentes de software — quatro em produção e um em desenvolvimento — comunicando-se via protocolo proprietário V18F. São implementadas quatro camadas de proteção: física, de software, de sistema e operacional. O ambiente de execução é baseado em Linux com OpenBox, SystemD e binários compilados via PyInstaller/Nuitka. A fase v1.0 foi entregue em 7 dias por um único desenvolvedor, com aceleração significativa proporcionada pelo uso de ferramentas de Inteligência Artificial no processo de desenvolvimento — uma tarefa que, no modelo tradicional com equipe, demandaria entre 30 e 60 dias.

**Palavras-chave:** Kiosk, Protocolo V18F, Bloqueio Físico, Automação, Linux, Python, Inteligência Artificial, Desenvolvimento Acelerado.

---

## 1. Introdução

Sistemas de Kiosk são amplamente utilizados em aplicações comerciais que exigem operação contínua e segura sem supervisão humana direta [1]. O desafio fundamental nesse domínio é garantir que o sistema opere de forma autônoma, resista a tentativas de manipulação física e digital, e se recupere automaticamente de falhas — tudo isso com latência mínima e sem interrupção do serviço.

Este trabalho apresenta a arquitetura e implementação de um sistema Kiosk desenvolvido sobre Linux com interface minimalista (tela preta), protocolo de comunicação serial customizado (V18F), sistema de bloqueio físico de dispositivos de entrada e automação completa de boot, atualizações e recuperação.

O sistema foi concebido com uma base técnica sólida pré-existente — arquitetura, protocolos e criptografia desenvolvidos por Cleyton Pedroza — e implementado em sua totalidade funcional por Leandro Batista em 7 dias, com auxílio de ferramentas de IA. Este resultado representa uma redução de 75–90% no tempo de desenvolvimento estimado pelo modelo tradicional (30–60 dias com equipe), ilustrando o impacto concreto da IA no ciclo de desenvolvimento de software embarcado.

---

## 2. Arquitetura do Sistema

### 2.1 Visão Geral

O sistema é composto por cinco drivers principais organizados em uma arquitetura modular:

| # | Componente | Função | Status |
|---|---|---|---|
| 1 | `driver_principal` | Core do protocolo V18F (botões, sensores, noteiro, lâmpadas) | Produção |
| 2 | `auto_updater` | Sistema de atualização automática com rollback | Produção |
| 3 | `kiosk_launcher` | Interface Kiosk fullscreen | Produção |
| 4 | `system_lock` | Bloqueio físico de dispositivos de entrada | Produção |
| 5 | `game` | Jogos Interativos | Em desenvolvimento |

Todos os componentes se comunicam via protocolo V18F e são gerenciados pelo OpenBox Window Manager com inicialização controlada via SystemD.

### 2.2 Ambiente de Execução

- **Sistema Operacional:** Linux
- **Window Manager:** OpenBox (ambiente minimalista sem acesso ao SO)
- **Gerenciador de Serviços:** SystemD
- **Linguagem:** Python 3
- **Build:** PyInstaller / Nuitka (binários compilados)
- **Versionamento:** Git

### 2.3 Ordem de Inicialização

```
1. Boot do Sistema Linux
2. OpenBox carrega (window manager)
3. autostart OpenBox executa scripts
4. driver_principal inicia (protocolo V18F)
5. auto_updater inicia (5 segundos após boot)
6. kiosk_launcher inicia (7 segundos após boot)
7. system_lock inicia via SystemD service
8. Monitoramento contínuo ativo
```

---

## 3. Protocolo V18F

### 3.1 Descrição

O protocolo V18F é um protocolo serial proprietário desenvolvido por Cleyton Pedroza para padronizar a comunicação entre os componentes do sistema. Opera sobre `/dev/ttyUSB0` e define mensagens para controle de sensores físicos, noteiro de créditos e lâmpadas.

### 3.2 Estrutura de Mensagens

```
# Sensores (botões físicos)
TA / TB / TC — Botões pressionados

# Noteiro (créditos)
V1–V8  — Créditos ativados
E0–E6  — Status do noteiro
#Z*    — Reset do noteiro

# Lâmpadas
L1–L8  — Controle de iluminação

# Sistema
#STATUS — Verificação de componentes
```

### 3.3 Integridade da Comunicação

O protocolo implementa:
- Validação de checksum por mensagem
- Timeout de comunicação com prevenção de deadlocks
- Reconexão automática serial e xdotool
- Monitoramento de status de componentes ativos

---

## 4. Sistema de Bloqueio Físico (system_lock)

### 4.1 Motivação

Em sistemas Kiosk de uso público, um vetor de ataque comum é a inserção de dispositivos de entrada externos (teclados USB, dongles wireless, adaptadores Bluetooth) para obter acesso ao sistema operacional subjacente. O `system_lock` foi desenvolvido especificamente para mitigar esse vetor, implementando bloqueio em múltiplas camadas do kernel Linux.

### 4.2 Arquitetura de Bloqueio em 6 Camadas

**Camada 1 — Bloqueio Direto (Prioridade Máxima)**
```python
subprocess.run(["chmod", "000", keyboard.path])
with open(f"{sysfs_path}/device/enabled", "w") as f:
    f.write("0")
```
Remoção completa de permissões e desabilitamento via sysfs no nível do kernel.

**Camada 2 — Bloqueio xinput (Camada X11)**
```python
subprocess.run(["xinput", "disable", device_id])
subprocess.run(["xinput", "set-prop", device_id, "Device Enabled", "0"])
subprocess.run(["xinput", "set-prop", device_id, "Device Events", ""])
```

**Camada 3 — Remoção de Módulos do Kernel**
```python
modules_to_check = ["hid_dell", "usbhid", "hid_generic", "hid"]
subprocess.run(["rmmod", module])
```

**Camada 4 — Bloqueio HIDRAW (Dispositivos Wireless/Bluetooth)**
```python
subprocess.run(["chmod", "000", hidraw_device])
```

**Camada 5 — EVIOCGRAB (IOCTL Exclusivo)**
```python
fcntl.ioctl(fd, EVIOCGRAB, 1)
```
Captura exclusiva do dispositivo via IOCTL, impedindo que outros processos recebam eventos.

**Camada 6 — Regras UDEV (Persistência)**
```python
subprocess.run(["udevadm", "control", "--reload-rules"])
# KERNEL=="eventX", OPTIONS+="ignore_device"
```
Persistência do bloqueio após reinicialização via regras do sistema.

### 4.3 Dispositivos Cobertos

- Teclados USB (todos os tipos e fabricantes)
- Teclados PS2 (portas legadas)
- Teclados Wireless RF / 2.4GHz / proprietários
- Teclados Bluetooth (todos os profiles)
- Dell Universal Receiver (testado e validado)
- Dispositivos HID genéricos

### 4.4 Monitoramento em Tempo Real

```python
# Verificação a cada 1 segundo
self.stop_event.wait(1.0)

# Detecção por timestamp de modificação
if stat_info.st_mtime > last_check_time:
    log_message("NOVO DISPOSITIVO INSERIDO - BLOQUEANDO IMEDIATAMENTE")
```

Latência máxima de detecção e bloqueio de novos dispositivos: **1 segundo**.

### 4.5 Serviço SystemD

```ini
[Unit]
Description=Braswin Keyboard Lock
After=graphical.target

[Service]
Type=simple
User=root
ExecStart=/home/lucky/lock_braswin
Restart=always
RestartSec=2

[Install]
WantedBy=graphical.target
```

---

## 5. Interface Kiosk (kiosk_launcher)

### 5.1 Design da Interface

A interface Kiosk implementa o princípio de mínima exposição ao sistema operacional:
- Tela preta fullscreen sem elementos visuais do SO
- Sem barra de tarefas, menus ou botões de sistema
- Cursor invisível (via `unclutter`)
- Sem opção de saída pelo usuário
- Reinicialização automática em caso de falha

### 5.2 Sistemas Integrados

O `kiosk_launcher` integra:
- **Detecção de monitor:** Identificação automática de displays, gestão de resolução, suporte multi-monitor
- **Gerenciamento de rede:** Monitoramento contínuo de conectividade, reconexão automática
- **Detecção de processos:** Monitoramento de aplicações ativas, controle por whitelist/blacklist
- **Machine Learning:** Análise preditiva de falhas, reconhecimento de padrões de uso, otimização de performance

### 5.3 Configuração OpenBox

```bash
# ~/.config/openbox/autostart

unclutter -idle 0 -root &
(/home/lucky/braswin/driver/driver_braswin >/dev/null 2>&1 &)
(sleep 5 && /home/lucky/braswin/_updater_braswin >/dev/null 2>&1) &
(sleep 7 && cd /home/lucky/braswin/launcher && ./launcher_braswin >/dev/null 2>&1) &
```

---

## 6. Sistema de Atualização Automática (auto_updater)

### 6.1 Fluxo de Atualização

```
1. Check de versão   → Comparar versão local vs remota
2. Download          → Baixar nova versão via HTTPS/SSL
3. Backup            → Preservar versão atual
4. Validação         → Verificar integridade (MD5/SHA256)
5. Instalação        → Aplicar nova versão silenciosamente
6. Teste             → Verificar funcionamento
7. Limpeza           → Remover arquivos temporários
8. Rollback          → Se falhar, restaurar backup automaticamente
```

### 6.2 Segurança do Processo

- Verificação de checksum MD5/SHA256 em todos os artefatos
- Assinatura digital de arquivos
- Comunicação exclusivamente via HTTPS/SSL
- Permissões restritas de acesso
- Auditoria completa em log

---

## 7. Camadas de Proteção — Visão Consolidada

```
┌─────────────────────────────────────────────┐
│           CAMADA 4: OPERACIONAL             │
│   Monitoramento contínuo · Recuperação      │
│   automática · Logs · Health check          │
├─────────────────────────────────────────────┤
│           CAMADA 3: SISTEMA                 │
│   Boot seguro · Atualizações automáticas    │
│   Rollback · Validação de integridade       │
├─────────────────────────────────────────────┤
│           CAMADA 2: SOFTWARE                │
│   Tela preta Kiosk · Sem terminal           │
│   Cursor invisível · Restart automático     │
├─────────────────────────────────────────────┤
│           CAMADA 1: FÍSICA                  │
│   Bloqueio USB · Wireless · Bluetooth       │
│   6 métodos de bloqueio · Hotplug           │
└─────────────────────────────────────────────┘
```

---

## 8. O Papel da Inteligência Artificial no Desenvolvimento

A fase v1.0 deste sistema foi concluída em **7 dias por um único desenvolvedor**, com auxílio ativo de ferramentas de IA no processo de desenvolvimento.

### 8.1 Comparativo de Tempo

| Modelo | Equipe | Tempo Estimado |
|---|---|---|
| Tradicional | 3–5 pessoas | 30–60 dias |
| Com IA | 1 pessoa | 7 dias |

### 8.2 Como a IA foi Utilizada

- **Geração de drivers:** Estrutura base dos componentes Python gerada e validada com auxílio de IA
- **Debug assistido:** Identificação e resolução de problemas em tempo real
- **Padronização de código:** Consistência entre os 5 drivers mantida automaticamente
- **Documentação:** Geração e organização da documentação técnica
- **Arquitetura:** Validação de decisões arquiteturais e sugestão de padrões

### 8.3 Considerações

O uso de IA não substitui o conhecimento técnico — ele amplifica a capacidade de execução. A base técnica sólida pré-existente (protocolo V18F, arquitetura, criptografia) foi fundamental para que a IA pudesse contribuir de forma efetiva. Sem esse conhecimento de domínio, o resultado não seria possível no mesmo prazo.

Este caso ilustra o que a literatura recente denomina de *engineering amplification* [2]: quando a IA é usada como parceira de desenvolvimento por engenheiros com conhecimento profundo do domínio, o resultado é uma compressão significativa do ciclo de desenvolvimento sem perda de qualidade técnica.

---

## 9. Validação e Testes

### 9.1 Componentes Validados em Produção

| Componente | Status | Testes |
|---|---|---|
| `driver_principal` (V18F) | 100% funcional | Sensores, noteiro, lâmpadas confirmados |
| `auto_updater` | 100% funcional | Boot automático confirmado |
| `kiosk_launcher` | 100% funcional | Interface Kiosk confirmada |
| `system_lock` | 100% funcional | Dell Universal Receiver bloqueado |
| Protocolo V18F | 100% funcional | xdotool e serial confirmados |

### 9.2 Comandos de Verificação Operacional

```bash
# Status do serviço de bloqueio
sudo systemctl status lock-braswin.service

# Monitoramento de logs em tempo real
tail -f /home/lucky/log_keyboard_lock.txt

# Logs do systemd
sudo journalctl -u lock-braswin.service -f

# Verificar processos ativos
ps aux | grep lock_braswin

# Testar comunicação serial (noteiro)
echo "#Z*" > /dev/ttyUSB0

# Testar simulação de teclas
xdotool key "a"
```

---

## 10. Stack Tecnológico

| Categoria | Tecnologia |
|---|---|
| Linguagem | Python 3 |
| Sistema Operacional | Linux |
| Window Manager | OpenBox |
| Gerenciador de Serviços | SystemD |
| Comunicação Serial | `/dev/ttyUSB0` (V18F) |
| Simulação de Teclas | xdotool |
| Compilação | PyInstaller / Nuitka |
| Versionamento | Git |
| Build Automation | Makefile |
| Criptografia/Integridade | MD5 / SHA256 |

---

## 11. Conclusão

Este paper apresentou a arquitetura e implementação de um sistema Kiosk com operação autônoma 24/7, proteção multi-camada e automação completa de ciclo de vida. O sistema demonstra que é possível construir infraestrutura de software embarcado robusta e de produção com:

1. **Arquitetura bem definida** como fundação (contribuição de Cleyton Pedroza)
2. **Implementação focada** com profundo conhecimento do domínio (contribuição de Leandro Batista)
3. **IA como acelerador** de execução — não substituto do engenheiro

O resultado é um produto funcional, em produção, com 4 camadas de proteção ativas, operação validada e documentação completa — entregue em 7 dias por uma única pessoa.

**✅ Fase v1.0 concluída em 16/04/2026.**

---

## Referências

[1] KIOSK INDUSTRY ASSOCIATION. *Best Practices for Unattended Kiosk Deployment and Security*. 2023. Disponível em: https://kioskindustry.org

[2] CHEN, M.; TWOREK, J. et al. *Evaluating Large Language Models Trained on Code*. OpenAI, 2021. arXiv:2107.03374.

[3] LINUX KERNEL DOCUMENTATION. *Input Subsystem — Event Interface*. The Linux Kernel Archives. Disponível em: https://www.kernel.org/doc/html/latest/input/input.html

[4] FREEDESKTOP.ORG. *udev — Dynamic Device Management*. Systemd Documentation, 2024. Disponível em: https://www.freedesktop.org/software/systemd/man/udev.html

[5] OPENBOX PROJECT. *Openbox Window Manager Documentation*. Disponível em: http://openbox.org/wiki/Main_Page

[6] PYINSTALLER DEVELOPMENT TEAM. *PyInstaller Manual*. Disponível em: https://pyinstaller.org/en/stable/

[7] PARADOXO DE JEVONS. In: POLIMENI, R.; FABIAN, F. *Microeconomics*. McGraw-Hill, 2019. Cap. 4 — Efficiency Paradox and Resource Consumption.

---

*Sistema Kiosk Protegido e Automatizado*  
*Versão 1.0.0 — Produção*  
*Fase v1.0 concluída em 16/04/2026*
