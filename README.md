# MKV Tool v1.0.0 by Tokon

Organizador de arquivos MKV em lote para Windows, com interface gráfica tema escuro, utilizando o **MKVToolNix** (`mkvmerge`).

> Projeto independente. Não é um produto oficial do MKVToolNix.

## Funcionalidades

- Análise de vários MKVs e agrupamento por estrutura de trilhas.
- Seleção, reorganização e edição de faixas de áudio e legenda.
- Filtros independentes de idiomas para áudio e legendas.
- Idiomas desmarcados são excluídos **dos arquivos de saída**, não dos originais.
- Remoção opcional de anexos, botões, capítulos e etiquetas.
- Limpeza do título interno do contêiner MKV.
- Escolha da pasta de saída e persistência das configurações.

## Requisitos

- Windows 10/11 (64 bits recomendado).
- [MKVToolNix](https://mkvtoolnix.download/downloads.html) instalado, com `mkvmerge.exe` acessível no caminho padrão ou no `PATH`.
- **Para rodar o código-fonte:** Python 3 com Tkinter (normalmente incluído no instalador oficial do Python para Windows).
- **Para gerar o executável:** Python 3, pip e conexão à internet para instalar PyInstaller.

O programa usa bibliotecas padrão do Python para executar; **PyInstaller só é necessário para compilar**.

## Como executar

1. Instale o MKVToolNix.
2. Instale Python 3 e marque a opção de adicionar o Python ao sistema, se necessário.
3. Extraia o projeto e execute `Iniciar.bat` (ou `py -3 MKVTool.py`).
4. Escolha os MKVs e a pasta de saída; confira a pré-visualização antes de processar.

### Gerar o EXE

Execute `Compilar_EXE.bat` em um computador Windows com Python instalado.
O executável será criado em `dist/MKV Tool v1.0.0 by Tokon.exe`.

O EXE gerado com PyInstaller dispensa Python no computador de destino, **mas ainda exige MKVToolNix instalado**. Não inclui o MKVToolNix.

## Filtros de idioma

Abra **Opções → Idiomas de áudio...** ou **Opções → Idiomas de legendas...**.
Os idiomas selecionados são mantidos; os não selecionados são removidos dos MKVs de saída quando o filtro estiver ativado. Desativar o filtro desativa essa exclusão automática.

**Atenção:** códigos como `pt`, `por` e `pt-BR` podem aparecer separadamente. Confira os idiomas detectados e a pré-visualização. Teste primeiro com cópias de arquivos.

## Configurações

As preferências ficam em `%APPDATA%\MKV Tool\settings.json`, incluindo pasta de saída, filtros e preferências de idiomas.

## Licenças e créditos

O código deste repositório está sob a [licença MIT](LICENSE), conforme a licença escolhida para este projeto. O **MKVToolNix** é software de terceiros e tem licenças próprias; não está incluído neste repositório. Consulte o [site oficial](https://mkvtoolnix.download/) antes de redistribuir seus binários.

## Menu Sobre

O menu **Sobre** exibe **Desenvolvido por Tokon** e **Versão v1.0.0**.

## Janela Sobre

A janela **Sobre** utiliza o tema escuro e exibe o desenvolvedor Tokon, versão v1.0.0 e plataforma Windows.

## Memorização de faixas

Alterações de ordem, idioma, nome, padrão, forçada e exclusão de faixas **não são salvas entre execuções**. Ao abrir novamente e analisar arquivos, o aplicativo lê as faixas originais. A pasta de saída e as preferências dos filtros de idiomas continuam salvas.

## Idiomas ISO 639-1

Os menus de áudio e legenda apresentam todos os códigos ISO 639-1 de duas letras (por exemplo, `pt`, `en`, `es`). O filtro compara pelo idioma geral: selecionar `pt` mantém `pt`, `por`, `pt-BR` e `pt-PT`; selecionar `en` mantém `en`, `eng`, `en-US` etc. **O programa não altera automaticamente o código da faixa no arquivo gerado**: se a faixa já tiver `pt-BR`, ela continua `pt-BR`. Idiomas sem equivalente de duas letras, como `und`, aparecem quando encontrados no arquivo. As seleções dos filtros continuam memorizadas.

## Novidades: nomes automáticos, aviso e cores

Em **Opções → Nomes automáticos de áudio...** ou **Nomes automáticos de legendas...**, cadastre até **10 nomes em cada categoria**. Na janela **Editar faixa**, ao digitar o começo do nome, aparece uma lista de sugestões; clique na sugestão ou pressione **Tab** para aceitar a primeira. Os nomes cadastrados são salvos entre sessões; as alterações feitas nas faixas continuam temporárias.

Quando o lote termina, o Windows emite um som de aviso (dependendo da configuração de áudio do sistema). Na tabela, faixas desmarcadas ficam **vermelhas**; faixas incluídas e marcadas como **Padrão** ficam **verdes**. A cor vermelha tem prioridade sobre a verde.

## Organizar automaticamente

O botão **Organizar automaticamente**, ao lado de **Editar faixa**, abre uma janela de opções e aplica a organização a todos os grupos analisados:

- Vídeo primeiro.
- Áudio português antes do inglês, mantendo os demais depois.
- Legenda portuguesa em primeiro lugar, marcada como padrão e forçada. Se já houver uma legenda portuguesa forçada, ela tem prioridade.
- Opção **Alterar idiomas portugueses para pt-BR (áudio e legenda)**. Quando ativada, converte a identificação `pt`, `por`, `pt-PT` e outras variantes para `pt-BR`, sem converter áudio ou texto. Essa preferência é memorizada.
- As alterações manuais e a organização aplicada **não** são memorizadas entre execuções. Confira a pré-visualização antes de processar.

**Importante:** marcar uma legenda completa como forçada não a transforma em uma legenda apenas de trechos forçados. O filtro de idiomas continua independente e pode remover faixas da saída.

Na organização automática, faixas de **áudio** identificadas como `en-US` (inclusive diferenças de maiúsculas/minúsculas) passam a `en`. Legendas `en-US` não são modificadas por essa regra. A conversão é aplicada aos arquivos de saída, não aos originais.

Na organização automática, áudio e legendas identificados como `en-US` passam para `en`.

### Exibição de idiomas
Na tabela da interface, `en-US` e `eng` são exibidos como `en` para áudio e legendas. O idioma original é preservado nos metadados e no editor de faixas. A organização automática não converte inglês.

- Organização automática: opção marcada por padrão para converter `en-US` em `en` em áudio e legendas. `eng` permanece sem alteração nos metadados, mas é exibido como `en` na interface.
