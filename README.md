# Motor de Validação de Suitability - CVM 30

Sistema que valida se operações de compra de ativos estão adequadas ao perfil de risco do cliente.

---

##  O que faz?

Calcula o risco da carteira do cliente e verifica se uma nova compra:
- ✅ **Aprova** - Mantém risco dentro do limite
- ⚠️ **Alerta** - Ultrapassa até 10% (precisa assinar termo)
- ❌ **Rejeita** - Risco muito alto

---

##  Como usar

### 1. Instalar
```bash
# Clone o projeto
git clone seu-repositorio.git
cd motor-suitability-genial

# Crie ambiente virtual
python -m venv venv

# Ative (Linux/Mac)
source venv/bin/activate

# Ative (Windows)
venv\Scripts\activate

# Instale dependências
pip install -r requirements.txt
```

### 2. Rodar
```bash
# Usar modo manual para preencher os dados
python main.py

# Rodar testes
python tests/test_motor.py
```

---

## 📁 Estrutura
```
motor-suitability-genial/
├── src/
│   └── motor_suitability.py    # Código principal
├── tests/
│   └── test_motor.py            # Testes
├── main.py                      # Demonstrações
├── interativo.py                # Modo interativo
├── case-report.md               # Relatório de negócio
└── README.md                    # Este arquivo
```


---

##  Como calcula o risco?

Usa **média ponderada**:
```
Risco = (Risco₁ × Valor₁ + Risco₂ × Valor₂ + ...) / (Valor₁ + Valor₂ + ...)
```

**Exemplo:**
- CDB: R$ 50.000 com risco 1.2
- Ação: R$ 10.000 com risco 4.0
- **Risco da carteira:** (1.2×50000 + 4.0×10000) / 60000 = **1.67**

---

##  Regras

| Status | Quando acontece |
|--------|-----------------|
| **Aprovado** | Risco ≤ Score máximo |
| **Alerta** | Score máximo < Risco ≤ Score máximo × 1.1 |
| **Rejeitado** | Risco > Score máximo × 1.1 |

---

##  Testes

6 testes automatizados cobrem todos os cenários.
```bash
python tests/test_motor.py
```

---

##  Autor

**Matheus Belarmino**


Feito para o Case Técnico - Programa de Estágio 2026