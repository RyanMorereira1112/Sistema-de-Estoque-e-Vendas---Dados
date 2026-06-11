from datetime import datetime
from produto import Produto


class Venda:

    def __init__(self, produto: Produto, quantidade: int):
        self.codigo_produto = produto.codigo
        self.nome_produto = produto.nome
        self.quantidade = quantidade
        self.preco_unitario = produto.preco
        self.total = quantidade * produto.preco
        self.data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def __str__(self) -> str:
        return (
            f"[{self.data_hora}] Venda: {self.nome_produto} "
            f"(cód. {self.codigo_produto}) | "
            f"Qtd: {self.quantidade} | "
            f"Unit.: R$ {self.preco_unitario:.2f} | "
            f"Total: R$ {self.total:.2f}"
        )


class GerenciadorVendas:

    def __init__(self):
        self._historico: list[Venda] = []

    def registrar(self, estoque, codigo: str, quantidade: int) -> Venda:
        
        try:
            quantidade = int(quantidade)
        except (TypeError, ValueError):
            raise ValueError("Quantidade deve ser um número inteiro.")

        if quantidade <= 0:
            raise ValueError("Quantidade para venda deve ser maior que zero.")

        produto = estoque.buscar_por_codigo(codigo)

        if produto.quantidade < quantidade:
            raise ValueError(
                f"Estoque insuficiente. Disponível: {produto.quantidade} unidade(s)."
            )

        produto.quantidade -= quantidade
        venda = Venda(produto, quantidade)
        self._historico.append(venda)
        return venda

    def historico(self) -> list[Venda]:
        return list(self._historico)

    def total_vendas(self) -> float:
        return sum(v.total for v in self._historico)
