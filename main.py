

import os
from produto import Produto
from estoque import Estoque
from vendas import GerenciadorVendas
import arquivos
import logs

LIMITE_ESTOQUE_BAIXO_PADRAO = 5
ITENS_POR_PAGINA = 10



def limpar_tela() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def pausar() -> None:
    input("\n  Pressione Enter para continuar...")


def linha(char: str = "─", tamanho: int = 50) -> None:
    print(f"  {char * tamanho}")


def cabecalho(titulo: str) -> None:
    limpar_tela()
    linha("═")
    print(f"  {'SISTEMA DE ESTOQUE E VENDAS':^50}")
    linha("═")
    print(f"  {titulo}")
    linha()


def ler_texto(prompt: str, obrigatorio: bool = True) -> str:
    while True:
        valor = input(f"  {prompt}: ").strip()
        if valor or not obrigatorio:
            return valor
        print("  ⚠ Campo obrigatório. Tente novamente.")


def ler_float(prompt: str) -> float:
    while True:
        try:
            return float(input(f"  {prompt}: ").replace(",", "."))
        except ValueError:
            print("  ⚠ Digite um número válido (ex: 12.50).")


def ler_inteiro(prompt: str, minimo: int = 0) -> int:
    while True:
        try:
            valor = int(input(f"  {prompt}: "))
            if valor < minimo:
                print(f"  ⚠ O valor mínimo é {minimo}.")
            else:
                return valor
        except ValueError:
            print("  ⚠ Digite um número inteiro válido.")


def paginar(lista: list, titulo: str) -> None:
    """Exibe uma lista com paginação simples."""
    if not lista:
        print("  Nenhum produto encontrado.")
        return

    total = len(lista)
    pagina = 0
    total_paginas = (total + ITENS_POR_PAGINA - 1) // ITENS_POR_PAGINA

    while True:
        inicio = pagina * ITENS_POR_PAGINA
        fim = min(inicio + ITENS_POR_PAGINA, total)

        print(f"\n  {titulo} — página {pagina + 1}/{total_paginas} ({total} produto(s))")
        linha()
        for produto in lista[inicio:fim]:
            print(f"  {produto}")
        linha()

        if total_paginas == 1:
            break

        opcoes = []
        if pagina > 0:
            opcoes.append("[A] Anterior")
        if pagina < total_paginas - 1:
            opcoes.append("[P] Próxima")
        opcoes.append("[S] Sair da listagem")

        print("  " + "  ".join(opcoes))
        nav = input("  Opção: ").strip().upper()
        if nav == "P" and pagina < total_paginas - 1:
            pagina += 1
        elif nav == "A" and pagina > 0:
            pagina -= 1
        elif nav == "S":
            break



def cadastrar_produto(estoque: Estoque) -> None:
    cabecalho("Cadastrar produto")
    try:
        codigo = ler_texto("Código do produto")
        nome = ler_texto("Nome")
        categoria = ler_texto("Categoria")
        preco = ler_float("Preço (R$)")
        quantidade = ler_inteiro("Quantidade em estoque", minimo=0)

        produto = Produto(codigo, nome, categoria, preco, quantidade)
        estoque.cadastrar(produto)
        arquivos.salvar(estoque)
        logs.registrar(f"Produto cadastrado: {produto.codigo} - {produto.nome}")
        print(f"\n  ✓ Produto '{nome}' cadastrado com sucesso!")
    except ValueError as e:
        print(f"\n  ✗ Erro: {e}")
    pausar()


def editar_produto(estoque: Estoque) -> None:
    cabecalho("Editar produto")
    codigo = ler_texto("Código do produto a editar")
    try:
        produto = estoque.buscar_por_codigo(codigo)
        print(f"\n  Produto atual: {produto}")
        print("  (Deixe em branco para manter o valor atual)\n")

        nome = input(f"  Novo nome [{produto.nome}]: ").strip() or None
        categoria = input(f"  Nova categoria [{produto.categoria}]: ").strip() or None

        preco_str = input(f"  Novo preço [{produto.preco:.2f}]: ").strip().replace(",", ".")
        preco = float(preco_str) if preco_str else None

        qtd_str = input(f"  Nova quantidade [{produto.quantidade}]: ").strip()
        quantidade = int(qtd_str) if qtd_str else None

        estoque.editar(codigo, nome=nome, categoria=categoria,
                       preco=preco, quantidade=quantidade)
        arquivos.salvar(estoque)
        logs.registrar(f"Produto editado: {codigo}")
        print("\n  ✓ Produto atualizado com sucesso!")
    except ValueError as e:
        print(f"\n  ✗ Erro: {e}")
    pausar()


def remover_produto(estoque: Estoque) -> None:
    cabecalho("Remover produto")
    codigo = ler_texto("Código do produto a remover")
    try:
        produto = estoque.buscar_por_codigo(codigo)
        print(f"\n  Produto encontrado: {produto}")
        confirmar = input("  Confirmar remoção? (s/N): ").strip().lower()
        if confirmar == "s":
            estoque.remover(codigo)
            arquivos.salvar(estoque)
            logs.registrar(f"Produto removido: {codigo} - {produto.nome}")
            print("  ✓ Produto removido com sucesso!")
        else:
            print("  Operação cancelada.")
    except ValueError as e:
        print(f"\n  ✗ Erro: {e}")
    pausar()


