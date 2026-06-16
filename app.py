import os
import pandas as pd
from flask import Flask, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "troque_por_algo_secreto_em_producao")

df = pd.read_excel("alunos_matricula.xlsx")
alunos = df.to_dict(orient="records")

# ─── Design System — Faculdade de Miguel Pereira ─────────────────────────────
BASE_HEAD = """
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --maroon:    #6d1d20;
    --maroon-dk: #5a1619;
    --maroon-lt: #f5e8e8;
    --gray:      #a59c97;
    --gray-lt:   #e8e4e1;
    --cream:     #f5f3f1;
    --white:     #ffffff;
    --text:      #2a1a1a;
    --muted:     #7a706d;
    --danger:    #b91c1c;
    --radius:    14px;
    --shadow:    0 4px 24px rgba(109,29,32,.10);
    --shadow-lg: 0 12px 40px rgba(109,29,32,.16);
    --font-heading: 'Playfair Display', Georgia, serif;
    --font-body:    'DM Sans', system-ui, sans-serif;
  }

  body { font-family: var(--font-body); color: var(--text); background: var(--cream); }

  .card {
    background: var(--white);
    border-radius: var(--radius);
    box-shadow: var(--shadow-lg);
    overflow: hidden;
  }

  .btn {
    display: inline-flex; align-items: center; justify-content: center; gap: 8px;
    padding: 13px 28px; border: none; border-radius: 10px;
    font-family: var(--font-body); font-size: 15px; font-weight: 600;
    cursor: pointer; text-decoration: none; transition: all .2s ease;
    width: 100%;
  }
  .btn-primary { background: var(--maroon); color: var(--white); }
  .btn-primary:hover { background: var(--maroon-dk); transform: translateY(-1px); box-shadow: 0 6px 20px rgba(109,29,32,.3); }

  input[type="text"], input[type="password"] {
    width: 100%; padding: 13px 16px;
    border: 1.5px solid #ddd6d6; border-radius: 10px;
    font-family: var(--font-body); font-size: 15px; color: var(--text);
    background: var(--white); transition: border-color .2s, box-shadow .2s;
    outline: none;
  }
  input:focus { border-color: var(--maroon); box-shadow: 0 0 0 3px rgba(109,29,32,.10); }

  label { display: block; font-size: 13px; font-weight: 600;
          color: var(--muted); text-transform: uppercase; letter-spacing: .05em; margin-bottom: 6px; }

  a { color: var(--maroon); text-decoration: none; }
  a:hover { text-decoration: underline; }
</style>
"""


