from telegraph import Telegraph
from datetime import datetime

class TelegraphUploader:
    def __init__(self):
        self.telegraph = Telegraph()
        try:
            self.telegraph.create_account(
                short_name='CinemaBRIndie',
                author_name='Cinema BR Indie Bot',
                author_url='https://t.me/CinemaBRIndieBot'
            )
        except Exception as e:
            print(f"Telegraph account: {e}")
    
    def create_daily_article(self, data):
        content = []
        
        # Header
        content.append({"tag": "h1", "children": ["🎬 Resumo do Cinema Independente BR"]})
        content.append({"tag": "p", "children": [f"📅 Atualização: {data['date']}"]})
        content.append({"tag": "p", "children": ["Confira os principais festivais, notícias e premiações do cinema independente brasileiro."]})
        
        # AD 1
        content.append({"tag": "p", "children": ["📢 ANÚNCIO - APOIE O CINEMA INDEPENDENTE"]})
        content.append({"tag": "p", "children": [{"tag": "img", "attrs": {"src": "https://via.placeholder.com/728x90/FF6B6B/FFFFFF?text=ANUNCIE+AQUI", "alt": "Ad"}}]})
        content.append({"tag": "hr", "children": []})
        
        # Festivals
        content.append({"tag": "h2", "children": ["🏆 Festivais em Andamento"]})
        if data['festivals']:
            for f in data['festivals'][:6]:
                content.append({"tag": "p", "children": [f"🎬 {f['name']}"]})
                content.append({"tag": "p", "children": [f"📝 {f['description']}"]})
                content.append({"tag": "p", "children": [{"tag": "a", "attrs": {"href": f['link']}, "children": ["🔗 Site oficial"]}]})
                content.append({"tag": "p", "children": [f"⏰ {f['deadline']}"]})
                content.append({"tag": "br", "children": []})
        else:
            content.append({"tag": "p", "children": ["Nenhum festival encontrado no momento."]})
        
        # AD 2
        content.append({"tag": "hr", "children": []})
        content.append({"tag": "p", "children": ["📢 PUBLICIDADE - SEU ANÚNCIO AQUI"]})
        content.append({"tag": "p", "children": [{"tag": "img", "attrs": {"src": "https://via.placeholder.com/300x250/4ECDC4/FFFFFF?text=ANUNCIE+AQUI", "alt": "Ad"}}]})
        content.append({"tag": "hr", "children": []})
        
        # News
        content.append({"tag": "h2", "children": ["📰 Últimas Notícias"]})
        if data['news']:
            for n in data['news'][:5]:
                content.append({"tag": "p", "children": [f"📌 {n['title']}"]})
                content.append({"tag": "p", "children": [f"📡 Fonte: {n['source']}"]})
                content.append({"tag": "p", "children": [{"tag": "a", "attrs": {"href": n['link']}, "children": ["🔗 Leia mais"]}]})
                content.append({"tag": "br", "children": []})
        else:
            content.append({"tag": "p", "children": ["Nenhuma notícia recente."]})
        
        # AD 3
        content.append({"tag": "hr", "children": []})
        content.append({"tag": "p", "children": ["📢 APOIE O CINEMA INDEPENDENTE BRASILEIRO"]})
        content.append({"tag": "p", "children": [{"tag": "img", "attrs": {"src": "https://via.placeholder.com/728x90/FF6B6B/FFFFFF?text=ANUNCIE+AQUI", "alt": "Footer Ad"}}]})
        content.append({"tag": "hr", "children": []})
        
        # Awards
        content.append({"tag": "h2", "children": ["🏅 Premiações"]})
        for a in data['awards']:
            content.append({"tag": "p", "children": [f"🎯 {a['name']}"]})
            content.append({"tag": "p", "children": [f"🏷️ Categoria: {a['category']}"]})
            content.append({"tag": "p", "children": [f"🏆 {a['winner']}"]})
            content.append({"tag": "p", "children": [f"📅 {a['year']}"]})
            content.append({"tag": "br", "children": []})
        
        # Footer
        content.append({"tag": "hr", "children": []})
        content.append({"tag": "p", "children": ["💡 Siga o @CinemaBRIndieBot para atualizações diárias!"]})
        content.append({"tag": "p", "children": ["📢 Anuncie aqui e alcance amantes do cinema independente!"]})
        
        try:
            response = self.telegraph.create_page(
                title=f"Cinema Independente BR - {datetime.now().strftime('%d/%m/%Y')}",
                author_name="Cinema BR Indie Bot",
                author_url="https://t.me/CinemaBRIndieBot",
                content=content,
                return_content=True
            )
            return response['url']
        except Exception as e:
            print(f"Error: {e}")
            return None
