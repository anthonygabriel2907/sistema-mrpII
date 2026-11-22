# MRP II - Pedal Forte Bicicletas

Trabalho 2 da disciplina de Programação em Python (CEFET-MG Divinópolis,
Engenharia de Computação). Sistema em modo texto que faz o planejamento da
produção (MPS, MRP, CRP, custo padrão) e a gestão de estoques de uma fábrica
fictícia de bicicletas.

**Autor:** Anthony Gabriel Sotto Mayor Silva

## Requisitos

- Python 3.10 ou superior
- matplotlib (só para os gráficos)
- Testado em Linux (WSL)

```
pip install -r requirements.txt
```

## Como executar

Dentro da pasta `MRP2_PedalForte`:

```
python3 main.py
```

Ao iniciar, o sistema carrega sozinho os arquivos da pasta `data/` (já vem com
a base de demonstração). Tudo o que for alterado é gravado de novo nos
arquivos automaticamente.

Os CSVs exportados e os gráficos (PNG) são salvos na pasta `saida/`, que é
criada na primeira vez que for preciso.

## Estrutura de pastas

```
MRP2_PedalForte/
    main.py          ponto de entrada
    menu.py          menus e navegação
    itens.py         cadastro de itens
    estrutura.py     BOM e árvore indentada
    estoque.py       movimentações, saldo e kardex
    mps.py           plano mestre de produção
    mrp.py           cálculo MRP
    ordens.py        OPs, OCs e apontamento
    capacidade.py    centros, roteiros e CRP
    custos.py        custo padrão
    relatorios.py    exportação CSV
    graficos.py      gráficos de gestão (matplotlib)
    persistencia.py  leitura/gravação de arquivos
    utils.py         validações e formatação
    data/            arquivos JSON/CSV
    saida/           CSVs exportados e gráficos PNG
    docs/README.md
```

Arquivos da pasta `data/`: `itens.json`, `estrutura.json`, `estoque.json`,
`movimentos.csv`, `centros.json`, `roteiros.json`, `mps.json`, `ordens.json`
e também `mrp.json` (guarda o resultado da última execução do MRP, para
poder consultar o registro de um item sem rodar o MRP de novo).

## Requisitos funcionais

| RF | Onde está | Como usar no menu |
|----|-----------|-------------------|
| RF01 | `menu.py` | menu principal |
| RF02 | `itens.py` | 1 - Cadastros > 1, 2 e 3 |
| RF03 | `estrutura.py` | 1 - Cadastros > 4, 5 e 6 |
| RF04 | `estoque.py` | 2 - Estoque > 1 |
| RF05 | `estoque.py` | 2 - Estoque > 2 e 3 (alerta de estoque de segurança) |
| RF06 | `capacidade.py` | 1 - Cadastros > 7, 8, 9 e 10 |
| RF07 | `mps.py` | 3 - MPS |
| RF08 | `mrp.py` | 4 - Executar MRP > 1 (executar) e 2 (registro de um item) |
| RF09 | `mrp.py` e `ordens.py` | gerado na execução do MRP, listado no menu 5 |
| RF10 | `ordens.py` | 5 - Ordens > F, L e E |
| RF11 | `ordens.py` | 5 - Ordens > A |
| RF12 | `capacidade.py` | 6 - Carga x capacidade |
| RF13 | `custos.py` | 7 - Custo padrão |
| RF14 | `relatorios.py` | 8 - Relatórios |
| RF15 | `persistencia.py` | automático |
| RF16 | `graficos.py` | 9 - Gráficos de gestão |

## Regras de negócio

| RN | Onde foi feita |
|----|----------------|
| RN01 | `utils.codigo_valido` e `itens.cadastrar_item` |
| RN02 | `estoque.erro_de_saldo` (usada em toda movimentação) |
| RN03 | `estrutura.pode_ser_componente` |
| RN04 | `mrp.executar_mrp` (PA, depois SA, depois MP) e `mrp.calcular_necessidade_bruta` |
| RN05, RN06, RN07 | `mrp.calcular_item` |
| RN08 | `mrp.executar_mrp` (apaga as planejadas) e `mrp.calcular_recebimentos` |
| RN09 | `capacidade.calcular_carga` |
| RN10 | `estoque.registrar_movimento` (só acrescenta no kardex; não existe exclusão) |

## Decisões de projeto

