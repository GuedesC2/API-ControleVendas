  // Variáveis globais
        let produtos = [];
        let vendas = [];
        let produtoSelecionado = null;

        // Carregar dados iniciais
        document.addEventListener('DOMContentLoaded', function() {
            carregarProdutos();
            carregarVendas();
            atualizarRelatorio();
            
            // Configurar data atual
            const hoje = new Date().toISOString().split('T')[0];
            document.getElementById('data').value = hoje;
        });

        // Função para carregar produtos
        async function carregarProdutos() {
            try {
                const response = await fetch('/api/produtos');
                produtos = await response.json();
                
                // Atualizar dropdown de produtos na seção de vendas
                const select = document.getElementById('produto');
                select.innerHTML = '<option value="">Selecione um produto</option>';
                produtos.forEach(produto => {
                    const option = document.createElement('option');
                    option.value = produto.id;
                    option.textContent = produto.nome;
                    select.appendChild(option);
                });

                // Atualizar lista de produtos na seção de configuração
                atualizarListaProdutos();
            } catch (error) {
                console.error('Erro ao carregar produtos:', error);
            }
        }

        // Função para atualizar lista de produtos na configuração
        function atualizarListaProdutos() {
            const container = document.getElementById('produtosList');
            container.innerHTML = '';

            produtos.forEach(produto => {
                const div = document.createElement('div');
                div.className = 'produto-item';
                div.onclick = () => selecionarProduto(produto);
                
                div.innerHTML = `
                    <div class="produto-info">
                        <div class="produto-nome">${produto.nome}</div>
                    </div>
                    <div class="produto-detalhes">
                        Meta: ${formatarMoeda(produto.meta)} | Ponderador: ${produto.ponderador}
                    </div>
                `;
                
                container.appendChild(div);
            });
        }

        // Função para selecionar produto para edição
        function selecionarProduto(produto) {
            // Remover seleção anterior
            document.querySelectorAll('.produto-item').forEach(item => {
                item.classList.remove('selected');
            });

            // Adicionar seleção atual
            event.target.closest('.produto-item').classList.add('selected');

            // Preencher formulário
            document.getElementById('produtoId').value = produto.id;
            document.getElementById('produtoNome').value = produto.nome;
            document.getElementById('produtoMeta').value = produto.meta;
            document.getElementById('produtoPonderador').value = produto.ponderador;

            produtoSelecionado = produto;
        }

        // Função para cancelar edição
        function cancelarEdicao() {
            document.getElementById('produtoForm').reset();
            document.querySelectorAll('.produto-item').forEach(item => {
                item.classList.remove('selected');
            });
            produtoSelecionado = null;
        }

        // Função para atualizar produto
        document.getElementById('produtoForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            if (!produtoSelecionado) {
                mostrarAlerta('Selecione um produto para editar.', 'warning', 'config-alert-container');
                return;
            }

            const formData = new FormData(e.target);
            const dados = {
                meta: parseFloat(formData.get('produtoMeta')),
                ponderador: parseFloat(formData.get('produtoPonderador'))
            };

            try {
                const response = await fetch(`/api/produtos/${produtoSelecionado.id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(dados)
                });

                if (response.ok) {
                    mostrarAlerta('Produto atualizado com sucesso!', 'success', 'config-alert-container');
                    carregarProdutos();
                    cancelarEdicao();
                    atualizarRelatorio();
                } else {
                    throw new Error('Erro ao atualizar produto');
                }
            } catch (error) {
                console.error('Erro:', error);
                mostrarAlerta('Erro ao atualizar produto.', 'error', 'config-alert-container');
            }
        });

        // Função para carregar vendas
        async function carregarVendas() {
            try {
                const response = await fetch('/api/vendas');
                vendas = await response.json();
                
                const container = document.getElementById('vendasList');
                container.innerHTML = '';
                
                vendas.forEach(venda => {
                    const div = document.createElement('div');
                    div.className = 'venda-item';
                    
                    div.innerHTML = `
                        <div class="venda-info">
                            <div class="venda-cliente">${venda.cliente_nome}</div>
                            <div class="venda-detalhes">${venda.produto_nome} - ${formatarData(venda.data)}</div>
                        </div>
                        <div class="venda-valor">${formatarMoeda(venda.valor_total)}</div>
                        <button class="delete-btn" onclick="excluirVenda(${venda.id})">🗑️</button>
                    `;
                    
                    container.appendChild(div);
                });
            } catch (error) {
                console.error('Erro ao carregar vendas:', error);
                mostrarAlerta('Erro ao carregar vendas: ' + error.message, 'error');
            }
        }

        // Função para calcular valor total
        document.getElementById('produto').addEventListener('change', calcularValorTotal);
        document.getElementById('valor').addEventListener('input', calcularValorTotal);

        function calcularValorTotal() {
            const produtoId = document.getElementById('produto').value;
            const valor = parseFloat(document.getElementById('valor').value) || 0;
            
            if (produtoId && valor > 0) {
                const produto = produtos.find(p => p.id == produtoId);
                if (produto) {
                    const valorTotal = valor * produto.ponderador;
                    document.getElementById('valorTotal').value = valorTotal.toFixed(2);
                }
            } else {
                document.getElementById('valorTotal').value = '';
            }
        }

        // Função para registrar venda
        document.getElementById('vendaForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const dados = {
                cliente_nome: formData.get('cliente'),
                produto_id: parseInt(formData.get('produto')),
                data: formData.get('data'),
                valor: parseFloat(formData.get('valor'))
            };

            try {
                // Primeiro, verificar se o cliente existe ou criar um novo
                let clienteResponse = await fetch('/api/clientes');
                let clientes = await clienteResponse.json();
                let cliente = clientes.find(c => c.nome.toLowerCase() === dados.cliente_nome.toLowerCase());
                
                if (!cliente) {
                    // Criar novo cliente
                    const novoClienteResponse = await fetch('/api/clientes', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ nome: dados.cliente_nome })
                    });
                    cliente = await novoClienteResponse.json();
                }

                // Registrar venda
                const vendaData = {
                    cliente_id: cliente.id,
                    produto_id: dados.produto_id,
                    data: dados.data,
                    valor: dados.valor
                };

                const response = await fetch('/api/vendas', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(vendaData)
                });

                if (response.ok) {
                    mostrarAlerta('Venda registrada com sucesso!', 'success');
                    e.target.reset();
                    document.getElementById('data').value = new Date().toISOString().split('T')[0];
                    carregarVendas();
                    atualizarRelatorio();
                } else {
                    throw new Error('Erro ao registrar venda');
                }
            } catch (error) {
                console.error('Erro:', error);
                mostrarAlerta('Erro ao registrar venda.', 'error');
            }
        });

        // Função para excluir venda
        async function excluirVenda(id) {
            if (confirm('Tem certeza que deseja excluir esta venda?')) {
                try {
                    const response = await fetch(`/api/vendas/${id}`, {
                        method: 'DELETE'
                    });

                    if (response.ok) {
                        mostrarAlerta('Venda excluída com sucesso!', 'success');
                        carregarVendas();
                        atualizarRelatorio();
                    } else {
                        throw new Error('Erro ao excluir venda');
                    }
                } catch (error) {
                    console.error('Erro:', error);
                    mostrarAlerta('Erro ao excluir venda.', 'error');
                }
            }
        }

        // Função para atualizar relatório
        async function atualizarRelatorio() {
            try {
                const response = await fetch('/api/relatorio/texto');
                const data = await response.json();
                document.getElementById('relatorio').textContent = data.texto;
            } catch (error) {
                console.error('Erro ao carregar relatório:', error);
                document.getElementById('relatorio').textContent = 'Erro ao carregar relatório';
            }
        }

        // Função para copiar relatório
        async function copiarRelatorio() {
            try {
                const response = await fetch('/api/relatorio/texto');
                const data = await response.json();
                
                await navigator.clipboard.writeText(data.texto);
                mostrarAlerta('Relatório copiado para a área de transferência!', 'success');
            } catch (error) {
                console.error('Erro ao copiar relatório:', error);
                mostrarAlerta('Erro ao copiar relatório.', 'error');
            }
        }

        // Função para mostrar alertas
        function mostrarAlerta(mensagem, tipo, container = 'alert-container') {
            const alertContainer = document.getElementById(container);
            const alert = document.createElement('div');
            alert.className = `alert alert-${tipo}`;
            alert.textContent = mensagem;
            
            alertContainer.innerHTML = '';
            alertContainer.appendChild(alert);
            
            setTimeout(() => {
                alert.remove();
            }, 5000);
        }

        // Função para formatar moeda
        function formatarMoeda(valor) {
            return new Intl.NumberFormat('pt-BR', {
                style: 'currency',
                currency: 'BRL'
            }).format(valor);
        }

        // Função para formatar data
        function formatarData(data) {
            return new Date(data + 'T00:00:00').toLocaleDateString('pt-BR');
        }