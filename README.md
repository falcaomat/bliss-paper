<p align="center"><img src="assets/logo.png" width="150"></p>

# 🏞️ Bliss Paper

Um programa pequeno para **Windows e Linux** que troca o seu wallpaper de acordo com o clima da sua região: sol, pôr do sol, nublado, chuva, tempestade, neve ou noite.

O fundo é sempre o clássico "Bliss", só muda a versão conforme o tempo lá fora.

> Projeto amador, feito para aprender Python. Veja a seção [Sobre o projeto](#sobre-o-projeto).

---

## Como funciona

1. O programa descobre a sua localização (pelo IP).
2. Pergunta o clima atual e o horário do pôr do sol para a API gratuita [Open-Meteo](https://open-meteo.com/).
3. Escolhe a imagem que combina com o momento e troca o wallpaper.
4. Espera alguns minutos e repete (só troca o fundo se a imagem mudou).

Ele usa poucos recursos: fica parado esperando quase o tempo todo.

## Imagens

São 10 imagens em **JPG**, e os nomes precisam ser exatamente estes:

| Arquivo | Quando aparece |
|---|---|
| `sol.jpg` | Dia de céu limpo |
| `por-do-sol.jpg` | Até 1 hora antes do pôr do sol, com o céu limpo |
| `nublado.jpg` | Dia nublado |
| `chuva.jpg` | Chuva e pancadas |
| `tempestade.jpg` | Tempestade, de dia ou de noite |
| `noite.jpg` | Noite |
| `noite-chuva.jpg` | Noite com chuva |
| `neve.jpg` | Neve |
| `neve-forte.jpg` | Neve forte |
| `neve-grao.jpg` | Grãos de neve |

As imagens **não estão no repositório** por serem pesadas. Baixe o `.zip` na aba [Releases](../../releases) e extraia a pasta `wallpapers` ao lado do `bliss_paper.py`.

## Como usar

Precisa do **Python 3** instalado. Não é preciso instalar nenhuma biblioteca.

1. Baixe o `bliss_paper.py` e o `.zip` das imagens (aba [Releases](../../releases)).
2. Deixe a pasta `wallpapers` ao lado do script:
   ```
   bliss_paper.py
   wallpapers/
       sol.jpg
       nublado.jpg
       ...
   ```
3. Execute:
   ```
   python3 bliss_paper.py       # fica rodando e atualiza de tempos em tempos
   python3 bliss_paper.py -u    # atualiza uma vez e fecha
   ```
   No Windows, use `python` no lugar de `python3`.

### Rodar em segundo plano

- **Linux:** `nohup python3 bliss_paper.py &`
- **Windows:** renomeie o arquivo para `bliss_paper.pyw` e dê dois cliques. Ele roda sem janela.

### Como fechar o programa

- **Windows:** Gerenciador de Tarefas (`Ctrl+Shift+Esc`) → aba **Detalhes** → `pythonw.exe` → **Finalizar tarefa**.
- **Linux:** `pkill -f bliss_paper.py` no terminal, ou pelo monitor do sistema.

O programa não instala nada e não agenda nada. Para remover, é só apagar os arquivos.

## Configuração

No começo do arquivo `bliss_paper.py`:

| Opção | O que faz |
|---|---|
| `LATITUDE` e `LONGITUDE` | Sua posição. O programa tenta descobrir pelo IP. |
| `INTERVALO_MINUTO` | De quantos em quantos minutos checar o clima (padrão: 15). |
| `MINUTOS_POR_DO_SOL` | Quantos minutos antes do pôr do sol a imagem `por-do-sol` aparece (padrão: 30). |

## Ordem de prioridade

Quando mais de uma condição vale ao mesmo tempo, o programa escolhe nesta ordem:

1. Tempestade
2. Noite (com ou sem chuva)
3. Chuva ou Nublado
4. Pôr do sol
5. Neve
5. Sol

Por isso, em um fim de tarde nublado ou chuvoso, aparece a imagem do clima e não a do pôr do sol.

## Sistemas testados

- Windows
- Linux com GNOME

O código também prevê KDE Plasma, XFCE, Cinnamon, MATE e qualquer ambiente com o programa `feh` instalado, mas **ainda não foram testados**.

## Créditos e avisos

- Dados de clima por [Open-Meteo.com](https://open-meteo.com/) (uso gratuito para fins não comerciais).
- Localização aproximada por IP via [ip-api.com](https://ip-api.com/) (também gratuito para uso não comercial).
- O wallpaper "Bliss" é de autoria da Microsoft. Este projeto **não tem nenhum vínculo** com a Microsoft. As variações de clima foram feitas por mim, com ajuda de IA, para uso pessoal.
- A licença abaixo vale **só para o código**, não para as imagens.

## Sobre o projeto

O Bliss Paper é o meu primeiro projeto publicado.

O código foi escrito com ajuda de IA (Claude), e eu estou modificando cada parte. Sugestões e correções são bem-vindas!

## Limitações conhecidas

- A troca não é instantânea: o programa checa de tempos em tempos, então pode haver um atraso de até `INTERVALO_MINUTO` minutos.
- O pôr do sol só aparece com o céu limpo ou quase limpo.
- Não existe uma imagem própria para neblina nem para tempestade à noite.

## Próximos passos

- [ ] Executáveis para Windows (`.exe`) e Linux
- [ ] Ícone na bandeja do sistema com opção "Sair"
- [ ] Opção de iniciar junto com o computador (ligar e desligar)
- [ ] Imagem própria para neblina e para tempestade à noite
- [ ] Testar em mais ambientes de desktop do Linux
- [ ] AppImage para Linux

## Licença

Código sob a licença [MIT](LICENSE).
