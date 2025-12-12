import os
import json
from uuid import uuid4
from datetime import datetime
from typing import List, Dict, Tuple

import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from shoppers_data import SHOPPERS
# ============================================================
# 0. CONFIG GLOBALE + CSS CUSTOM
# ============================================================

st.set_page_config(
    page_title="Pershop Pilote",
    page_icon="👗",
    layout="wide",
)

def inject_css():
    st.markdown(
        """
        <style>
        /* Fond global et container */
        .stApp {
            background: radial-gradient(circle at top, #262654 0, #050510 50%, #02020a 100%);
            color: #f7f7ff;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", sans-serif;
        }
        .block-container {
            padding-top: 1.8rem;
            padding-bottom: 2.5rem;
            max-width: 1100px;
        }

        /* En-tête principal */
        .pershop-header {
            padding: 1.2rem 1.4rem;
            border-radius: 18px;
            background: linear-gradient(135deg, rgba(255, 79, 139, 0.12), rgba(90, 99, 255, 0.15));
            border: 1px solid rgba(255, 255, 255, 0.14);
            box-shadow: 0 18px 40px rgba(0,0,0,0.55);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: 1rem;
        }
        .pershop-header-left {
            display: flex;
            align-items: center;
            gap: 0.9rem;
        }
        .pershop-logo-mark {
            width: 42px;
            height: 42px;
            border-radius: 999px;
            background: radial-gradient(circle at 20% 0, #ffe2f0, #ff4f8b 40%, #8b3dff);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 1.1rem;
            color: #140514;
            box-shadow: 0 0 20px rgba(255, 79, 139, 0.7);
        }
        .pershop-header-title {
            font-size: 1.3rem;
            font-weight: 650;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }
        .pershop-header-sub {
            font-size: 0.9rem;
            color: #d1cfe9;
        }
        .pershop-header-badge {
            font-size: 0.78rem;
            padding: 0.3rem 0.65rem;
            border-radius: 999px;
            background: rgba(5,5,16,0.7);
            border: 1px solid rgba(255,255,255,0.18);
            color: #e6e4ff;
        }

        /* Cards génériques */
        .card {
            padding: 1.4rem 1.3rem;
            border-radius: 18px;
            background: rgba(9, 9, 30, 0.97);
            border: 1px solid rgba(255, 255, 255, 0.07);
            box-shadow: 0 18px 40px rgba(0, 0, 0, 0.65);
            margin-top: 1.2rem;
        }
        .card-title {
            font-size: 1.05rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        .card-subtitle {
            font-size: 0.9rem;
            color: #b9b7d4;
            margin-bottom: 0.2rem;
        }

        /* Champs & labels */
        label, .stMarkdown p {
            font-size: 0.9rem;
        }
        .stTextInput > div > div > input,
        .stSelectbox > div > div,
        .stTextArea textarea {
            background-color: #050516 !important;
            border-radius: 999px !important;
            border: 1px solid #2b2b47 !important;
            color: #f7f7ff !important;
            font-size: 0.9rem !important;
        }
        .stTextArea textarea {
            border-radius: 12px !important;
        }
        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div:focus,
        .stTextArea textarea:focus {
            border-color: #ff82b0 !important;
            box-shadow: 0 0 0 1px rgba(255,130,176,0.9) !important;
        }

        /* Boutons */
        div.stButton > button {
            width: 100%;
            border-radius: 999px;
            border: none;
            background-image: linear-gradient(135deg, #ff4f8b, #ffd5f0);
            color: #200414;
            font-weight: 600;
            padding: 0.6rem 1.4rem;
            font-size: 0.95rem;
            box-shadow: 0 14px 30px rgba(255, 79, 139, 0.45);
            transition: transform 0.08s ease-out, box-shadow 0.08s ease-out;
        }
        div.stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 18px 36px rgba(255, 79, 139, 0.6);
        }

        /* Expander styling (cartes clients / shoppers) */
        .streamlit-expanderHeader {
            background: linear-gradient(to right, rgba(255,79,139,0.12), rgba(50,60,180,0.3));
            border-radius: 12px;
            padding: 0.4rem 0.75rem;
        }
        .streamlit-expanderHeader p {
            font-size: 0.9rem;
        }
        .streamlit-expanderContent {
            padding-top: 0.5rem;
        }

        /* Pré-brief bloc */
        .prebrief-block h3 {
            margin-top: 0.4rem;
            margin-bottom: 0.3rem;
        }
        .prebrief-block ul {
            margin-top: 0.1rem;
            margin-bottom: 0.4rem;
        }
        .prebrief-block li {
            margin-bottom: 0.2rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

inject_css()

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
GROQ_ENABLED = groq_client is not None

ASSIGNMENTS_PATH = "assignments.jsonl"



# ============================================================
# 2. PERSISTENCE ASSIGNATIONS
# ============================================================

def save_assignment(assignment: Dict):
    with open(ASSIGNMENTS_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(assignment, ensure_ascii=False) + "\n")


def load_assignments() -> List[Dict]:
    if not os.path.exists(ASSIGNMENTS_PATH):
        return []
    assignments = []
    with open(ASSIGNMENTS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                assignments.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return assignments


# ============================================================
# 3. MATCHING
# ============================================================

def compute_budget_level(budget: str) -> str:
    txt = budget.lower()
    if "moins" in txt or "<" in txt:
        return "bas"
    if "plus" in txt or "1000" in txt:
        return "élevé"
    if "100 - 300" in txt or "300 - 1000" in txt:
        return "moyen"
    return "moyen"

import unicodedata
import re

def normalize_city(name: str) -> str:
    """
    Normalise un nom de ville pour le matching :
    - minuscules
    - sans accents
    - on garde lettres / chiffres / espaces
    - on compacte les espaces
    """
    if not name:
        return ""
    # minuscules
    text = name.lower().strip()
    # retirer accents
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    # garder lettres/chiffres/espaces
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    # compacter les espaces
    text = re.sub(r"\s+", " ", text).strip()
    return text


def match(client: Dict, shopper: Dict) -> Tuple[int, List[str]]:
    score = 0
    reasons: List[str] = []

    city_client_norm = normalize_city(client.get("city", ""))
    city_shopper_norm = normalize_city(shopper.get("zone", ""))

    if city_client_norm:
        same_area = (
            city_client_norm in city_shopper_norm
            or city_shopper_norm in city_client_norm
        )

        # Si le client veut absolument du présentiel → la ville devient bloquante
        if client.get("mode") == "presentiel":
            if not same_area:
                return 0, []  # pas dans la zone, on élimine
            else:
                score += 2
                reasons.append("Basé(e) dans ta ville ou à proximité (présentiel)")

        # Si visio ou peu_importe → pas bloquant, mais on donne un bonus si c'est proche
        else:
            if same_area:
                score += 1
                reasons.append("Dans ta zone géographique (utile si un jour tu veux du présentiel)")

    # Style
    if client["style"]:
        if any(style_item in shopper["styles"] for style_item in client["style"]):
            score += 2
            reasons.append("Style compatible avec ce que tu recherches")

    # Objectif
    if client["objective"]:
        if any(client["objective"].lower() in spec.lower() for spec in shopper["specialites"]):
            score += 2
            reasons.append("Spécialisé(e) sur ton objectif principal")

    # Budget
    level = compute_budget_level(client["budget"])
    if level in shopper["niveau_budget"]:
        score += 2
        reasons.append("Adapté à ton budget vestimentaire")

    # Mode
    if client["mode"] == "visio":
        if any("visio" in f for f in shopper["formats"]):
            score += 1
            reasons.append("Peut te proposer une séance en visio")
    elif client["mode"] == "presentiel":
        if any(f in shopper["formats"] for f in ["magasin", "domicile", "presentiel", "visio/presentiel"]):
            score += 1
            reasons.append("Peut te recevoir en présentiel")

    # Texte libre
    if client["extra_info"]:
        text = client["extra_info"].lower()
        for field in ["styles", "specialites", "tags"]:
            for item in shopper[field]:
                if item.lower().replace("_", " ") in text:
                    score += 1
                    reasons.append(f"Correspond à ton besoin : {item}")
                    break

    return score, reasons


# ============================================================
# 4. IA GROQ
# ============================================================

def call_llm(prompt: str) -> str:
    if not GROQ_ENABLED:
        return (
            "⚠️ IA désactivée (clé GROQ_API_KEY manquante). "
            "Dans un environnement complet, ce texte serait généré par Groq."
        )
    try:
        resp = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Tu es un expert en mode et personal shopping."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=700,
            temperature=0.5,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print("Erreur Groq :", repr(e))
        return "Erreur lors de la génération IA (Groq)."


def generate_ai_summary(client: Dict, shopper: Dict) -> str:
    prompt = f"""
Client :
{client}

Personal shopper :
{shopper}

Explique en 3 à 4 phrases maximum, en français, pourquoi ce personal shopper
est bien adapté à ce client. Parle au client à la deuxième personne ("tu").
Ne fais pas de liste à puces, répond sous forme de paragraphe.
"""
    return call_llm(prompt)


def generate_prebrief(client: Dict, shopper: Dict) -> str:
    prenom = client.get("prenom") or "le client"
    prompt = f"""
Tu es un copilote IA pour personal shoppers sur une plateforme de personal shopping phygital.

Voici le profil client (données JSON) :
{client}

Voici le profil du personal shopper (données JSON) :
{shopper}

Rédige un pré-brief structuré en **Markdown** pour préparer une séance de personal shopping.
Respecte exactement cette structure :

1. Première ligne : un titre en gras de ce type :  
   **Pré-brief pour la séance de personal shopping avec {prenom}**

2. Ensuite, crée les sections avec des titres de niveau 3 (###) :
   ### 1. Résumé du client
   ### 2. Points d'attention
   ### 3. Pistes de préparation
   ### 4. Recommandations de déroulé de séance

3. Dans chaque section, utilise des listes à puces avec des labels en gras, par exemple :
   * **Style** : ...
   * **Budget** : ...
   * **Objectif** : ...

Contenu attendu :
- Dans "Résumé du client" : style, budget, objectif, contexte pro / moment de vie.
- Dans "Points d'attention" : confiance en soi, freins possibles, sensibilités.
- Dans "Pistes de préparation" : idées de silhouettes, pièces clés, où chercher (types de boutiques ou niveaux de gamme).
- Dans "Recommandations de déroulé de séance" : format (présentiel/visio), étapes principales de la séance.

Réponds uniquement avec le Markdown final, sans commentaire autour.
"""
    return call_llm(prompt)


# ============================================================
# 5. UI – VUE CLIENT
# ============================================================

def page_client():
    st.markdown(
        """
        <div class="pershop-header">
          <div class="pershop-header-left">
            <div class="pershop-logo-mark">P</div>
            <div>
              <div class="pershop-header-title">Pershop Pilote</div>
              <div class="pershop-header-sub">
                Copilote IA pour matcher chaque client avec le bon personal shopper.
              </div>
            </div>
          </div>
          <div class="pershop-header-badge">
            Vue client
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not GROQ_ENABLED:
        st.warning(
            "La clé GROQ_API_KEY n'est pas configurée – l'IA utilisera des textes génériques.",
            icon="⚠️",
        )

    st.markdown(
        """
        <div class="card">
          <div class="card-title">Parle-moi de toi</div>
          <div class="card-subtitle">
            Quelques questions rapides, et je te propose une short-list de personal shoppers adaptés à ta réalité.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("client_form"):
        st.markdown("#### 1. À propos de toi")
        col1, col2, col3 = st.columns(3)
        with col1:
            prenom = st.text_input("Prénom", placeholder="Clara")
        with col2:
            nom = st.text_input("Nom", placeholder="Martin")
        with col3:
            gender = st.selectbox("Genre", ["", "femme", "homme", "autre"], index=0)

        col4, col5, col6 = st.columns(3)
        with col4:
            city = st.text_input("Ville principale", placeholder="Paris, Lyon…")
        with col5:
            language = st.selectbox(
                "Langue d’accompagnement",
                ["", "français", "anglais", "arabe", "espagnol", "italien"],
                index=0,
            )
        with col6:
            size = st.selectbox(
                "Taille / morphologie (optionnel)",
                ["", "XS", "S", "M", "L", "XL", "2XL+"],
            )

        st.markdown("#### 2. Ton style & ton contexte")

        col7, col8 = st.columns(2)
        with col7:
            st.write("Style(s) dans lequel tu te reconnais")
            style = st.multiselect(
                "",
                ["casual", "chic", "streetwear", "minimal", "bohème", "élégant"],
                default=[],
            )

        with col8:
            job_sector = st.selectbox(
                "Contexte pro (facultatif)",
                [
                    "",
                    "cadres",
                    "dirigeantes",
                    "consultants",
                    "startups",
                    "étudiants",
                    "creatifs",
                    "freelances",
                ],
            )
            work_env = st.selectbox(
                "Ambiance vestimentaire au travail",
                [
                    "",
                    "Très formel (costume / tailleur)",
                    "Business casual",
                    "Créatif / détendu",
                    "Télétravail / freelance",
                ],
            )

        st.markdown("#### 3. Ton besoin aujourd’hui")

        col9, col10, col11 = st.columns(3)
        with col9:
            budget = st.selectbox(
                "Budget vestimentaire pour cette étape",
                ["", "moins de 100€", "100 - 300€", "300 - 1000€", "plus de 1000€"],
            )

        with col10:
            service_type = st.selectbox(
                "Type d’accompagnement",
                [
                    "",
                    "accompagnement_magasin",
                    "virtual_style",
                    "tri_dressing",
                    "relooking_complet",
                    "live_shopping",
                ],
            )

            mode = st.selectbox(
                "Format préféré",
                ["peu_importe", "presentiel", "visio"],
                index=0,
            )

        with col11:
            objective = st.selectbox(
                "Objectif principal",
                [
                    "",
                    "style_pro",
                    "mariage",
                    "confiance_en_soi",
                    "grandes_tailles",
                    "petit_budget",
                    "relooking",
                ],
            )
            life_event = st.selectbox(
                "Moment de vie",
                [
                    "aucun_particulier",
                    "nouveau_job",
                    "reconversion",
                    "grossesse/post-partum",
                    "séparation",
                    "burnout/épuisement",
                ],
            )

        needs_confidence = st.checkbox(
            "Je veux travailler ma confiance en moi / mon image"
        )

        st.markdown("#### 4. Quelques précisions (optionnel)")
        extra_info = st.text_area(
            "Raconte ton besoin (événement, complexes, couleurs que tu aimes, ce que tu veux éviter, etc.)",
            placeholder="Ex : tenues pro mais confortables, j’adore le noir et le beige, je ne veux pas de talons…",
            height=100,
        )
        favorite_brand = st.text_input(
            "Marques préférées (optionnel)",
            placeholder="Zara, Sézane, Uniqlo, Asos…",
        )

        submitted = st.form_submit_button("Trouver mon/ma personal shopper ✨")

    if not submitted:
        return

    client = {
        "nom": nom,
        "prenom": prenom,
        "gender": gender,
        "job_sector": job_sector,
        "work_env": work_env,
        "style": style,
        "size": size,
        "budget": budget,
        "language": language,
        "city": city,
        "favorite_brand": favorite_brand,
        "service_type": service_type,
        "objective": objective,
        "life_event": life_event,
        "needs_confidence": needs_confidence,
        "mode": mode,
        "extra_info": extra_info,
    }

    if not prenom or not nom or not city or not budget:
        st.error(
            "Merci de remplir au minimum prénom, nom, ville et budget pour que je puisse travailler correctement."
        )
        return

    with st.spinner("Analyse de ton profil et matching avec les personal shoppers…"):
        scored: List[Tuple[Dict, int, List[str]]] = []
        for sh in SHOPPERS:
            sc, reasons = match(client, sh)
            scored.append((sh, sc, reasons))

        scored = [item for item in scored if item[1] > 0]
        scored.sort(key=lambda x: x[1], reverse=True)

        if not scored:
            st.error(
                "Aucun personal shopper adapté pour le moment. Essaie d’élargir ta ville, ton style ou ton budget."
            )
            return

        best_shopper, best_score, best_reasons = scored[0]
        prebrief = generate_prebrief(client, best_shopper)

        assignment = {
            "id": str(uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "shopper_id": best_shopper["id"],
            "shopper_nom": best_shopper["nom"],
            "client": client,
            "prebrief": prebrief,
        }
        save_assignment(assignment)

    st.markdown("### Short-list de personal shoppers recommandés")

    for sh, sc, reasons in scored[:3]:
        # Header plus stylé : Nom — ⭐ note/5 — Ville
        with st.expander(f"{sh['nom']} — ⭐ {sh['note_moyenne']}/5 — {sh['zone']}"):
            st.markdown(
                f"**Styles :** {', '.join(sh['styles'])}  \n"
                f"**Spécialités :** {', '.join(sh['specialites'])}  \n"
                f"**Formats :** {', '.join(sh['formats'])}  \n"
                f"**Niveaux de budget pris en charge :** {', '.join(sh['niveau_budget'])}  \n"
                f"**Tags :** {' '.join(sh['tags'])}  \n"
                f"**Score de matching (règles + profil) :** {sc}/10"
            )
            if reasons:
                st.markdown("**Pourquoi ce profil te correspond (logique métier) :**")
                for r in reasons:
                    st.markdown(f"- {r}")


    st.markdown("---")
    st.markdown(f"### Focus IA sur ton meilleur match : **{best_shopper['nom']}**")

    with st.spinner("Génération d’un résumé personnalisé…"):
        summary = generate_ai_summary(client, best_shopper)

    st.write(summary)
    st.info(
        "Ton/ta personal shopper reçoit en coulisses un pré-brief détaillé pour préparer au mieux votre séance."
    )

def format_prebrief_markdown(prebrief: str) -> str:
    """
    Nettoie légèrement le Markdown renvoyé par le modèle pour garantir
    des sauts de ligne corrects (titres, listes, etc.).
    """
    if not prebrief:
        return ""

    text = prebrief

    # Forcer un saut de ligne avant les titres ### s'ils sont collés
    text = text.replace("###", "\n\n###")

    # Forcer chaque puce sur une nouvelle ligne
    text = text.replace("* **", "\n* **")

    # Éviter que le titre principal soit collé au reste
    text = text.replace("**Pré-brief", "\n**Pré-brief")

    return text.strip()

# ============================================================
# 6. UI – VUE PERSONAL SHOPPER
# ============================================================

def page_shopper():
    st.markdown(
        """
        <div class="pershop-header">
          <div class="pershop-header-left">
            <div class="pershop-logo-mark">P</div>
            <div>
              <div class="pershop-header-title">Pershop Pilote</div>
              <div class="pershop-header-sub">
                Cockpit pour préparer vos séances avec le support de l’IA.
              </div>
            </div>
          </div>
          <div class="pershop-header-badge">
            Espace personal shopper
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="card">
          <div class="card-title">Vos clients à venir</div>
          <div class="card-subtitle">
            Sélectionnez votre profil, puis parcourez les clients matchés avec vous
            et les pré-briefs générés automatiquement.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Sélection du PS
    options = {f"{s['nom']} – {s['zone']}": s["id"] for s in SHOPPERS}
    label = st.selectbox("Votre profil personal shopper", [""] + list(options.keys()))

    if not label or label not in options:
        return

    shopper_id = options[label]
    shopper = next(s for s in SHOPPERS if s["id"] == shopper_id)

    assignments = load_assignments()
    my_assignments = [a for a in assignments if a.get("shopper_id") == shopper_id]

    st.markdown(f"### Clients assignés à **{shopper['nom']}**")

    if not my_assignments:
        st.info("Aucun client n’a encore été assigné à ce profil.")
        return

    for a in reversed(my_assignments):  # plus récents en premier
        client = a["client"]
        raw_prebrief = a["prebrief"]
        prebrief = format_prebrief_markdown(raw_prebrief)
        timestamp = a.get("timestamp", "")[:19].replace("T", " ")

        titre_client = (client.get("prenom") or "Client") + " " + (client.get("nom") or "")

        with st.expander(f"{titre_client} — {timestamp}"):
            col1, col2 = st.columns(2)

            # --------- COLONNE 1 : profil client ---------
            with col1:
                st.markdown("#### Profil client")
                st.markdown(
                    f"""
                    - **Ville :** {client.get('city', 'N/A')}
                    - **Genre :** {client.get('gender', 'N/A')}
                    - **Style souhaité :** {', '.join(client.get('style', [])) or 'N/A'}
                    - **Budget :** {client.get('budget', 'N/A')}
                    - **Objectif :** {client.get('objective', 'N/A') or 'Non précisé'}
                    - **Moment de vie :** {client.get('life_event', 'N/A')}
                    - **Confiance en soi :** {"Oui" if client.get('needs_confidence') else "Non"}
                    """
                )
                extra = client.get("extra_info", "")
                if extra:
                    st.markdown("**Notes client :**")
                    st.write(extra)

            # --------- COLONNE 2 : pré-brief IA ---------
            with col2:
                st.markdown("#### Pré-brief IA pour préparer la séance")
                # On affiche le pré-brief dans un bloc stylé mais avec vrai Markdown
                st.markdown("<div class='prebrief-block'>", unsafe_allow_html=True)
                st.markdown(prebrief)
                st.markdown("</div>", unsafe_allow_html=True)



# ============================================================
# 7. ROUTAGE
# ============================================================

def main():
    st.sidebar.markdown("## Pershop Pilote")
    mode = st.sidebar.radio(
        "Choisissez votre espace",
        ["Je suis client", "Je suis personal shopper"],
    )

    if mode == "Je suis client":
        page_client()
    else:
        page_shopper()


if __name__ == "__main__":
    main()
