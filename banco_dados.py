import sqlite3
import os

DB_NAME = "resumos.db"

def conectar():
    """Conecta ao banco SQLite (cria o arquivo se não existir)"""
    conn = sqlite3.connect(DB_NAME)
    return conn

def inicializar_banco():
    """Cria a tabela se ela ainda não existir"""
    conn = conectar()
    cursor = conn.cursor()
    
    # Tabela simples: ID do vídeo (chave) e o Resumo (valor)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            video_id TEXT PRIMARY KEY,
            titulo TEXT,
            resumo TEXT,
            data_processamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def salvar_resumo(video_id: str, titulo: str, resumo: str):
    """Salva ou atualiza um resumo no banco"""
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT OR REPLACE INTO videos (video_id, titulo, resumo)
            VALUES (?, ?, ?)
        """, (video_id, titulo, resumo))
        conn.commit()
        print(f"💾 Resumo salvo no banco de dados (ID: {video_id})")
    except Exception as e:
        print(f"❌ Erro ao salvar no banco: {e}")
    finally:
        conn.close()

def buscar_resumo(video_id: str):
    """Busca se já existe resumo para este ID"""
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT resumo FROM videos WHERE video_id = ?", (video_id,))
    resultado = cursor.fetchone()
    
    conn.close()
    
    if resultado:
        return resultado[0] # Retorna apenas o texto do resumo
    return None