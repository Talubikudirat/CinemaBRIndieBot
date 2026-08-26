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
            print(f"Telegraph account exists or error: {e}")
    
    def create_daily_article(self, data):
        """Create a Telegraph article with ad placements"""
        
        content = []
        
        # HEADER
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
        
        # AD PLACEMENT 1
        content.append({
            "tag": "p",
            "children": [
                "📢 ANÚNCIO - APOIE O CINEMA INDEPENDENTE",
                {"tag": "br"},
                {"tag": "img", "attrs": {"src": "https://via.placeholder.com/728x90/FF6B6B/FFFFFF?text=Anuncie+Aqui", "alt": "Ad"}},
                {"tag": "br"},
                {"tag": "i", "children": ["Este conteúdo é patrocinado"]}
            ]
        })
        
        # FESTIVALS
        content.append({
            "tag": "h2",
            "children": ["🏆 Festivais em Andamento"]
        })
        
        if data['festivals']:
            for f in data['festivals'][:5]:
                content.append({
                    "tag": "p",
                    "children": [
                        f"🎬 {f['name']}",
                        {"tag": "br"},
                        f"📝 {f['description']}",
                        {"tag": "br"},
                        {"tag": "a", "attrs": {"href": f['link']}, "children": ["🔗 Mais informações"]},
                        {"tag": "br"},
                        f"⏰ {f['deadline']}",
                        {"tag": "br"}
                    ]
                })
        else:
            content.append({
                "tag": "p",
                "children": ["Nenhum festival encontrado no momento."]
            })
        
        # AD PLACEMENT 2
        content.append({
            "tag": "p",
            "children": [
                "📢 PUBLICIDADE",
                {"tag": "br"},
                {"tag": "img", "attrs": {"src": "https://via.placeholder.com/300x250/4ECDC4/FFFFFF?text=Anuncie+Aqui", "alt": "Ad"}}
            ]
        })
        
        # NEWS
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
                        f"📡 Fonte: {n['source']}",
                        {"tag": "br"},
                        {"tag": "a", "attrs": {"href": n['link']}, "children": ["🔗 Leia mais"]},
                        {"tag": "br"}
                    ]
                })
        else:
            content.append({
                "tag": "p",
                "children": ["Nenhuma notícia recente."]
            })
        
        # AD PLACEMENT 3
        content.append({
            "tag": "p",
            "children": [
                "📢 APOIE O CINEMA INDEPENDENTE",
                {"tag": "br"},
                {"tag": "img", "attrs": {"src": "https://via.placeholder.com/728x90/FF6B6B/FFFFFF?text=Seu+Anuncio+Aqui", "alt": "Footer Ad"}}
            ]
        })
        
        # AWARDS
        content.append({
            "tag": "h2",
            "children": ["🏅 Premiações"]
        })
        
        for a in data['awards']:
            content.append({
                "tag": "p",
                "children": [
                    f"🎯 {a['name']}",
                    {"tag": "br"},
                    f"🏷️ Categoria: {a['category']}",
                    {"tag": "br"},
                    f"🏆 {a['winner']}",
                    {"tag": "br"},
                    f"📅 {a['year']}",
                    {"tag": "br"}
                ]
            })
        
        # FOOTER
        content.append({
            "tag": "hr"
        })
        
        content.append({
            "tag": "p",
            "children": [
                "💡 Siga o ",
                {"tag": "a", "attrs": {"href": "https://t.me/CinemaBRIndieBot"}, "children": ["@CinemaBRIndieBot"]},
                " para atualizações diárias!"
            ]
        })
        
        # PUBLISH
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
            print(f"Error creating telegraph page: {e}")
            return None
