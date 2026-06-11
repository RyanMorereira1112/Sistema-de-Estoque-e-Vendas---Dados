

import json
import os

ARQUIVO_DADOS = "dados.json"


def salvar(estoque) -> None:
    dados = estoque.to_list()
    try:
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
    except OSError as e:
        raise RuntimeError(f"Erro ao salvar dados: {e}")


def carregar(estoque) -> int:
    
    if not os.path.exists(ARQUIVO_DADOS):
        return 0

    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            conteudo = f.read().strip()
            if not conteudo:
                return 0
            dados = json.loads(conteudo)
    except json.JSONDecodeError:
        raise RuntimeError(
            f"Arquivo '{ARQUIVO_DADOS}' está corrompido ou com formato inválido."
        )
    except OSError as e:
        raise RuntimeError(f"Erro ao carregar dados: {e}")

    estoque.carregar_lista(dados)
    return len(dados)
