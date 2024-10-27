from app import app
from flask import render_template,request, redirect, url_for
import sqlite3
import models

@app.route("/login.html")
def login():
    return render_template('login.html')

#telas_iniciais

@app.route("/tela_inicial.html")
def telaInicio():
    return render_template('tela_inicial.html')

@app.route('/cadastro.html')
def cadastro():
    return render_template('cadastro.html')

@app.route('/clientes.html')
def clientes():
    return render_template('clientes.html')

@app.route('/seguradoras.html')
def seguradoras():
    return render_template('seguradoras.html')

@app.route('/seguros.html')
def seguros():
    return render_template('seguros.html')

@app.route('/cotações.html')
def cotacoes():
    return render_template('cotações.html')

#TELAS CADASTRAR
#CADASTRAR CLIENTE
@app.route("/")
@app.route('/cadastrar_cliente.html', methods=['POST', 'GET'])
def cadastrar_cliente():
    # Criar a tabela apenas uma vez no início da aplicação
    models.criar_tabela_cliente()  

    if request.method == 'POST':
        nome = request.form.get('nome_cadastrar_cliente')
        cpf = int(request.form.get('cpf_cadastrar_cliente'))
        email = request.form.get('email_cadastrar_cliente')
        data_nascimento = request.form.get('dt_nasc_cadastrar_cliente')
        endereco = request.form.get('endereco_cadastrar_cliente')
        telefone = request.form.get('tel_cadastrar_cliente')
        profissao = request.form.get('prof_cadastrar_cliente')
        faixa_salarial = float(request.form.get('sal_cadastrar_cliente'))
        condutor_principal = int(request.form.get('condutor_principal_cadastrar_cliente'))
        proprietario = int(request.form.get('proprietario_cadastrar_cliente'))
        estado_civil = request.form.get('civil_cadastrar_cliente')

        print("Nome:", nome)
        print("CPF:", cpf)
        print("Email:", email)
        print("Data de Nascimento:", data_nascimento)
        print("Endereço:", endereco)
        print("Telefone:", telefone)
        print("Profissão:", profissao)
        print("Faixa Salarial:", faixa_salarial)
        print("Condutor Principal", condutor_principal)
        print("Proprietario", proprietario)
        print("Estado Civil:", estado_civil)

        banco = models.criar_conexao()
        cursor = banco.cursor()

        try:
            cursor.execute('''
                INSERT INTO clientes (
                    cpf, nome, email, data_nascimento, endereco,
                    telefone, profissao, faixa_salarial,
                    condutor_principal, proprietario, estado_civil
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (cpf, nome, email, data_nascimento, endereco,
                  telefone, profissao, faixa_salarial,
                  condutor_principal, proprietario, estado_civil))
            banco.commit()
            return render_template('sucesso.html', sucesso="Cliente cadastrado com sucesso!")  
        
        except sqlite3.IntegrityError as e:
            # Verifica qual campo causou o erro
            if 'UNIQUE constraint failed: clientes.nome' in str(e):
                return render_template('cadastrar_cliente.html', erro="O nome já existe no banco de dados.")
            elif 'UNIQUE constraint failed: clientes.cpf' in str(e):
                return render_template('cadastrar_cliente.html', erro="O CPF já existe no banco de dados.")
            else:
                return render_template('cadastrar_cliente.html', erro="Erro de integridade desconhecido.")
            
        finally:
            banco.close()  

    return render_template('cadastrar_cliente.html')

@app.route('/cadastrar_veiculo.html')
def cadastrarVeiculo():
    return render_template('/cadastrar_veiculo.html')


#CADASTRAR SEGURADORA
@app.route('/cadastrar_seguradora.html', methods=['POST', 'GET'])
def cadastrarSeguradora():
    # Criar a tabela apenas uma vez no início da aplicação
    models.criar_tabela_seguradora()  
    
    if request.method == 'POST':
        nome = request.form.get('nome_cadastrar_seguradora')
        cnpj = request.form.get('cnpj_cadastrar_seguradora')
        email = request.form.get('email_cadastrar_seguradora')
        endereco = request.form.get('endereco_cadastrar_seguradora')
        tel = request.form.get('tel_cadastrar_seguradora')

        # Estabelecer a conexão com o banco de dados aqui
        banco = models.criar_conexao()
        cursor = banco.cursor()

        try:
            cursor.execute("INSERT INTO Seguradora (nome, cnpj, email, endereco, telefone) VALUES (?, ?, ?, ?, ?)", (nome, cnpj, email, endereco, tel))
            banco.commit()
            return render_template('sucesso.html', sucesso="Cadastro Feito com Sucesso!")
        except sqlite3.IntegrityError:
            return render_template('cadastrar_seguradora.html',erro ="O CNPJ já existe no banco de dados.")
        finally:
            banco.close()  # Sempre feche a conexão, independentemente do resultado

    return render_template('cadastrar_seguradora.html')

@app.route('/cadastrar_seguros.html', methods=['POST', 'GET'])
def cadastrarSeguros():
     models.criar_tabela_seguros()  
     if request.method == 'POST':
        apolice = int(request.form.get('apolice'))
        id_cotacao = int(request.form.get('id_cotacao'))
        valor_total = float(request.form.get('valor_total'))
        data_inicio = request.form.get('data_inicio')
        data_termino = request.form.get('data_termino')
        vencimento = request.form.get('vencimento')

      banco = models.criar_conexao()
      cursor = banco.cursor()

      try:
            cursor.execute('''
                INSERT INTO Seguros (
                    apolice, id_cotacao, valor_total, data_inicio, data_termino, vencimento
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (apolice, id_cotacao, valor_total, data_inicio, data_termino, vencimento))
            
            banco.commit()
            return render_template('sucesso.html', sucesso="Seguro cadastrado com sucesso!")

        except sqlite3.IntegrityError as e:            
            if 'UNIQUE constraint failed: Seguros.apolice' in str(e):
                return render_template('cadastrar_seguros.html', erro="O número da apólice já existe no banco de dados.")
            elif 'FOREIGN KEY constraint failed' in str(e):
                return render_template('cadastrar_seguros.html', erro="O ID da cotação não existe no banco de dados.")
            else:
                return render_template('cadastrar_seguros.html', erro="Erro de integridade desconhecido.")

        finally:
            banco.close()      

    return render_template('/cadastrar_seguros.html')

# Função para cadastrar Cotações
@app.route('/cadastrar_cotação.html', methods=['POST', 'GET'])
def cadastrarCotacao():    
    models.criar_tabela_cotacoes()

    if request.method == 'POST':        
        placa = request.form.get('placa')
        cpf = request.form.get('cpf')
        data_inicio = request.form.get('data_inicio')
        data_termino = request.form.get('data_termino')
        vencimento = request.form.get('vencimento')
        valor = float(request.form.get('valor'))

        
        banco = models.criar_conexao()
        cursor = banco.cursor()

        try:
            cursor.execute('''
                INSERT INTO Cotacoes (
                    placa, cpf, data_inicio, data_termino, vencimento, valor
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (placa, cpf, data_inicio, data_termino, vencimento, valor))

            banco.commit()
            return render_template('sucesso.html', sucesso="Cotação cadastrada com sucesso!")

        except sqlite3.IntegrityError as e:
            # Verifica qual campo causou o erro
            if 'FOREIGN KEY constraint failed' in str(e):
                if 'clientes' in str(e):
                    return render_template('cadastrar_cotação.html', erro="O CPF informado não existe no banco de dados.")
                elif 'veiculos' in str(e):
                    return render_template('cadastrar_cotação.html', erro="A placa informada não existe no banco de dados.")
            else:
                return render_template('cadastrar_cotação.html', erro="Erro de integridade desconhecido.")

        finally:
            banco.close()
        return render_template('/cadastrar_cotação.html')

#consultar1
@app.route('/consultar_cliente1.html', methods=['POST', 'GET'])
def consultarCliente1():
    if request.method == 'POST':
        #get filtros
        cpf = request.form.get('cpf')
        nome = request.form.get('nome')

        
        banco = models.criar_conexao()
        cursor = banco.cursor()
        
        try:
            query = "SELECT * FROM clientes WHERE cpf = ? OR nome = ?"
            cursor.execute(query, (cpf, nome))
            cliente = cursor.fetchone()  # busca primeira linha
           
            if cliente:
                cliente_data = {
                    'cpf': cliente[0],
                    'nome': cliente[1],
                    'email': cliente[2],
                    'data_nascimento': cliente[3],
                    'endereco': cliente[4],
                    'telefone': cliente[5],
                    'profissao': cliente[6],
                    'faixa_salarial': cliente[7],
                    'condutor_principal': 'Sim' if cliente[8] == 1 else 'Não',
                    'proprietario': 'Sim' if cliente[9] == 1 else 'Não',
                    'estado_civil': cliente[10]
                }
                return render_template('consultar_cliente1.html', cliente=cliente_data)
            else:
                return render_template('consultar_cliente1.html', erro="Cliente não encontrado.")

        except sqlite3.Error as e:
            return render_template('consultar_cliente1.html', erro="Erro ao consultar o banco de dados.")

        finally:
            banco.close()
    
    return render_template('/consultar_cliente1.html')

@app.route('/consultar_veículo.html')
def consultarVeiculo1():
    if request.method == 'POST':
        # get filtros
        placa = request.form.get('placa')
     
        # conexao
        banco = models.criar_conexao()
        cursor = banco.cursor()
        
        try:
            query = "SELECT * FROM Veiculos WHERE placa = ?"
            cursor.execute(query, (placa))
            veiculo = cursor.fetchone()  # busca primeira linha

            
            if Veiculos:
                veiculo_data = {
                    'modelo': veiculo[0],
                    'ano': veiculo[1],
                    'cor': veiculo[2],
                    'placa': veiculo[3],
                    'chasi': veiculo[4],
                    'cpf': veiculo[5]
                }
                return render_template('consultar_veiculo.html', veiculo=veiculo_data)
            else:
                return render_template('consultar_veiculo.html', erro="Veiculo não encontrado.")

        except sqlite3.Error as e:
            return render_template('consultar_veiculo.html', erro="Erro ao consultar o banco de dados.")

        finally:
            banco.close()
    return render_template('/consultar_veículo.html')

@app.route('/consultar_seguradora.html', methods=['POST', 'GET'])
def consultarSeguradora1():
    if request.method == 'POST':
        # get filtros
        cnpj = request.form.get('cnpj')
        nome = request.form.get('nome')

        # conexao
        banco = models.criar_conexao()
        cursor = banco.cursor()

       
        try:
            query = "SELECT * FROM Seguradora WHERE cnpj = ? OR nome = ?"
            cursor.execute(query, (cnpj, nome))
            seguradora = cursor.fetchone()  # busca primeira linha

            
            if seguradora:
                seguradora_data = {
                    'nome': seguradora[0],
                    'cnpj': seguradora[1],
                    'email': seguradora[2],
                    'endereco': seguradora[3],
                    'telefone': seguradora[4]
                }
                return render_template('consultar_seguradora.html', seguradora=seguradora_data)
            else:
                return render_template('consultar_seguradora.html', erro="Seguradora não encontrada.")

        except sqlite3.Error as e:
            return render_template('consultar_seguradora.html', erro="Erro ao consultar o banco de dados.")

        finally:
            banco.close()
    
    return render_template('/consultar_seguradora.html')

@app.route('/consultar_seguros.html', methods=['POST', 'GET'])
def consultarSeguros1():
    if request.method == 'POST':
        # get filtros
        apolice = request.form.get('apolice')
        id_cotacao = request.form.get('id_cotacao')

        # conexao
        banco = models.criar_conexao()
        cursor = banco.cursor()

       
        try:
            query = "SELECT * FROM Seguros WHERE apolice = ? OR id_cotacao = ?"
            cursor.execute(query, (apolice, id_cotacao))
            seguro = cursor.fetchone()  # busca primeiro resultado

            
            if seguro:
                seguro_data = {
                    'apolice': seguro[0],
                    'id_cotacao': seguro[1],
                    'valor_total': seguro[2],
                    'data_inicio': seguro[3],
                    'data_termino': seguro[4],
                    'vencimento': seguro[5]
                }
                return render_template('consultar_seguros.html', seguro=seguro_data)
            else:
                return render_template('consultar_seguros.html', erro="Seguro não encontrado.")

        except sqlite3.Error as e:
            return render_template('consultar_seguros.html', erro="Erro ao consultar o banco de dados.")

        finally:
            banco.close()
    
    return render_template('/consultar_seguros.html')

@app.route('/consultar_cotação1.html', methods=['POST', 'GET'])
def consultarCotacoes1():
    if request.method == 'POST': 
        # get filtro
        id_cotacao = request.form.get('id_cotacao')
        cpf = request.form.get('cpf')
        placa = request.form.get('placa')
       # conexao
        banco = models.criar_conexao()
        cursor = banco.cursor()
        
        try:
            query = "SELECT * FROM Cotacoes WHERE id_cotacao = ? OR cpf = ? OR placa = ?"
            cursor.execute(query, (id_cotacao, cpf, placa))
            cotacao = cursor.fetchone()  # busca primeira linha 

            # verifica
            if cotacao:
                cotacao_data = {
                    'id_cotacao': cotacao[0],
                    'placa': cotacao[1],
                    'cpf': cotacao[2],
                    'data_inicio': cotacao[3],
                    'data_termino': cotacao[4],
                    'vencimento': cotacao[5],
                    'valor': cotacao[6]
                }
                return render_template('consultar_cotação1.html', cotacao=cotacao_data)
            else:
                return render_template('consultar_cotação1.html', erro="Cotação não encontrada.")

        except sqlite3.Error as e:
            return render_template('consultar_cotação1.html', erro="Erro ao consultar o banco de dados.")

        finally:
            banco.close()
   
    return render_template('/consultar_cotação1.html')

#consultar2
@app.route('/consultar_cliente2.html')
def consultarCliente2():
    return render_template('/consultar_cliente2.html')

@app.route('/consultar_veículo2.html')
def consultarVeiculo2():
    return render_template('/consultar_veículo2.html')

@app.route('/consultar_seguradora2.html')
def consultarSeguradora2():
    return render_template('/consultar_seguradora2.html')

@app.route('/consultar_seguros2.html')
def consultarSeguros2():
    return render_template('/consultar_seguros2.html')

@app.route('/consultar_cotações2.html')
def consultarCotacoes2():
    return render_template('/consultar_cotações2.html')

#visualizar
@app.route('/visualizar_cliente.html')
def visualizarCliente():
    return render_template('/visualizar_cliente.html')

@app.route('/visualizar_veículo.html')
def visualizarVeiculo():
    return render_template('/visualizar_veículo.html')

@app.route('/visualizar_seguradora.html')
def visualizarSeguradora():
    return render_template('/visualizar_seguradora.html')

@app.route('/visualizar_seguros.html')
def visualizarSeguros():
    return render_template('/visualizar_seguros.html')

@app.route('/visualizar_cotações.html')
def visualizarCotacoes():
    return render_template('/visualizar_cotações.html')

#Sucesso
@app.route('/sucesso.html')
def sucesso():
    return render_template('/sucesso.html')
