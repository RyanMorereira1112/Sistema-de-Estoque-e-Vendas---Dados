# 🗃️ Sistema de Estoque e Vendas

Sistema de linha de comando em Python para controle de produtos, vendas e relatórios, desenvolvido como Projeto 1 da disciplina (Seções 2 a 5).

---

## 📋 Sumário

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Como Executar](#como-executar)
- [Exemplos de Uso](#exemplos-de-uso)
- [Estrutura de Dados](#estrutura-de-dados)
- [Complexidade dos Algoritmos](#complexidade-dos-algoritmos)
- [Regras de Negócio](#regras-de-negócio)
- [Relatório de Escolhas Técnicas](#relatório-de-escolhas-técnicas)
- [Boas Práticas Aplicadas](#boas-práticas-aplicadas)

---

## Sobre o Projeto

Este sistema permite o gerenciamento completo de um estoque de produtos via terminal. O projeto aplica conceitos de estruturas de dados (vetores ordenados e não ordenados), algoritmos de busca (linear e binária) e persistência de dados em arquivo JSON.

---

## Funcionalidades

### Gestão de Produtos
- ✅ Cadastrar produto com código único, nome, categoria, preço e quantidade
- ✅ Editar produto (nome, preço, quantidade, categoria)
- ✅ Remover produto pelo código

### Busca
- ✅ Buscar produto por código — **busca binária** em vetor ordenado
- ✅ Buscar produtos por nome — **busca linear** em vetor não ordenado

### Vendas e Estoque
- ✅ Registrar venda com validação de estoque disponível
- ✅ Listar produtos ordenados por código
- ✅ Listar produtos por categoria

### Relatórios
- ✅ Relatório de estoque baixo (limite configurável)
- ✅ Logs de operações com data e hora

### Persistência
- ✅ Salvar e carregar dados em arquivo JSON (`dados.json`)

---

## Estrutura do Projeto

```
FWDA/
├── main.py          # Menu principal e fluxo de controle
├── produto.py       # Classe Produto e validações
├── estoque.py       # Operações de cadastro, busca e ordenação
├── vendas.py        # Registro de vendas e atualização de estoque
├── arquivos.py      # Leitura e escrita de dados em JSON
├── logs.py          # Registro de logs com timestamp
├── dados.json       # Arquivo de persistência dos dados
└── README.md        # Este arquivo
```

### Descrição dos Módulos

| Arquivo | Responsabilidade |
|---|---|
| `main.py` | Exibe o menu, captura entradas e direciona as operações |
| `produto.py` | Define a estrutura do produto e valida os dados de entrada |
| `estoque.py` | Mantém o vetor ordenado e o não ordenado; implementa buscas |
| `vendas.py` | Valida e registra vendas, atualiza quantidade em estoque |
| `arquivos.py` | Serializa/deserializa os dados para JSON |
| `logs.py` | Grava logs de cada operação com data e hora |

---

## Pré-requisitos

- Python 3.8 ou superior
- Nenhuma biblioteca externa necessária (somente biblioteca padrão)

Para verificar sua versão do Python:

```bash
python --version
```

---

## Como Executar

1. **Clone o repositório:**

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

2. **Execute o sistema:**

```bash
python main.py
```

O menu será exibido automaticamente no terminal. Na primeira execução, o arquivo `dados.json` será criado automaticamente caso não exista.

---

## Exemplos de Uso

### Menu Principal

```
========================================
     SISTEMA DE ESTOQUE E VENDAS
========================================
 1. Cadastrar produto
 2. Editar produto
 3. Remover produto
 4. Buscar por código
 5. Buscar por nome
 6. Registrar venda
 7. Listar todos os produtos
 8. Listar por categoria
 9. Relatório de estoque baixo
 0. Sair
========================================
Escolha uma opção:
```

### Cadastrar um Produto

```
Código    : 101
Nome      : Caneta Azul
Categoria : Papelaria
Preço     : 2.50
Quantidade: 100

✅ Produto cadastrado com sucesso!
```

### Buscar por Código (Busca Binária)

```
Informe o código: 101

Código    : 101
Nome      : Caneta Azul
Categoria : Papelaria
Preço     : R$ 2.50
Quantidade: 100
```

### Registrar Venda

```
Código do produto : 101
Quantidade vendida: 10

✅ Venda registrada! Estoque atualizado: 90 unidades.
```

### Relatório de Estoque Baixo

```
Limite mínimo: 20

⚠️  PRODUTOS COM ESTOQUE BAIXO:
--------------------------------------
Código | Nome          | Qtd | Categoria
101    | Caneta Azul   |  15 | Papelaria
205    | Borracha      |   8 | Papelaria
--------------------------------------
```

### Exemplo de `dados.json`

```json
{
  "produtos": [
    {
      "codigo": 101,
      "nome": "Caneta Azul",
      "categoria": "Papelaria",
      "preco": 2.50,
      "quantidade": 90
    },
    {
      "codigo": 205,
      "nome": "Borracha",
      "categoria": "Papelaria",
      "preco": 1.20,
      "quantidade": 8
    }
  ]
}
```

---

## Estrutura de Dados

O sistema utiliza duas estruturas de vetor simultâneas:

### Vetor Não Ordenado
- Armazena os produtos na ordem de inserção.
- Usado para buscas por nome (busca linear).
- Reflete a ordem natural de cadastro.

### Vetor Ordenado (por código)
- Mantido sempre ordenado após cada inserção ou remoção.
- Usado para buscas por código (busca binária).
- A inserção é feita na posição correta para preservar a ordem (inserção ordenada).

---

## Complexidade dos Algoritmos

| Operação | Algoritmo | Complexidade | Justificativa |
|---|---|---|---|
| Busca por código | Busca binária | O(log n) | O vetor é mantido ordenado por código, permitindo divisão pela metade a cada passo |
| Busca por nome | Busca linear | O(n) | Nome não é chave de ordenação; todos os registros podem ser consultados |
| Inserção ordenada | Deslocamento | O(n) | É necessário abrir espaço no vetor ordenado na posição correta |
| Remoção | Deslocamento | O(n) | Após remover, o vetor é compactado para manter a ordem |
| Listagem geral | Iteração | O(n) | Percorre todos os elementos do vetor ordenado |

### Por que busca binária para código?

O código do produto é um identificador único e o vetor é mantido sempre ordenado por ele. A busca binária aproveita essa propriedade para encontrar qualquer produto em O(log n) comparações — para mil produtos, são no máximo 10 comparações, contra 1000 na busca linear.

### Por que busca linear para nome?

O nome não é chave de ordenação, logo não há garantia de ordem que possa ser explorada. A busca linear é necessária e adequada para esse caso, percorrendo o vetor não ordenado.

---

## Regras de Negócio

- Código de produto deve ser único (não permite duplicatas).
- Venda só é registrada se houver estoque suficiente.
- Preço deve ser um valor positivo (> 0).
- Quantidade não pode ser negativa.
- O vetor ordenado é sempre mantido em ordem crescente de código após inserções e remoções.

---

## Relatório de Escolhas Técnicas

### Por que JSON e não CSV?

O JSON foi escolhido por representar nativamente os dados como objetos Python (dicionários e listas), facilitando a leitura e escrita com a biblioteca padrão (`json`). Além disso, JSON é mais legível e extensível que CSV para estruturas com múltiplos campos.

### Por que dois vetores?

Manter dois vetores (um ordenado e um não ordenado) é uma troca deliberada de espaço por desempenho: o custo extra de memória (duplicação dos dados) é compensado pela possibilidade de aplicar busca binária no vetor ordenado sem comprometer a ordem de inserção para buscas por nome.

### Por que inserção ordenada e não ordenação a cada operação?

Ordenar o vetor a cada inserção seria O(n log n). Inserir na posição correta é O(n) (deslocamento), o que é mais eficiente quando inserções são frequentes.

---

## Boas Práticas Aplicadas

- Código organizado em módulos com responsabilidades únicas (Single Responsibility)
- Funções pequenas e bem nomeadas
- Tratamento de erros de entrada (tipo, vazio, intervalo)
- Nomes de variáveis e funções em português seguindo o contexto do projeto
- Indentação e estilo seguindo PEP 8
- Commits pequenos com mensagens claras no Git
- Logs de operações com timestamp para rastreabilidade

---

## Autor

Desenvolvido como parte do Projeto 1 — Seções 2 a 5.
