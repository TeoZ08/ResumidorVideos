import banco_dados


def inicializar():
    banco_dados.inicializar_banco()


def salvar(video_id: str, titulo: str, resumo: str, url: str | None = None):
    banco_dados.salvar_resumo(video_id, titulo, resumo, url)


def buscar(video_id: str):
    return banco_dados.buscar_resumo_completo(video_id)


def listar():
    return banco_dados.listar_resumos()
