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

# Aktuelle Briefings basierend auf echten Nachrichten
SAMPLE_NEWS_DATA = [
    {
        "id": 1,
        "headline": "Israel-Iran Konflikt eskaliert dramatisch",
        "topic": "Nahost-Konflikt",
        "date": "2025-06-13",
        "current_news": {
            "text": "Israel hat in der Nacht einen Großangriff auf iranische Atomanlagen und militärische Ziele gestartet, gefolgt von einer zweiten Angriffswelle am Tag. Iran droht mit massiver Vergeltung und spricht von einem 'Atomkonflikt'.",
            "source": "ARD Brennpunkt",
            "date": "13.06.2025"
        },
        "context": {
            "key_facts": [
                "Direkter Angriff auf iranische Nuklearanlagen",
                "Zweite Angriffswelle verstärkt die Eskalation",
                "Iran droht mit beispielloser Vergeltung"
            ],
            "timeline": [
                {"date": "Oktober 2023", "event": "Hamas-Angriff löst Gaza-Krieg aus"},
                {"date": "April 2024", "event": "Erste direkte Iran-Israel Konfrontation"},
                {"date": "Januar 2025", "event": "Verstärkte Spannungen um Nuklearprogramm"},
                {"date": "Juni 2025", "event": "Israel greift iranische Atomanlagen an"}
            ],
            "perspectives": {
                "pro": "Israel sieht präventive Schläge als notwendig zur Verhinderung iranischer Atomwaffen.",
                "con": "Militärische Eskalation gefährdet regionalen Frieden und könnte globale Krise auslösen."
            },
            "deep_dive": {
                "question": "Welche Auswirkungen hat die Eskalation auf die Weltwirtschaft?",
                "video_link": "https://www.tagesschau.de/multimedia/video/video-1234567.html",
                "article_link": "https://www.tagesschau.de/ausland/asien/israel-iran-konflikt-100.html"
            }
        }
    },
    {
        "id": 2,
        "headline": "Musk-Trump Allianz zerbricht in öffentlicher Schlammschlacht",
        "topic": "US-Politik",
        "date": "2025-06-06",
        "current_news": {
            "text": "Die monatelange politische Allianz zwischen Tech-Milliardär Elon Musk und US-Präsident Donald Trump ist in einer öffentlich ausgetragenen Schlammschlacht zerbrochen. Beide attackieren sich gegenseitig über soziale Medien.",
            "source": "news.de",
            "date": "06.06.2025"
        },
        "context": {
            "key_facts": [
                "Ehemals enge politische Partnerschaft zerbrochen",
                "Öffentliche Angriffe über Social Media Plattformen",
                "Auswirkungen auf Tech-Politik und Wirtschaft erwartet"
            ],
            "timeline": [
                {"date": "November 2024", "event": "Musk unterstützt Trump-Wahlkampf massiv"},
                {"date": "Januar 2025", "event": "Musk wird informeller Tech-Berater"},
                {"date": "März 2025", "event": "Erste Meinungsverschiedenheiten über KI-Regulierung"},
                {"date": "Juni 2025", "event": "Öffentlicher Bruch der Allianz"}
            ],
            "perspectives": {
                "pro": "Unabhängigkeit von Tech-Unternehmern stärkt demokratische Institutionen.",
                "con": "Politische Instabilität schadet amerikanischer Technologie-Führerschaft."
            },
            "deep_dive": {
                "question": "Wie beeinflusst der Streit die Zukunft der Tech-Regulierung?",
                "video_link": "https://www.tagesschau.de/multimedia/video/video-trump-musk.html",
                "article_link": "https://www.tagesschau.de/ausland/amerika/trump-musk-konflikt-100.html"
            }
        }
    },
    {
        "id": 3,
        "headline": "Deutsche Wirtschaft wächst überraschend stark",
        "topic": "Deutsche Wirtschaft",
        "date": "2025-06-13",
        "current_news": {
            "text": "Deutschlands Wirtschaft ist im ersten Quartal 2025 um 0,4% gewachsen und übertrifft damit die ursprünglichen Prognosen. Das Wachstum fiel stärker aus als zunächst gemeldet, zeigen neue Daten des Wirtschaftsministeriums.",
            "source": "DATEV magazin",
            "date": "13.06.2025"
        },
        "context": {
            "key_facts": [
                "BIP-Wachstum von 0,4% übertrifft Erwartungen",
                "Preisbereinigte Daten zeigen solide Entwicklung",
                "Positive Signale nach schwierigen Vorjahren"
            ],
            "timeline": [
                {"date": "2023", "event": "Deutschland in technischer Rezession"},
                {"date": "Q4 2024", "event": "Erste Erholungszeichen sichtbar"},
                {"date": "Q1 2025", "event": "Überraschend starkes Wachstum"},
                {"date": "Juni 2025", "event": "Korrektur der Zahlen nach oben"}
            ],
            "perspectives": {
                "pro": "Robuste Wirtschaft trotz globaler Herausforderungen zeigt deutsche Stärke.",
                "con": "Ein Quartal reicht nicht aus, um von nachhaltiger Erholung zu sprechen."
            },
            "deep_dive": {
                "question": "Ist die deutsche Wirtschaftskrise überwunden?",
                "video_link": "https://www.tagesschau.de/multimedia/video/video-wirtschaft-deutschland.html",
                "article_link": "https://www.tagesschau.de/wirtschaft/deutschland/wirtschaftswachstum-q1-2025-100.html"
            }
        }
    },
    {
        "id": 4,
        "headline": "Ukraine-Krieg: Massive russische Angriffe auf Kiew und Odessa",
        "topic": "Ukraine-Krieg",
        "date": "2025-06-10",
        "current_news": {
            "text": "Russland hat die Ukraine erneut mit massiven Drohnen- und Raketen-Angriffen überzogen. In der Hafenstadt Odessa starb mindestens ein Mensch bei einem Drohnenangriff, während Kiew unter schwerem Beschuss stand.",
            "source": "news.de",
            "date": "10.06.2025"
        },
        "context": {
            "key_facts": [
                "Massive Angriffe auf zivile Infrastruktur",
                "Mindestens ein Todesopfer in Odessa bestätigt",
                "Verstärkte Angriffe auf Hafenstädte"
            ],
            "timeline": [
                {"date": "Februar 2022", "event": "Russischer Überfall auf Ukraine"},
                {"date": "2024", "event": "Krieg entwickelt sich zu Stellungskrieg"},
                {"date": "Frühjahr 2025", "event": "Neue russische Offensive"},
                {"date": "Juni 2025", "event": "Intensivierte Angriffe auf Städte"}
            ],
            "perspectives": {
                "pro": "Verstärkte Waffenlieferungen an Ukraine sind moralisch und strategisch notwendig.",
                "con": "Militärische Eskalation verlängert nur das Leiden und verhindert Verhandlungen."
            },
            "deep_dive": {
                "question": "Wie entwickelt sich die militärische Lage nach über 3 Jahren Krieg?",
                "video_link": "https://www.tagesschau.de/multimedia/video/video-ukraine-krieg.html",
                "article_link": "https://www.tagesschau.de/ausland/ukraine/ukraine-russland-angriffe-100.html"
            }
        }
    },
    {
        "id": 5,
        "headline": "Anstieg politisch motivierter Straftaten in Deutschland",
        "topic": "Innere Sicherheit",
        "date": "2025-06-10",
        "current_news": {
            "text": "Die Zahl politisch motivierter Straftaten in Deutschland ist deutlich gestiegen. Besonders Angriffe auf Politiker und demokratische Institutionen nehmen zu, wie neue Statistiken zeigen.",
            "source": "ZDF heute",
            "date": "10.06.2025"
        },
        "context": {
            "key_facts": [
                "Deutlicher Anstieg politisch motivierter Gewalt",
                "Politiker zunehmend Ziel von Angriffen",
                "Demokratische Institutionen unter Druck"
            ],
            "timeline": [
                {"date": "2020-2022", "event": "Erste Zunahme extremistischer Vorfälle"},
                {"date": "2023", "event": "Angriffe auf Wahlkampfveranstaltungen"},
                {"date": "2024", "event": "Verstärkte Bedrohungen gegen Amtsträger"},
                {"date": "Juni 2025", "event": "Neue Rekordwerte in Kriminalstatistik"}
            ],
            "perspectives": {
                "pro": "Härte gegen politische Gewalt schützt die Demokratie und ihre Vertreter.",
                "con": "Übertriebene Sicherheitsmaßnahmen könnten demokratische Teilhabe einschränken."
            },
            "deep_dive": {
                "question": "Wie kann die Demokratie vor Extremismus geschützt werden?",
                "video_link": "https://www.tagesschau.de/multimedia/video/video-politische-gewalt.html",
                "article_link": "https://www.tagesschau.de/inland/innenpolitik/politische-gewalt-statistik-100.html"
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
