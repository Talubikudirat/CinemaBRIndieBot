import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import feedparser

class CinemaBRScraper:
    def __init__(self):
        self.festivals = []
        self.news = []
        self.awards = []
    
    def get_festivals(self):
        """Scrape from public Brazilian film festival sites"""
        festivals_data = []
        
        # 1. ANCINE - Public announcements (no API key needed)
        try:
            url = "https://www.gov.br/ancine/pt-br/assuntos/noticias"
            response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for item in soup.find_all('a', class_='summary'):
                title = item.get_text(strip=True)
                if 'festival' in title.lower() or 'edital' in title.lower():
                    festivals_data.append({
                        'name': title[:60],
                        'description': 'Edital/Convênio ANCINE',
                        'link': item.get('href', '#'),
                        'deadline': 'Verifique o edital'
                    })
        except:
            pass
        
        # 2. Festival do Rio - Public schedule
        try:
            url = "https://www.festivaldorio.com.br/"
            response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.text, 'html.parser')
            # Just generic scraping - adjust as needed
            festivals_data.append({
                'name': 'Festival do Rio',
                'description': 'Um dos maiores festivais de cinema do Brasil',
                'link': url,
                'deadline': 'Verifique site oficial'
            })
        except:
            pass
        
        # 3. Festival de Gramado
        try:
            festivals_data.append({
                'name': 'Festival de Gramado',
                'description': 'Principal festival de cinema brasileiro',
                'link': 'https://www.festivaldegramado.net',
                'deadline': 'Inscrições abertas anualmente'
            })
        except:
            pass
        
        # 4. Mostra de Cinema de Tiradentes
        try:
            festivals_data.append({
                'name': 'Mostra de Cinema de Tiradentes',
                'description': 'Mostra de cinema independente',
                'link': 'https://www.mostratiradentes.com.br',
                'deadline': 'Inscrições abertas'
            })
        except:
            pass
        
        # 5. Brasília Festival - Cine Brasília
        try:
            festivals_data.append({
                'name': 'Festival de Brasília do Cinema Brasileiro',
                'description': 'Festival tradicional de cinema nacional',
                'link': 'https://www.festivaldebrasilia.com.br',
                'deadline': 'Consultar site'
            })
        except:
            pass
        
        # 6. API pública de cinemas - Free RSS feeds
        try:
            # Some festivals have RSS feeds (no key needed)
            rss_urls = [
                'https://www.festivaldorio.com.br/feed',
                # Add more public RSS feeds
            ]
            for rss in rss_urls:
                try:
                    feed = feedparser.parse(rss)
                    if feed.entries:
                        for entry in feed.entries[:2]:
                            festivals_data.append({
                                'name': entry.title[:60] if hasattr(entry, 'title') else 'Evento',
                                'description': entry.summary[:100] if hasattr(entry, 'summary') else 'Evento',
                                'link': entry.link if hasattr(entry, 'link') else '#',
                                'deadline': 'Verifique site'
                            })
                except:
                    pass
        except:
            pass
        
        # Deduplicate
        seen = set()
        unique_festivals = []
        for f in festivals_data:
            if f['name'] not in seen:
                seen.add(f['name'])
                unique_festivals.append(f)
        
        self.festivals = unique_festivals[:10]  # Limit to 10
        return self.festivals
    
    def get_news(self):
        """Scrape Brazilian cinema news from public sources"""
        news_list = []
        
        # 1. ANCINE News
        try:
            url = "https://www.gov.br/ancine/pt-br/assuntos/noticias"
            response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for item in soup.find_all('a', class_='summary')[:5]:
                title = item.get_text(strip=True)
                if title:
                    news_list.append({
                        'title': title[:100],
                        'link': item.get('href', '#'),
                        'source': 'ANCINE'
                    })
        except:
            pass
        
        # 2. Cinema Brazil - Public site
        try:
            url = "https://cinemabrasil.com.br/"
            response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.text, 'html.parser')
            for item in soup.find_all('h2', class_='entry-title')[:3]:
                title = item.get_text(strip=True)
                link = item.find('a')
                if title:
                    news_list.append({
                        'title': title[:100],
                        'link': link.get('href', '#') if link else '#',
                        'source': 'Cinema Brasil'
                    })
        except:
            pass
        
        # 3. Public RSS from film websites
        try:
            rss_feeds = [
                'https://cinemabrasil.com.br/feed',
            ]
            for feed_url in rss_feeds:
                try:
                    feed = feedparser.parse(feed_url)
                    for entry in feed.entries[:2]:
                        news_list.append({
                            'title': entry.title[:100] if hasattr(entry, 'title') else 'Notícia',
                            'link': entry.link if hasattr(entry, 'link') else '#',
                            'source': 'RSS'
                        })
                except:
                    pass
        except:
            pass
        
        self.news = news_list[:8]
        return self.news
    
    def get_awards(self):
        """Get recent award winners"""
        awards = [
            {
                'name': 'Grande Prêmio do Cinema Brasileiro',
                'category': 'Melhor Filme',
                'winner': 'Verifique site oficial',
                'year': datetime.now().year
            },
            {
                'name': 'Festival de Gramado - Kikito de Ouro',
                'category': 'Melhor Filme',
                'winner': 'Resultados do último festival',
                'year': datetime.now().year
            }
        ]
        
        # Try to get actual data
        try:
            url = "https://www.ancine.gov.br"
            response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            if response.status_code == 200:
                awards.append({
                    'name': 'Edital ANCINE',
                    'category': 'Fomento',
                    'winner': 'Chamada pública aberta',
                    'year': datetime.now().year
                })
        except:
            pass
        
        self.awards = awards
        return self.awards

    def get_daily_summary(self):
        """Get all data in one call"""
        return {
            'festivals': self.get_festivals(),
            'news': self.get_news(),
            'awards': self.get_awards(),
            'date': datetime.now().strftime('%d/%m/%Y')
        }
