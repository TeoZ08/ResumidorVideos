import sqlite3

DB_NAME = "resumos.db"

def conectar():
    """Conecta ao banco SQLite (cria o arquivo se não existir)"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def inicializar_banco():
    """Cria a tabela se ela ainda não existir e aplica migrações seguras."""
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            video_id TEXT PRIMARY KEY,
            titulo TEXT,
            url TEXT,
            resumo TEXT,
            data_processamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("PRAGMA table_info(videos)")
    colunas = {linha["name"] for linha in cursor.fetchall()}

    if "url" not in colunas:
        cursor.execute("ALTER TABLE videos ADD COLUMN url TEXT")
    
    conn.commit()
    conn.close()

def _formatar_data(data):
    if not data:
        return None
    return str(data).replace(" ", "T")

def _linha_para_resumo(linha):
    if not linha:
        return None

    titulo = linha["titulo"] or f"Video {linha['video_id']}"

    return {
        "video_id": linha["video_id"],
        "title": titulo,
        "titulo": titulo,
        "url": linha["url"] if "url" in linha.keys() else None,
        "summary": linha["resumo"],
        "resumo": linha["resumo"],
        "created_at": _formatar_data(linha["data_processamento"]),
        "data_processamento": _formatar_data(linha["data_processamento"]),
    }

def salvar_resumo(video_id: str, titulo: str, resumo: str, url: str | None = None):
    """Salva ou atualiza um resumo no banco"""
    inicializar_banco()
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO videos (video_id, titulo, url, resumo, data_processamento)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(video_id) DO UPDATE SET
                titulo = excluded.titulo,
                url = COALESCE(excluded.url, videos.url),
                resumo = excluded.resumo,
                data_processamento = CURRENT_TIMESTAMP
        """, (video_id, titulo, url, resumo))
        conn.commit()
        print(f"💾 Resumo salvo no banco de dados (ID: {video_id})")
    except Exception as e:
        print(f"❌ Erro ao salvar no banco: {e}")
    finally:
        conn.close()

def buscar_resumo(video_id: str):
    """Busca se já existe resumo para este ID"""
    inicializar_banco()
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT resumo FROM videos WHERE video_id = ?", (video_id,))
    resultado = cursor.fetchone()
    
    conn.close()
    
    if resultado:
        return resultado[0] # Retorna apenas o texto do resumo
    return None

def buscar_resumo_completo(video_id: str):
    """Busca todos os dados salvos de um resumo."""
    inicializar_banco()
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT video_id, titulo, url, resumo, data_processamento
        FROM videos
        WHERE video_id = ?
    """, (video_id,))
    resultado = cursor.fetchone()

    conn.close()
    return _linha_para_resumo(resultado)

def listar_resumos():
    """Lista resumos processados, do mais recente para o mais antigo."""
    inicializar_banco()
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT video_id, titulo, url, resumo, data_processamento
        FROM videos
        ORDER BY data_processamento DESC
    """)
    resultados = [_linha_para_resumo(linha) for linha in cursor.fetchall()]

    conn.close()
    return resultados
