# Testar o Mirror Frame no Windows Sandbox

## Pré-requisitos (host)
- Windows 10/11 **Pro/Enterprise** com *Windows Sandbox* habilitado
  (Recursos do Windows → "Área restrita do Windows").
- Este repositório em `C:\VSCode\mirror-exe` com o app já empacotado em
  `frame\out\MirrorFrame-win32-x64\` (gerado pela Fatia de empacotamento).

## Como rodar
Duplo clique em **`mirror-frame-test.wsb`**. O sandbox abre, copia tudo para
dentro dele (o repo do host entra somente-leitura — nada escreve na sua máquina)
e lança o Mirror Frame sozinho.

## Roteiro de teste (o que esperar)
1. **App abre limpo** numa máquina 100% vazia — janela "Mirror Mind".
   Como `uv`/`pi`/`git` não existem no sandbox, o app cai no aviso e aponta o Setup.
2. **⚙ Setup** — luzes vermelhas em uv/Pi/Git. Clique **"Instalar pré-requisitos"**:
   abre uma aba de terminal real rodando o `installer/bootstrap.ps1` oficial
   (sem winget no sandbox, ele usa os downloads diretos — ~5–10 min de rede).
3. **Feche o app** e reabra pelo atalho **"Mirror Frame"** criado na área de
   trabalho (ele relê o PATH novo do registro).
4. **Wizard de 1º acesso** — informe um nome (ex.: `Teste`) e, se quiser testar a
   memória de verdade, uma chave OpenRouter real. O app roda `memory init` +
   `seed` reais e o **warm-up** (que aplica migrations e libera as sessões).
5. **Abrir sessão ◇** — o Pi abre num terminal real dentro da aba. Para conversar
   é preciso `/login` (assinatura) — lembre que o sandbox é efêmero: a credencial
   morre quando ele fecha.
6. Teste os painéis: **◇ Personas** (identity list + detect-persona reais) e o
   bloqueio do **update com sessão aberta** (regra R2) no Setup.

## Limites conhecidos deste teste
- Sandbox é descartável: tudo (logins, banco, instalações) evapora ao fechar.
- O bootstrap baixa ~200–400 MB (Git, Node, uv, Pi) a cada rodada de sandbox.
- Sem assinatura conectada o Pi abre mas não conversa — o teste de UX do frame
  (janela, abas, gates, wizard, painéis) funciona mesmo assim.
