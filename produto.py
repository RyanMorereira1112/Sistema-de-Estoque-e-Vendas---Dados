
class Produto:

    def __init__(self, codigo: str, nome: str, categoria: str,
                 preco: float, quantidade: int):
        self.codigo = self._validar_codigo(codigo)
        self.nome = self._validar_nome(nome)
        self.categoria = self._validar_categoria(categoria)
        self.preco = self._validar_preco(preco)
        self.quantidade = self._validar_quantidade(quantidade)

    @staticmethod
    def _validar_codigo(codigo: str) -> str:
        codigo = str(codigo).strip()
        if not codigo:
            raise ValueError("Código não pode ser vazio.")
        return codigo

    @staticmethod
    def _validar_nome(nome: str) -> str:
        nome = str(nome).strip()
        if not nome:
            raise ValueError("Nome não pode ser vazio.")
        return nome

    @staticmethod
    def _validar_categoria(categoria: str) -> str:
        categoria = str(categoria).strip()
        if not categoria:
            raise ValueError("Categoria não pode ser vazia.")
        return categoria

    @staticmethod
    def _validar_preco(preco) -> float:
        try:
            preco = float(preco)
        except (TypeError, ValueError):
            raise ValueError("Preço deve ser um número.")
        if preco <= 0:
            raise ValueError("Preço deve ser maior que zero.")
        return preco

    @staticmethod
    def _validar_quantidade(quantidade) -> int:
        try:
            quantidade = int(quantidade)
        except (TypeError, ValueError):
            raise ValueError("Quantidade deve ser um número inteiro.")
        if quantidade < 0:
            raise ValueError("Quantidade não pode ser negativa.")
        return quantidade

    def to_dict(self) -> dict:
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "categoria": self.categoria,
            "preco": self.preco,
            "quantidade": self.quantidade,
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "Produto":
        return cls(
            codigo=dados["codigo"],
            nome=dados["nome"],
            categoria=dados["categoria"],
            preco=dados["preco"],
            quantidade=dados["quantidade"],
        )

    def __str__(self) -> str:
        return (
            f"[{self.codigo}] {self.nome} | "
            f"Categoria: {self.categoria} | "
            f"Preço: R$ {self.preco:.2f} | "
            f"Qtd: {self.quantidade}"
        )

    def __repr__(self) -> str:
        return f"Produto(codigo={self.codigo!r}, nome={self.nome!r})"
