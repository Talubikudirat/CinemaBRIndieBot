from telegraph import Telegraph
from datetime import datetime

class TelegraphUploader:
    def __init__(self):
        self.telegraph = Telegraph()
        try:
            self.telegraph.create_account(short_name='CinemaBRIndie', author_name='Cinema BR Indie Bot')
        except:
            pass
    
    def create_daily_article(self, data):
        content = [
            {"tag": "h1", "children": ["🎬 Cinema Independente BR"]},
            {"tag": "p", "children": [f"📅 {data['date']}"]},
            {"tag": "p", "children": ["📢 ANÚNCIO - Seu anúncio aqui"]},
            {"tag": "p", "children": ["<img src='https://via.placeholder.com/728x90/FF6B6B/FFFFFF?text=ANUNCIE+AQUI' />"]},
            {"tag": "h2", "children": ["🏆 Festivais"]},
        ]
        for f in data['festivals'][:5]:
            content.append({"tag": "p", "children": [f"🎬 {f['name']} - {f['link']}"]})
        
        content.append({"tag": "p", "children": ["📢 ANÚNCIO - Seu anúncio aqui"]})
        content.append({"tag": "h2", "children": ["📰 Notícias"]})
        
        for n in data['news'][:5]:
            content.append({"tag": "p", "children": [f"📌 {n['title']} - {n['link']}"]})
        
        content.append({"tag": "h2", "children": ["🏅 Premiações"]})
        for a in data['awards']:
            content.append({"tag": "p", "children": [f"🎯 {a['name']} - {a['winner']}"]})
        
        content.append({"tag": "p", "children": ["💡 Siga @CinemaBRIndieBot"]})
        
        try:
            r = self.telegraph.create_page(
                title=f"Cinema BR - {datetime.now().strftime('%d/%m/%Y')}",
                author_name="Cinema BR Indie Bot",
                content=content
            )
            return r['url']
        except:
            return None
