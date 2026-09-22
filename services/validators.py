CAMPOS_ESPERADOS = {
    'cliente': str,
    'categoria': str,
    'prioridade': str,
    'prazo': str,
    'tipo_solicitacao': str,
    'resumo': str,
}

PRIORIDADES_VALIDAS = {'Alta', 'Media', 'Média', 'Baixa'}


def validar_analise(dados: dict) -> tuple[bool, str | None]:
    """
    Valida a resposta vinda do ClaudeService antes de confiarmos nela.

    Retorna (True, None) se válido, ou (False, motivo) se inválido.
    Não lança exceção — quem chamar decide o que fazer com o resultado.
    """
    if not isinstance(dados, dict):
        return False, 'Resposta da IA não é um objeto JSON válido.'

    for campo, tipo_esperado in CAMPOS_ESPERADOS.items():
        if campo not in dados:
            return False, f'Campo obrigatório ausente na resposta da IA: "{campo}".'

        valor = dados[campo]

        # Campos podem vir como None (ex: "prazo" não identificado no texto)
        if valor is None:
            continue

        if not isinstance(valor, tipo_esperado):
            return False, f'Campo "{campo}" veio com tipo inválido: esperado {tipo_esperado.__name__}, recebido {type(valor).__name__}.'

    prioridade = dados.get('prioridade')
    if prioridade is not None and prioridade not in PRIORIDADES_VALIDAS:
        return False, f'Valor de "prioridade" não reconhecido: "{prioridade}".'

    return True, None