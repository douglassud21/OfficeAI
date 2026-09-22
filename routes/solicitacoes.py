from flask import Blueprint, request, jsonify
from app import db
from models.solicitacao import Solicitacao
from services.claude_service import ClaudeService
from services.validators import validar_analise

solicitacoes_bp = Blueprint('solicitacoes', __name__, url_prefix='/solicitacoes')

claude_service = ClaudeService()


@solicitacoes_bp.route('/', methods=['POST'])
def criar_solicitacao():
    data = request.get_json(silent=True)

    if not data or 'texto_original' not in data:
        return jsonify({'erro': 'Campo "texto_original" é obrigatório.'}), 400

    texto = data['texto_original'].strip()
    if not texto:
        return jsonify({'erro': 'O texto não pode estar vazio.'}), 400

    nova_solicitacao = Solicitacao(texto_original=texto)

    aviso_analise = None

    try:
        analise = claude_service.analisar_solicitacao(texto)
        valido, motivo_erro = validar_analise(analise)

        if valido:
            nova_solicitacao.cliente = analise.get('cliente')
            nova_solicitacao.categoria = analise.get('categoria')
            nova_solicitacao.prioridade = analise.get('prioridade')
            nova_solicitacao.prazo = analise.get('prazo')
            nova_solicitacao.tipo_solicitacao = analise.get('tipo_solicitacao')
            nova_solicitacao.resumo = analise.get('resumo')
        else:
            aviso_analise = f'A solicitação foi salva, mas a análise automática falhou na validação: {motivo_erro}'

    except Exception as e:
        aviso_analise = f'A solicitação foi salva, mas a análise automática falhou: {str(e)}'

    db.session.add(nova_solicitacao)
    db.session.commit()

    resposta = nova_solicitacao.to_dict()
    if aviso_analise:
        resposta['aviso'] = aviso_analise

    return jsonify(resposta), 201


@solicitacoes_bp.route('/', methods=['GET'])
def listar_solicitacoes():
    solicitacoes = Solicitacao.query.order_by(Solicitacao.criado_em.desc()).all()
    return jsonify([s.to_dict() for s in solicitacoes]), 200


@solicitacoes_bp.route('/<int:id>', methods=['GET'])
def obter_solicitacao(id):
    solicitacao = Solicitacao.query.get(id)

    if solicitacao is None:
        return jsonify({'erro': f'Solicitação #{id} não encontrada.'}), 404

    return jsonify(solicitacao.to_dict()), 200


@solicitacoes_bp.route('/<int:id>', methods=['DELETE'])
def excluir_solicitacao(id):
    solicitacao = Solicitacao.query.get(id)

    if solicitacao is None:
        return jsonify({'erro': f'Solicitação #{id} não encontrada.'}), 404

    db.session.delete(solicitacao)
    db.session.commit()

    return jsonify({'mensagem': f'Solicitação #{id} excluída com sucesso.'}), 200