"""
Script para verificar estrutura do banco SQLite
"""
import sqlite3
import sys
import os

def check_database():
    """Verificar estrutura do banco de dados"""
    db_path = "sales_portal.db"
    
    if not os.path.exists(db_path):
        print("❌ Banco de dados não encontrado!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Listar todas as tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("✅ Banco de dados encontrado!")
        print(f"📊 Tabelas encontradas: {len(tables)}")
        
        for table in tables:
            table_name = table[0]
            print(f"  📋 {table_name}")
            
            # Verificar estrutura da tabela
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            for col in columns:
                col_name = col[1]
                col_type = col[2]
                is_pk = " (PK)" if col[5] else ""
                print(f"    - {col_name}: {col_type}{is_pk}")
            
            # Contar registros
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"    📊 Registros: {count}")
            print()
        
        conn.close()
        print("🎉 Verificação concluída com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar banco: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Verificando estrutura do banco SQLite...")
    print("=" * 50)
    success = check_database()
    sys.exit(0 if success else 1)
