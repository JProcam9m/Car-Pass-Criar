from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# --- SIMULAÇÃO DE BANCO DE DATA ---

minha_frota = [
    {
        'modelo': 'Toyota Corolla', 
        'chassi': '9BW-COR-2026', 
        'status_rastreio': 'Ativo', 
        'token': 'CP-8877',
        'status_uso': 'Disponível',
        'imagem': 'corolla.jpg'
    },
    {
        'modelo': 'HB20 2024 Manual', 
        'chassi': '9BW-HB20-2024', 
        'status_rastreio': 'Chip Solicitado', 
        'token': None,
        'status_uso': 'Em Aula',
        'imagem': 'hb20.jpg'
    }
]

dados_instrutor = {
    'nome': 'João da Silva Oliveira',
    'cnh': '00987654321',
    'categoria': 'AD',
    'total_alunos': 47, 
    'aprovados': 38,
    'media_aulas': 22
}

# Dados para a Agenda e Solicitações (Novidade)
agenda_aulas = [
    {'id': 1, 'aluno': 'Ricardo Silva', 'horario': '08:00', 'veiculo': 'HB20', 'info': 'Aula 12/20'},
    {'id': 2, 'aluno': 'Amanda Costa', 'horario': '10:30', 'veiculo': 'Corolla', 'info': 'Simulado'}
]

solicitacoes_pendentes = [
    {'id': 101, 'aluno': 'Pedro Santos', 'data': '05/02', 'horario': '14:00', 'veiculo': 'HB20'}
]

# --- ROTAS ---

@app.route('/')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', frota=minha_frota)

@app.route('/instrutordb')
def instrutor_dashboard():
    # Agora passamos também a agenda e as solicitações para o HTML
    return render_template('instrutor_dashboard.html', 
                           instrutor=dados_instrutor,
                           agenda=agenda_aulas,
                           solicitacoes=solicitacoes_pendentes)

@app.route('/cadastrar')
def cadastrar():
    return render_template('cadastro.html')

@app.route('/salvar_veiculo', methods=['POST'])
def salvar_veiculo():
    modelo = request.form.get('modelo_veiculo')
    chassi = request.form.get('chassi')
    token = request.form.get('token_rastreador')
    solicitar_chip = request.form.get('solicitar_chip')
    
    if solicitar_chip:
        status_r, token_final = "Chip Solicitado", "PENDENTE"
    else:
        status_r = "Ativo" if token else "Inativo"
        token_final = token if token else None

    novo_veiculo = {
        'modelo': modelo, 'chassi': chassi, 'status_rastreio': status_r,
        'token': token_final, 'status_uso': 'Cadastrado', 'imagem': 'default.jpg'
    }
    
    minha_frota.append(novo_veiculo)
    return redirect(url_for('dashboard'))

# Rota para processar cancelamentos (Exemplo de lógica necessária)
@app.route('/cancelar_aula/<int:aula_id>')
def cancelar_aula(aula_id):
    # Lógica para remover da lista ou marcar como cancelado
    return redirect(url_for('instrutor_dashboard'))

@app.route('/checklist')
def checklist():
    return render_template('checklist.html')

if __name__ == "__main__":
    app.run(debug=True)