import streamlit as st
from groq import Groq
from datetime import datetime
import json
import re

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="CLÁSSICAS MOTOS IA", layout="wide")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@400;500;600&display=swap');

    .stApp { background-color: #FFFFFF; color: #000000; font-family: 'DM Sans', sans-serif; }
    [data-testid="stSidebar"] { display: none; }

    .stTextInput>div>div>input,
    .stTextArea>div>textarea,
    .stSelectbox>div>div>div {
        background-color: #FEF2F2 !important;
        color: #000000 !important;
        border: 1px solid #B91C1C !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    .stButton>button {
        width: 100%; border-radius: 12px; height: 3.5em;
        background: linear-gradient(135deg, #7F1D1D, #B91C1C) !important;
        color: white !important; font-weight: 600; border: none;
        box-shadow: 2px 2px 8px rgba(127,29,29,0.25);
        font-family: 'DM Sans', sans-serif !important;
        transition: all 0.2s ease;
    }
    .stButton>button *, .stButton>button p { color: white !important; }
    .stButton>button:hover { background: linear-gradient(135deg, #5F1414, #7F1D1D) !important; transform: translateY(-1px); }

    h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: #1A1A2E !important; }
    p, span, label, div { color: #1A1A2E !important; font-family: 'DM Sans', sans-serif; }

    .card {
        background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
        padding: 22px; border-radius: 16px;
        border: 1px solid #B91C1C; margin-bottom: 15px;
        color: #1A1A2E; box-shadow: 0 2px 12px rgba(127,29,29,0.08);
        white-space: pre-wrap;
    }
    .card-dark {
        background: linear-gradient(135deg, #1C0606 0%, #150404 100%);
        padding: 22px; border-radius: 16px;
        border: 1px solid #B91C1C; margin-bottom: 15px;
        white-space: pre-wrap;
    }
    .card-dark, .card-dark * { color: #FECACA !important; }

    .card-green { background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%); padding: 22px; border-radius: 16px; border: 1px solid #86EFAC; margin-bottom: 15px; white-space: pre-wrap; }
    .card-blue { background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%); padding: 22px; border-radius: 16px; border: 1px solid #93C5FD; margin-bottom: 15px; white-space: pre-wrap; }
    .card-purple { background: linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 100%); padding: 22px; border-radius: 16px; border: 1px solid #C4B5FD; margin-bottom: 15px; white-space: pre-wrap; }
    .card-orange { background: linear-gradient(135deg, #FFF7ED 0%, #FFEDD5 100%); padding: 22px; border-radius: 16px; border: 1px solid #FDBA74; margin-bottom: 15px; white-space: pre-wrap; }
    .card-gold { background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%); padding: 22px; border-radius: 16px; border: 2px solid #D97706; margin-bottom: 15px; white-space: pre-wrap; }
    .card-teal { background: linear-gradient(135deg, #F0FDFA 0%, #CCFBF1 100%); padding: 22px; border-radius: 16px; border: 1px solid #5EEAD4; margin-bottom: 15px; white-space: pre-wrap; }

    .indice-box { border-radius: 18px; padding: 24px; text-align: center; margin: 14px 0; border: 2px solid; }
    .indice-alto { background: linear-gradient(135deg,#F0FDF4,#DCFCE7); border-color:#22C55E; }
    .indice-medio { background: linear-gradient(135deg,#FFFBEB,#FEF3C7); border-color:#F59E0B; }
    .indice-baixo { background: linear-gradient(135deg,#FEF2F2,#FEE2E2); border-color:#EF4444; }
    .indice-titulo { font-family:'Playfair Display',serif; font-size:1.5em; font-weight:700; }

    .badge { background: #7F1D1D; color: white !important; padding: 4px 14px; border-radius: 20px; font-size: 0.78em; font-weight: 600; display: inline-block; margin: 2px; }
    .badge-verde { background: #059669; color: white !important; padding: 4px 14px; border-radius: 20px; font-size: 0.78em; font-weight: 600; display: inline-block; margin: 2px; }
    .badge-vermelho { background: #DC2626; color: white !important; padding: 4px 14px; border-radius: 20px; font-size: 0.78em; font-weight: 600; display: inline-block; margin: 2px; }
    .badge-amarelo { background: #D97706; color: white !important; padding: 4px 14px; border-radius: 20px; font-size: 0.78em; font-weight: 600; display: inline-block; margin: 2px; }
    .badge-dourado { background: linear-gradient(135deg,#D97706,#F59E0B); color: white !important; padding: 4px 14px; border-radius: 20px; font-size: 0.78em; font-weight: 700; display: inline-block; margin: 2px; }

    .stat-box { background: #FEF2F2; border-radius: 12px; padding: 18px; text-align: center; border: 1px solid #B91C1C; }
    .stat-numero { font-size: 2em; font-weight: 700; color: #7F1D1D !important; font-family: 'Playfair Display', serif; }

    .hist-item { background: #FEF2F2; border-radius: 10px; padding: 12px 16px; margin-bottom: 8px; border-left: 4px solid #B91C1C; }

    .perfil-btn>button { background: linear-gradient(135deg, #7F1D1D, #B91C1C) !important; color: white !important; font-weight: 700 !important; border-radius: 12px !important; height: 3em !important; }
    .perfil-btn>button *, .perfil-btn>button p { color: white !important; }

    .disclaimer { background: #FFFBEB; border: 1px solid #FDE68A; border-radius: 10px; padding: 12px 16px; font-size: 0.8em; color: #92400E; margin-top: 14px; line-height: 1.6; }
    .disclaimer-avaliacao { background: #FEF2F2; border: 2px solid #EF4444; border-radius: 12px; padding: 14px 18px; margin-bottom: 16px; font-size: 0.86em; color: #991B1B; line-height: 1.6; }

    .divider { border: none; height: 1px; background: linear-gradient(to right, transparent, #B91C1C, transparent); margin: 20px 0; }
    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CACHE
# ─────────────────────────────────────────────
@st.cache_resource
def get_cache_motos():
    return {"perfis": {}}

_cache = get_cache_motos()

# ─────────────────────────────────────────────
# PERSISTÊNCIA LOCAL (JSON)
# ─────────────────────────────────────────────
CHAVES_SALVAR = [
    'usuario', 'historico_consultas', 'consultas_salvas',
    'moto_padrao', 'diario_restauracao', 'quiz_pontuacao', 'quiz_nivel_atual',
]

def gerar_json_sessao() -> str:
    dados = {k: st.session_state.get(k) for k in CHAVES_SALVAR}
    dados['salvo_em'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)

def carregar_json_sessao(dados: dict):
    for k in CHAVES_SALVAR:
        if k in dados:
            st.session_state[k] = dados[k]

def salvar_perfil_cache(usuario: str):
    _cache["perfis"][usuario] = {k: st.session_state.get(k) for k in CHAVES_SALVAR}

def perfis_salvos() -> list:
    return list(_cache["perfis"].keys())

def carregar_perfil_cache(usuario: str) -> dict | None:
    return _cache["perfis"].get(usuario)

def salvar_consulta(modulo: str, tema: str, conteudo: str):
    st.session_state.historico_consultas.append({
        'data': datetime.now().strftime('%d/%m %H:%M'), 'modulo': modulo, 'tema': tema, 'conteudo': conteudo,
    })

# --- INICIALIZAÇÃO DE ESTADO ---
defaults = {
    'etapa': "Login", 'usuario': "", 'api_key': "", 'pagina': "Home",
    'historico_consultas': [], 'consultas_salvas': [],
    'moto_padrao': "", 'diario_restauracao': [], 'quiz_pontuacao': 0, 'quiz_nivel_atual': "Iniciante",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- PRINCÍPIO DE HONESTIDADE TÉCNICA — compartilhado ---
PRINCIPIO_HONESTIDADE = """
PRINCÍPIO OBRIGATÓRIO DE HONESTIDADE TÉCNICA — siga isso em TODA resposta:
- Você é um especialista em motocicletas clássicas, mas trabalha apenas com DESCRIÇÕES EM TEXTO fornecidas pela pessoa —
  você não recebe fotos reais nem tem acesso a bancos de dados de chassi, leilões ou cotações em tempo real
- Para análises de originalidade, peças e autenticidade: baseie-se no que foi DESCRITO pela pessoa, sempre deixando claro
  que é uma orientação educativa, e que avaliação presencial por especialista é necessária para decisões de compra,
  venda ou certificação
- Para certificação de coleção: explique os critérios GERAIS normalmente considerados, mas seja claro que a certificação
  oficial é feita por entidades específicas (clubes de marca, federações de veículos antigos) com vistoria presencial —
  sua análise é apenas uma pré-avaliação educativa, nunca uma garantia de aprovação
- Para valores e valorização de mercado: você NÃO tem acesso a cotações atuais nem dados de leilões em tempo real.
  Baseie-se em padrões históricos conhecidos do mercado de motos clássicas e tendências gerais, sempre recomendando
  confirmar valores com tabelas especializadas, avaliadores profissionais e anúncios reais do mercado antes de
  qualquer decisão financeira
- Nunca afirme um valor exato de mercado como fato — sempre apresente faixas e como estimativas
- Para diagnóstico mecânico: sempre recomende confirmação com mecânico especializado em motos clássicas antes de
  intervenções, especialmente em itens de segurança (freios, suspensão, pneus)
- Para roteiros de viagem: você não tem dados em tempo real sobre condições de estradas, postos ou hospedagens —
  recomende sempre confirmar informações atualizadas antes de viajar
- Seja apaixonado e didático — você é um conhecedor que genuinamente ama motocicletas clássicas, não um robô burocrático
- Português do Brasil
"""

DISCLAIMER_PADRAO = """
<div class="disclaimer">
⚠️ <strong>Importante:</strong> esta análise é educativa, baseada na descrição fornecida — não substitui avaliação
presencial por especialista, perito ou avaliador profissional. Para decisões de compra, venda, restauração ou
certificação, sempre confirme com profissionais qualificados.
</div>
"""

DISCLAIMER_AVALIACAO = """
<div class="disclaimer-avaliacao">
💰 <strong>Sobre valores de mercado:</strong> esta é uma estimativa educativa baseada em padrões históricos gerais —
não reflete cotações em tempo real. Antes de comprar, vender ou negociar, consulte tabelas especializadas,
avaliadores e anúncios reais de motos similares no mercado atual.
</div>
"""

# --- MOTOR DE IA ---
def motos_ia(prompt: str, system_extra: str = "") -> str:
    try:
        client = Groq(api_key=st.session_state.api_key)
        system = f"""Você é o maior especialista em motocicletas clássicas do Brasil — um misto de restaurador
experiente, historiador, mecânico especializado em motos antigas e avaliador de mercado.
Usuário: {st.session_state.usuario}. Moto de interesse: {st.session_state.moto_padrao or 'não informada'}.
{PRINCIPIO_HONESTIDADE}
{system_extra}"""
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

def renderizar_indice(texto: str, titulo_indice: str = "ÍNDICE"):
    percentuais = re.findall(r'(\d+)\s*/\s*100|(\d+)%', texto)
    valores = [int(a or b) for a, b in percentuais if a or b]
    indice = valores[0] if valores else 50

    if indice >= 70:
        classe, emoji, label = "indice-alto", "🟢", "ALTO"
    elif indice >= 40:
        classe, emoji, label = "indice-medio", "🟡", "MÉDIO"
    else:
        classe, emoji, label = "indice-baixo", "🔴", "BAIXO"

    st.markdown(f"""
    <div class="indice-box {classe}">
        <div style="font-size:2.2em;">{emoji}</div>
        <div class="indice-titulo">{titulo_indice}: {indice}/100</div>
        <div style="font-size:0.95em;color:#444;font-weight:600;">Nível: {label}</div>
        <div style="font-size:0.82em;color:#555;margin-top:6px;">Estimativa educativa baseada na descrição fornecida</div>
    </div>
    """, unsafe_allow_html=True)

# --- BARRA DE SALVAR ---
def barra_salvar():
    salvar_perfil_cache(st.session_state.usuario)
    nome_usuario = st.session_state.usuario.lower().replace(' ', '_') or 'minha_sessao'
    total = len(st.session_state.historico_consultas)
    diario = len(st.session_state.diario_restauracao)

    col_info, col_btn = st.columns([4, 2])
    with col_info:
        st.markdown(
            f"<div style='background:#FEF2F2;border:1px solid #B91C1C;border-radius:10px;"
            f"padding:10px 14px;font-size:0.84em;color:#1A1A2E;line-height:1.6;'>"
            f"💾 <strong>Antes de sair, salve seus dados no computador.</strong><br>"
            f"<span style='color:#888;font-size:0.88em;'>{total} consultas geradas · {diario} entradas no diário de restauração</span>"
            f"</div>", unsafe_allow_html=True
        )
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button("💾 SALVAR MEUS DADOS (.json)", data=gerar_json_sessao(),
            file_name=f"classicas_motos_{nome_usuario}.json", mime="application/json", use_container_width=True)
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ============================================================
# TELA: LOGIN
# ============================================================
if st.session_state.etapa == "Login":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.title("🏍️ CLÁSSICAS MOTOS IA")
        st.markdown("**O Maior Especialista em Motos Clássicas — restaurador, historiador e avaliador disponível 24h**")

        st.markdown("""<div style="background:#FEF2F2;border:1px solid #B91C1C;border-radius:10px;
        padding:10px 16px;margin:10px 0 16px 0;font-size:0.88em;color:#1A1A2E;line-height:1.6;">
        🔒 <strong>ACESSO RESTRITO A CLIENTES DO QUIZ COM PRÊMIOS</strong><br>
        🔗 <a href="https://quizcompremios.com.br/" target="_blank"
        style="color:#7F1D1D;font-weight:600;text-decoration:none;">quizcompremios.com.br</a>
        </div>""", unsafe_allow_html=True)

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)

        perfis = perfis_salvos()
        if perfis:
            st.markdown("#### 🏍️ Clássicas Motos — clique para acessar seus dados")
            chave_rapida = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_rapida")
            for nome_p in perfis:
                dados_p = carregar_perfil_cache(nome_p)
                total_p = len(dados_p.get('historico_consultas', [])) if dados_p else 0
                moto_p = dados_p.get('moto_padrao', '') if dados_p else ''
                st.markdown('<div class="perfil-btn">', unsafe_allow_html=True)
                if st.button(f"🏍️ {nome_p}  —  {total_p} consultas  {('· ' + moto_p) if moto_p else ''}", key=f"perfil_{nome_p}", use_container_width=True):
                    if not chave_rapida.strip():
                        st.warning("Cole sua chave API acima antes de entrar.")
                    else:
                        st.session_state.usuario = nome_p
                        st.session_state.api_key = chave_rapida
                        carregar_json_sessao(dados_p)
                        st.session_state.etapa = "App"
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown("**Ou entre com outro nome:**")

        nome  = st.text_input("Seu Nome:")
        chave = st.text_input("Sua Chave API da Groq:", type="password", key="chave_nova")

        if not perfis:
            st.markdown("""<div style="background:#FEF2F2;border:1px solid #B91C1C;border-radius:10px;
            padding:12px 16px;font-size:0.86em;color:#1A1A2E;line-height:1.7;margin:10px 0;">
            📥 <strong>Seus dados sumiram?</strong> Selecione abaixo o arquivo <strong>.json</strong> que você salvou antes.
            </div>""", unsafe_allow_html=True)
            arq_login = st.file_uploader("Carregar meus dados salvos (.json):", type=["json"], key="upload_login")
        else:
            arq_login = None

        dados_login = None
        if arq_login is not None:
            try:
                dados_login = json.load(arq_login)
                st.success(f"✅ Dados de **{dados_login.get('usuario','')}** reconhecidos! Clique em Entrar.")
            except Exception:
                st.error("Arquivo inválido.")
                dados_login = None

        if st.button("✨ ENTRAR NA GARAGEM"):
            if nome and chave:
                st.session_state.usuario = nome
                st.session_state.api_key = chave
                if dados_login:
                    carregar_json_sessao(dados_login)
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

        st.markdown("🔑 Não tem chave Groq? Crie grátis em <a href='https://console.groq.com/keys' target='_blank' style='color:#7F1D1D;font-weight:600;'>console.groq.com/keys</a>", unsafe_allow_html=True)

# ============================================================
# TELA: APP
# ============================================================
elif st.session_state.etapa == "App":

    barra_salvar()

    cols1 = st.columns(7)
    paginas1 = [("🏠","Home"),("🏍️","Identificacao"),("📸","Originalidade"),("🔎","Detector"),("🎨","Cores"),("🏆","Indice"),("💰","Avaliacao")]
    labels1 = {"Home":"Painel Principal","Identificacao":"Identificação Completa","Originalidade":"Scanner de Originalidade",
               "Detector":"Detector de Peças Não Originais","Cores":"Cores Originais","Indice":"Índice do Colecionador","Avaliacao":"Avaliação Inteligente"}
    for i,(icone,pag) in enumerate(paginas1):
        if cols1[i].button(icone, key=f"nav1_{pag}", help=labels1[pag]):
            st.session_state.pagina = pag
            st.rerun()

    cols2 = st.columns(7)
    paginas2 = [("🛠️","Restauracao"),("🔧","Diagnostico"),("📦","Pecas"),("🧾","Documentacao"),("🏅","Certificacao"),("💎","Radar"),("🏁","Timeline")]
    labels2 = {"Restauracao":"Planejamento da Restauração","Diagnostico":"Diagnóstico Mecânico","Pecas":"Guia de Peças",
               "Documentacao":"Documentação","Certificacao":"Simulador de Certificação","Radar":"Radar do Colecionador","Timeline":"Linha do Tempo"}
    for i,(icone,pag) in enumerate(paginas2):
        if cols2[i].button(icone, key=f"nav2_{pag}", help=labels2[pag]):
            st.session_state.pagina = pag
            st.rerun()

    cols3 = st.columns(7)
    paginas3 = [("🌎","Historia"),("🏕️","Diario"),("🔊","Som"),("🧠","Quiz"),("🔬","Engenharia"),("🧬","DNA"),("🏁","Competicoes")]
    labels3 = {"Historia":"História da Motocicleta","Diario":"Diário da Restauração","Som":"Som Original","Quiz":"Quiz do Motociclista",
               "Engenharia":"Engenharia Explicada","DNA":"DNA da Motocicleta","Competicoes":"História nas Competições"}
    for i,(icone,pag) in enumerate(paginas3):
        if cols3[i].button(icone, key=f"nav3_{pag}", help=labels3[pag]):
            st.session_state.pagina = pag
            st.rerun()

    cols4 = st.columns(4)
    paginas4 = [("🌍","Viagens"),("🤝","Clube"),("🤖","Consultor"),("📚","Biblioteca")]
    labels4 = {"Viagens":"Viagens Clássicas","Clube":"Clube do Colecionador","Consultor":"Consultor 24 Horas","Biblioteca":"Biblioteca de Consultas"}
    for i,(icone,pag) in enumerate(paginas4):
        if cols4[i].button(icone, key=f"nav4_{pag}", help=labels4[pag]):
            st.session_state.pagina = pag
            st.rerun()

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # ========================
    # HOME
    # ========================
    if st.session_state.pagina == "Home":
        col_u, col_r = st.columns([3, 1])
        with col_u:
            st.title(f"Olá, {st.session_state.usuario}! 🏍️")
            st.markdown("<span class='badge'>Garagem Aberta</span>", unsafe_allow_html=True)
        with col_r:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚪 Sair"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()

        if len(st.session_state.historico_consultas) == 0:
            st.markdown("""<div style="background:#FEF3C7;border:2px solid #F59E0B;border-radius:12px;
            padding:12px 18px;margin-bottom:4px;color:#000;font-size:0.9em;font-weight:600;">
            ⚠️ Seus dados não estão mais no servidor.
            </div>""", unsafe_allow_html=True)
            arq_home = st.file_uploader("Carregar meus dados salvos (.json):", type=["json"], key="upload_home")
            if arq_home is not None:
                try:
                    dados_home = json.load(arq_home)
                    carregar_json_sessao(dados_home)
                    salvar_perfil_cache(st.session_state.usuario)
                    st.success("✅ Dados recuperados!")
                    st.rerun()
                except Exception:
                    st.error("Arquivo inválido.")
            st.markdown("<br>", unsafe_allow_html=True)

        st.session_state.moto_padrao = st.text_input("🏍️ Sua moto (modelo e ano):",
            value=st.session_state.moto_padrao, placeholder="ex: Honda CB 450 1975, Yamaha RD 350 1980, Harley Shovelhead...")

        st.markdown("<br>", unsafe_allow_html=True)

        modulos_count = {}
        for c in st.session_state.historico_consultas:
            modulos_count[c['modulo']] = modulos_count.get(c['modulo'], 0) + 1

        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.historico_consultas)}</div><div>Consultas geradas</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.diario_restauracao)}</div><div>Registros de restauração</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.consultas_salvas)}</div><div>Salvas</div></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.quiz_pontuacao}</div><div>Pontos no Quiz</div></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='card'>💡 <em>'Uma moto clássica não se guia apenas com as mãos — se guia com o coração.'</em></div>", unsafe_allow_html=True)

        st.markdown("### 🗺️ O que cada módulo faz")
        guia = {
            "🏍️ Identificação": "História, especificações, motor e curiosidades de qualquer modelo/ano",
            "📸 Scanner de Originalidade": "Descreva a moto e receba índice educativo de originalidade",
            "🔎 Detector de Peças": "Identifica possíveis incompatibilidades com base na descrição",
            "🎨 Cores Originais": "Cores de fábrica, códigos de tinta e combinações por ano",
            "🏆 Índice do Colecionador": "Nota completa considerando originalidade, conservação e raridade",
            "💰 Avaliação Inteligente": "Estimativa de valor considerando múltiplos fatores do mercado de clássicas",
            "🛠️ Planejamento da Restauração": "Ordem ideal de serviços, tempo e custos estimados",
            "🔧 Diagnóstico Mecânico": "Descreva um problema e receba possíveis causas",
            "📦 Guia de Peças": "Originais vs reproduzidas, compatibilidade e onde procurar",
            "🧾 Documentação": "Transferência, placa de coleção, regularização, importação",
            "🏅 Simulador de Certificação": "Pré-avaliação educativa dos critérios de certificação para coleção",
            "💎 Radar do Colecionador": "Tendências, valorização e oportunidades no mercado de clássicas",
            "🏁 Linha do Tempo": "Evolução do modelo ano a ano",
            "🌎 História da Motocicleta": "Origem, fabricante, designers e curiosidades",
            "🏕️ Diário da Restauração": "Registre gastos, peças e etapas do seu projeto",
            "🔊 Som Original": "Como era o ronco original do motor e escapamento de fábrica",
            "🧠 Quiz do Motociclista": "Teste seu conhecimento em 5 níveis de dificuldade",
            "🔬 Engenharia Explicada": "2 tempos, 4 tempos, carburador, embreagem — de forma simples",
            "🧬 DNA da Motocicleta": "Viagem no tempo até a época em que a moto nasceu",
            "🏁 Competições": "Motocross, Enduro, Rally, Dakar — participações e pilotos famosos",
            "🌍 Viagens Clássicas": "Roteiros para rodar com sua moto antiga",
            "🤝 Clube do Colecionador": "Encontros, feiras, clubes e museus",
            "🤖 Consultor 24h": "Pergunte qualquer coisa sobre qualquer moto clássica",
        }
        for aba, desc in guia.items():
            st.markdown(f"**{aba}** — {desc}")

        if st.session_state.historico_consultas:
            st.markdown("### 🕐 Últimas Consultas")
            for item in reversed(st.session_state.historico_consultas[-4:]):
                st.markdown(f"<div class='hist-item'><span class='badge'>{item['modulo']}</span> <small style='color:#888'>{item['data']}</small><br><small>{item['tema'][:80]}</small></div>", unsafe_allow_html=True)

    # ========================
    # IDENTIFICAÇÃO COMPLETA
    # ========================
    elif st.session_state.pagina == "Identificacao":
        st.header("🏍️ Identificação Completa")
        st.markdown("Informe modelo e ano para uma análise histórica e técnica completa.")

        col1, col2 = st.columns(2)
        with col1:
            modelo_id = st.text_input("🏍️ Modelo:", value=st.session_state.moto_padrao.split(' ')[0] if st.session_state.moto_padrao else "", placeholder="ex: CB 450, RD 350, Shovelhead...", key="input_modelo_id")
        with col2:
            ano_id = st.text_input("📅 Ano:", placeholder="ex: 1975")

        if st.button("🏍️ IDENTIFICAR MOTOCICLETA"):
            if modelo_id.strip():
                with st.spinner("Buscando informações..."):
                    prompt = (
                        f"Crie uma identificação completa da motocicleta: {modelo_id} {ano_id}.\n\n"
                        f"FORMATO:\n\n"
                        f"🏍️ {modelo_id.upper()} {ano_id}\n\n"
                        f"📖 HISTÓRIA RESUMIDA:\n[origem e contexto do modelo]\n\n"
                        f"⚙️ ESPECIFICAÇÕES TÉCNICAS:\n[motor, torque, potência, câmbio, peso, consumo — para esse ano específico]\n\n"
                        f"🔧 VERSÕES E OPCIONAIS:\n[versões disponíveis nesse ano e principais opcionais]\n\n"
                        f"🏭 PRODUÇÃO:\n[quantidade produzida aproximada, se conhecida, e países onde foi comercializada]\n\n"
                        f"📈 EVOLUÇÃO:\n[principais diferenças desse ano em relação aos anteriores/seguintes]\n\n"
                        f"💡 CURIOSIDADES:\n[2-3 curiosidades interessantes sobre esse modelo/ano]"
                    )
                    res = motos_ia(prompt)
                    salvar_consulta("Identificacao", f"{modelo_id} {ano_id}", res)
                    st.session_state['ident_temp'] = res
            else:
                st.warning("Informe o modelo.")

        if st.session_state.get('ident_temp'):
            st.markdown(f"<div class='card'>{st.session_state['ident_temp']}</div>", unsafe_allow_html=True)
            st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['ident_temp'], file_name="identificacao.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_ident", use_container_width=True):
                    st.session_state.consultas_salvas.append({'modulo':'Identificacao','tema':f"{modelo_id} {ano_id}" if 'modelo_id' in dir() else '','conteudo':st.session_state['ident_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

    # ========================
    # SCANNER DE ORIGINALIDADE
    # ========================
    elif st.session_state.pagina == "Originalidade":
        st.header("📸 Scanner de Originalidade")
        st.markdown("Descreva a motocicleta em detalhes para uma análise educativa de originalidade.")

        st.info("📝 Este app trabalha por descrição em texto. Quanto mais detalhes você der, melhor a análise.")

        col1, col2 = st.columns(2)
        with col1:
            moto_orig = st.text_input("🏍️ Modelo e ano:", value=st.session_state.moto_padrao)
        with col2:
            cor_orig = st.text_input("🎨 Cor atual:", placeholder="ex: vermelho original")

        descricao_orig = st.text_area("📝 Descreva detalhadamente: pintura, tanque, banco, rodas, painel, guidão, escapamento, farol, lanterna, setas, motor:",
            height=180, placeholder="ex: Pintura vermelha original com pequenos retoques no tanque. Banco original em bom estado. "
                                     "Rodas raiadas originais. Escapamento parece reproduzido. Motor original funcionando...")

        if st.button("📸 ANALISAR ORIGINALIDADE"):
            if descricao_orig.strip():
                with st.spinner("Analisando originalidade..."):
                    prompt = (
                        f"Analise a originalidade desta motocicleta com base na descrição.\n"
                        f"Moto: {moto_orig}. Cor: {cor_orig}.\n"
                        f"Descrição: {descricao_orig}\n\n"
                        f"FORMATO:\n\n"
                        f"📸 ÍNDICE DE ORIGINALIDADE: [X]/100\n"
                        f"[1-2 linhas explicando a estimativa com base no que foi descrito]\n\n"
                        f"✅ ITENS QUE PARECEM ORIGINAIS:\n[com base na descrição]\n\n"
                        f"⚠️ ITENS QUE MERECEM VERIFICAÇÃO:\n[itens com descrição ambígua ou suspeita de não-originalidade]\n\n"
                        f"🔍 O QUE VERIFICAR PRESENCIALMENTE:\n[pontos que só um especialista presencial pode confirmar — números de chassi/motor, código de tinta, etc]\n\n"
                        f"💡 DICA PARA PRÓXIMA ANÁLISE:\n[que outras informações ajudariam a refinar essa análise]"
                    )
                    res = motos_ia(prompt)
                    salvar_consulta("Originalidade", moto_orig, res)
                    st.session_state['orig_temp'] = res
            else:
                st.warning("Descreva a motocicleta.")

        if st.session_state.get('orig_temp'):
            renderizar_indice(st.session_state['orig_temp'], "ÍNDICE DE ORIGINALIDADE")
            st.markdown(f"<div class='card'>{st.session_state['orig_temp']}</div>", unsafe_allow_html=True)
            st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['orig_temp'], file_name="originalidade.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_orig", use_container_width=True):
                    st.session_state.consultas_salvas.append({'modulo':'Originalidade','tema':moto_orig if 'moto_orig' in dir() else '','conteudo':st.session_state['orig_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

    # ========================
    # DETECTOR DE PEÇAS NÃO ORIGINAIS
    # ========================
    elif st.session_state.pagina == "Detector":
        st.header("🔎 Detector de Peças Não Originais")
        st.markdown("Descreva peças específicas para identificar possíveis incompatibilidades.")

        moto_det = st.text_input("🏍️ Modelo e ano:", value=st.session_state.moto_padrao, key="moto_det")
        pecas_det = st.text_area("🔧 Descreva as peças que quer verificar:", height=150,
            placeholder="ex: Escapamento esportivo cromado, guidão tipo dragbar, rodas de liga, banco solo personalizado, farol redondo menor...")

        if st.button("🔎 VERIFICAR COMPATIBILIDADE"):
            if pecas_det.strip() and moto_det.strip():
                with st.spinner("Verificando..."):
                    prompt = (
                        f"Analise se estas peças são compatíveis com a originalidade da motocicleta.\n"
                        f"Moto: {moto_det}.\nPeças descritas: {pecas_det}\n\n"
                        f"FORMATO:\n\n"
                        f"🔎 ANÁLISE DE COMPATIBILIDADE — {moto_det.upper()}\n\n"
                        f"[Para cada peça descrita:]\n"
                        f"🔧 [NOME DA PEÇA]\n"
                        f"Status provável: [Original / Possivelmente não original / Não foi possível avaliar]\n"
                        f"Justificativa: [por que, com base no conhecimento sobre esse modelo/ano]\n\n"
                        f"📋 RESUMO GERAL:\n[conclusão geral sobre o conjunto de peças]\n\n"
                        f"🔍 RECOMENDAÇÃO:\n[o que fazer para confirmar com certeza — pesquisa de catálogo original, comparação com outros exemplares, etc]"
                    )
                    res = motos_ia(prompt)
                    salvar_consulta("Detector", moto_det, res)
                    st.session_state['detector_temp'] = res
            else:
                st.warning("Informe a moto e as peças.")

        if st.session_state.get('detector_temp'):
            st.markdown(f"<div class='card-orange'>{st.session_state['detector_temp']}</div>", unsafe_allow_html=True)
            st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['detector_temp'], file_name="deteccao_pecas.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_det", use_container_width=True):
                    st.session_state.consultas_salvas.append({'modulo':'Detector','tema':moto_det if 'moto_det' in dir() else '','conteudo':st.session_state['detector_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

    # ========================
    # CORES ORIGINAIS
    # ========================
    elif st.session_state.pagina == "Cores":
        st.header("🎨 Cores Originais")
        st.markdown("Descubra as cores de fábrica de qualquer modelo.")

        moto_cor = st.text_input("🏍️ Modelo e ano:", value=st.session_state.moto_padrao, key="moto_cor")

        if st.button("🎨 VER CORES ORIGINAIS"):
            if moto_cor.strip():
                with st.spinner("Buscando cores..."):
                    prompt = (
                        f"Liste as cores originais de fábrica para: {moto_cor}\n\n"
                        f"FORMATO:\n\n"
                        f"🎨 CORES ORIGINAIS — {moto_cor.upper()}\n\n"
                        f"[Para cada cor:]\n"
                        f"🎨 [Nome da cor]\n"
                        f"Código de tinta: [se conhecido]\n"
                        f"Anos de utilização: [período]\n"
                        f"Onde aparecia: [tanque, carenagem, guarda-lamas, etc]\n\n"
                        f"⭐ SÉRIES ESPECIAIS:\n[cores exclusivas de versões especiais/edições limitadas, se houver]\n\n"
                        f"💡 DICA:\n[como verificar a cor original em uma moto restaurada — local da etiqueta/código]"
                    )
                    res = motos_ia(prompt)
                    salvar_consulta("Cores", moto_cor, res)
                    st.session_state['cores_temp'] = res
            else:
                st.warning("Informe a moto.")

        if st.session_state.get('cores_temp'):
            st.markdown(f"<div class='card-blue'>{st.session_state['cores_temp']}</div>", unsafe_allow_html=True)
            st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['cores_temp'], file_name="cores_originais.txt", mime="text/plain")

    # ========================
    # ÍNDICE DO COLECIONADOR
    # ========================
    elif st.session_state.pagina == "Indice":
        st.header("🏆 Índice do Colecionador")
        st.markdown("Avaliação completa considerando 7 critérios fundamentais.")

        moto_idx = st.text_input("🏍️ Modelo e ano:", value=st.session_state.moto_padrao, key="moto_idx")

        col1, col2 = st.columns(2)
        with col1:
            originalidade_idx = st.slider("⭐ Originalidade (sua avaliação):", 0, 10, 5)
            conservacao_idx = st.slider("⭐ Conservação:", 0, 10, 5)
            raridade_idx = st.slider("⭐ Raridade (sua percepção):", 0, 10, 5)
            mecanica_idx = st.slider("⭐ Estado mecânico:", 0, 10, 5)
        with col2:
            estetica_idx = st.slider("⭐ Estado estético:", 0, 10, 5)
            documentacao_idx = st.slider("⭐ Documentação:", 0, 10, 5)
            notas_idx = st.text_area("📝 Observações adicionais:", height=80)

        if st.button("🏆 CALCULAR ÍNDICE COMPLETO"):
            if moto_idx.strip():
                with st.spinner("Calculando..."):
                    prompt = (
                        f"Crie uma avaliação completa de colecionador para esta motocicleta.\n"
                        f"Moto: {moto_idx}.\n"
                        f"Autoavaliação do proprietário: Originalidade {originalidade_idx}/10, Conservação {conservacao_idx}/10, "
                        f"Raridade {raridade_idx}/10, Mecânica {mecanica_idx}/10, Estética {estetica_idx}/10, Documentação {documentacao_idx}/10.\n"
                        f"Observações: {notas_idx or 'nenhuma'}\n\n"
                        f"FORMATO:\n\n"
                        f"🏆 ÍNDICE DO COLECIONADOR: [X]/100\n"
                        f"[Calcule uma nota geral ponderada com base nos 6 critérios + conhecimento sobre raridade real desse modelo]\n\n"
                        f"⭐ ORIGINALIDADE: {originalidade_idx}/10 — [comentário]\n"
                        f"⭐ CONSERVAÇÃO: {conservacao_idx}/10 — [comentário]\n"
                        f"⭐ RARIDADE: [sua avaliação real baseada no modelo]/10 — [comentário, considerando se a autoavaliação do dono está alinhada com a raridade real do modelo]\n"
                        f"⭐ ESTADO MECÂNICO: {mecanica_idx}/10 — [comentário]\n"
                        f"⭐ ESTADO ESTÉTICO: {estetica_idx}/10 — [comentário]\n"
                        f"⭐ DOCUMENTAÇÃO: {documentacao_idx}/10 — [comentário]\n"
                        f"⭐ POTENCIAL DE VALORIZAÇÃO: [X]/10 — [comentário baseado em tendências gerais do modelo]\n\n"
                        f"🎯 O QUE MAIS AUMENTARIA O VALOR DESTA MOTOCICLETA:\n[1-2 ações prioritárias]"
                    )
                    res = motos_ia(prompt)
                    salvar_consulta("Indice", moto_idx, res)
                    st.session_state['indice_temp'] = res
            else:
                st.warning("Informe a moto.")

        if st.session_state.get('indice_temp'):
            renderizar_indice(st.session_state['indice_temp'], "ÍNDICE DO COLECIONADOR")
            st.markdown(f"<div class='card-gold'>{st.session_state['indice_temp']}</div>", unsafe_allow_html=True)
            st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['indice_temp'], file_name="indice_colecionador.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_idx", use_container_width=True):
                    st.session_state.consultas_salvas.append({'modulo':'Indice','tema':moto_idx if 'moto_idx' in dir() else '','conteudo':st.session_state['indice_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

    # ========================
    # AVALIAÇÃO INTELIGENTE
    # ========================
    elif st.session_state.pagina == "Avaliacao":
        st.header("💰 Avaliação Inteligente")
        st.markdown(DISCLAIMER_AVALIACAO, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            moto_aval = st.text_input("🏍️ Modelo e ano:", value=st.session_state.moto_padrao, key="moto_aval")
            estado_aval = st.selectbox("📊 Estado geral:", ["Original e impecável","Bem conservada","Restaurada","Em restauração","Sucata/projeto","Modificada (custom)"])
        with col2:
            documentacao_aval = st.selectbox("🧾 Documentação:", ["Em dia, placa de coleção","Em dia, comum","Pendências simples","Pendências complexas","Sem documentação"])
            regiao_aval = st.text_input("📍 Região (opcional):", placeholder="ex: São Paulo, SP")

        detalhes_aval = st.text_area("📝 Detalhes adicionais:", height=100,
            placeholder="ex: Motor original, pintura refeita há 1 ano, banco original, escapamento não original...")

        if st.button("💰 GERAR ESTIMATIVA"):
            if moto_aval.strip():
                with st.spinner("Calculando estimativa..."):
                    prompt = (
                        f"Crie uma estimativa de valor para esta motocicleta clássica.\n"
                        f"Moto: {moto_aval}. Estado: {estado_aval}. Documentação: {documentacao_aval}.\n"
                        f"Região: {regiao_aval or 'não informada'}. Detalhes: {detalhes_aval or 'não informado'}.\n\n"
                        f"FORMATO:\n\n"
                        f"💰 ESTIMATIVA DE VALOR — {moto_aval.upper()}\n\n"
                        f"📊 FAIXA DE VALOR ESTIMADA: R$[X] a R$[X]\n"
                        f"[Baseado em padrões históricos do mercado de clássicas para esse modelo/estado]\n\n"
                        f"📈 FATORES QUE AUMENTAM O VALOR:\n[com base no estado e detalhes informados]\n\n"
                        f"📉 FATORES QUE REDUZEM O VALOR:\n[com base no estado e detalhes informados]\n\n"
                        f"🎯 ONDE ESSA MOTO SE POSICIONA NO MERCADO:\n[comparação geral com a faixa de exemplares desse modelo]\n\n"
                        f"💡 COMO AUMENTAR O VALOR:\n[2-3 ações com melhor custo-benefício]\n\n"
                        f"🔍 ONDE CONFIRMAR ESSE VALOR:\n[tabelas especializadas, anúncios reais, avaliadores especializados, clubes de marca]"
                    )
                    res = motos_ia(prompt)
                    salvar_consulta("Avaliacao", moto_aval, res)
                    st.session_state['aval_temp'] = res
            else:
                st.warning("Informe a moto.")

        if st.session_state.get('aval_temp'):
            st.markdown(f"<div class='card-gold'>{st.session_state['aval_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['aval_temp'], file_name="avaliacao.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_aval", use_container_width=True):
                    st.session_state.consultas_salvas.append({'modulo':'Avaliacao','tema':moto_aval if 'moto_aval' in dir() else '','conteudo':st.session_state['aval_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

    # ========================
    # PLANEJAMENTO DA RESTAURAÇÃO
    # ========================
    elif st.session_state.pagina == "Restauracao":
        st.header("🛠️ Planejamento da Restauração")

        col1, col2 = st.columns(2)
        with col1:
            moto_rest = st.text_input("🏍️ Modelo e ano:", value=st.session_state.moto_padrao, key="moto_rest")
            orcamento_rest = st.number_input("💰 Orçamento disponível (R$):", min_value=0.0, value=5000.0, step=500.0)
        with col2:
            estado_atual_rest = st.selectbox("📊 Estado atual:", ["Rodando, precisa de retoques","Parada, mecânica ok","Parada há anos","Apenas o chassi/carcaça","Projeto desde zero"])
            prazo_rest = st.text_input("📅 Prazo desejado:", placeholder="ex: 6 meses, 1 ano, sem pressa...")

        descricao_rest = st.text_area("📝 Descreva o estado e o que precisa ser feito:", height=120,
            placeholder="ex: Motor funciona mas fumaça branca no escape, pintura descascando, banco rasgado, elétrica com problemas...")

        if st.button("🛠️ CRIAR PLANO DE RESTAURAÇÃO"):
            if moto_rest.strip():
                with st.spinner("Montando plano..."):
                    prompt = (
                        f"Crie um plano completo de restauração.\n"
                        f"Moto: {moto_rest}. Orçamento: R${orcamento_rest}. Estado atual: {estado_atual_rest}.\n"
                        f"Prazo: {prazo_rest or 'flexível'}. Descrição: {descricao_rest or 'não detalhada'}.\n\n"
                        f"FORMATO:\n\n"
                        f"🛠️ PLANO DE RESTAURAÇÃO — {moto_rest.upper()}\n"
                        f"Orçamento: R${orcamento_rest} | Prazo: {prazo_rest or 'flexível'}\n\n"
                        f"📋 ORDEM IDEAL DOS SERVIÇOS:\n"
                        f"1. [serviço] — Dificuldade: [X] — Tempo estimado: [X] — Custo aproximado: R$[X]\n"
                        f"[continue numerando todos os serviços necessários, na ordem lógica de execução]\n\n"
                        f"🎯 PRIORIDADES (o que fazer primeiro mesmo com orçamento limitado):\n[itens críticos de segurança/mecânica antes de estética]\n\n"
                        f"📅 CRONOGRAMA SUGERIDO:\n[divisão por fases/meses considerando o prazo informado]\n\n"
                        f"💰 DISTRIBUIÇÃO DO ORÇAMENTO:\n[como dividir os R${orcamento_rest} entre as categorias de serviço]\n\n"
                        f"⚠️ RISCOS DESSE TIPO DE RESTAURAÇÃO:\n[o que costuma sair do orçamento/prazo nesse tipo de projeto]"
                    )
                    res = motos_ia(prompt)
                    salvar_consulta("Restauracao", moto_rest, res)
                    st.session_state['rest_temp'] = res
            else:
                st.warning("Informe a moto.")

        if st.session_state.get('rest_temp'):
            st.markdown(f"<div class='card-purple'>{st.session_state['rest_temp']}</div>", unsafe_allow_html=True)
            st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['rest_temp'], file_name="plano_restauracao.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_rest", use_container_width=True):
                    st.session_state.consultas_salvas.append({'modulo':'Restauracao','tema':moto_rest if 'moto_rest' in dir() else '','conteudo':st.session_state['rest_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

    # ========================
    # DIAGNÓSTICO MECÂNICO
    # ========================
    elif st.session_state.pagina == "Diagnostico":
        st.header("🔧 Diagnóstico Mecânico")

        moto_diag = st.text_input("🏍️ Modelo e ano:", value=st.session_state.moto_padrao, key="moto_diag")
        problema_diag = st.text_area("📝 Descreva o problema:", height=120,
            placeholder="ex: A moto está soltando fumaça branca pelo escape ao acelerar, principalmente quando fria...")

        if st.button("🔧 DIAGNOSTICAR"):
            if problema_diag.strip():
                with st.spinner("Analisando..."):
                    prompt = (
                        f"Faça um diagnóstico mecânico preliminar.\n"
                        f"Moto: {moto_diag}. Problema: {problema_diag}\n\n"
                        f"FORMATO:\n\n"
                        f"🔧 DIAGNÓSTICO — {moto_diag.upper()}\n\n"
                        f"🔍 POSSÍVEIS CAUSAS (da mais para a menos provável):\n[liste com base no sintoma descrito e no conhecimento sobre esse modelo]\n\n"
                        f"⚙️ COMPONENTES ENVOLVIDOS:\n[peças que tipicamente causam esse sintoma]\n\n"
                        f"🧪 TESTES RECOMENDADOS:\n[testes simples que ajudam a confirmar a causa]\n\n"
                        f"🚨 NÍVEL DE URGÊNCIA: [Baixo/Médio/Alto/Crítico]\n[justificativa — é seguro continuar rodando?]\n\n"
                        f"🔧 RECOMENDAÇÃO:\n[orientação final, sempre recomendando confirmação com mecânico especializado em motos clássicas]"
                    )
                    res = motos_ia(prompt)
                    salvar_consulta("Diagnostico", problema_diag[:60], res)
                    st.session_state['diag_temp'] = res
            else:
                st.warning("Descreva o problema.")

        if st.session_state.get('diag_temp'):
            st.markdown(f"<div class='card-orange'>{st.session_state['diag_temp']}</div>", unsafe_allow_html=True)
            st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['diag_temp'], file_name="diagnostico.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_diag", use_container_width=True):
                    st.session_state.consultas_salvas.append({'modulo':'Diagnostico','tema':problema_diag[:60] if 'problema_diag' in dir() else '','conteudo':st.session_state['diag_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

    # ========================
    # GUIA DE PEÇAS
    # ========================
    elif st.session_state.pagina == "Pecas":
        st.header("📦 Guia de Peças")

        moto_pecas = st.text_input("🏍️ Modelo e ano:", value=st.session_state.moto_padrao, key="moto_pecas")
        peca_busca = st.text_input("🔧 Peça que você procura:", placeholder="ex: tanque de combustível, carburador, lente do farol...")

        if st.button("📦 BUSCAR INFORMAÇÕES DA PEÇA"):
            if peca_busca.strip() and moto_pecas.strip():
                with st.spinner("Buscando informações..."):
                    prompt = (
                        f"Forneça um guia completo sobre esta peça.\n"
                        f"Moto: {moto_pecas}. Peça: {peca_busca}\n\n"
                        f"FORMATO:\n\n"
                        f"📦 {peca_busca.upper()} — {moto_pecas.upper()}\n\n"
                        f"🏭 PEÇA ORIGINAL:\n[características da peça original de fábrica]\n\n"
                        f"🔄 PEÇAS REPRODUZIDAS:\n[se existem reproduções no mercado e qualidade geral]\n\n"
                        f"✅ COMPATIBILIDADE:\n[outros modelos/anos que usam peça igual ou similar]\n\n"
                        f"🔍 DIFICULDADE PARA ENCONTRAR:\n[Fácil/Moderada/Difícil/Raríssima — e onde normalmente são encontradas: clubes, feiras, importação]\n\n"
                        f"⚠️ CUIDADOS NA COMPRA:\n[como verificar se é original, problemas comuns em peças usadas desse tipo]"
                    )
                    res = motos_ia(prompt)
                    salvar_consulta("Pecas", f"{moto_pecas} — {peca_busca}", res)
                    st.session_state['pecas_temp'] = res
            else:
                st.warning("Informe a moto e a peça.")

        if st.session_state.get('pecas_temp'):
            st.markdown(f"<div class='card-green'>{st.session_state['pecas_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['pecas_temp'], file_name="guia_pecas.txt", mime="text/plain")

    # ========================
    # DOCUMENTAÇÃO
    # ========================
    elif st.session_state.pagina == "Documentacao":
        st.header("🧾 Documentação")

        tema_doc = st.selectbox("Tema:", [
            "Transferência de propriedade", "Placa de coleção — o que é e como solicitar",
            "Regularização de moto sem documento", "Modificações permitidas — o que é legal alterar",
            "Importação e nacionalização", "Compra em leilão — cuidados documentais",
            "Licenciamento de moto antiga", "Outro (perguntar)",
        ])
        pergunta_doc = ""
        if tema_doc == "Outro (perguntar)":
            pergunta_doc = st.text_input("Sua dúvida sobre documentação:")

        if st.button("🧾 EXPLICAR"):
            topico = pergunta_doc if tema_doc == "Outro (perguntar)" and pergunta_doc.strip() else tema_doc
            if topico.strip():
                with st.spinner("Preparando explicação..."):
                    prompt = (
                        f"Explique de forma clara e prática: {topico}, no contexto de motos clássicas no Brasil.\n\n"
                        f"FORMATO:\n\n"
                        f"🧾 {topico.upper()}\n\n"
                        f"📖 O QUE É / COMO FUNCIONA:\n[explicação clara]\n\n"
                        f"📋 PASSO A PASSO GERAL:\n[processo típico — sempre observando que procedimentos variam por estado/DETRAN]\n\n"
                        f"📄 DOCUMENTOS GERALMENTE NECESSÁRIOS:\n[lista]\n\n"
                        f"⚠️ CUIDADOS E PEGADINHAS COMUNS:\n[erros frequentes nesse processo]\n\n"
                        f"💡 DICA:\n[1 dica prática]\n\n"
                        f"📍 IMPORTANTE: procedimentos de DETRAN variam por estado — confirme sempre no órgão local."
                    )
                    res = motos_ia(prompt)
                    salvar_consulta("Documentacao", topico, res)
                    st.session_state['doc_temp'] = res
            else:
                st.warning("Escolha ou descreva o tema.")

        if st.session_state.get('doc_temp'):
            st.markdown(f"<div class='card-blue'>{st.session_state['doc_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['doc_temp'], file_name="documentacao.txt", mime="text/plain")

    # ========================
    # SIMULADOR DE CERTIFICAÇÃO
    # ========================
    elif st.session_state.pagina == "Certificacao":
        st.header("🏅 Simulador de Certificação")

        st.markdown("""<div class="disclaimer-avaliacao">
        🏅 <strong>Importante:</strong> a certificação oficial para coleção é feita por clubes de marca ou federações
        de veículos antigos com vistoria presencial. Esta é apenas uma PRÉ-AVALIAÇÃO educativa — não garante
        aprovação real.
        </div>""", unsafe_allow_html=True)

        moto_cert = st.text_input("🏍️ Modelo e ano:", value=st.session_state.moto_padrao, key="moto_cert")
        idade_cert = st.text_input("📅 Idade da motocicleta (anos):", placeholder="ex: 35 anos")
        descricao_cert = st.text_area("📝 Descreva o estado de originalidade e conservação:", height=150,
            placeholder="ex: Moto com 35 anos, motor original, pintura original com pequenos retoques, banco original, documentação em dia...")

        if st.button("🏅 FAZER PRÉ-AVALIAÇÃO"):
            if descricao_cert.strip() and moto_cert.strip():
                with st.spinner("Avaliando critérios..."):
                    prompt = (
                        f"Faça uma pré-avaliação educativa para certificação de motocicleta de coleção.\n"
                        f"Moto: {moto_cert}. Idade: {idade_cert or 'não informada'}.\n"
                        f"Descrição: {descricao_cert}\n\n"
                        f"FORMATO:\n\n"
                        f"🏅 PRÉ-AVALIAÇÃO — {moto_cert.upper()}\n\n"
                        f"📅 CRITÉRIO DE IDADE:\n[geralmente exige-se 30+ anos — avalie se atende com base na idade informada]\n\n"
                        f"✅ CRITÉRIOS QUE PARECEM ATENDIDOS:\n[com base na descrição]\n\n"
                        f"⚠️ CRITÉRIOS QUE MERECEM ATENÇÃO:\n[pontos que costumam ser exigidos e podem não estar claros na descrição]\n\n"
                        f"📊 ESTIMATIVA DE CHANCE DE APROVAÇÃO: [Baixa/Moderada/Alta]\n"
                        f"[IMPORTANTE: deixe claro que isso é uma estimativa educativa, não uma garantia]\n\n"
                        f"📋 PRÓXIMOS PASSOS REAIS:\n[como buscar a certificação oficial — clube de marca ou federação de veículos antigos]"
                    )
                    res = motos_ia(prompt, "Seja conservador nas estimativas de aprovação — sempre deixe claro que apenas a vistoria presencial oficial determina a certificação real.")
                    salvar_consulta("Certificacao", moto_cert, res)
                    st.session_state['cert_temp'] = res
            else:
                st.warning("Informe a moto e a descrição.")

        if st.session_state.get('cert_temp'):
            st.markdown(f"<div class='card-gold'>{st.session_state['cert_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['cert_temp'], file_name="certificacao.txt", mime="text/plain")

    # ========================
    # RADAR DO COLECIONADOR
    # ========================
    elif st.session_state.pagina == "Radar":
        st.header("💎 Radar do Colecionador")
        st.markdown(DISCLAIMER_AVALIACAO, unsafe_allow_html=True)

        tema_radar = st.selectbox("O que você quer explorar:", [
            "As motos que mais se valorizaram (tendência histórica)", "Potencial de valorização futura",
            "Melhores oportunidades (preço acessível + potencial)", "Modelos raros pouco conhecidos",
            "Índice de raridade de um modelo específico", "Índice de desejo (mais procuradas)",
            "Mercado nacional vs internacional", "Modelos possivelmente supervalorizados",
            "Melhor momento para comprar/vender", "Futuras motos clássicas (modelos recentes com potencial)",
        ], key="select_tema_radar")
        categoria_radar = st.text_input("🎯 Categoria ou modelo específico (opcional):", placeholder="ex: nacionais dos anos 80, custom, esportivas japonesas...")

        if st.button("💎 EXPLORAR TENDÊNCIAS"):
            with st.spinner("Analisando tendências..."):
                prompt = (
                    f"Explore o tema: {tema_radar}, no contexto do mercado de motocicletas clássicas.\n"
                    f"Categoria/modelo de interesse: {categoria_radar or 'geral, sem foco específico'}.\n\n"
                    f"FORMATO:\n\n"
                    f"💎 {tema_radar.upper()}\n\n"
                    f"📊 ANÁLISE:\n[desenvolva o tema com base em padrões históricos conhecidos do mercado de motos clássicas]\n\n"
                    f"🏍️ MODELOS/EXEMPLOS RELEVANTES:\n[liste exemplos concretos relacionados ao tema, com explicação breve de cada]\n\n"
                    f"💡 INSIGHT PARA O COLECIONADOR:\n[1-2 conclusões práticas]\n\n"
                    f"⚠️ LEMBRETE:\n[reforçar que são tendências históricas gerais, não previsões garantidas, e recomendar pesquisa em anúncios reais e tabelas especializadas]"
                )
                res = motos_ia(prompt)
                salvar_consulta("Radar", tema_radar, res)
                st.session_state['radar_temp'] = res

        if st.session_state.get('radar_temp'):
            st.markdown(f"<div class='card-gold'>{st.session_state['radar_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['radar_temp'], file_name="radar_colecionador.txt", mime="text/plain")

    # ========================
    # LINHA DO TEMPO
    # ========================
    elif st.session_state.pagina == "Timeline":
        st.header("🏁 Linha do Tempo")

        modelo_time = st.text_input("🏍️ Modelo (sem ano específico):", value=st.session_state.moto_padrao.split(' ')[0] if st.session_state.moto_padrao else "", placeholder="ex: CB 450, RD 350...")

        if st.button("🏁 VER EVOLUÇÃO ANO A ANO"):
            if modelo_time.strip():
                with st.spinner("Montando linha do tempo..."):
                    prompt = (
                        f"Crie uma linha do tempo da evolução do modelo: {modelo_time}\n\n"
                        f"FORMATO:\n\n"
                        f"🏁 LINHA DO TEMPO — {modelo_time.upper()}\n\n"
                        f"[Para cada geração/período importante de mudança:]\n"
                        f"📅 [PERÍODO/ANOS]\n"
                        f"Principais mudanças: [motor, chassi, suspensão, freios, painel, iluminação, banco, rodas, escapamento — "
                        f"o que mudou especificamente nesse período]\n\n"
                        f"[Repita para todos os períodos relevantes da produção do modelo]\n\n"
                        f"🏆 GERAÇÃO MAIS DESEJADA PELOS COLECIONADORES:\n[qual período/ano é mais procurado e por quê]"
                    )
                    res = motos_ia(prompt)
                    salvar_consulta("Timeline", modelo_time, res)
                    st.session_state['timeline_temp'] = res
            else:
                st.warning("Informe o modelo.")

        if st.session_state.get('timeline_temp'):
            st.markdown(f"<div class='card'>{st.session_state['timeline_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['timeline_temp'], file_name="linha_do_tempo.txt", mime="text/plain")

    # ========================
    # HISTÓRIA DA MOTOCICLETA
    # ========================
    elif st.session_state.pagina == "Historia":
        st.header("🌎 História da Motocicleta")

        modelo_hist = st.text_input("🏍️ Modelo:", value=st.session_state.moto_padrao.split(' ')[0] if st.session_state.moto_padrao else "", placeholder="ex: CB 450, RD 350...")

        if st.button("🌎 CONTAR A HISTÓRIA"):
            if modelo_hist.strip():
                with st.spinner("Reunindo a história..."):
                    prompt = (
                        f"Conte a história completa do modelo: {modelo_hist}\n\n"
                        f"FORMATO:\n\n"
                        f"🌎 A HISTÓRIA DA {modelo_hist.upper()}\n\n"
                        f"💡 ORIGEM DO PROJETO:\n[por que e como a moto foi criada]\n\n"
                        f"🏭 HISTÓRIA DA FABRICANTE:\n[contexto da marca na época]\n\n"
                        f"👨‍🔧 DESIGNERS E ENGENHEIROS:\n[pessoas-chave por trás do projeto, se conhecidas]\n\n"
                        f"🏆 PARTICIPAÇÕES EM COMPETIÇÕES:\n[se aplicável, conquistas em corridas]\n\n"
                        f"📺 COMERCIAIS DA ÉPOCA:\n[como a moto era anunciada, slogans marcantes]\n\n"
                        f"💡 CURIOSIDADES:\n[2-3 fatos pouco conhecidos]"
                    )
                    res = motos_ia(prompt)
                    salvar_consulta("Historia", modelo_hist, res)
                    st.session_state['hist_temp'] = res
            else:
                st.warning("Informe o modelo.")

        if st.session_state.get('hist_temp'):
            st.markdown(f"<div class='card-dark'>{st.session_state['hist_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['hist_temp'], file_name="historia_moto.txt", mime="text/plain")

    # ========================
    # DIÁRIO DA RESTAURAÇÃO
    # ========================
    elif st.session_state.pagina == "Diario":
        st.header("🏕️ Diário da Restauração")
        st.markdown("Registre a evolução do seu projeto.")

        col1, col2 = st.columns(2)
        with col1:
            etapa_diario = st.text_input("🔧 Etapa/serviço realizado:", placeholder="ex: Retífica do motor")
            gasto_diario = st.number_input("💰 Gasto nesta etapa (R$):", min_value=0.0, value=0.0, step=50.0)
        with col2:
            fornecedor_diario = st.text_input("🏪 Fornecedor/mecânico (opcional):", placeholder="ex: Moto Peças Clássicas, Mecânico do Zé...")
            horas_diario = st.number_input("⏱️ Horas trabalhadas:", min_value=0.0, value=0.0, step=0.5)

        notas_diario = st.text_area("📝 Notas sobre essa etapa:", height=100, placeholder="ex: Encontrei peças originais NOS, processo mais difícil do que esperado...")

        if st.button("📝 REGISTRAR NO DIÁRIO"):
            if etapa_diario.strip():
                st.session_state.diario_restauracao.append({
                    'data': datetime.now().strftime('%d/%m/%Y'),
                    'etapa': etapa_diario, 'gasto': gasto_diario, 'fornecedor': fornecedor_diario,
                    'horas': horas_diario, 'notas': notas_diario,
                })
                st.success("✅ Registrado no diário!")
                st.rerun()
            else:
                st.warning("Descreva a etapa.")

        if st.session_state.diario_restauracao:
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            total_gasto = sum(e['gasto'] for e in st.session_state.diario_restauracao)
            total_horas = sum(e['horas'] for e in st.session_state.diario_restauracao)

            c1, c2, c3 = st.columns(3)
            c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.diario_restauracao)}</div><div>Etapas registradas</div></div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='stat-box'><div class='stat-numero'>R${total_gasto:,.0f}</div><div>Gasto total</div></div>", unsafe_allow_html=True)
            c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{total_horas:.0f}h</div><div>Horas trabalhadas</div></div>", unsafe_allow_html=True)

            st.markdown("### 📖 Histórico de Etapas")
            for i, etapa in enumerate(reversed(st.session_state.diario_restauracao)):
                idx_real = len(st.session_state.diario_restauracao) - 1 - i
                with st.expander(f"🔧 {etapa['etapa']} — {etapa['data']} — R${etapa['gasto']:,.0f}"):
                    st.markdown(f"**Fornecedor:** {etapa.get('fornecedor','não informado')}")
                    st.markdown(f"**Horas trabalhadas:** {etapa.get('horas',0)}h")
                    if etapa.get('notas'):
                        st.markdown(f"**Notas:** {etapa['notas']}")
                    if st.button("🗑️ Remover", key=f"del_diario_{i}"):
                        st.session_state.diario_restauracao.pop(idx_real)
                        st.rerun()

            if st.button("🤖 GERAR RESUMO COMPLETO DO PROJETO"):
                with st.spinner("Gerando resumo..."):
                    etapas_txt = "\n".join([f"- {e['etapa']} ({e['data']}): R${e['gasto']:,.0f}, {e['horas']}h" for e in st.session_state.diario_restauracao])
                    prompt = (
                        f"Crie um resumo completo do projeto de restauração com base no histórico.\n"
                        f"Moto: {st.session_state.moto_padrao}.\n"
                        f"Etapas registradas:\n{etapas_txt}\n"
                        f"Total gasto: R${total_gasto:,.2f}. Total horas: {total_horas}h.\n\n"
                        f"FORMATO:\n\n"
                        f"🏕️ RESUMO DO PROJETO DE RESTAURAÇÃO\n\n"
                        f"📊 VISÃO GERAL:\n[resumo do progresso até agora]\n\n"
                        f"💰 ANÁLISE DE CUSTOS:\n[comentário sobre o investimento até agora]\n\n"
                        f"📋 PRÓXIMAS ETAPAS SUGERIDAS:\n[com base no que já foi feito, o que tipicamente viria a seguir]\n\n"
                        f"🏆 VALOR AGREGADO ESTIMADO:\n[como esse investimento tende a impactar o valor da moto — estimativa educativa]"
                    )
                    res = motos_ia(prompt)
                    st.session_state['resumo_diario_temp'] = res

            if st.session_state.get('resumo_diario_temp'):
                st.markdown(f"<div class='card-purple'>{st.session_state['resumo_diario_temp']}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar resumo (.txt)", data=st.session_state['resumo_diario_temp'], file_name="resumo_restauracao.txt", mime="text/plain")

    # ========================
    # SOM ORIGINAL
    # ========================
    elif st.session_state.pagina == "Som":
        st.header("🔊 Som Original")

        moto_som = st.text_input("🏍️ Modelo e ano:", value=st.session_state.moto_padrao, key="moto_som")

        if st.button("🔊 DESCREVER SOM ORIGINAL"):
            if moto_som.strip():
                with st.spinner("Descrevendo..."):
                    prompt = (
                        f"Descreva como era o som/ronco original desta motocicleta: {moto_som}\n\n"
                        f"FORMATO:\n\n"
                        f"🔊 SOM ORIGINAL — {moto_som.upper()}\n\n"
                        f"🎵 CARACTERÍSTICA DO RONCO:\n[descrição sonora detalhada — grave, agudo, rítmico, etc]\n\n"
                        f"⚙️ CONFIGURAÇÃO DE FÁBRICA:\n[motor, escapamento original que geravam esse som]\n\n"
                        f"🔄 DIFERENÇAS ENTRE GERAÇÕES:\n[se houver múltiplas versões, como o som varia]\n\n"
                        f"🛠️ ESCAPAMENTOS ALTERNATIVOS DA ÉPOCA:\n[opções de escape esportivo que existiam para esse modelo]\n\n"
                        f"💡 CURIOSIDADE SONORA:\n[algo interessante sobre o som desse modelo específico]"
                    )
                    res = motos_ia(prompt)
                    salvar_consulta("Som", moto_som, res)
                    st.session_state['som_temp'] = res
            else:
                st.warning("Informe a moto.")

        if st.session_state.get('som_temp'):
            st.markdown(f"<div class='card'>{st.session_state['som_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['som_temp'], file_name="som_original.txt", mime="text/plain")

    # ========================
    # QUIZ DO MOTOCICLISTA
    # ========================
    elif st.session_state.pagina == "Quiz":
        st.header("🧠 Quiz do Motociclista")
        st.markdown(f"Pontuação atual: **{st.session_state.quiz_pontuacao} pontos** | Nível: **{st.session_state.quiz_nivel_atual}**")

        nivel_quiz = st.selectbox("Escolha o nível:", ["Iniciante","Intermediário","Avançado","Especialista","Mestre das Clássicas"], key="select_nivel_quiz")
        tema_quiz = st.text_input("Tema específico (opcional):", placeholder="ex: motos nacionais, motores 2 tempos, história geral...")

        if st.button("🧠 GERAR PERGUNTA"):
            with st.spinner("Preparando pergunta..."):
                prompt = (
                    f"Crie 1 pergunta de quiz sobre motocicletas clássicas, nível {nivel_quiz}.\n"
                    f"Tema: {tema_quiz or 'geral'}.\n\n"
                    f"FORMATO:\n\n"
                    f"🧠 PERGUNTA ({nivel_quiz}):\n[a pergunta]\n\n"
                    f"A) [opção]\nB) [opção]\nC) [opção]\nD) [opção]\n\n"
                    f"✅ RESPOSTA CORRETA: [letra]\n"
                    f"📖 EXPLICAÇÃO: [por que essa é a resposta, com contexto interessante]"
                )
                res = motos_ia(prompt)
                st.session_state['quiz_pergunta_temp'] = res
                st.session_state['quiz_respondido'] = False

        if st.session_state.get('quiz_pergunta_temp'):
            partes = st.session_state['quiz_pergunta_temp'].split('✅ RESPOSTA CORRETA')
            st.markdown(f"<div class='card'>{partes[0]}</div>", unsafe_allow_html=True)

            if not st.session_state.get('quiz_respondido'):
                if st.button("👁️ VER RESPOSTA"):
                    st.session_state['quiz_respondido'] = True
                    st.rerun()
            else:
                st.markdown(f"<div class='card-gold'>✅ RESPOSTA CORRETA{partes[1] if len(partes)>1 else ''}</div>", unsafe_allow_html=True)
                col_acertei, col_errei = st.columns(2)
                with col_acertei:
                    if st.button("✅ Acertei!"):
                        pontos = {"Iniciante":5,"Intermediário":10,"Avançado":15,"Especialista":20,"Mestre das Clássicas":30}
                        st.session_state.quiz_pontuacao += pontos.get(nivel_quiz, 10)
                        st.session_state.quiz_nivel_atual = nivel_quiz
                        st.success(f"🎉 +{pontos.get(nivel_quiz,10)} pontos!")
                with col_errei:
                    if st.button("❌ Errei"):
                        st.info("Sem problema, vamos para a próxima!")

    # ========================
    # ENGENHARIA EXPLICADA
    # ========================
    elif st.session_state.pagina == "Engenharia":
        st.header("🔬 Engenharia Explicada")

        tema_eng = st.selectbox("Componente:", [
            "Motor 2 tempos", "Motor 4 tempos", "Sistema de alimentação", "Carburador",
            "Injeção eletrônica (motos mais recentes)", "Suspensão (telescópica vs convencional)",
            "Freios a tambor vs disco", "Embreagem", "Câmbio sequencial de época", "Sistema elétrico 6V vs 12V",
        ], key="select_tema_eng")

        if st.button("🔬 EXPLICAR"):
            with st.spinner("Preparando explicação..."):
                prompt = (
                    f"Explique de forma simples e visual: {tema_eng}, no contexto de motocicletas clássicas.\n\n"
                    f"FORMATO:\n\n"
                    f"🔬 {tema_eng.upper()}\n\n"
                    f"📖 O QUE É E PARA QUE SERVE:\n[explicação simples]\n\n"
                    f"⚙️ COMO FUNCIONA:\n[explicação do mecanismo, passo a passo]\n\n"
                    f"🔧 PROBLEMAS COMUNS EM CLÁSSICAS:\n[o que tipicamente dá problema nesse componente em motos antigas]\n\n"
                    f"🛠️ MANUTENÇÃO BÁSICA:\n[cuidados que o proprietário pode ter]\n\n"
                    f"💡 CURIOSIDADE TÉCNICA:\n[1 fato interessante sobre a evolução desse componente]"
                )
                res = motos_ia(prompt)
                salvar_consulta("Engenharia", tema_eng, res)
                st.session_state['eng_temp'] = res

        if st.session_state.get('eng_temp'):
            st.markdown(f"<div class='card-blue'>{st.session_state['eng_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['eng_temp'], file_name="engenharia.txt", mime="text/plain")

    # ========================
    # DNA DA MOTOCICLETA
    # ========================
    elif st.session_state.pagina == "DNA":
        st.header("🧬 DNA da Motocicleta")
        st.markdown("Uma viagem no tempo até a época em que sua clássica nasceu.")

        moto_dna = st.text_input("🏍️ Modelo e ano:", value=st.session_state.moto_padrao, key="moto_dna")

        if st.button("🧬 VIAJAR NO TEMPO"):
            if moto_dna.strip():
                with st.spinner("Reconstruindo a época..."):
                    prompt = (
                        f"Reconstrua a época em que esta motocicleta nasceu: {moto_dna}\n\n"
                        f"FORMATO:\n\n"
                        f"🧬 DNA — {moto_dna.upper()}\n\n"
                        f"📅 COMO ERA O BRASIL E O MUNDO NAQUELE ANO:\n[contexto histórico geral]\n\n"
                        f"💰 QUANTO CUSTAVA A MOTO NO LANÇAMENTO:\n[valor aproximado na época, em moeda da época]\n\n"
                        f"🏭 COMO FUNCIONAVA A FÁBRICA:\n[contexto da produção na época]\n\n"
                        f"📰 PRINCIPAIS ACONTECIMENTOS HISTÓRICOS DO ANO:\n[2-3 eventos marcantes]\n\n"
                        f"⛽ PREÇO DOS COMBUSTÍVEIS NA ÉPOCA:\n[contexto aproximado]\n\n"
                        f"🎵 MÚSICAS MAIS POPULARES DA ÉPOCA:\n[2-3 exemplos]\n\n"
                        f"🛣️ COMO ERAM AS ESTRADAS:\n[contexto da infraestrutura da época]\n\n"
                        f"🏍️ PRINCIPAIS CONCORRENTES:\n[outros modelos que disputavam o mesmo mercado]\n\n"
                        f"📈 SALÁRIO MÍNIMO DA ÉPOCA:\n[contexto aproximado — quantos salários mínimos custava a moto]\n\n"
                        f"👨 PERFIL TÍPICO DE QUEM COMPRAVA:\n[quem comprava essa moto na época]"
                    )
                    res = motos_ia(prompt)
                    salvar_consulta("DNA", moto_dna, res)
                    st.session_state['dna_temp'] = res
            else:
                st.warning("Informe a moto.")

        if st.session_state.get('dna_temp'):
            st.markdown(f"<div class='card-dark'>{st.session_state['dna_temp']}</div>", unsafe_allow_html=True)
            st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['dna_temp'], file_name="dna_moto.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_dna", use_container_width=True):
                    st.session_state.consultas_salvas.append({'modulo':'DNA','tema':moto_dna if 'moto_dna' in dir() else '','conteudo':st.session_state['dna_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

    # ========================
    # HISTÓRIA NAS COMPETIÇÕES
    # ========================
    elif st.session_state.pagina == "Competicoes":
        st.header("🏁 História nas Competições")
        st.markdown("Motocross, Enduro, Rally, Velocidade, Trial, Dakar.")

        moto_comp = st.text_input("🏍️ Modelo e ano:", value=st.session_state.moto_padrao, key="moto_comp")
        modalidade_comp = st.selectbox("🏆 Modalidade de interesse:", ["Todas as modalidades","Motocross","Enduro","Rally","Velocidade","Trial","Dakar"])

        if st.button("🏁 VER HISTÓRICO NAS COMPETIÇÕES"):
            if moto_comp.strip():
                with st.spinner("Buscando histórico..."):
                    prompt = (
                        f"Pesquise e apresente o histórico de competições desta motocicleta/modelo.\n"
                        f"Moto: {moto_comp}. Modalidade de interesse: {modalidade_comp}\n\n"
                        f"FORMATO:\n\n"
                        f"🏁 HISTÓRICO NAS COMPETIÇÕES — {moto_comp.upper()}\n\n"
                        f"🏆 MODALIDADES EM QUE PARTICIPOU/SE DESTACOU:\n[se esse modelo (ou a marca/categoria) teve presença relevante em competições]\n\n"
                        f"👨‍🏁 PILOTOS FAMOSOS ASSOCIADOS:\n[pilotos conhecidos que usaram esse modelo ou modelos da mesma linhagem, se conhecidos]\n\n"
                        f"🏆 CONQUISTAS E RESULTADOS:\n[títulos, vitórias ou resultados notáveis, se houver]\n\n"
                        f"💡 CURIOSIDADE COMPETITIVA:\n[1 fato interessante sobre o histórico competitivo desse modelo/marca]\n\n"
                        f"⚠️ NOTA:\n[se o modelo não teve histórico relevante em competições, seja honesto sobre isso em vez de inventar]"
                    )
                    res = motos_ia(prompt, "Seja honesto se o modelo não teve participação relevante em competições — não invente histórico competitivo que não existiu.")
                    salvar_consulta("Competicoes", moto_comp, res)
                    st.session_state['comp_temp'] = res
            else:
                st.warning("Informe a moto.")

        if st.session_state.get('comp_temp'):
            st.markdown(f"<div class='card-orange'>{st.session_state['comp_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['comp_temp'], file_name="competicoes.txt", mime="text/plain")

    # ========================
    # VIAGENS CLÁSSICAS
    # ========================
    elif st.session_state.pagina == "Viagens":
        st.header("🌍 Viagens Clássicas")
        st.markdown("Monte roteiros para rodar com sua moto antiga.")

        col1, col2 = st.columns(2)
        with col1:
            moto_viagem = st.text_input("🏍️ Modelo e ano:", value=st.session_state.moto_padrao, key="moto_viagem")
            origem_viagem = st.text_input("📍 Saindo de:", placeholder="ex: São Paulo, SP")
            destino_viagem = st.text_input("📍 Indo para:", placeholder="ex: Serra da Mantiqueira, litoral...")
        with col2:
            duracao_viagem = st.selectbox("⏱️ Duração:", ["1 dia","Fim de semana","3-5 dias","1 semana ou mais"])
            estilo_viagem = st.selectbox("🛣️ Estilo de estrada:", ["Estradas históricas/cênicas","Rodovias principais","Mix de asfalto e terra","Trilhas leves"])

        if st.button("🌍 MONTAR ROTEIRO"):
            if origem_viagem.strip() and destino_viagem.strip():
                with st.spinner("Montando roteiro..."):
                    prompt = (
                        f"Monte um roteiro de viagem para motociclista de moto clássica.\n"
                        f"Moto: {moto_viagem}. Origem: {origem_viagem}. Destino: {destino_viagem}.\n"
                        f"Duração: {duracao_viagem}. Estilo: {estilo_viagem}.\n\n"
                        f"FORMATO:\n\n"
                        f"🌍 ROTEIRO — {origem_viagem.upper()} → {destino_viagem.upper()}\n"
                        f"Moto: {moto_viagem} | Duração: {duracao_viagem}\n\n"
                        f"🛣️ TRAJETO SUGERIDO:\n[descrição geral da rota, priorizando estradas históricas/cênicas quando possível]\n\n"
                        f"⛽ PONTOS DE APOIO NO CAMINHO:\n[tipos de parada recomendados — postos, oficinas — sem inventar nomes específicos não verificados]\n\n"
                        f"🏨 ONDE FICAR:\n[tipo de hospedagem recomendada para motociclistas na região]\n\n"
                        f"🧰 KIT DE FERRAMENTAS PARA LEVAR:\n[específico para esse tipo de moto em viagem]\n\n"
                        f"🚨 RISCOS DO TRAJETO PARA UMA CLÁSSICA:\n[atenção especial — moto antiga pode ter limitações de autonomia, refrigeração, etc]\n\n"
                        f"💡 DICA DE QUEM RODA CLÁSSICA:\n[1 dica prática de quem viaja com moto antiga]"
                    )
                    res = motos_ia(prompt, "Você não tem dados em tempo real sobre condições reais de estradas, postos específicos ou hospedagens — fale em termos gerais e sempre recomende confirmar informações atualizadas antes da viagem.")
                    salvar_consulta("Viagens", f"{origem_viagem} → {destino_viagem}", res)
                    st.session_state['viagem_temp'] = res
            else:
                st.warning("Informe origem e destino.")

        if st.session_state.get('viagem_temp'):
            st.markdown(f"<div class='card-teal'>{st.session_state['viagem_temp']}</div>", unsafe_allow_html=True)
            st.markdown("""<div class="disclaimer">⚠️ Roteiro educativo geral — confirme sempre condições atuais de estradas, postos e hospedagens antes de viajar.</div>""", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['viagem_temp'], file_name="roteiro_viagem.txt", mime="text/plain")

    # ========================
    # CLUBE DO COLECIONADOR
    # ========================
    elif st.session_state.pagina == "Clube":
        st.header("🤝 Clube do Colecionador")
        st.markdown("Encontre encontros, feiras, clubes e museus de motos clássicas.")

        regiao_clube = st.text_input("📍 Sua região:", placeholder="ex: São Paulo, SP")
        interesse_clube = st.multiselect("🎯 O que você procura:", [
            "Encontros de motos antigas","Eventos/exposições","Feiras de peças","Clubes de colecionadores","Museus",
        ], default=["Clubes de colecionadores"])

        if st.button("🤝 BUSCAR INFORMAÇÕES"):
            if regiao_clube.strip():
                with st.spinner("Buscando..."):
                    interesses_txt = ", ".join(interesse_clube) if interesse_clube else "informações gerais"
                    prompt = (
                        f"Forneça orientação sobre comunidade de colecionadores de motos clássicas.\n"
                        f"Região: {regiao_clube}. Interesse: {interesses_txt}\n\n"
                        f"FORMATO:\n\n"
                        f"🤝 COMUNIDADE DO COLECIONADOR — {regiao_clube.upper()}\n\n"
                        f"👥 COMO ENCONTRAR CLUBES NA SUA REGIÃO:\n[orientação geral de como buscar — federações estaduais, redes sociais, etc]\n\n"
                        f"🎪 TIPOS DE EVENTOS QUE COSTUMAM EXISTIR:\n[encontros regionais, feiras de peças, exposições — padrões gerais do hobby]\n\n"
                        f"🏛️ MUSEUS RELACIONADOS A VEÍCULOS ANTIGOS NO BRASIL:\n[museus conhecidos e estabelecidos, se você tiver certeza da existência]\n\n"
                        f"💡 COMO COMEÇAR A SE CONECTAR COM A COMUNIDADE:\n[dicas práticas para quem está começando no hobby]\n\n"
                        f"⚠️ IMPORTANTE:\n[informações sobre eventos específicos mudam com frequência — recomende buscar grupos/páginas atualizadas de colecionadores na região]"
                    )
                    res = motos_ia(prompt, "Não invente nomes específicos de clubes, eventos ou museus que você não tem certeza que existem — prefira orientação geral de como buscar, e só cite instituições muito conhecidas e estabelecidas.")
                    salvar_consulta("Clube", regiao_clube, res)
                    st.session_state['clube_temp'] = res
            else:
                st.warning("Informe sua região.")

        if st.session_state.get('clube_temp'):
            st.markdown(f"<div class='card-green'>{st.session_state['clube_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['clube_temp'], file_name="clube_colecionador.txt", mime="text/plain")

    # ========================
    # CONSULTOR 24 HORAS
    # ========================
    elif st.session_state.pagina == "Consultor":
        st.header("🤖 Consultor 24 Horas")
        st.markdown("Pergunte qualquer coisa sobre qualquer motocicleta clássica.")

        if 'chat_consultor' not in st.session_state:
            st.session_state.chat_consultor = []
        if 'consultor_key' not in st.session_state:
            st.session_state.consultor_key = 0

        if st.session_state.chat_consultor:
            for msg in st.session_state.chat_consultor:
                if msg['role'] == 'user':
                    st.markdown(f"<div style='background:#FEF2F2;border:1px solid #B91C1C;border-radius:12px 12px 4px 12px;padding:12px 16px;margin:8px 0;'><b>Você:</b> {msg['content']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='card-dark' style='margin:8px 0;'><b>🏍️ Consultor:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown("""<div style="background:#FEF2F2;border:1px dashed #B91C1C;border-radius:12px;padding:16px;text-align:center;">
            🤖 <strong>Pergunte qualquer coisa!</strong> Ex: "Qual a diferença entre a CB 450 e a CB 500?",
            "Vale a pena converter o carburador original para um mais moderno?"
            </div>""", unsafe_allow_html=True)

        pergunta_consultor = st.text_input("Sua pergunta:", key=f"consultor_input_{st.session_state.consultor_key}", placeholder="Pergunte qualquer coisa sobre motos clássicas...")

        col_env, col_limpar = st.columns([3, 1])
        with col_env:
            if st.button("📤 PERGUNTAR"):
                if pergunta_consultor.strip():
                    with st.spinner("Consultando..."):
                        historico_msgs = [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_consultor[-10:]]
                        resp = motos_ia(pergunta_consultor, "Responda como um restaurador experiente, historiador e avaliador de mercado ao mesmo tempo. Seja didático e apaixonado.")
                    st.session_state.chat_consultor.append({"role": "user", "content": pergunta_consultor})
                    st.session_state.chat_consultor.append({"role": "assistant", "content": resp})
                    st.session_state.consultor_key += 1
                    salvar_consulta("Consultor", pergunta_consultor[:60], resp)
                    st.rerun()
                else:
                    st.warning("Digite sua pergunta.")
        with col_limpar:
            if st.button("🗑️ Limpar"):
                st.session_state.chat_consultor = []
                st.rerun()

    # ========================
    # BIBLIOTECA
    # ========================
    elif st.session_state.pagina == "Biblioteca":
        st.header("📚 Biblioteca de Consultas")

        if not st.session_state.consultas_salvas:
            st.info("Biblioteca vazia. Gere consultas nos módulos e salve as importantes aqui!")
        else:
            modulos_bib = list(set(c['modulo'] for c in st.session_state.consultas_salvas))
            filtro = st.selectbox("Filtrar por módulo:", ["Todos"] + modulos_bib, key="select_filtro_bib")
            consultas_f = [c for c in st.session_state.consultas_salvas if filtro == "Todos" or c['modulo'] == filtro]

            st.markdown(f"**{len(consultas_f)} consulta(s) encontrada(s)**")
            for i, item in enumerate(reversed(consultas_f)):
                idx_real = len(st.session_state.consultas_salvas) - 1 - i
                with st.expander(f"[{item['modulo']}] {item['tema'][:60]} — {item['data']}"):
                    st.markdown(f"<div class='card'>{item['conteudo']}</div>", unsafe_allow_html=True)
                    col_dl, col_del = st.columns([3, 1])
                    with col_dl:
                        st.download_button("📋 Baixar", data=item['conteudo'], file_name=f"{item['modulo'].lower()}.txt", mime="text/plain", key=f"dl_bib_{i}")
                    with col_del:
                        if st.button("🗑️ Remover", key=f"del_bib_{i}"):
                            st.session_state.consultas_salvas.pop(idx_real)
                            st.rerun()

        if st.session_state.historico_consultas:
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            historico_txt = "\n\n".join(f"[{c['data']}] {c['modulo']} — {c['tema']}\n{c['conteudo']}\n{'─'*40}" for c in st.session_state.historico_consultas)
            st.download_button("⬇️ Exportar todo o histórico (.txt)", data=historico_txt, file_name="historico_motos.txt", mime="text/plain")
            if st.button("🗑️ Limpar Todo o Histórico"):
                st.session_state.historico_consultas = []
                st.rerun()

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "© 2026 Clássicas Motos IA — Especialista em Motocicletas Clássicas com IA · Quiz Com Prêmios"
    "</div>", unsafe_allow_html=True
)
