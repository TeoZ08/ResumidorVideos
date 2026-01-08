import xml.etree.ElementTree as ET
from pytubefix import YouTube

def obter_transcricao(url_video: str) -> str | None:
    try:
        print(f"Processando: {url_video}...")
        yt = YouTube(url_video)
        
        # A pytubefix lista as legendas disponíveis
        captions = yt.captions
        
        # Lógica de prioridade: Manual PT -> Auto PT -> Manual EN -> Auto EN
        legenda_escolhida = None
        
        prioridades = ['pt', 'a.pt', 'pt-BR', 'a.pt-BR', 'en', 'a.en']
        
        for lang in prioridades:
            if lang in captions:
                legenda_escolhida = captions[lang]
                print(f"✅ Legenda encontrada: {lang}")
                break
        
        if not legenda_escolhida:
            if len(captions) > 0:
                legenda_escolhida = list(captions.values())[0]
                print(f"⚠️ Usando legenda alternativa: {legenda_escolhida.code}")
            else:
                print("❌ Nenhuma legenda encontrada.")
                return None

        # Obtém o XML da legenda
        xml_captions = legenda_escolhida.xml_captions

        # Limpa o XML para obter apenas o texto corrido
        root = ET.fromstring(xml_captions)
        linhas = []
        for child in root:
            if child.text and child.text.strip():
                texto_limpo = child.text.replace('\n', ' ').strip()
                linhas.append(texto_limpo)
        
        texto_completo = " ".join(linhas)
        return texto_completo

    except Exception as e:
        print(f"❌ Erro ao obter transcrição com pytubefix: {e}")
        return None