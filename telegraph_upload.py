import telegraph
from telegraph import Telegraph
from datetime import datetime

class TelegraphUploader:
    def __init__(self):
        self.telegraph = Telegraph()
        self.telegraph.create_account(
            short_name='CinemaBRIndie',
            author_name='Cinema BR Indie Bot',
            author_url='https://t.me/CinemaBRIndieBot'
        )
    
    def create_daily_article(self, data):
        """Create a Telegraph article with ads"""
        
        # Format the content with ads
        content = []
        
        # Header
        content.append({
            "tag": "h1",
            "children": ["🎬 Resumo do Cinema Independente BR"]
        })
        
        content.append({
            "tag": "p",
            "children": [f"📅 Atualização: {data['date']}"]
        })
        
        content.append({
            "tag": "p",
            "children": ["Confira os principais festivais, notícias e premiações do cinema independente brasileiro."]
        })
        
        # AD PLACEMENT 1 - Adsterra Banner (replace with your own)
        content.append({
            "tag": "div",
            "children": [
                {
                    "tag": "p",
                    "children": ["📢 ANÚNCIO"]
                },
                {
                    "tag": "img",
                    "attrs": {
                        "src": "https://via.placeholder.com/728x90/FF6B6B/FFFFFF?text=Seu+Anuncio+Aqui",
                        "alt": "Advertisement"
                    }
                },
                {
                    "tag": "i",
                    "children": ["Este conteúdo é patrocinado - apoie o cinema independente!"]
                }
            ]
        })
        
        # Festivals Section
        content.append({
            "tag": "h2",
            "children": ["🏆 Festivais em Andamento"]
        })
        
        if data['festivals']:
            for f in data['festivals'][:5]:
                content.append({
                    "tag": "p",
                    "children": [
                        f"**{f['name']}**",
                        {"tag": "br"},
                        f"📝 {f['description']}",
                        {"tag": "br"},
                        f"🔗 {f['link']}",
                        {"tag": "br"},
                        f"⏰ {f['deadline']}"
                    ]
                })
        else:
            content.append({
                "tag": "p",
                "children": ["Nenhum festival encontrado no momento. Volte amanhã!"]
            })
        
        # AD PLACEMENT 2
        content.append({
            "tag": "div",
            "children": [
                {
                    "tag": "p",
                    "children": ["📢 PUBLICIDADE"]
                },
                {
                    "tag": "img",
                    "attrs": {
                        "src": "https://via.placeholder.com/300x250/4ECDC4/FFFFFF?text=Anuncie+Aqui",
                        "alt": "Ad"
                    }
                }
            ]
        })
        
        # News Section
        content.append({
            "tag": "h2",
            "children": ["📰 Últimas Notícias"]
        })
        
        if data['news']:
            for n in data['news'][:5]:
                content.append({
                    "tag": "p",
                    "children": [
                        f"📌 {n['title']}",
                        {"tag": "br"},
                        f"Fonte: {n['source']}",
                        {"tag": "br"},
                        f"🔗 {n['link']}"
                    ]
                })
        else:
            content.append({
                "tag": "p",
                "children": ["Nenhuma notícia recente."]
            })
        
        # AD PLACEMENT 3 - Bottom
        content.append({
            "tag": "div",
            "children": [
                {
                    "tag": "p",
                    "children": ["📢 APOIE O CINEMA INDEPENDENTE"]
                },
                {
                    "tag": "img",
                    "attrs": {
                        "src": "https://via.placeholder.com/728x90/FF6B6B/FFFFFF?text=Seu+Anuncio+Aqui",
                        "alt": "Footer Ad"
                    }
                }
            ]
        })
        
        # Awards Section
        content.append({
            "tag": "h2",
            "children": ["🏅 Premiações"]
        })
        
        for a in data['awards']:
            content.append({
                "tag": "p",
                "children": [
                    f"**{a['name']}**",
                    {"tag": "br"},
                    f"🏷️ {a['category']}",
                    {"tag": "br"},
                    f"🎯 {a['winner']}",
                    {"tag": "br"},
                    f"📅 {a['year']}"
                ]
            })
        
        # Footer - Call to Action
        content.append({
            "tag": "hr"
        })
        
        content.append({
            "tag": "p",
            "children": [
                "💡 Siga o ",
                {
                    "tag": "a",
                    "attrs": {"href": "https://t.me/CinemaBRIndieBot"},
                    "children": ["@CinemaBRIndieBot"]
                },
                " para atualizações diárias!"
            ]
        })
        
        # Publish to Telegraph
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
            print(f"Error creating page: {e}")
            return None