# ─── LOGIN ────────────────────────────────────────────────────────────────────
@app.route("/", methods=["GET", "POST"])
def login():
    erro = ""
    if request.method == "POST":
        matricula = request.form.get("matricula", "").strip()
        senha = request.form.get("senha", "").strip()
        for aluno in alunos:
            if str(aluno["Matrícula"]) == matricula and str(aluno["Senha"]) == senha:
                session.clear()
                session["aluno"] = aluno
                return redirect(url_for("boas_vindas"))
        erro = "Matrícula ou senha incorreta. Tente novamente."

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <title>Login · Portal do Aluno · FAMIPE</title>
  {BASE_HEAD}
  <style>
    body {{
      min-height: 100vh;
      display: flex; align-items: center; justify-content: center;
      padding: 24px;
      position: relative; overflow: hidden;
    }}
    body::before {{
      content: '';
      position: fixed; inset: 0;
      background: url('/static/famipe_cleanup.png') center center / cover no-repeat;
      filter: blur(6px) brightness(0.45);
      transform: scale(1.05);
      z-index: 0;
    }}
    .login-card {{ width: 100%; max-width: 400px; position: relative; z-index: 1; }}

    .login-header {{
      background: linear-gradient(160deg, #6d1d20, #8f2629);
      padding: 36px 36px 28px;
      text-align: center; color: var(--white);
      border-bottom: 3px solid rgba(165,156,151,.3);
    }}
    .logo-wrap {{
      margin-bottom: 16px;
    }}
    .logo-wrap img {{
      height: 52px; width: auto;
      filter: brightness(0) invert(1);
      opacity: .92;
    }}
    .login-header p {{
      margin-top: 10px; color: rgba(255,255,255,.65); font-size: 13px;
      font-weight: 500; letter-spacing: .03em;
    }}
    .login-body {{ padding: 32px 36px 36px; }}
    .field {{ margin-bottom: 20px; }}
    .alert-error {{
      display: flex; align-items: center; gap: 10px;
      background: #fef2f2; border: 1.5px solid #fca5a5;
      color: var(--danger); border-radius: 10px;
      padding: 12px 16px; font-size: 14px; font-weight: 500;
      margin-bottom: 20px;
    }}
    .divider {{
      height: 1px; background: var(--gray-lt); margin: 20px 0;
    }}
    .forgot-link {{
      display: block; text-align: center; margin-top: 16px;
      font-size: 13px; color: var(--muted);
    }}
    .forgot-link a {{ color: var(--maroon); font-weight: 600; }}
  </style>
</head>
<body>
  <div class="card login-card">
    <div class="login-header">
      <div class="logo-wrap">
        <img src="/static/horizontal_branca.png" alt="Faculdade de Miguel Pereira">
      </div>
      <p>Portal do Aluno — Acesse sua conta</p>
    </div>
    <div class="login-body">
      {"<div class='alert-error'><span>⚠️</span>" + erro + "</div>" if erro else ""}
      <form method="post" novalidate>
        <div class="field">
          <label for="matricula">Matrícula</label>
          <input type="text" id="matricula" name="matricula"
                 autocomplete="username" required>
        </div>
        <div class="field">
          <label for="senha">Senha</label>
          <input type="password" id="senha" name="senha"
                 placeholder="Sua senha" autocomplete="current-password" required>
        </div>
        <button type="submit" class="btn btn-primary">Entrar →</button>
      </form>
      <p class="forgot-link">Problemas de acesso?
        <a href="mailto:suporte@famipe.edu.br">Fale com a secretaria</a>
      </p>
    </div>
  </div>
</body>
</html>"""


# ─── BOAS-VINDAS ──────────────────────────────────────────────────────────────
@app.route("/boas_vindas")
def boas_vindas():
    if "aluno" not in session:
        return redirect(url_for("login"))
    aluno = session["aluno"]
    primeiro_nome = aluno["Nome"].split()[0]

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <title>Bem-vindo · Portal do Aluno · FAMIPE</title>
  {BASE_HEAD}
  <style>
    body {{
      min-height: 100vh;
      display: flex; flex-direction: column; align-items: center;
      background: var(--cream); padding: 0;
    }}
    .page-header {{
      width: 100%; background: var(--maroon);
      padding: 16px 24px;
      display: flex; align-items: center; justify-content: space-between;
      box-shadow: 0 2px 12px rgba(109,29,32,.3);
    }}
    .page-header img {{ height: 36px; width: auto; filter: brightness(0) invert(1); opacity:.9; }}
    .logout-top {{
      color: rgba(255,255,255,.75); font-size: 13px; font-weight: 600;
      text-decoration: none; transition: color .15s;
    }}
    .logout-top:hover {{ color: var(--white); text-decoration: none; }}

    .welcome-wrap {{
      flex: 1; display: flex; align-items: center; justify-content: center;
      padding: 32px 24px; width: 100%;
    }}
    .welcome-card {{ width: 100%; max-width: 440px; }}
    .welcome-hero {{
      background: linear-gradient(160deg, #6d1d20, #8f2629);
      padding: 36px 36px 32px; text-align: center; color: var(--white);
      position: relative; overflow: hidden;
    }}
    .welcome-hero::before {{
      content: '';
      position: absolute; inset: 0;
      background: radial-gradient(circle at 80% 20%, rgba(165,156,151,.15) 0%, transparent 60%);
    }}
    .avatar {{
      width: 64px; height: 64px; border-radius: 50%;
      background: rgba(255,255,255,.15); border: 2px solid rgba(255,255,255,.3);
      display: flex; align-items: center; justify-content: center;
      font-size: 26px; margin: 0 auto 14px; position: relative;
    }}
    .welcome-hero h1 {{
      font-family: var(--font-heading); font-size: 24px;
      color: var(--white); margin-bottom: 5px;
    }}
    .welcome-hero p {{ color: rgba(255,255,255,.65); font-size: 13px; }}

    .welcome-body {{ padding: 28px 32px 32px; }}
    .info-strip {{
      display: flex; gap: 10px; flex-wrap: wrap;
      background: var(--cream); border-radius: 10px;
      padding: 13px 15px; margin-bottom: 24px;
      border: 1px solid var(--gray-lt);
    }}
    .info-chip {{
      font-size: 12px; font-weight: 600; color: var(--muted);
      display: flex; align-items: center; gap: 4px;
    }}
    .info-chip span {{ color: var(--maroon); }}
    .section-title {{
      font-size: 11px; font-weight: 700; text-transform: uppercase;
      letter-spacing: .08em; color: var(--muted); margin-bottom: 12px;
    }}
    .option-card {{
      display: flex; align-items: center; gap: 15px;
      border: 1.5px solid var(--gray-lt); border-radius: 12px;
      padding: 16px 18px; margin-bottom: 10px;
      text-decoration: none; color: var(--text);
      transition: all .2s ease;
    }}
    .option-card:hover {{
      border-color: var(--maroon);
      box-shadow: 0 4px 16px rgba(109,29,32,.12);
      transform: translateY(-2px); text-decoration: none;
    }}
    .option-icon {{
      width: 46px; height: 46px; border-radius: 11px;
      display: flex; align-items: center; justify-content: center;
      font-size: 20px; flex-shrink: 0;
    }}
    .icon-tour {{ background: var(--maroon-lt); }}
    .icon-chat {{ background: var(--gray-lt); }}
    .option-title {{ font-size: 15px; font-weight: 600; margin-bottom: 2px; }}
    .option-desc {{ font-size: 13px; color: var(--muted); }}
    .option-arrow {{ margin-left: auto; color: var(--gray); font-size: 18px; }}
  </style>
</head>
<body>
  <header class="page-header">
    <img src="/static/horizontal_branca.png" alt="FAMIPE">
    <a href="/logout" class="logout-top">Sair ›</a>
  </header>

  <div class="welcome-wrap">
    <div class="card welcome-card">
      <div class="welcome-hero">
        <div class="avatar">🎓</div>
        <h1>Olá, {primeiro_nome}!</h1>
        <p>O que você gostaria de fazer hoje?</p>
      </div>
      <div class="welcome-body">
        <div class="info-strip">
          <div class="info-chip">📚 <span>{aluno["Curso"]}</span></div>
          <div class="info-chip">🔑 Mat. <span>{aluno["Matrícula"]}</span></div>
          <div class="info-chip">📍 Sala <span>{aluno["Sala Atual"]}</span></div>
          <div class="info-chip">🕐 <span>{aluno["Horário Aula"]}</span></div>
        </div>
        <p class="section-title">Escolha uma opção</p>
        <a href="/tour" class="option-card">
          <div class="option-icon icon-tour">🗺️</div>
          <div>
            <div class="option-title">Tour pela Faculdade</div>
            <div class="option-desc">Explore o mapa interativo do campus</div>
          </div>
          <span class="option-arrow">›</span>
        </a>
        <a href="/chat" class="option-card">
          <div class="option-icon icon-chat">🤖</div>
          <div>
            <div class="option-title">Assistente Acadêmico</div>
            <div class="option-desc">Tire dúvidas sobre sua matrícula</div>
          </div>
          <span class="option-arrow">›</span>
        </a>
      </div>
    </div>
  </div>
</body>
</html>"""


# ─── CHAT ─────────────────────────────────────────────────────────────────────
@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "aluno" not in session:
        return redirect(url_for("login"))
    aluno = session["aluno"]

    if "historico" not in session:
        session["historico"] = []

    if request.method == "POST":
        pergunta = request.form.get("pergunta", "").strip()
        if pergunta:
            p = pergunta.lower()
            if "pendência" in p or "pendencia" in p:
                resposta = f"Sua pendência é: {aluno['Pendências']}"
            elif "sala" in p:
                resposta = f"Sua aula é na sala {aluno['Sala Atual']}"
            elif "horário" in p or "horario" in p:
                resposta = f"Seu horário de aula é {aluno['Horário Aula']}"
            elif "professor" in p:
                resposta = f"Seu professor é {aluno['Professor']}"
            elif "mensalidade" in p:
                resposta = f"Status da mensalidade: {aluno['Mensalidade']}"
            elif "curso" in p:
                resposta = f"Seu curso é {aluno['Curso']}"
            elif "matrícula" in p or "matricula" in p:
                resposta = f"Status da matrícula: {aluno['Matrícula Ativa']}"
            else:
                resposta = "Não entendi. Tente perguntar sobre: sala, horário, professor, mensalidade, pendências ou curso."
            session["historico"].append({"role": "user", "content": pergunta})
            session["historico"].append({"role": "assistant", "content": resposta})
            session.modified = True
        return redirect(url_for("chat"))

    historico = session.get("historico", [])

    def render_msgs():
        html = ""
        for msg in historico:
            if msg["role"] == "user":
                html += f'<div class="msg-row user-row"><div class="bubble user-bubble">{msg["content"]}</div></div>'
            else:
                html += f'<div class="msg-row bot-row"><div class="bubble-avatar">🤖</div><div class="bubble bot-bubble">{msg["content"]}</div></div>'
        return html or '<div class="empty-state">👋 Olá! Pergunte sobre sua matrícula, sala, horário, pendências ou mensalidade.</div>'

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <title>Assistente · Portal do Aluno · FAMIPE</title>
  {BASE_HEAD}
  <style>
    body {{
      min-height: 100vh; display: flex; flex-direction: column;
      background: var(--cream); padding: 0;
    }}
    .topbar {{
      background: var(--maroon); color: var(--white);
      display: flex; align-items: center; gap: 14px;
      padding: 14px 20px; box-shadow: 0 2px 8px rgba(109,29,32,.3);
      flex-shrink: 0;
    }}
    .topbar-back {{
      color: rgba(255,255,255,.7); font-size: 22px;
      text-decoration: none; transition: color .15s; line-height: 1;
    }}
    .topbar-back:hover {{ color: var(--white); text-decoration: none; }}
    .topbar-logo {{ flex: 1; display: flex; align-items: center; }}
    .topbar-logo img {{ height: 28px; width: auto; max-width: 180px; object-fit: contain; filter: brightness(0) invert(1); opacity:.85; }}
    .topbar-sub {{ font-size: 12px; color: rgba(255,255,255,.6); white-space: nowrap; }}
    .topbar-clear {{
      background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.2);
      color: rgba(255,255,255,.85); border-radius: 8px; padding: 6px 11px;
      font-size: 12px; font-weight: 600; cursor: pointer; text-decoration: none;
      transition: all .15s; white-space: nowrap;
    }}
    .topbar-clear:hover {{ background: rgba(255,255,255,.22); color: var(--white); text-decoration: none; }}

    .chat-area {{
      flex: 1; overflow-y: auto; padding: 20px 16px;
      display: flex; flex-direction: column; gap: 12px;
      max-width: 680px; width: 100%; margin: 0 auto;
    }}
    .msg-row {{ display: flex; align-items: flex-end; gap: 8px; }}
    .user-row {{ justify-content: flex-end; }}
    .bot-row  {{ justify-content: flex-start; }}
    .bubble {{
      max-width: 75%; padding: 11px 15px; border-radius: 18px;
      font-size: 14px; line-height: 1.55;
    }}
    .user-bubble {{
      background: var(--maroon); color: var(--white);
      border-bottom-right-radius: 4px;
    }}
    .bot-bubble {{
      background: var(--white); color: var(--text);
      border: 1.5px solid var(--gray-lt); border-bottom-left-radius: 4px;
      box-shadow: 0 1px 4px rgba(0,0,0,.06);
    }}
    .bubble-avatar {{
      width: 30px; height: 30px; border-radius: 50%;
      background: var(--gray-lt); display: flex; align-items: center;
      justify-content: center; font-size: 15px; flex-shrink: 0;
    }}
    .empty-state {{
      text-align: center; color: var(--muted); font-size: 14px;
      padding: 32px 16px; background: var(--white); border-radius: 12px;
      border: 1.5px dashed var(--gray-lt);
    }}
    .quick-chips {{
      display: flex; flex-wrap: wrap; gap: 8px;
      max-width: 680px; width: 100%; margin: 0 auto;
      padding: 0 16px 12px;
    }}
    .chip {{
      background: var(--white); border: 1.5px solid var(--gray-lt);
      border-radius: 20px; padding: 6px 14px; font-size: 12px;
      font-weight: 500; color: var(--maroon); cursor: pointer;
      transition: all .15s; font-family: var(--font-body);
    }}
    .chip:hover {{ background: var(--maroon); color: var(--white); border-color: var(--maroon); }}
    .input-bar {{
      background: var(--white); border-top: 1.5px solid var(--gray-lt);
      padding: 12px 16px; flex-shrink: 0;
    }}
    .input-row {{
      display: flex; gap: 10px; max-width: 680px; margin: 0 auto;
    }}
    .input-row input {{ flex: 1; padding: 12px 16px; border-radius: 12px; }}
    .send-btn {{
      background: var(--maroon); color: var(--white); border: none;
      border-radius: 12px; padding: 0 20px; font-size: 18px;
      cursor: pointer; transition: all .2s; flex-shrink: 0;
    }}
    .send-btn:hover {{ background: var(--maroon-dk); transform: scale(1.05); }}
  </style>