def buscar_por_codigo(estoque: Estoque) -> None:
    cabecalho("Buscar por código (busca binária)")
    codigo = ler_texto("Código do produto")
    try:
        produto = estoque.buscar_por_codigo(codigo)
        print(f"\n  Produto encontrado:\n  {produto}")
    except ValueError as e:
        print(f"\n  ✗ {e}")
    pausar()


def buscar_por_nome(estoque: Estoque) -> None:
    cabecalho("Buscar por nome (busca linear)")
    termo = ler_texto("Digite parte do nome")
    resultados = estoque.buscar_por_nome(termo)
    print()
    paginar(resultados, f"Resultados para '{termo}'")
    pausar()


def registrar_venda(estoque: Estoque, gerenciador: GerenciadorVendas) -> None:
    cabecalho("Registrar venda")
    codigo = ler_texto("Código do produto")
    try:
        produto = estoque.buscar_por_codigo(codigo)
        print(f"\n  Produto: {produto}")
        quantidade = ler_inteiro("Quantidade a vender", minimo=1)

        venda = gerenciador.registrar(estoque, codigo, quantidade)
        arquivos.salvar(estoque)
        logs.registrar(f"Venda registrada: {venda.quantidade}x {codigo}")
        print(f"\n  ✓ Venda registrada!\n  {venda}")
    except ValueError as e:
        print(f"\n  ✗ Erro: {e}")
    pausar()


def listar_por_codigo(estoque: Estoque) -> None:
    cabecalho("Listar produtos por código")
    print()
    paginar(estoque.listar_ordenado(), "Produtos ordenados por código")
    pausar()


def listar_por_categoria(estoque: Estoque) -> None:
    cabecalho("Listar por categoria")
    categorias = estoque.listar_categorias()
    if not categorias:
        print("  Nenhuma categoria cadastrada.")
        pausar()
        return

    print("  Categorias disponíveis:")
    for i, cat in enumerate(categorias, 1):
        print(f"    {i}. {cat}")
    print()

    categoria = ler_texto("Digite a categoria desejada")
    resultados = estoque.listar_por_categoria(categoria)
    print()
    paginar(resultados, f"Categoria: {categoria}")
    pausar()


def relatorio_estoque_baixo(estoque: Estoque, limite: list) -> None:
    cabecalho("Relatório de estoque baixo")
    print(f"  Limite atual: {limite[0]} unidades")
    alterar = input("  Deseja alterar o limite? (s/N): ").strip().lower()
    if alterar == "s":
        limite[0] = ler_inteiro("Novo limite", minimo=1)

    resultados = estoque.listar_estoque_baixo(limite[0])
    print()
    if resultados:
        print(f"  ⚠ {len(resultados)} produto(s) com estoque abaixo de {limite[0]}:\n")
        for p in resultados:
            print(f"  {p}")
    else:
        print("  ✓ Nenhum produto com estoque baixo.")
    pausar()


def historico_vendas(gerenciador: GerenciadorVendas) -> None:
    cabecalho("Histórico de vendas da sessão")
    vendas = gerenciador.historico()
    if not vendas:
        print("  Nenhuma venda registrada nesta sessão.")
    else:
        for venda in vendas:
            print(f"  {venda}")
        linha()
        print(f"  Total em vendas: R$ {gerenciador.total_vendas():.2f}")
    pausar()


def exibir_logs() -> None:
    cabecalho("Log de operações da sessão")
    logs.exibir()
    pausar()


# ── Menu principal ────────────────────────────────────────────────────────────

MENU = """
  PRODUTOS
  [1] Cadastrar produto
  [2] Editar produto
  [3] Remover produto
  [4] Buscar por código    (busca binária)
  [5] Buscar por nome      (busca linear)

  VENDAS
  [6] Registrar venda
  [7] Histórico de vendas

  RELATÓRIOS
  [8] Listar todos por código
  [9] Listar por categoria
  [10] Relatório de estoque baixo

  SISTEMA
  [11] Ver logs da sessão
  [0]  Sair
"""


def main() -> None:
    estoque = Estoque()
    gerenciador = GerenciadorVendas()
    limite_baixo = [LIMITE_ESTOQUE_BAIXO_PADRAO]

    # Carrega dados salvos
    try:
        total = arquivos.carregar(estoque)
        if total:
            logs.registrar(f"Sistema iniciado — {total} produto(s) carregado(s).")
    except RuntimeError as e:
        print(f"\n  ⚠ Aviso ao carregar dados: {e}\n")

    acoes = {
        "1": lambda: cadastrar_produto(estoque),
        "2": lambda: editar_produto(estoque),
        "3": lambda: remover_produto(estoque),
        "4": lambda: buscar_por_codigo(estoque),
        "5": lambda: buscar_por_nome(estoque),
        "6": lambda: registrar_venda(estoque, gerenciador),
        "7": lambda: historico_vendas(gerenciador),
        "8": lambda: listar_por_codigo(estoque),
        "9": lambda: listar_por_categoria(estoque),
        "10": lambda: relatorio_estoque_baixo(estoque, limite_baixo),
        "11": lambda: exibir_logs(),
    }

    while True:
        cabecalho(f"Menu Principal  |  {estoque.total} produto(s) em estoque")
        print(MENU)
        opcao = input("  Opção: ").strip()

        if opcao == "0":
            print("\n  Até logo!\n")
            break
        elif opcao in acoes:
            acoes[opcao]()
        else:
            print("  ⚠ Opção inválida. Tente novamente.")
            pausar()


if __name__ == "__main__":
    main()
