import streamlit as st
from pulp import *
import matplotlib.pyplot as plt

st.title("Otimização de Produção com Alocação de Recursos 📊🏭")

st.markdown("""
**Sistema de otimização industrial** que calcula a combinação ideal de produção para maximizar lucros, considerando:

- 📈 **Lucro por produto**  
- ⚙️ **Capacidade produtiva** (horas/máquina)  
- 🧱 **Matérias-primas disponíveis**  

""")

# Inputs do usuário na sidebar
st.sidebar.header("Configurações")
produto1_lucro = st.sidebar.number_input("Lucro por Produto 1 (R$)", min_value=1, value=30)
produto2_lucro = st.sidebar.number_input("Lucro por Produto 2 (R$)", min_value=1, value=40)
horas_disponiveis = st.sidebar.number_input("Horas de Máquina Disponíveis", min_value=1, value=100)
material_disponivel = st.sidebar.number_input("Material Disponível (kg)", min_value=1, value=200)

# Modelo de otimização
prob = LpProblem("Maximizar_Lucro", LpMaximize)
x = LpVariable("Produto_1", lowBound=0, cat='Integer')  # Quantidade inteira não negativa
y = LpVariable("Produto_2", lowBound=0, cat='Integer')  # Quantidade inteira não negativa

# Função objetivo
prob += produto1_lucro * x + produto2_lucro * y, "Lucro Total"

# Restrições (valores ajustados para forçar solução mista)
prob += 2 * x + 4 * y <= horas_disponiveis, "Restrição_Horas"
prob += 3 * x + 2 * y <= material_disponivel, "Restrição_Material"

# Resolver e exibir resultados
if st.button("Calcular Otimização"):
    prob.solve()
    
    st.subheader("Resultados")
    st.success(f"**Status:** {LpStatus[prob.status]}")
    
    # Verifica se a solução foi encontrada
    if prob.status == 1:  # 1 = Optimal
        # Garante que os valores são inteiros
        qtd_produto1 = int(x.varValue)
        qtd_produto2 = int(y.varValue)
        
        st.write(f"**Produto 1 a produzir:** {qtd_produto1} unidades")
        st.write(f"**Produto 2 a produzir:** {qtd_produto2} unidades")
        st.write(f"**Lucro Total:** R$ {value(prob.objective):.2f}")

        # Gráfico 1: Quantidade de produtos (CORREÇÃO PRINCIPAL)
        plt.close('all')  # Fecha quaisquer figuras anteriores
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        
        produtos = ['Produto 1', 'Produto 2']
        quantidades = [qtd_produto1, qtd_produto2]
        
        # Cores condicionais (verde para >0, cinza para 0)
        cores = ['#4CAF50' if q > 0 else '#BDBDBD' for q in quantidades]
        
        bars = ax1.bar(produtos, quantidades, color=cores)
        
        # Configuração do eixo Y baseada nos valores reais
        max_y = max(quantidades) if max(quantidades) > 0 else 10
        ax1.set_ylim(0, max_y * 1.2)
        
        ax1.set_title("Quantidade Ótima de Produção", pad=20)
        ax1.set_ylabel("Unidades")
        
        # Remove bordas desnecessárias
        for spine in ['top', 'right']:
            ax1.spines[spine].set_visible(False)
        
        # Adiciona os valores nas barras
        for bar in bars:
            height = bar.get_height()
            if height > 0:  # Só mostra texto se a barra tiver altura > 0
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}',
                        ha='center', va='bottom', fontsize=12)
        
        st.pyplot(fig1)

        # Gráfico 2: Uso de recursos
        horas_utilizadas = 2 * qtd_produto1 + 4 * qtd_produto2
        material_utilizado = 3 * qtd_produto1 + 2 * qtd_produto2

        fig2, (ax2, ax3) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Pie chart para horas
        ax2.pie([horas_utilizadas, max(0, horas_disponiveis - horas_utilizadas)],
                labels=["Utilizadas", "Disponíveis"],
                colors=["#FF5722", "#BDBDBD"],
                autopct=lambda p: f'{p:.1f}%\n({int(p/100*horas_disponiveis)}h)',
                startangle=90)
        ax2.set_title("Uso de Horas de Máquina")

        # Pie chart para material
        ax3.pie([material_utilizado, max(0, material_disponivel - material_utilizado)],
                labels=["Utilizado", "Disponível"],
                colors=["#9C27B0", "#BDBDBD"],
                autopct=lambda p: f'{p:.1f}%\n({int(p/100*material_disponivel)}kg)',
                startangle=90)
        ax3.set_title("Uso de Material")

        st.pyplot(fig2)

        # Verificação das restrições
        st.subheader("Verificação de Restrições")
        st.write(f"**Horas utilizadas:** {horas_utilizadas}/{horas_disponiveis} "
               f"({horas_utilizadas/horas_disponiveis:.1%})")
        st.write(f"**Material utilizado:** {material_utilizado}/{material_disponivel} "
               f"({material_utilizado/material_disponivel:.1%})")
        
    else:
        st.error("Não foi possível encontrar uma solução ótima com os parâmetros fornecidos.")

# Exemplo de valores para teste
st.sidebar.markdown("""
**Exemplo para testar:**
- Lucro P1: 30
- Lucro P2: 50
- Horas: 40
- Material: 60
""")