</head>
<body>
  <div class="topbar">
    <a href="/boas_vindas" class="topbar-back" aria-label="Voltar">‹</a>
    <div class="topbar-logo"><img src="/static/horizontal_branca.png" alt="FAMIPE"></div>
    <span class="topbar-sub">{aluno["Nome"].split()[0]}</span>
    <a href="/limpar_chat" class="topbar-clear">🗑 Limpar</a>
  </div>

  <div class="chat-area" id="chat-area">
    {render_msgs()}
  </div>

  {"" if historico else '''
  <div class="quick-chips" id="chips">
    <button class="chip" onclick="sendChip(this)">📅 Meu horário</button>
    <button class="chip" onclick="sendChip(this)">📍 Minha sala</button>
    <button class="chip" onclick="sendChip(this)">⚠️ Minhas pendências</button>
    <button class="chip" onclick="sendChip(this)">💰 Status da mensalidade</button>
    <button class="chip" onclick="sendChip(this)">👨‍🏫 Meu professor</button>
    <button class="chip" onclick="sendChip(this)">📖 Meu curso</button>
  </div>
  '''}

  <div class="input-bar">
    <form method="post" class="input-row" id="form">
      <input type="text" name="pergunta" id="pergunta"
             placeholder="Digite sua pergunta..." autocomplete="off" required>
      <button type="submit" class="send-btn" aria-label="Enviar">↑</button>
    </form>
  </div>

  <script>
    var ca = document.getElementById('chat-area');
    if (ca) ca.scrollTop = ca.scrollHeight;
    function sendChip(btn) {{
      var text = btn.textContent.replace(/^\\S+\\s*/, '').trim();
      document.getElementById('pergunta').value = text;
      var chips = document.getElementById('chips');
      if (chips) chips.style.display = 'none';
      document.getElementById('form').submit();
    }}
  </script>
</body>
</html>"""


@app.route("/limpar_chat")
def limpar_chat():
    session.pop("historico", None)
    return redirect(url_for("chat"))


# ─── TOUR ─────────────────────────────────────────────────────────────────────
@app.route("/tour")
def tour():
    return open("tour.html", encoding="utf-8").read()


# ─── LOGOUT ───────────────────────────────────────────────────────────────────
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ─── SERVIDOR ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
