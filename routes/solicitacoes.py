from flask import Blueprint, request, jsonify
from app import db
from models.solicitacao import Solicitacao

solicitacoes_bp = Blueprint('solicitacoes', __name__, url_prefix='/solicitacoes')

@solicitacoes_bp.route('/', methods=['POST'])
def criar_solicitacao():
    data = request.get_json(silent=True)

    if not data or 'texto_original' not in data:
        return jsonify({'erro': 'Campo "texto_original" é obrigatório.'}), 400

    texto = data['texto_original'].strip()
    if not texto:
        return jsonify({'erro': 'O texto não pode estar vazio.'}), 400

    nova_solicitacao = Solicitacao(texto_original=texto)
    db.session.add(nova_solicitacao)
    db.session.commit()

    return jsonify(nova_solicitacao.to_dict()), 201


@solicitacoes_bp.route('/', methods=['GET'])
def listar_solicitacoes():
    solicitacoes = Solicitacao.query.order_by(Solicitacao.criado_em.desc()).all()
    return jsonify([s.to_dict() for s in solicitacoes]), 200