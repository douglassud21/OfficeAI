class ClaudeService:
    """
    NOTA: Esta é uma versão simulada (mock) do serviço.
    Ela não faz chamadas reais à API da Anthropic, para evitar custos
    durante o desenvolvimento do projeto.

    Quando quiser usar a API de verdade, substitua o corpo do método
    analisar_solicitacao() pela chamada real ao client.messages.create()
    (essa versão real já foi escrita e testada na etapa anterior).
    """

    def analisar_solicitacao(self, texto: str) -> dict:
        # Resposta fixa simulando o que o Claude retornaria.
        # Sempre devolve os mesmos dados, independente do texto de entrada.
        return {
            "cliente": "João da Silva",
            "categoria": "Contrato",
            "prioridade": "Alta",
            "prazo": "sexta-feira",
            "tipo_solicitacao": "Revisão de contrato",
            "resumo": "Cliente solicita revisão do contrato de prestação de serviços."
        }