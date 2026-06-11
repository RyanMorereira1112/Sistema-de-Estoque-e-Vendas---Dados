
from datetime import datetime

_historico: list[str] = []


def registrar(operacao: str) -> None:
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    entrada = f"[{agora}] {operacao}"
    _historico.append(entrada)


def exibir() -> None:
    if not _historico:
        print("  Nenhuma operação registrada nesta sessão.")
        return
    for linha in _historico:
        print(f"  {linha}")
