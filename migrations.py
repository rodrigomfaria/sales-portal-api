"""
Script para gerenciamento de migrações com Alembic
"""
import subprocess
import sys
import os


def run_alembic_command(command: str):
    """Executar comando do Alembic"""
    alembic_path = r"C:\Users\rodri\.virtualenvs\sales-portal-api-oeCnPKDq\Scripts\alembic.exe"
    full_command = f'& "{alembic_path}" {command}'
    
    print(f"🔄 Executando: {command}")
    try:
        result = subprocess.run(
            ["powershell", "-Command", full_command],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
            
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def main():
    """Menu principal para gerenciamento de migrações"""
    
    print("🗄️  Gerenciador de Migrações - Sales Portal API")
    print("=" * 50)
    print("1. Criar nova migração (autogenerate)")
    print("2. Aplicar migrações (upgrade)")
    print("3. Reverter última migração (downgrade)")
    print("4. Ver histórico de migrações")
    print("5. Ver status atual")
    print("6. Criar migração manual")
    print("0. Sair")
    print("=" * 50)
    
    try:
        choice = input("Escolha uma opção: ").strip()
        
        if choice == "1":
            message = input("Descrição da migração: ").strip()
            if not message:
                message = "Auto migration"
            run_alembic_command(f'revision --autogenerate -m "{message}"')
            
        elif choice == "2":
            run_alembic_command("upgrade head")
            
        elif choice == "3":
            run_alembic_command("downgrade -1")
            
        elif choice == "4":
            run_alembic_command("history")
            
        elif choice == "5":
            run_alembic_command("current")
            
        elif choice == "6":
            message = input("Descrição da migração: ").strip()
            if not message:
                message = "Manual migration"
            run_alembic_command(f'revision -m "{message}"')
            
        elif choice == "0":
            print("👋 Até logo!")
            sys.exit(0)
            
        else:
            print("❌ Opção inválida!")
            
    except KeyboardInterrupt:
        print("\n👋 Até logo!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Erro: {e}")


if __name__ == "__main__":
    while True:
        main()
        print("\n" + "=" * 50)
        input("Pressione Enter para continuar...")
        print("\n")
