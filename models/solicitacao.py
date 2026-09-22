from datetime import datetime
from app import db

class Solicitacao(db.Model):
    __tablename__ = 'solicitacoes'

    id = db.Column(db.Integer, primary_key=True)
    texto_original = db.Column(db.Text, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    # Campos preenchidos após a análise (mockada, por enquanto) do Claude.
    # Ficam nullable porque uma solicitação pode existir antes de ser analisada.
    cliente = db.Column(db.String(200), nullable=True)
    categoria = db.Column(db.String(100), nullable=True)
    prioridade = db.Column(db.String(20), nullable=True)
    prazo = db.Column(db.String(100), nullable=True)
    tipo_solicitacao = db.Column(db.String(200), nullable=True)
    resumo = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'texto_original': self.texto_original,
            'criado_em': self.criado_em.isoformat(),
            'cliente': self.cliente,
            'categoria': self.categoria,
            'prioridade': self.prioridade,
            'prazo': self.prazo,
            'tipo_solicitacao': self.tipo_solicitacao,
            'resumo': self.resumo,
        }