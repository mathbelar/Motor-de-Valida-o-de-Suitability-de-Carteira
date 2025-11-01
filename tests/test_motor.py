import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.motor_suitability import ( calcular_risco_carteira, projetar_carteira_pos_compra, validar_suitability)


def test_carteira_vazia():
    carteira = []
    risco = calcular_risco_carteira(carteira)
    assert risco == 0.0, "Carteira vazia deve ter risco 0"
    print("Teste 1 passou: Carteira vazia")

def test_calcular_risco_carteira_simples():
    carteira = [
        {"ativo": "CDB XPTO", "risco": 1.2, "valor_investido": 50000},
        {"ativo": "Ação ABC", "risco": 4.0, "valor_investido": 10000}
    ]
    
    risco = calcular_risco_carteira(carteira)
    risco_esperado = 1.67
    
    assert abs(risco - risco_esperado) < 0.01, f"Esperado {risco_esperado}, obtido {risco}"
    print(f"Teste 2 passou: Risco calculado = {risco}")

def test_projetar_carteira():

    carteira_atual = [
        {"ativo": "CDB XPTO", "risco": 1.2, "valor_investido": 50000}
    ]
    
    nova_ordem = {"ativo": "FII YYY", "risco": 3.5, "valor_ordem": 5000}
    
    carteira_projetada = projetar_carteira_pos_compra(carteira_atual, nova_ordem)
    
    assert len(carteira_projetada) == 2, "Carteira projetada deve ter 2 ativos"
    assert carteira_projetada[1]["ativo"] == "FII YYY", "Novo ativo deve estar na carteira"
    print("Teste 3 passou: Projeção de carteira")

def test_cenario_aprovado():

    perfil = {"perfil": "Moderado", "score_max_risco": 2.5}
    
    carteira = [
        {"ativo": "CDB XPTO", "risco": 1.2, "valor_investido": 50000},
        {"ativo": "Ação ABC", "risco": 4.0, "valor_investido": 10000}
    ]
    
    nova_ordem = {"ativo": "CDB Seguro", "risco": 1.0, "valor_ordem": 10000}
    
    resultado = validar_suitability(perfil, carteira, nova_ordem)
    
    assert resultado["status"] == "Aprovado", f"Deveria ser Aprovado, foi {resultado['status']}"
    assert resultado["risco_projetado"] <= 2.5, "Risco projetado deve estar dentro do limite"
    
    print(" Teste 4 passou: CENÁRIO APROVADO")
    print(f"   Risco projetado: {resultado['risco_projetado']}")
    print(f"   Mensagem: {resultado['mensagem']}")

def test_cenario_alerta():
    perfil = {"perfil": "Moderado", "score_max_risco": 2.5}
    
    carteira = [
        {"ativo": "CDB XPTO", "risco": 1.2, "valor_investido": 50000},
        {"ativo": "Ação ABC", "risco": 4.0, "valor_investido": 10000}
    ]
    
    nova_ordem = {"ativo": "FII YYY", "risco": 3.5, "valor_ordem": 15000}
    
    resultado = validar_suitability(perfil, carteira, nova_ordem)
    
    assert resultado["status"] == "Alerta", f"Deveria ser Alerta, foi {resultado['status']}"
    assert resultado["risco_projetado"] > 2.5, "Risco deve ultrapassar o score"
    assert resultado["risco_projetado"] <= 2.75, "Risco deve estar dentro do limite de alerta"
    
    print(" Teste 5 passou: CENÁRIO ALERTA")
    print(f"   Risco projetado: {resultado['risco_projetado']}")
    print(f"   Mensagem: {resultado['mensagem']}")

def test_cenario_rejeitado():

    perfil = {"perfil": "Moderado", "score_max_risco": 2.5}
    
    carteira = [
        {"ativo": "CDB XPTO", "risco": 1.2, "valor_investido": 50000},
        {"ativo": "Ação ABC", "risco": 4.0, "valor_investido": 10000}
    ]
    
    nova_ordem = {"ativo": "Ação Arriscada", "risco": 5.0, "valor_ordem": 50000}
    
    resultado = validar_suitability(perfil, carteira, nova_ordem)
    
    assert resultado["status"] == "Rejeitado", f"Deveria ser Rejeitado, foi {resultado['status']}"
    assert resultado["risco_projetado"] > 2.75, "Risco deve ultrapassar o limite de alerta"
    
    print(" Teste 6 passou: CENÁRIO REJEITADO")
    print(f"   Risco projetado: {resultado['risco_projetado']}")
    print(f"   Mensagem: {resultado['mensagem']}")



def rodar_todos_testes():

    print("\n" + "="*60)
    print("INICIANDO TESTES")
    print("="*60 + "\n")
    
    testes = [
        test_carteira_vazia,
        test_calcular_risco_carteira_simples,
        test_projetar_carteira,
        test_cenario_aprovado,
        test_cenario_alerta,
        test_cenario_rejeitado,

    ]
    
    total = len(testes)
    passou = 0
    
    for teste in testes:
        try:
            teste()
            passou += 1
        except AssertionError as e:
            print(f" {teste.__name__} FALHOU: {e}")
        except Exception as e:
            print(f" {teste.__name__} ERRO: {e}")
    
    print("\n" + "="*60)
    print(f"📊 RESULTADO: {passou}/{total} testes passaram")
    print("="*60 + "\n")
    
    if passou == total:
        print("TODOS OS TESTES PASSARAM!")
    else:
        print("Algum teste falhou. Revise o código.")


if __name__ == "__main__":
    rodar_todos_testes()