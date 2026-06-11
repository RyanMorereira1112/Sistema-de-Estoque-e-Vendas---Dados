
from produto import Produto


class Estoque:

    def __init__(self):
        self._produtos: list[Produto] = []
        self._produtos_ordenados: list[Produto] = []


    @property
    def total(self) -> int:
        return len(self._produtos)


    def cadastrar(self, produto: Produto) -> None:
        
        if self._busca_binaria(produto.codigo) is not None:
            raise ValueError(f"Já existe um produto com o código '{produto.codigo}'.")

        self._produtos.append(produto)
        self._inserir_ordenado(produto)

    def _inserir_ordenado(self, produto: Produto) -> None:
        pos = 0
        while pos < len(self._produtos_ordenados):
            if produto.codigo < self._produtos_ordenados[pos].codigo:
                break
            pos += 1
        self._produtos_ordenados.insert(pos, produto)


    def remover(self, codigo: str) -> Produto:
       
        produto = self._busca_linear_codigo(codigo)
        if produto is None:
            raise ValueError(f"Produto com código '{codigo}' não encontrado.")

        self._produtos.remove(produto)
        self._produtos_ordenados.remove(produto)
        return produto

   

    def editar(self, codigo: str, nome: str = None, categoria: str = None,
               preco: float = None, quantidade: int = None) -> Produto:
        produto = self.buscar_por_codigo(codigo)

        if nome is not None:
            produto.nome = Produto._validar_nome(nome)
        if categoria is not None:
            produto.categoria = Produto._validar_categoria(categoria)
        if preco is not None:
            produto.preco = Produto._validar_preco(preco)
        if quantidade is not None:
            produto.quantidade = Produto._validar_quantidade(quantidade)

        return produto


    def buscar_por_codigo(self, codigo: str) -> Produto:
       
        produto = self._busca_binaria(codigo)
        if produto is None:
            raise ValueError(f"Produto com código '{codigo}' não encontrado.")
        return produto

    def _busca_binaria(self, codigo: str):
       
        esquerda = 0
        direita = len(self._produtos_ordenados) - 1

        while esquerda <= direita:
            meio = (esquerda + direita) // 2
            codigo_meio = self._produtos_ordenados[meio].codigo

            if codigo_meio == codigo:
                return self._produtos_ordenados[meio]
            elif codigo_meio < codigo:
                esquerda = meio + 1
            else:
                direita = meio - 1

        return None


    def buscar_por_nome(self, termo: str) -> list[Produto]:
      
        termo = termo.lower().strip()
        return [p for p in self._produtos if termo in p.nome.lower()]

    def _busca_linear_codigo(self, codigo: str):
        for produto in self._produtos:
            if produto.codigo == codigo:
                return produto
        return None


    def listar_ordenado(self) -> list[Produto]:
        return list(self._produtos_ordenados)

    def listar_por_categoria(self, categoria: str) -> list[Produto]:
        categoria = categoria.lower().strip()
        return [p for p in self._produtos if p.categoria.lower() == categoria]

    def listar_estoque_baixo(self, limite: int = 5) -> list[Produto]:
        return [p for p in self._produtos if p.quantidade < limite]

    def listar_categorias(self) -> list[str]:
        return sorted(set(p.categoria for p in self._produtos))


    def to_list(self) -> list[dict]:
        return [p.to_dict() for p in self._produtos]

    def carregar_lista(self, lista: list[dict]) -> None:
        self._produtos.clear()
        self._produtos_ordenados.clear()
        for dados in lista:
            produto = Produto.from_dict(dados)
            self._produtos.append(produto)
            self._inserir_ordenado(produto)
