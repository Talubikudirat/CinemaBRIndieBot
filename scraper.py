import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

class CinemaBRScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    
    def get_festivals(self):
        data = []
        sites = [
            ('Festival do Rio', 'https://www.festivaldorio.com.br'),
            ('Festival de Gramado', 'https://www.festivaldegramado.net'),
            ('Mostra de Tiradentes', 'https://www.mostratiradentes.com.br'),
            ('Festival de Brasília', 'https://www.festivaldebrasilia.com.br'),
            ('Cine PE - Recife', 'https://www.cinepe.com.br'),
            ('Curta Cinema - RJ', 'https://www.curtacinema.com.br'),
            ('In-Edit Brasil', 'https://www.in-editbrasil.com.br'),
            ('Forumdoc.bh', 'https://www.forumdocbh.com.br'),
            ('FestCurtas BH', 'https://www.festcurtasbh.com.br'),
        ]
        for name, url in sites:
            try:
                response = self.session.get(url, timeout=8)
                if response.status_code == 200:
                    data.append({
                        'name': name,
                        'description': 'Festival de cinema - Verifique site para inscrições',
                        'link': url,
                        'deadline': 'Consulte o site oficial'
                    })
            except:
                data.append({
                    'name': name,
                    'description': 'Festival de cinema - Visite o site',
                    'link': url,
                    'deadline': 'Verifique site'
                })
        
        # Try ANCINE
        try:
            url = "https://www.gov.br/ancine/pt-br/assuntos/noticias"
            response = self.session.get(url, timeout=8)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                for item in soup.find_all('a', class_='summary')[:2]:
                    title = item.get_text(strip=True)
                    if title and ('festival' in title.lower() or 'edital' in title.lower()):
                        link = item.get('href', '')
                        if link and not link.startswith('http'):
                            link = urljoin(url, link)
                        data.append({
                            'name': title[:60],
                            'description': 'Edital/Convênio ANCINE',
                            'link': link if link else url,
                            'deadline': 'Consulte edital'
                        })
                        break
        except:
            pass
        
        return data
    
    def get_news(self):
        data = []
        sites = [
            ('AdoroCinema', 'https://www.adorocinema.com/noticias'),
            ('Omelete', 'https://www.omelete.com.br/filmes'),
        ]
        for name, url in sites:
            try:
                response = self.session.get(url, timeout=8)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    for item in soup.find_all(['h2', 'h3'])[:3]:
                        title = item.get_text(strip=True)
                        if title and len(title) > 10:
                            link_tag = item.find('a')
                            link = link_tag.get('href') if link_tag else url
                            if link and not link.startswith('http'):
                                link = urljoin(url, link)
                            data.append({
                                'title': title[:100],
                                'link': link if link else url,
                                'source': name
                            })
            except:
                pass
        
        # Try ANCINE news
        try:
            url = "https://www.gov.br/ancine/pt-br/assuntos/noticias"
            response = self.session.get(url, timeout=8)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                for item in soup.find_all('a', class_='summary')[:3]:
                    title = item.get_text(strip=True)
                    if title and len(title) > 10:
                        link = item.get('href', '')
                        if link and not link.startswith('http'):
                            link = urljoin(url, link)
                        data.append({
                            'title': title[:100],
                            'link': link if link else url,
                            'source': 'ANCINE'
                        })
        except:
            pass
        
        return data[:8]
    
    def get_awards(self):
        return [
            {'name': 'Grande Prêmio do Cinema Brasileiro', 'category': 'Melhor Filme', 'winner': 'Ver site ANCINE', 'year': datetime.now().year},
            {'name': 'Festival de Gramado - Kikito de Ouro', 'category': 'Melhor Filme Brasileiro', 'winner': 'Ver site oficial', 'year': datetime.now().year},
            {'name': 'Prêmio ABRACCINE', 'category': 'Melhor Filme', 'winner': 'Ver site ABRACCINE', 'year': datetime.now().year},
            {'name': 'Festival do Rio - Redentor', 'category': 'Competição Oficial', 'winner': 'Ver site do festival', 'year': datetime.now().year},
        ]
    
    def get_daily_summary(self):
        return {
            'festivals': self.get_festivals(),
            'news': self.get_news(),
            'awards': self.get_awards(),
            'date': datetime.now().strftime('%d/%m/%Y')
        }
