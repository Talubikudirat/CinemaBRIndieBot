import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

class CinemaBRScraper:
    def __init__(self):
        self.festivals = []
        self.news = []
        self.awards = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.timeout = 10
    
    def safe_get(self, url):
        """Safely fetch URL with error handling"""
        try:
            response = self.session.get(url, timeout=self.timeout)
            if response.status_code == 200:
                return response
            return None
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def get_festivals(self):
        """Scrape Brazilian film festivals from public sources"""
        festivals_data = []
        
        # Festival do Rio
        try:
            url = "https://www.festivaldorio.com.br"
            response = self.safe_get(url)
            if response:
                soup = BeautifulSoup(response.text, 'html.parser')
                festivals_data.append({
                    'name': 'Festival do Rio',
                    'description': 'Festival Internacional de Cinema do Rio de Janeiro',
                    'link': url,
                    'deadline': 'Verifique site oficial'
                })
        except Exception as e:
            print(f"Error: {e}")
        
        # Festival de Gramado
        try:
            url = "https://www.festivaldegramado.net"
            response = self.safe_get(url)
            if response:
                festivals_data.append({
                    'name': 'Festival de Gramado',
                    'description': 'Principal festival de cinema brasileiro',
                    'link': url,
                    'deadline': 'Inscrições abertas - Verifique site'
                })
        except Exception as e:
            print(f"Error: {e}")
        
        # Mostra de Tiradentes
        try:
            url = "https://www.mostratiradentes.com.br"
            response = self.safe_get(url)
            if response:
                festivals_data.append({
                    'name': 'Mostra de Cinema de Tiradentes',
                    'description': 'Mostra de cinema independente',
                    'link': url,
                    'deadline': 'Inscrições abertas - Verifique site'
                })
        except Exception as e:
            print(f"Error: {e}")
        
        # Festival de Brasília
        try:
            url = "https://www.festivaldebrasilia.com.br"
            response = self.safe_get(url)
            if response:
                festivals_data.append({
                    'name': 'Festival de Brasília do Cinema Brasileiro',
                    'description': 'Festival tradicional de cinema nacional',
                    'link': url,
                    'deadline': 'Consultar site oficial'
                })
        except Exception as e:
            print(f"Error: {e}")
        
        # Cine PE - Recife
        try:
            url = "https://www.cinepe.com.br"
            response = self.safe_get(url)
            if response:
                festivals_data.append({
                    'name': 'Cine PE - Festival do Recife',
                    'description': 'Festival de cinema de Pernambuco',
                    'link': url,
                    'deadline': 'Verifique site oficial'
                })
        except Exception as e:
            print(f"Error: {e}")
        
        # Curta Cinema
        try:
            url = "https://www.curtacinema.com.br"
            response = self.safe_get(url)
            if response:
                festivals_data.append({
                    'name': 'Curta Cinema - Festival de Curtas do Rio',
                    'description': 'Festival de curtas-metragens',
                    'link': url,
                    'deadline': 'Inscrições abertas'
                })
        except Exception as e:
            print(f"Error: {e}")
        
        # In-Edit Brasil
        try:
            url = "https://www.in-editbrasil.com.br"
            response = self.safe_get(url)
            if response:
                festivals_data.append({
                    'name': 'In-Edit Brasil',
                    'description': 'Festival de documentários',
                    'link': url,
                    'deadline': 'Consultar site'
                })
        except Exception as e:
            print(f"Error: {e}")
        
        # Forumdoc.bh
        try:
            url = "https://www.forumdocbh.com.br"
            response = self.safe_get(url)
            if response:
                festivals_data.append({
                    'name': 'Forumdoc.bh',
                    'description': 'Festival de documentários de Belo Horizonte',
                    'link': url,
                    'deadline': 'Verifique site oficial'
                })
        except Exception as e:
            print(f"Error: {e}")
        
        # FestCurtas BH
        try:
            url = "https://www.festcurtasbh.com.br"
            response = self.safe_get(url)
            if response:
                festivals_data.append({
                    'name': 'FestCurtas BH',
                    'description': 'Festival de curtas de Belo Horizonte',
                    'link': url,
                    'deadline': 'Inscrições abertas'
                })
        except Exception as e:
            print(f"Error: {e}")
        
        # ANCINE
        try:
            url = "https://www.gov.br/ancine/pt-br/assuntos/noticias"
            response = self.safe_get(url)
            if response:
                soup = BeautifulSoup(response.text, 'html.parser')
                for item in soup.find_all(['a', 'div'], class_=['summary', 'title'])[:2]:
                    title = item.get_text(strip=True)
                    if title and ('festival' in title.lower() or 'edital' in title.lower()):
                        link = item.get('href') if hasattr(item, 'get') else ''
                        if link and not link.startswith('http'):
                            link = urljoin(url, link)
                        festivals_data.append({
                            'name': title[:80],
                            'description': 'Edital/Convênio ANCINE',
                            'link': link if link else url,
                            'deadline': 'Consultar edital'
                        })
                        break
        except Exception as e:
            print(f"Error: {e}")
        
        # Deduplicate by name
        seen = set()
        unique_festivals = []
        for f in festivals_data:
            if f['name'] not in seen:
                seen.add(f['name'])
                unique_festivals.append(f)
        
        self.festivals = unique_festivals[:10]
        return self.festivals
    
    def get_news(self):
        """Scrape Brazilian cinema news"""
        news_list = []
        
        # AdoroCinema
        try:
            url = "https://www.adorocinema.com/noticias"
            response = self.safe_get(url)
            if response:
                soup = BeautifulSoup(response.text, 'html.parser')
                for item in soup.find_all(['h2', 'h3'], class_=['news-title', 'title'])[:3]:
                    title = item.get_text(strip=True)
                    link_tag = item.find('a')
                    link = link_tag.get('href') if link_tag else url
                    if title and len(title) > 5:
                        if not link.startswith('http'):
                            link = urljoin(url, link)
                        news_list.append({
                            'title': title[:100],
                            'link': link,
                            'source': 'AdoroCinema'
                        })
        except Exception as e:
            print(f"Error: {e}")
        
        # Omelete
        try:
            url = "https://www.omelete.com.br/filmes"
            response = self.safe_get(url)
            if response:
                soup = BeautifulSoup(response.text, 'html.parser')
                for item in soup.find_all(['h2', 'h3'])[:3]:
                    title = item.get_text(strip=True)
                    link_tag = item.find('a')
                    link = link_tag.get('href') if link_tag else url
                    if title and len(title) > 5:
                        if not link.startswith('http'):
                            link = urljoin(url, link)
                        news_list.append({
                            'title': title[:100],
                            'link': link,
                            'source': 'Omelete'
                        })
        except Exception as e:
            print(f"Error: {e}")
        
        # ANCINE
        try:
            url = "https://www.gov.br/ancine/pt-br/assuntos/noticias"
            response = self.safe_get(url)
            if response:
                soup = BeautifulSoup(response.text, 'html.parser')
                for item in soup.find_all('a', class_='summary')[:3]:
                    title = item.get_text(strip=True)
                    if title and len(title) > 5:
                        link = item.get('href', '')
                        if link and not link.startswith('http'):
                            link = urljoin(url, link)
                        news_list.append({
                            'title': title[:100],
                            'link': link if link else url,
                            'source': 'ANCINE'
                        })
        except Exception as e:
            print(f"Error: {e}")
        
        self.news = news_list[:8]
        return self.news
    
    def get_awards(self):
        """Get recent award winners"""
        awards = [
            {
                'name': 'Grande Prêmio do Cinema Brasileiro',
                'category': 'Melhor Filme',
                'winner': 'Confira no site da ANCINE',
                'year': datetime.now().year
            },
            {
                'name': 'Festival de Gramado - Kikito de Ouro',
                'category': 'Melhor Filme Brasileiro',
                'winner': 'Resultados divulgados no site oficial',
                'year': datetime.now().year
            },
            {
                'name': 'Prêmio ABRACCINE',
                'category': 'Melhor Filme',
                'winner': 'Indicações e vencedores no site oficial',
                'year': datetime.now().year
            },
            {
                'name': 'Festival do Rio - Redentor',
                'category': 'Competição Oficial',
                'winner': 'Consultar site para vencedores',
                'year': datetime.now().year
            },
            {
                'name': 'Mostra de Tiradentes - Aurora de Ouro',
                'category': 'Competição',
                'winner': 'Resultados disponíveis no site',
                'year': datetime.now().year
            }
        ]
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
