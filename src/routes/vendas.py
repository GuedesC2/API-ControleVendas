from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.vendas import Cliente, Produto, Venda
from datetime import datetime, date
from sqlalchemy import func

vendas_bp = Blueprint('vendas', __name__)

# Rotas para Clientes
@vendas_bp.route('/clientes', methods=['GET'])
def get_clientes():
    clientes = Cliente.query.all()
    return jsonify([cliente.to_dict() for cliente in clientes])

@vendas_bp.route('/clientes', methods=['POST'])
def create_cliente():
    data = request.get_json()
    if not data or 'nome' not in data:
        return jsonify({'error': 'Nome é obrigatório'}), 400
    
    cliente = Cliente(nome=data['nome'])
    db.session.add(cliente)
    db.session.commit()
    
    return jsonify(cliente.to_dict()), 201

@vendas_bp.route('/clientes/<int:cliente_id>', methods=['DELETE'])
def delete_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    db.session.delete(cliente)
    db.session.commit()
    return '', 204

# Rotas para Produtos
@vendas_bp.route('/produtos', methods=['GET'])
def get_produtos():
    produtos = Produto.query.all()
    return jsonify([produto.to_dict() for produto in produtos])

@vendas_bp.route('/produtos', methods=['POST'])
def create_produto():
    data = request.get_json()
    if not data or 'nome' not in data:
        return jsonify({'error': 'Nome é obrigatório'}), 400
    
    produto = Produto(
        nome=data['nome'],
        ponderador=data.get('ponderador', 1.0),
        meta=data.get('meta', 0.0)
    )
    db.session.add(produto)
    db.session.commit()
    
    return jsonify(produto.to_dict()), 201

@vendas_bp.route('/produtos/<int:produto_id>', methods=['PUT'])
def update_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    data = request.get_json()
    
    if 'nome' in data:
        produto.nome = data['nome']
    if 'ponderador' in data:
        produto.ponderador = data['ponderador']
    if 'meta' in data:
        produto.meta = data['meta']
    
    db.session.commit()
    return jsonify(produto.to_dict())

@vendas_bp.route('/produtos/<int:produto_id>', methods=['DELETE'])
def delete_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    db.session.delete(produto)
    db.session.commit()
    return '', 204

# Rotas para Vendas
@vendas_bp.route('/vendas', methods=['GET'])
def get_vendas():
    vendas = Venda.query.all()
    return jsonify([venda.to_dict() for venda in vendas])

@vendas_bp.route('/vendas', methods=['POST'])
def create_venda():
    data = request.get_json()
    
    # Validação dos dados obrigatórios
    required_fields = ['cliente_id', 'produto_id', 'data', 'valor']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} é obrigatório'}), 400
    
    # Verificar se cliente e produto existem
    cliente = Cliente.query.get(data['cliente_id'])
    produto = Produto.query.get(data['produto_id'])
    
    if not cliente:
        return jsonify({'error': 'Cliente não encontrado'}), 404
    if not produto:
        return jsonify({'error': 'Produto não encontrado'}), 404
    
    # Converter data string para objeto date
    try:
        data_venda = datetime.strptime(data['data'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD'}), 400
    
    # Calcular valor total
    valor_total = data['valor'] * produto.ponderador
    
    venda = Venda(
        cliente_id=data['cliente_id'],
        produto_id=data['produto_id'],
        data=data_venda,
        valor=data['valor'],
        valor_total=valor_total
    )
    
    db.session.add(venda)
    db.session.commit()
    
    return jsonify(venda.to_dict()), 201

@vendas_bp.route('/vendas/<int:venda_id>', methods=['DELETE'])
def delete_venda(venda_id):
    venda = Venda.query.get_or_404(venda_id)
    db.session.delete(venda)
    db.session.commit()
    return '', 204

# Rota para relatórios
@vendas_bp.route('/relatorio', methods=['GET'])
def get_relatorio():
    # Buscar todos os produtos
    produtos = Produto.query.all()
    relatorio = []
    
    for produto in produtos:
        # Calcular realizado (soma dos valores totais das vendas)
        realizado = db.session.query(func.sum(Venda.valor_total)).filter_by(produto_id=produto.id).scalar() or 0
        
        # Calcular ICM (Índice de Cumprimento de Meta)
        icm = (realizado / produto.meta * 100) if produto.meta > 0 else 0
        
        relatorio.append({
            'produto': produto.nome,
            'meta': produto.meta,
            'realizado': realizado,
            'icm': round(icm, 2)
        })
    
    return jsonify(relatorio)

# Rota para gerar texto do relatório
@vendas_bp.route('/relatorio/texto', methods=['GET'])
def get_relatorio_texto():
    # Buscar todos os produtos
    produtos = Produto.query.all()
    linhas = []
    
    for produto in produtos:
        # Calcular realizado (soma dos valores totais das vendas)
        realizado = db.session.query(func.sum(Venda.valor_total)).filter_by(produto_id=produto.id).scalar() or 0
        
        # Calcular ICM (Índice de Cumprimento de Meta)
        icm = (realizado / produto.meta * 100) if produto.meta > 0 else 0
        
        # Formatar valores
        if produto.nome in ['Abertura de Conta', 'Combinaqui', 'Engajamento']:
            meta_formatada = f"{int(produto.meta)}"
            realizado_formatado = f"R$ {realizado:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        else:
            meta_formatada = f"R$ {produto.meta:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            realizado_formatado = f"R$ {realizado:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        
        icm_formatado = f"{icm:.0f}%"
        
        # Formatação com espaçamento adequado para melhor legibilidade
        linha = f"{produto.nome:<20} | {meta_formatada:>15} | {realizado_formatado:>15} | {icm_formatado:>6}"
        linhas.append(linha)
    
    # Cabeçalho com separadores claros
    separador = "-" * 70
    cabecalho = f"{'PRODUTO':<20} | {'META':>15} | {'REALIZADO':>15} | {'ICM':>6}"
    
    texto = f"{cabecalho}\n{separador}\n" + "\n".join(linhas)
    
    return jsonify({'texto': texto})

