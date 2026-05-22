from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd

app = Flask(__name__)
app.secret_key = "chave_secreta"

# Carregar a planilha
df = pd.read_excel("alunos_matricula.xlsx")

# Converter para lista de dicionários
alunos = df.to_dict(orient="records")


# 🔐 ROTA DE LOGIN
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        matricula = request.form["matricula"]
        senha = request.form["senha"]

        for aluno in alunos:
            if str(aluno["Matrícula"]) == matricula and str(aluno["Senha"]) == senha:
                session["aluno"] = aluno
                return redirect(url_for("boas_vindas"))

        return "Matrícula ou senha incorretas"

    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <style>
        body {
            font-family: Arial;
            background: linear-gradient(to right, #4facfe, #00f2fe);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .login-box {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.2);
            text-align: center;
        }

        input {
            width: 80%;
            padding: 10px;
            margin: 10px;
            border-radius: 5px;
            border: 1px solid #ccc;
        }

        button {
            background: #4facfe;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        button:hover {
            background: #00c6ff;
        }
    </style>
</head>

<body>
    <div class="login-box">
        <h2>🎓 Login do Aluno</h2>
        <form method="post">
            <input type="text" name="matricula" placeholder="Matrícula" required><br>
            <input type="password" name="senha" placeholder="Senha" required><br>
            <button type="submit">Entrar</button>
        </form>
    </div>
</body>
</html>
'''


# 🤖 ROTA DO CHAT
@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "aluno" not in session:
        return redirect(url_for("login"))

    aluno = session["aluno"]
    resposta = ""

    if request.method == "POST":
        pergunta = request.form["pergunta"].lower()

        if "pendência" in pergunta:
            resposta = f"Sua pendência é: {aluno.get['Pendências']}"
        
        elif "sala" in pergunta:
            resposta = f"Sua aula é na sala {aluno.get['Sala Atual']}"
        
        elif "horário" in pergunta:
            resposta = f"Seu horário de aula é {aluno.get['Horário Aula']}"
        
        elif "professor" in pergunta:
            resposta = f"Seu professor é {aluno.get['Professor']}"
        
        elif "mensalidade" in pergunta:
            resposta = f"Status da mensalidade: {aluno.get['Mensalidade']}"
        
        elif "curso" in pergunta:
            resposta = f"Seu curso é {aluno.get['Curso']}"

        elif "matrícula ativa" in pergunta or "matricula ativa" in pergunta:
            resposta = f"status da matrícula: {aluno.get['Matrícula Ativa']}"
            
        else:
            resposta = "Desculpe, não entendi sua pergunta."

    return f'''
<!DOCTYPE html>
<html>
<head>
    <title>Chat do Aluno</title>
    <style>
        body {{
            font-family: Arial;
            background: #f0f2f5;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        .chat-container {{
            width: 400px;
            background: white;
            margin-top: 50px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.2);
            padding: 20px;
        }}

        .header {{
            text-align: center;
            margin-bottom: 20px;
        }}

        .messages {{
            height: 200px;
            overflow-y: auto;
            border: 1px solid #ccc;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
        }}

        .user {{
            text-align: right;
            margin: 5px;
            color: blue;
        }}

        .bot {{
            text-align: left;
            margin: 5px;
            color: green;
        }}

        input {{
            width: 70%;
            padding: 10px;
        }}

        button {{
            padding: 10px;
            background: #4facfe;
            color: white;
            border: none;
            border-radius: 5px;
        }}

        button:hover {{
            background: #00c6ff;
        }}

        a {{
            display: block;
            text-align: center;
            margin-top: 10px;
        }}
    </style>
</head>

<body>

<div class="chat-container">
    <div class="header">
        <h3>🎓 {aluno["Nome"]}</h3>
    </div>

    <div class="messages">
        {"<div class='user'>" + pergunta + "</div>" if request.method == "POST" else ""}
        {"<div class='bot'>" + resposta + "</div>" if resposta else ""}
    </div>

    <form method="post">
        <input type="text" name="pergunta" placeholder="Digite sua pergunta..." required>
        <button type="submit">Enviar</button>
    </form>

    <a href="/logout">Sair</a>
</div>

</body>
</html>
'''


# 🚪 LOGOUT
@app.route("/logout")
def logout():
    session.pop("aluno", None)
    return redirect(url_for("login"))


# 🎬 TOUR
@app.route("/tour")
def tour():
    return open("tour.html", encoding="utf-8").read()

# 🏠 TELA DE BOAS-VINDAS
@app.route("/boas_vindas")
def boas_vindas():

    # verifica se o aluno está logado
    if "aluno" not in session:
        return redirect(url_for("login"))

    aluno = session["aluno"]

    return f'''
    <!DOCTYPE html>
    <html lang="pt-br">

    <head>
        <meta charset="UTF-8">
        <title>Bem-vindo</title>

        <style>

            body {{
                margin: 0;
                font-family: 'Segoe UI', Arial, sans-serif;
                background: linear-gradient(to right, #4facfe, #00f2fe);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}

            .box {{
                background: white;
                padding: 40px;
                border-radius: 20px;
                text-align: center;
                box-shadow: 0px 10px 30px rgba(0,0,0,0.2);
                width: 350px;
            }}

            h2 {{
                color: #333;
                margin-bottom: 10px;
            }}

            p {{
                color: #666;
                margin-bottom: 25px;
            }}

            button {{
                width: 100%;
                padding: 14px;
                margin-top: 10px;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                color: white;
                cursor: pointer;
                transition: 0.3s;
            }}

            button:hover {{
                transform: scale(1.03);
            }}

            .tour {{
                background: #4facfe;
            }}

            .tour:hover {{
                background: #008cff;
            }}

            .chat {{
                background: #00c6ff;
            }}

            .chat:hover {{
                background: #0099cc;
            }}

        </style>
    </head>

    <body>

        <div class="box">

            <h2>🎓 Bem-vindo, {aluno["Nome"]}!</h2>

            <p>Escolha uma opção abaixo:</p>

            <!-- BOTÃO TOUR -->
            <a href="/tour">
                <button class="tour">
                    🎬 Fazer Tour
                </button>
            </a>

            <!-- BOTÃO CHAT -->
            <a href="/chat">
                <button class="chat">
                    🤖 Ir direto para o ChatBot
                </button>
            </a>

        </div>

    </body>
    </html>
    '''



# ▶️ RODAR SERVIDOR
if __name__ == "__main__":
   import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
