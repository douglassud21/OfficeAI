from dotenv import load_dotenv
load_dotenv()

from services.claude_service import ClaudeService

texto_exemplo = (
    "João da Silva solicitou a revisão do contrato de prestação de "
    "serviços. Ele precisa de um retorno até sexta-feira e informou "
    "que o assunto é urgente."
)

service = ClaudeService()
resultado = service.analisar_solicitacao(texto_exemplo)

print("Resultado da análise:")
print(resultado)