- **Dados em memória:** ao iniciar, tudo é lido para um dicionário `dados`
  (itens, estrutura, estoque, movimentos, centros, roteiros, mps, ordens, mrp)
  que é passado para as funções de cada módulo. Depois de cada alteração,
  `persistencia.salvar_tudo` regrava os arquivos.
- **Tipo do item:** vem do prefixo do código (PA, SA ou MP), por causa da RN01.
  O código precisa ter 3 dígitos (PA-001), para não haver PA-1 e PA-001.
- **Custo do item:** só a matéria-prima tem custo unitário digitado. O custo
  dos itens fabricados é calculado pela estrutura (custo padrão, RF13).
- **Recursividade:** usada na árvore da BOM (`estrutura.mostrar_arvore`) e no
  custo padrão (`custos.custo_unitario`).
- **Semanas:** o horizonte é de 8 semanas e a semana 1 é a semana atual.
  Ordem com liberação antes da semana 1 é marcada como ATRASADA (aparece como
  S0, S-1...) e gera mensagem de exceção.
- **Necessidade bruta de componentes:** soma das ordens abertas (planejadas,
  firmes e liberadas) dos itens pais na semana de liberação, vezes a
  quantidade por unidade. Uma ordem atrasada consome o componente já na
  semana 1.
- **Carga do centro (RN09):** conta todas as OPs que não foram encerradas,
  na semana de liberação (as atrasadas contam na semana 1). Foi assim para o
  CRP mostrar a sobrecarga antes de liberar as ordens, como no exemplo do
  enunciado.
- **Status das ordens:** PLANEJADA (ou ATRASADA) -> FIRME -> LIBERADA ->
  ENCERRADA. Uma OP é encerrada pelo apontamento de produção (a opção "A" e
  a opção "E" fazem a mesma coisa para OP). Uma OC encerrada significa que o
  material chegou, então entra no estoque com o documento da OC.
- **Apontamento:** confere se todos os componentes têm saldo antes de baixar
  qualquer coisa. Se faltar algum, rejeita e mostra o que falta.
- **Numeração das ordens:** OP e OC têm contadores separados, que continuam
  crescendo mesmo quando as planejadas são apagadas pelo MRP.
- **CSV exportado:** separador `;` e vírgula decimal, para abrir direto no
  Excel em português.
- **Gráfico de ordens:** conta o número de ordens por semana de entrega, já
  que OP e OC têm unidades diferentes.
- Foi adicionada a opção 9 (Gráficos) no menu principal, além das do mockup.

## Base de demonstração

- 2 produtos acabados: PA-001 (Bicicleta Aro 29 MTB) e PA-002 (Bicicleta
  Aro 29 Urbana)
- 2 semiacabados: SA-010 (Quadro) e SA-020 (Roda)
- 8 matérias-primas: MP-100, MP-101, MP-200, MP-201, MP-202, MP-300, MP-301
  e MP-302
- 3 centros de trabalho: CT-01 (Soldagem), CT-02 (Montagem de rodas) e
  CT-03 (Montagem final, 16 h/semana)
- MPS de 8 semanas para os dois PA
- O custo padrão do PA-001 dá R$ 792,60, igual ao exemplo do enunciado.
- O pneu MP-202 começa abaixo do estoque de segurança (saldo 18, segurança
  20), para mostrar o alerta do kardex.

## Roteiro para testar o ciclo completo

1. Menu **3**: conferir o MPS (opção 1).
2. Menu **4 > 1**: executar o MRP. Aparecem as ordens planejadas e as
   mensagens de exceção. Em **4 > 2** ver o registro de um item (ex.: SA-020).
3. Menu **5**: firmar (F) e liberar (L) uma ordem, por exemplo `OP-0001`.
4. Ainda no menu 5: apontar a produção (A). A OP é encerrada, os componentes
   saem do estoque e o item produzido entra.
5. Tentar apontar uma OP de SA-020 sem pneu suficiente: o sistema rejeita e
   mostra o componente que falta. Depois firmar, liberar e encerrar a OC do
   MP-202 (entra no estoque) e apontar de novo.
6. Menu **2 > 3**: kardex do item para ver as movimentações.
7. Menu **6**: carga x capacidade (CT-03 mostra semanas com sobrecarga).
8. Menu **7**: custo padrão. Menu **8**: exportar CSV. Menu **9**: gráficos.

## Observações

- Os dados da demonstração podem ser restaurados copiando de novo a pasta
  `data/` original do repositório (`git checkout -- data`).
- O MRP deve ser executado de novo sempre que o MPS, o estoque ou as ordens
  forem alterados.
