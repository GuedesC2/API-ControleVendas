import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.main import app
from src.models.user import db
from src.models.vendas import Produto

with app.app_context():
    # Criar produtos baseados na planilha
    produtos_iniciais = [
        {'nome': 'Equilíbrio de Conta', 'ponderador': 1.0, 'meta': 1522000.0},
        {'nome': 'Aquisição de Bens', 'ponderador': 1.0, 'meta': 550000.0},
        {'nome': 'Proteção', 'ponderador': 1.0, 'meta': 5500.0},
        {'nome': 'Sorte', 'ponderador': 1.0, 'meta': 3000.0},
        {'nome': 'Recuperação', 'ponderador': 1.0, 'meta': 25000.0},
        {'nome': 'Abertura de Conta', 'ponderador': 1.0, 'meta': 120.0},
        {'nome': 'Combinaqui', 'ponderador': 1.0, 'meta': 120.0},
        {'nome': 'Engajamento', 'ponderador': 1.0, 'meta': 120.0}
    ]
    
    for produto_data in produtos_iniciais:
        produto_existente = Produto.query.filter_by(nome=produto_data['nome']).first()
        if not produto_existente:
            produto = Produto(**produto_data)
            db.session.add(produto)
    
    db.session.commit()
    print('Produtos iniciais criados com sucesso!')

