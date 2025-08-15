"""
Script para executar todos os testes
"""
import unittest
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_all_tests():
    """
    Executar todos os testes da aplicação
    """
    print("🧪 Executando todos os testes do Sales Portal API...")
    print("=" * 60)
    
    # Descobrir todos os testes na pasta test
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Executar testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES:")
    print(f"✅ Testes executados: {result.testsRun}")
    print(f"❌ Falhas: {len(result.failures)}")
    print(f"🚫 Erros: {len(result.errors)}")
    
    if result.failures:
        print("\n💥 FALHAS:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print("\n🔥 ERROS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    # Status final
    if result.wasSuccessful():
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        return True
    else:
        print("\n💔 ALGUNS TESTES FALHARAM!")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
