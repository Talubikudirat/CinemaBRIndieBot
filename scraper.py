import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

class CinemaBRScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0'})
    
    def get_festivals(self):
        data = []
        sites = [
            ('Festival do Rio', 'https://www.festivaldorio.com.br'),
            ('Festival de Gramado', 'https://www.festivaldegramado.net'),
            ('Mostra de Tiradentes', 'https://www.mostratiradentes.com.br'),
            ('Festival de Brasília', 'https://www.festivaldebrasilia.com.br'),
            ('Cine PE', 'https://www.cinepe.com.br'),
            ('Curta Cinema RJ', 'https://www.curtacinema.com.br'),
        ]
        for name, url in sites:
            data.append({'name': name, 'description': 'Festival de cinema', 'link': url, 'deadline': 'Verifique site'})
        return data
    
    def get_news(self):
        data = []
        sites = [
            ('AdoroCinema', 'https://www.adorocinema.com/noticias'),
            ('Omelete', 'https://www.omelete.com.br/filmes'),
        ]
        for name, url in sites:
            try:
                r = self.session.get(url, timeout=10)
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text, 'html.parser')
                    for item in soup.find_all(['h2', 'h3'])[:2]:
                        title = item.get_text(strip=True)
                        if title and len(title) > 5:
                            link = item.find('a')
                            link_url = link.get('href') if link else url
                            if link_url and not link_url.startswith('http'):
                                link_url = urljoin(url, link_url)
                            data.append({'title': title[:80], 'link': link_url, 'source': name})
            except:
                pass
        return data
    
    def get_awards(self):
        return [
            {'name': 'Grande Prêmio do Cinema Brasileiro', 'category': 'Melhor Filme', 'winner': 'Confira ANCINE', 'year': datetime.now().year},
            {'name': 'Festival de Gramado', 'category': 'Kikito de Ouro', 'winner': 'Site oficial', 'year': datetime.now().year},
        ]
    
    def get_daily_summary(self):
        return {'festivals': self.get_festivals(), 'news': self.get_news(), 'awards': self.get_awards(), 'date': datetime.now().strftime('%d/%m/%Y')}
