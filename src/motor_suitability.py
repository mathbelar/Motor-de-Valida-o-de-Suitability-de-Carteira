def calcular_risco_carteira(carteira):
    if not carteira:
        return 0.0
    
    # Somatoria (Risco x Valor Investido)
    soma_ponderada = sum(ativo["risco"] * ativo["valor_investido"] for ativo in carteira)
    
    # Valor total Investido
    valor_total = sum(
        ativo["valor_investido"] 
        for ativo in carteira
    )
    
    if valor_total == 0:
        return 0.0
    
    return soma_ponderada / valor_total

def projetar_carteira_pos_compra(carteira_atual, nova_ordem):

    carteira_projetada = carteira_atual.copy()
    
    novo_ativo = {
        "ativo": nova_ordem["ativo"],
        "risco": nova_ordem["risco"],
        "valor_investido": nova_ordem["valor_ordem"]
    }
    
    carteira_projetada.append(novo_ativo)
    
    return carteira_projetada


def validar_suitability(perfil_cliente, carteira_atual, nova_ordem):
    """
    - APROVADO: Risco projetado <= Score máximo
    - ALERTA: Risco projetado > Score máximo, mas <= Score máximo x 1.1
    - REJEITADO: Risco projetado > Score máximo x 1.1
    """
    # Calcula risco atual
    risco_atual = calcular_risco_carteira(carteira_atual)
    
    # Projeta nova carteira usando a nova ordem
    carteira_projetada = projetar_carteira_pos_compra(carteira_atual, nova_ordem)

    # Calcula risco considerando nova ordem
    risco_projetado = calcular_risco_carteira(carteira_projetada)

    score_maximo = perfil_cliente["score_max_risco"]
    limite_alerta = score_maximo * 1.1  # 10% acima do máximo

    # Arredondar para 2 casas decimais
    risco_atual = round(risco_atual, 2)
    risco_projetado = round(risco_projetado, 2)
    limite_alerta = round(limite_alerta, 2)

    if risco_projetado <= score_maximo:
        Situacao = {
            "status": "Aprovado",
            "risco_atual": risco_atual,
            "risco_projetado": risco_projetado,
            "score_maximo": score_maximo,
            "limite_alerta": limite_alerta,
            "mensagem": "Ordem executada."
        }

    elif risco_projetado <= limite_alerta:
        Situacao = {
            "status": "Alerta",
            "risco_atual": risco_atual,
            "risco_projetado": risco_projetado,
            "score_maximo": score_maximo,
            "limite_alerta": limite_alerta,
            "mensagem": f"Atenção: O risco da carteira ultrapassará o limite de {limite_alerta}."
        }
    
        
    else:
        Situacao = {
            "status": "Rejeitado",
            "risco_atual": risco_atual,
            "risco_projetado": risco_projetado,
            "score_maximo": score_maximo,
            "limite_alerta": limite_alerta,
            "mensagem": "Risco excessivo. A operação viola a política de Suitability."
        }

    return Situacao