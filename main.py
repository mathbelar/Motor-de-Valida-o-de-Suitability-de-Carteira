import json
import os
import sys
from src.motor_suitability import validar_suitability, calcular_risco_carteira


def ler_perfil_cliente():
    """
    Solicita os dados do perfil do cliente
    
    Returns:
        dict: Perfil do cliente
    """
    print(" PERFIL DO CLIENTE")
    print("-" * 70)
    
    nome_perfil = input("\nDigite o nome do perfil (ex: Conservador, Moderado, Arrojado): ").strip()
    
    while True:
        try:
            score_max = float(input("Digite o score máximo de risco permitido (ex: 2.5): "))
            if score_max <= 0:
                print(" Score deve ser maior que zero!")
                continue
            break
        except ValueError:
            print(" Digite um número válido!")
    
    print(f"\n Perfil criado: {nome_perfil} (Score máximo: {score_max})")
    
    return {
        "perfil": nome_perfil,
        "score_max_risco": score_max
    }


def ler_carteira_atual():
    """
    Solicita os ativos da carteira atual
    
    Returns:
        list: Lista de ativos da carteira
    """
    print("\n💼 CARTEIRA ATUAL")
    print("-" * 70)
    
    carteira = []
    
    while True:
        qtd = input("\nQuantos ativos existem na carteira atual? (0 para carteira vazia): ")
        try:
            qtd = int(qtd)
            if qtd < 0:
                print(" Quantidade não pode ser negativa!")
                continue
            break
        except ValueError:
            print(" Digite um número válido!")
    
    if qtd == 0:
        print(" Carteira vazia registrada.")
        return carteira
    
    print(f"\nVamos cadastrar {qtd} ativo(s):\n")
    
    for i in range(qtd):
        print(f" Ativo {i+1}/{qtd}")
        
        nome = input("  Nome do ativo: ").strip()
        
        while True:
            try:
                risco = float(input("  Risco do ativo (ex: 1.2, 4.0): "))
                if risco < 0:
                    print("   Risco não pode ser negativo!")
                    continue
                break
            except ValueError:
                print("   Digite um número válido!")
        
        while True:
            try:
                valor = float(input("  Valor investido (R$): "))
                if valor < 0:
                    print("   Valor não pode ser negativo!")
                    continue
                break
            except ValueError:
                print("   Digite um número válido!")
        
        carteira.append({
            "ativo": nome,
            "risco": risco,
            "valor_investido": valor
        })
        
        print(f"   {nome} adicionado!\n")
    
    # Mostra resumo da carteira
    valor_total = sum(a['valor_investido'] for a in carteira)
    risco_atual = calcular_risco_carteira(carteira)
    
    print("📊 RESUMO DA CARTEIRA:")
    for ativo in carteira:
        print(f"  • {ativo['ativo']}: R$ {ativo['valor_investido']:,.2f} (Risco: {ativo['risco']})")
    print(f"\n   Valor Total: R$ {valor_total:,.2f}")
    print(f"   Risco Atual: {risco_atual:.2f}")
    
    return carteira


def ler_nova_ordem():
    """
    Solicita os dados da nova ordem de compra
    
    Returns:
        dict: Nova ordem
    """
    print("\n🛒 NOVA ORDEM DE COMPRA")
    print("-" * 70)
    
    nome = input("\nNome do ativo que deseja comprar: ").strip()
    
    while True:
        try:
            risco = float(input("Risco do ativo (ex: 3.5): "))
            if risco < 0:
                print(" Risco não pode ser negativo!")
                continue
            break
        except ValueError:
            print(" Digite um número válido!")
    
    while True:
        try:
            valor = float(input("Valor da ordem (R$): "))
            if valor <= 0:
                print(" Valor deve ser maior que zero!")
                continue
            break
        except ValueError:
            print("Digite um número válido!")
    
    print(f"\n Ordem registrada: {nome} - R$ {valor:,.2f} (Risco: {risco})")
    
    return {
        "ativo": nome,
        "risco": risco,
        "valor_ordem": valor
    }


def exibir_resultado(resultado):
    """
    Exibe o resultado da validação de forma visual
    
    Args:
        resultado: Resultado retornado pelo motor
    """
    print(" RESULTADO DA VALIDAÇÃO")
    
    # Define emoji e cor baseado no status
    if resultado['status'] == 'Aprovado':
        emoji = "✅"
        status_cor = "APROVADO"
    elif resultado['status'] == 'Alerta':
        emoji = "⚠️"
        status_cor = "ALERTA"
    else:
        emoji = "❌"
        status_cor = "REJEITADO"
    
    print(f"\n{emoji} STATUS: {status_cor}\n")
    print(f"📊 Métricas:")
    print(f"   • Risco Atual da Carteira: {resultado['risco_atual']}")
    print(f"   • Risco Projetado (após compra): {resultado['risco_projetado']}")
    print(f"   • Score Máximo Permitido: {resultado['score_maximo']}")
    print(f"   • Limite de Alerta (110%): {resultado['limite_alerta']}")
    
    print(f"\n Mensagem:")
    print(f"   {resultado['mensagem']}")
    
    # Análise adicional
    print(f"\n Análise:")
    
    if resultado['status'] == 'Aprovado':
        diferenca = resultado['score_maximo'] - resultado['risco_projetado']
        print(f"   • Você ainda tem margem de {diferenca:.2f} pontos de risco.")
        print(f"   • A operação está em conformidade com seu perfil.")
    
    elif resultado['status'] == 'Alerta':
        excesso = resultado['risco_projetado'] - resultado['score_maximo']
        print(f"   • Você está excedendo em {excesso:.2f} pontos o limite do seu perfil.")
    
    else:
        excesso = resultado['risco_projetado'] - resultado['limite_alerta']
        print(f"   • O risco excede em {excesso:.2f} pontos o limite de tolerância.")
        print(f"   • Esta operação viola a política de Suitability da Genial.")
    
    # Mostra JSON completo
    print(f"\n Resposta JSON completa:")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
    print("\n" + "="*70)


def modo_tradicional():
    """Modo onde o usuário preenche tudo do zero"""
    print("\n MODO TRADICIONAL - Preencha todos os dados")
    print("="*70)
    
    perfil = ler_perfil_cliente()
    carteira = ler_carteira_atual()
    nova_ordem = ler_nova_ordem()
    
    print("\n Processando validação...")
    resultado = validar_suitability(perfil, carteira, nova_ordem)
    
    exibir_resultado(resultado)


def modo_testes():
    """Roda o arquivo de testes automatizados"""
    print("\n MODO TESTES - Executando testes automatizados")
    print("="*70)
    print()
    
    # Executa o arquivo de testes
    os.system("python tests/test_motor.py")


def main():
    """Função principal do modo interativo"""
    
    # Menu de escolha
    print("Escolha o modo de operação:\n")
    print("  1. Modo Tradicional - Preencha todos os dados manualmente")
    print("  2. Modo Testes - Execute os testes automatizados pré feitos")
    print("  3. Sair")
    
    while True:
        opcao = input("\nOpção (1/2/3): ").strip()
        
        if opcao == "1":
            modo_tradicional()
            break
        
        elif opcao == "2":
            modo_testes()
            break
        
        elif opcao == "3":
            return
        
        else:
            print(" Opção inválida!")
    
    # Perguntar se quer fazer outra ação
    print("\n" + "="*70)
    outra = input("\n Deseja fazer outra operação? (s/n): ").strip().lower()
    
    if outra == 's':
        main()
    else:
        print("Para rodar apenas os testes, execute: python tests/test_motor.py\n")


if __name__ == "__main__":
    main()
