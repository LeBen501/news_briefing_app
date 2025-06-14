import streamlit as st
import datetime
from typing import Dict, List
import requests
import json

# Seitenkonfiguration
st.set_page_config(
    page_title="Weltgeschehen Briefings",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS für besseres Design
st.markdown("""
<style>
    .hook-container {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        background-color: #f8f9fa;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .hook-container:hover {
        background-color: #e9ecef;
        border-color: #007bff;
    }
    .hook-headline {
        font-size: 18px;
        font-weight: bold;
        color: #333;
        margin-bottom: 5px;
    }
    .hook-topic {
        color: #007bff;
        font-size: 14px;
        font-weight: 500;
        margin-bottom: 3px;
    }
    .hook-date {
        color: #666;
        font-size: 12px;
    }
    .briefing-section {
        margin: 20px 0;
        padding: 15px;
        border-left: 4px solid #007bff;
        background-color: #f8f9fa;
    }
    .pro-con-container {
        display: flex;
        gap: 20px;
        margin: 15px 0;
    }
    .pro-argument, .con-argument {
        flex: 1;
        padding: 15px;
        border-radius: 8px;
    }
    .pro-argument {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
    }
    .con-argument {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
    }
    .timeline-item {
        border-left: 2px solid #007bff;
        padding-left: 15px;
        margin-bottom: 10px;
        position: relative;
    }
    .timeline-item::before {
        content: '';
        position: absolute;
        left: -6px;
        top: 0;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background-color: #007bff;
    }
</style>
""", unsafe_allow_html=True)

# Beispieldaten (in echter App würden hier API-Aufrufe stehen)
SAMPLE_NEWS_DATA = [
    {
        "id": 1,
        "headline": "EU-Parlament verabschiedet KI-Gesetz",
        "topic": "Technologie & Regulierung",
        "date": "2025-06-14",
        "current_news": {
            "text": "Das Europäische Parlament hat heute das weltweit erste umfassende KI-Gesetz verabschiedet. Das Gesetz soll Risiken von Künstlicher Intelligenz minimieren und gleichzeitig Innovation fördern. Die Abstimmung fiel mit 523 zu 46 Stimmen deutlich aus.",
            "source": "Tagesschau",
            "date": "14.06.2025"
        },
        "context": {
            "key_facts": [
                "Erstes umfassendes KI-Gesetz weltweit",
                "Risikobasierter Ansatz: Höhere Risiken = strengere Regeln",
                "Inkrafttreten schrittweise ab 2026"
            ],
            "timeline": [
                {"date": "April 2021", "event": "EU-Kommission stellt ersten Entwurf vor"},
                {"date": "Juni 2023", "event": "Parlament stimmt Verhandlungsposition zu"},
                {"date": "Dezember 2023", "event": "Politische Einigung mit EU-Rat"},
                {"date": "Juni 2025", "event": "Finale Verabschiedung im Parlament"}
            ],
            "perspectives": {
                "pro": "Schafft Rechtssicherheit für Unternehmen und schützt Bürgerrechte vor KI-Missbrauch.",
                "con": "Könnte Innovation bremsen und europäische Unternehmen im globalen Wettbewerb benachteiligen."
            },
            "deep_dive": {
                "question": "Wie wird das KI-Gesetz konkret umgesetzt?",
                "video_link": "https://www.tagesschau.de/multimedia/video/",
                "article_link": "https://www.tagesschau.de/ausland/europa/ki-gesetz-eu-100.html"
            }
        }
    },
    {
        "id": 2,
        "headline": "Klimagipfel COP30 startet in Rio",
        "topic": "Klimawandel",
        "date": "2025-06-13",
        "current_news": {
            "text": "In Rio de Janeiro hat die 30. UN-Klimakonferenz begonnen. Über 190 Länder beraten über verschärfte Klimaziele bis 2035. Brasilien als Gastgeber drängt auf konkrete Zusagen zum Regenwaldschutz.",
            "source": "ARD",
            "date": "13.06.2025"
        },
        "context": {
            "key_facts": [
                "Fokus auf 2035-Klimaziele (NDCs)",
                "Finanzierung für Entwicklungsländer im Zentrum",
                "Erstmals verbindliche Regenwaldschutz-Zusagen geplant"
            ],
            "timeline": [
                {"date": "November 2024", "event": "COP29 in Baku: Finanzierungszusagen"},
                {"date": "März 2025", "event": "G20 einigt sich auf Vorverhandlungen"},
                {"date": "Mai 2025", "event": "EU präsentiert verschärfte Klimaziele"},
                {"date": "Juni 2025", "event": "COP30 beginnt in Rio de Janeiro"}
            ],
            "perspectives": {
                "pro": "Internationale Zusammenarbeit ist der einzige Weg, die Klimakrise zu bewältigen.",
                "con": "Klimagipfel führen oft zu unverbindlichen Absichtserklärungen ohne echte Wirkung."
            },
            "deep_dive": {
                "question": "Welche konkreten Ergebnisse sind von COP30 zu erwarten?",
                "video_link": "https://www.tagesschau.de/multimedia/video/",
                "article_link": "https://www.tagesschau.de/ausland/amerika/cop30-rio-100.html"
            }
        }
    },
    {
        "id": 3,
        "headline": "Chinas Wirtschaft wächst schwächer als erwartet",
        "topic": "Weltwirtschaft",
        "date": "2025-06-12",
        "current_news": {
            "text": "Chinas BIP ist im zweiten Quartal nur um 4,2% gewachsen, deutlich unter den prognostizierten 5,1%. Experten sehen die schwächelnde Immobilienbranche und geringe Konsumausgaben als Hauptgründe. Die Regierung kündigt Konjunkturmaßnahmen an.",
            "source": "Handelsblatt",
            "date": "12.06.2025"
        },
        "context": {
            "key_facts": [
                "Wachstum von 4,2% unter Erwartungen (5,1%)",
                "Immobilienkrise belastet weiterhin die Wirtschaft",
                "Neue Konjunkturpakete in Vorbereitung"
            ],
            "timeline": [
                {"date": "2023", "event": "Immobilienkrise erreicht Höhepunkt"},
                {"date": "Q1 2025", "event": "Wachstum bei 5,3%"},
                {"date": "April 2025", "event": "Erste Warnzeichen in Industrieproduktion"},
                {"date": "Juni 2025", "event": "Q2-Zahlen enttäuschen Märkte"}
            ],
            "perspectives": {
                "pro": "Chinas verlangsamtes Wachstum kann globale Inflation dämpfen und Rohstoffpreise stabilisieren.",
                "con": "Als zweitgrößte Volkswirtschaft bedroht Chinas Schwäche die globale Konjunktur."
            },
            "deep_dive": {
                "question": "Wie wirkt sich Chinas Wirtschaftslage auf Deutschland aus?",
                "video_link": "https://www.tagesschau.de/multimedia/video/",
                "article_link": "https://www.tagesschau.de/wirtschaft/weltwirtschaft/china-wachstum-100.html"
            }
        }
    }
]

def get_news_data():
    """
    In einer echten App würde hier eine API-Abfrage stehen:
    - News API (newsapi.org)
    - RSS Feeds von Nachrichtenquellen
    - Eigene Datenbank mit gecrawlten Artikeln
    """
    return SAMPLE_NEWS_DATA

def display_hook(news_item: Dict):
    """Zeigt einen News-Hook an"""
    hook_html = f"""
    <div class="hook-container">
        <div class="hook-headline">{news_item['headline']}</div>
        <div class="hook-topic">{news_item['topic']}</div>
        <div class="hook-date">{datetime.datetime.strptime(news_item['date'], '%Y-%m-%d').strftime('%d.%m.%Y')}</div>
    </div>
    """
    return hook_html

def display_briefing(news_item: Dict):
    """Zeigt ein vollständiges Briefing an"""
    st.markdown("## 📰 Aktuelle Nachricht")
    
    current = news_item['current_news']
    st.markdown(f"""
    <div class="briefing-section">
        <p><strong>{current['text']}</strong></p>
        <p><em>Quelle: {current['source']} | {current['date']}</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## 🧠 Kontext")
    
    # Kernfakten
    st.markdown("### 🎯 Kernfakten")
    for fact in news_item['context']['key_facts']:
        st.markdown(f"• {fact}")
    
    # Verlauf/Timeline
    st.markdown("### 📅 Verlauf")
    for item in news_item['context']['timeline']:
        st.markdown(f"""
        <div class="timeline-item">
            <strong>{item['date']}:</strong> {item['event']}
        </div>
        """, unsafe_allow_html=True)
    
    # Perspektiven
    st.markdown("### 💭 Perspektiven")
    perspectives = news_item['context']['perspectives']
    st.markdown(f"""
    <div class="pro-con-container">
        <div class="pro-argument">
            <strong>✅ Pro-Argument:</strong><br>
            {perspectives['pro']}
        </div>
        <div class="con-argument">
            <strong>❌ Contra-Argument:</strong><br>
            {perspectives['con']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Vertiefung
    st.markdown("### 🔍 Vertiefung")
    deep_dive = news_item['context']['deep_dive']
    st.markdown(f"**{deep_dive['question']}**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"[📺 Video ansehen]({deep_dive['video_link']})")
    with col2:
        st.markdown(f"[📄 Artikel lesen]({deep_dive['article_link']})")

def main():
    st.title("🌍 Weltgeschehen Briefings")
    st.markdown("*Schnell informiert, bereit für Diskussionen*")
    
    # Daten laden
    news_data = get_news_data()
    
    # Session State für expandierte Briefings
    if 'expanded_briefing' not in st.session_state:
        st.session_state.expanded_briefing = None
    
    # Zurück-Button falls Briefing geöffnet
    if st.session_state.expanded_briefing is not None:
        if st.button("⬅️ Zurück zur Übersicht"):
            st.session_state.expanded_briefing = None
            st.experimental_rerun()
    
    # Briefing anzeigen oder Hook-Übersicht
    if st.session_state.expanded_briefing is not None:
        # Vollständiges Briefing anzeigen
        selected_item = next(item for item in news_data if item['id'] == st.session_state.expanded_briefing)
        display_briefing(selected_item)
    else:
        # Hook-Übersicht anzeigen
        st.markdown("## 📊 Aktuelle Themen")
        st.markdown("*Klicke auf einen Hook für das vollständige Briefing*")
        
        for news_item in news_data:
            # Hook anzeigen
            hook_html = display_hook(news_item)
            st.markdown(hook_html, unsafe_allow_html=True)
            
            # Button für Briefing
            if st.button(f"Briefing öffnen", key=f"btn_{news_item['id']}"):
                st.session_state.expanded_briefing = news_item['id']
                st.experimental_rerun()
            
            st.markdown("---")
    
    # Sidebar mit Informationen
    with st.sidebar:
        st.markdown("## ℹ️ Über diese App")
        st.markdown("""
        Diese App hilft dir dabei:
        - **Schnell** über Weltgeschehnisse informiert zu werden
        - **Kontext** zu verstehen
        - **Diskussionen** vorzubereiten
        
        ### 🔧 Features:
        - Aktuelle Nachrichten-Hooks
        - Detaillierte Briefings
        - Pro & Contra Perspektiven
        - Vertiefende Materialien
        """)
        
        st.markdown("## 🔄 Datenquellen")
        st.markdown("""
        - Tagesschau
        - ARD/ZDF
        - Handelsblatt
        - Reuters
        
        *Letzte Aktualisierung: Heute*
        """)

if __name__ == "__main__":
    main()
