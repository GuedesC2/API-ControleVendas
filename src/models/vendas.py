from src.models.user import db
from datetime import datetime

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com vendas
    vendas = db.relationship('Venda', backref='cliente', lazy=True)

    def __repr__(self):
        return f'<Cliente {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    ponderador = db.Column(db.Float, default=1.0)
    meta = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com vendas
    vendas = db.relationship('Venda', backref='produto', lazy=True)

    def __repr__(self):
        return f'<Produto {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'ponderador': self.ponderador,
            'meta': self.meta,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    data = db.Column(db.Date, nullable=False)
    valor = db.Column(db.Float, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)  # valor * ponderador
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Venda {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'produto_id': self.produto_id,
            'data': self.data.isoformat() if self.data else None,
            'valor': self.valor,
            'valor_total': self.valor_total,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'cliente': self.cliente.to_dict() if self.cliente else None,
            'produto': self.produto.to_dict() if self.produto else None
        }

