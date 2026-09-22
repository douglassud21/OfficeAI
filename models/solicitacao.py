from datetime import datetime
from app import db

class Solicitacao(db.Model):
    __tablename__ = 'solicitacoes'

    id = db.Column(db.Integer, primary_key=True)
    texto_original = db.Column(db.Text, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'texto_original': self.texto_original,
            'criado_em': self.criado_em.isoformat()
        }