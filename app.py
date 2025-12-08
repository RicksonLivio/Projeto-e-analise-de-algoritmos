import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import time
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Detecção de Fraudes em Transações",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para manter o tema
st.markdown("""
    <style>
    .main {
        background: linear-gradient(to bottom right, #EFF6FF, #E0E7FF);
    }
    .stAlert {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .algorithm-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Título principal
st.markdown("""
    <h1 style='text-align: center; color: #FFFFFF; margin-bottom: 10px;'>
        💳 Detecção de Fraudes em Transações Financeiras
    </h1>
    <p style='text-align: center; color: #FFFFFF; font-size: 18px; margin-bottom: 30px;'>
        Comparação de três algoritmos: Naive O(n³), Sort+TwoPointer O(n²) e HashMap O(n²)
    </p>
""", unsafe_allow_html=True)

# ==================== FUNÇÕES DOS ALGORITMOS ====================

def three_sum_naive(arr, target):
    """O(n³) — Força bruta, retorna valores (v1,v2,v3) ou None."""
    n = len(arr)
    for i in range(n-2):
        ai = arr[i]
        for j in range(i+1, n-1):
            aj = arr[j]
            for k in range(j+1, n):
                if ai + aj + arr[k] == target:
                    return (ai, aj, arr[k])
    return None


def three_sum_sort_two_pointer(arr, target):
    """O(n log n + n²) — Ordenação + dois ponteiros, retorna valores ou None."""
    n = len(arr)
    a = sorted(arr)
    for i in range(n-2):
        if a[i] > target:
            break
        left = i + 1
        right = n - 1
        while left < right:
            s = a[i] + a[left] + a[right]
            if s == target:
                return (a[i], a[left], a[right])
            elif s < target:
                left += 1
            else:
                right -= 1
    return None


def three_sum_hash(arr, target):
    """
    O(n²) usando Hash Map.
    Para cada i, faz um two-sum no restante usando hash.
    """
    n = len(arr)
    for i in range(n):
        need = target - arr[i]
        seen = set()
        for j in range(i+1, n):
            comp = need - arr[j]
            if comp in seen:
                return (arr[i], arr[j], comp)
            seen.add(arr[j])
    return None


def make_instances(n, trials):
    """Gera `trials` instâncias: (arr, target, guaranteed_boolean)."""
    instances = []
    for t in range(trials):
        arr = np.random.randint(1, 100001, size=n).tolist()
        if t < trials // 2:
            # Garante que existe solução
            i, j, k = np.random.choice(n, size=3, replace=False)
            target = arr[i] + arr[j] + arr[k]
            guaranteed = True
        else:
            # Alvo aleatório (pode não ter solução)
            target = np.random.randint(1, 300000)
            guaranteed = False
        instances.append((arr, target, guaranteed))
    return instances


# ==================== SIDEBAR ====================

with st.sidebar:
    st.markdown("### ⚙️ Configurações do Experimento")
    
    st.markdown("#### 📊 Tamanhos de Entrada")
    
    # Para algoritmos O(n²)
    st.markdown("**Algoritmos O(n²):**")
    max_size_opt = st.slider(
        "Tamanho máximo",
        min_value=1000,
        max_value=50000,
        value=10000,
        step=1000,
        help="Usado para Sort+TwoPointer e HashMap"
    )
    
    num_points_opt = st.slider(
        "Número de pontos",
        min_value=10,
        max_value=100,
        value=50,
        step=5
    )
    
    st.markdown("---")
    
    # Para algoritmo O(n³)
    st.markdown("**Algoritmo O(n³) (Naive):**")
    max_size_naive = st.slider(
        "Tamanho máximo",
        min_value=100,
        max_value=5000,
        value=1000,
        step=100,
        help="⚠️ Muito lento! Use valores pequenos"
    )
    
    num_points_naive = st.slider(
        "Número de pontos",
        min_value=10,
        max_value=50,
        value=30,
        step=5
    )
    
    st.markdown("---")
    
    trials = st.slider(
        "Repetições por Tamanho",
        min_value=3,
        max_value=20,
        value=5,
        step=1,
        help="Número de execuções para calcular média"
    )
    
    st.markdown("---")
    
    run_button = st.button("▶️ Iniciar Experimento", width='stretch', type="primary")
    
    st.markdown("---")
    st.markdown("### 📚 Sobre os Algoritmos")
    st.markdown("""
    **🔴 Naive O(n³)**
    - Três loops aninhados
    - Muito lento para n > 2000
    
    **🟢 Sort+TwoPointer O(n²)**
    - Ordena + busca inteligente
    - Até 1000x mais rápido!
    
    **🔵 HashMap O(n²)**
    - Usa tabela hash
    - Não precisa ordenar
    """)

# ==================== CARDS INFORMATIVOS ====================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class='algorithm-card' style='background: linear-gradient(135deg, #FEE2E2 0%, #FCA5A5 100%);'>
            <h3 style='color: #7F1D1D; margin: 0;'>🔴 Naive (Força Bruta)</h3>
            <p style='color: #991B1B; margin: 10px 0 0 0;'><strong>Complexidade: O(n³)</strong></p>
            <p style='color: #6B7280; font-size: 14px; margin: 5px 0 0 0;'>
                Testa todas as n×(n-1)×(n-2)/6 combinações
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class='algorithm-card' style='background: linear-gradient(135deg, #D1FAE5 0%, #6EE7B7 100%);'>
            <h3 style='color: #065F46; margin: 0;'>🟢 Sort + TwoPointer</h3>
            <p style='color: #047857; margin: 10px 0 0 0;'><strong>Complexidade: O(n²)</strong></p>
            <p style='color: #6B7280; font-size: 14px; margin: 5px 0 0 0;'>
                Ordena uma vez + busca com dois ponteiros
            </p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class='algorithm-card' style='background: linear-gradient(135deg, #DBEAFE 0%, #93C5FD 100%);'>
            <h3 style='color: #1E40AF; margin: 0;'>🔵 HashMap</h3>
            <p style='color: #1E3A8A; margin: 10px 0 0 0;'><strong>Complexidade: O(n²)</strong></p>
            <p style='color: #6B7280; font-size: 14px; margin: 5px 0 0 0;'>
                Usa tabela hash para busca rápida
            </p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== EXECUÇÃO DO EXPERIMENTO ====================

if run_button:
    st.markdown("### 📊 Executando Experimento...")
    
    # Gerar tamanhos
    sizes_opt = np.linspace(100, max_size_opt, num_points_opt, dtype=int)
    sizes_naive = np.linspace(100, max_size_naive, num_points_naive, dtype=int)
    
    # Gerar TODAS as instâncias de uma vez
    all_sizes = sorted(set(sizes_opt) | set(sizes_naive))
    all_instances = {}
    
    with st.spinner("Gerando instâncias de teste..."):
        for n in all_sizes:
            all_instances[n] = make_instances(n, trials)
    
    results = []
    
    # Barra de progresso
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Container para gráfico em tempo real
    chart_placeholder = st.empty()
    
    total_steps = len(sizes_opt) * 2 + len(sizes_naive)  # 2 algoritmos O(n²) + 1 O(n³)
    current_step = 0
    
    # ==================== 1) Sort + TwoPointer ====================
    status_text.text("🟢 Executando Sort + TwoPointer...")
    
    for idx, n in enumerate(sizes_opt):
        instances = all_instances[n]
        times = []
        correct_found = 0
        
        for arr, target, guaranteed in instances:
            start = time.perf_counter()
            out = three_sum_sort_two_pointer(arr, target)
            elapsed = time.perf_counter() - start
            times.append(elapsed)
            if guaranteed and out is not None:
                correct_found += 1
        
        results.append({
            'algorithm': 'Sort+TwoPointer',
            'n': n,
            'avg_time': np.mean(times),
            'median_time': np.median(times),
            'std_time': np.std(times),
            'trials': trials,
            'correct_found': correct_found,
            'total_guaranteed': trials // 2
        })
        
        current_step += 1
        progress_bar.progress(current_step / total_steps)
        
        # Atualizar gráfico em tempo real
        if idx % 5 == 0 or idx == len(sizes_opt) - 1:
            df_temp = pd.DataFrame(results)
            fig_temp = go.Figure()
            
            for alg in df_temp['algorithm'].unique():
                sub = df_temp[df_temp['algorithm'] == alg]
                color = '#10B981' if alg == 'Sort+TwoPointer' else '#3B82F6'
                fig_temp.add_trace(go.Scatter(
                    x=sub['n'], y=sub['avg_time'] * 1000,  # Converter para ms
                    mode='lines+markers', name=alg,
                    line=dict(color=color, width=3),
                    marker=dict(size=6)
                ))
            
            fig_temp.update_layout(
                title="Tempo de Execução (Atualização em Tempo Real)",
                xaxis_title="Tamanho (n)",
                yaxis_title="Tempo (ms)",
                template="plotly_white",
                height=400
            )
            chart_placeholder.plotly_chart(fig_temp, width='stretch')
    
    # ==================== 2) HashMap ====================
    status_text.text("🔵 Executando HashMap...")
    
    for idx, n in enumerate(sizes_opt):
        instances = all_instances[n]
        times = []
        correct_found = 0
        
        for arr, target, guaranteed in instances:
            start = time.perf_counter()
            out = three_sum_hash(arr, target)
            elapsed = time.perf_counter() - start
            times.append(elapsed)
            if guaranteed and out is not None:
                correct_found += 1
        
        results.append({
            'algorithm': 'HashMap',
            'n': n,
            'avg_time': np.mean(times),
            'median_time': np.median(times),
            'std_time': np.std(times),
            'trials': trials,
            'correct_found': correct_found,
            'total_guaranteed': trials // 2
        })
        
        current_step += 1
        progress_bar.progress(current_step / total_steps)
        
        # Atualizar gráfico
        if idx % 5 == 0 or idx == len(sizes_opt) - 1:
            df_temp = pd.DataFrame(results)
            fig_temp = go.Figure()
            
            for alg in df_temp['algorithm'].unique():
                sub = df_temp[df_temp['algorithm'] == alg]
                if alg == 'Sort+TwoPointer':
                    color = '#10B981'
                elif alg == 'HashMap':
                    color = '#3B82F6'
                else:
                    color = '#EF4444'
                
                fig_temp.add_trace(go.Scatter(
                    x=sub['n'], y=sub['avg_time'] * 1000,
                    mode='lines+markers', name=alg,
                    line=dict(color=color, width=3),
                    marker=dict(size=6)
                ))
            
            fig_temp.update_layout(
                title="Tempo de Execução (Atualização em Tempo Real)",
                xaxis_title="Tamanho (n)",
                yaxis_title="Tempo (ms)",
                template="plotly_white",
                height=400
            )
            chart_placeholder.plotly_chart(fig_temp, width='stretch')
    
    # ==================== 3) Naive (O(n³)) ====================
    status_text.text("🔴 Executando Naive (pode demorar)...")
    
    for idx, n in enumerate(sizes_naive):
        instances = all_instances[n]
        times = []
        correct_found = 0
        
        for arr, target, guaranteed in instances:
            start = time.perf_counter()
            out = three_sum_naive(arr, target)
            elapsed = time.perf_counter() - start
            times.append(elapsed)
            if guaranteed and out is not None:
                correct_found += 1
        
        results.append({
            'algorithm': 'Naive',
            'n': n,
            'avg_time': np.mean(times),
            'median_time': np.median(times),
            'std_time': np.std(times),
            'trials': trials,
            'correct_found': correct_found,
            'total_guaranteed': trials // 2
        })
        
        current_step += 1
        progress_bar.progress(current_step / total_steps)
        
        # Atualizar gráfico
        if idx % 3 == 0 or idx == len(sizes_naive) - 1:
            df_temp = pd.DataFrame(results)
            fig_temp = go.Figure()
            
            for alg in df_temp['algorithm'].unique():
                sub = df_temp[df_temp['algorithm'] == alg]
                if alg == 'Sort+TwoPointer':
                    color = '#10B981'
                elif alg == 'HashMap':
                    color = '#3B82F6'
                else:
                    color = '#EF4444'
                
                fig_temp.add_trace(go.Scatter(
                    x=sub['n'], y=sub['avg_time'] * 1000,
                    mode='lines+markers', name=alg,
                    line=dict(color=color, width=3),
                    marker=dict(size=6)
                ))
            
            fig_temp.update_layout(
                title="Tempo de Execução (Atualização em Tempo Real)",
                xaxis_title="Tamanho (n)",
                yaxis_title="Tempo (ms)",
                template="plotly_white",
                height=400,
                xaxis_type='log',
                yaxis_type='log'
            )
            chart_placeholder.plotly_chart(fig_temp, width='stretch')
    
    progress_bar.empty()
    status_text.empty()
    
    # Converter para DataFrame
    df_results = pd.DataFrame(results)
    
    st.success("✅ Experimento concluído com sucesso!")
    
    # ==================== VISUALIZAÇÕES ====================
    
    # Gráfico 1: Escala Linear
    st.markdown("### 📈 Tempo de Execução - Escala Linear")
    
    fig1 = go.Figure()
    
    for alg in df_results['algorithm'].unique():
        sub = df_results[df_results['algorithm'] == alg]
        if alg == 'Sort+TwoPointer':
            color = '#10B981'
        elif alg == 'HashMap':
            color = '#3B82F6'
        else:
            color = '#EF4444'
        
        fig1.add_trace(go.Scatter(
            x=sub['n'],
            y=sub['avg_time'] * 1000,  # ms
            mode='lines+markers',
            name=alg,
            line=dict(color=color, width=3),
            marker=dict(size=8),
            hovertemplate='<b>n=%{x}</b><br>Tempo: %{y:.3f} ms<extra></extra>'
        ))
    
    fig1.update_layout(
        xaxis_title="Tamanho da Entrada (n)",
        yaxis_title="Tempo Médio (ms)",
        template="plotly_white",
        height=500,
        hovermode='x unified',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255, 255, 255, 0.8)"
        )
    )
    
    st.plotly_chart(fig1, width='stretch')
    
    # Gráfico 2: Escala Log-Log
    st.markdown("### 📊 Tempo de Execução - Escala Log-Log")
    
    fig2 = go.Figure()
    
    for alg in df_results['algorithm'].unique():
        sub = df_results[df_results['algorithm'] == alg]
        if alg == 'Sort+TwoPointer':
            color = '#10B981'
        elif alg == 'HashMap':
            color = '#3B82F6'
        else:
            color = '#EF4444'
        
        fig2.add_trace(go.Scatter(
            x=sub['n'],
            y=sub['avg_time'] * 1000,
            mode='lines+markers',
            name=alg,
            line=dict(color=color, width=3),
            marker=dict(size=8),
            hovertemplate='<b>n=%{x}</b><br>Tempo: %{y:.3f} ms<extra></extra>'
        ))
    
    fig2.update_layout(
        xaxis_title="Tamanho da Entrada (n) - Log Scale",
        yaxis_title="Tempo Médio (ms) - Log Scale",
        template="plotly_white",
        height=500,
        xaxis_type='log',
        yaxis_type='log',
        hovermode='x unified',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255, 255, 255, 0.8)"
        )
    )
    
    st.plotly_chart(fig2, width='stretch')
    
    st.info("📌 A escala log-log facilita visualizar a diferença de crescimento entre O(n²) e O(n³)")
    
    # Gráfico 3: Comparação O(n²) - Zoom
    st.markdown("### 🔍 Zoom: Comparação entre Sort+TwoPointer e HashMap")
    
    df_n2 = df_results[df_results['algorithm'].isin(['Sort+TwoPointer', 'HashMap'])]
    
    fig3 = go.Figure()
    
    for alg in df_n2['algorithm'].unique():
        sub = df_n2[df_n2['algorithm'] == alg]
        color = '#10B981' if alg == 'Sort+TwoPointer' else '#3B82F6'
        
        fig3.add_trace(go.Scatter(
            x=sub['n'],
            y=sub['avg_time'] * 1000,
            mode='lines+markers',
            name=alg,
            line=dict(color=color, width=3),
            marker=dict(size=8),
            error_y=dict(
                type='data',
                array=sub['std_time'] * 1000,
                visible=True
            ),
            hovertemplate='<b>n=%{x}</b><br>Tempo: %{y:.3f} ms<br>Std: ±%{error_y.array:.3f}<extra></extra>'
        ))
    
    fig3.update_layout(
        xaxis_title="Tamanho da Entrada (n)",
        yaxis_title="Tempo Médio (ms)",
        template="plotly_white",
        height=450,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig3, width='stretch')
    
    # Estatísticas
    st.markdown("### 📊 Estatísticas e Verificação")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Taxa de Sucesso (Soluções Garantidas)")
        
        success_data = []
        for alg in df_results['algorithm'].unique():
            sub = df_results[df_results['algorithm'] == alg]
            total_correct = sub['correct_found'].sum()
            total_guaranteed = sub['total_guaranteed'].sum()
            success_rate = (total_correct / total_guaranteed * 100) if total_guaranteed > 0 else 0
            success_data.append({
                'Algoritmo': alg,
                'Correto': total_correct,
                'Total': total_guaranteed,
                'Taxa (%)': f"{success_rate:.1f}%"
            })
        
        df_success = pd.DataFrame(success_data)
        st.dataframe(df_success, hide_index=True, width='stretch')
        
        st.caption("Verifica se o algoritmo encontra soluções quando elas existem")
    
    with col2:
        st.markdown("#### ⚡ Speedup: Naive vs Otimizados")
        
        # Calcular speedup nos tamanhos comuns
        common_sizes = sorted(set(sizes_opt) & set(sizes_naive))
        if len(common_sizes) > 0:
            speedup_data = []
            for n in common_sizes[:10]:  # Mostrar até 10 tamanhos
                naive_time = df_results[(df_results['algorithm'] == 'Naive') & (df_results['n'] == n)]['avg_time'].values
                sort_time = df_results[(df_results['algorithm'] == 'Sort+TwoPointer') & (df_results['n'] == n)]['avg_time'].values
                hash_time = df_results[(df_results['algorithm'] == 'HashMap') & (df_results['n'] == n)]['avg_time'].values
                
                if len(naive_time) > 0 and len(sort_time) > 0 and len(hash_time) > 0:
                    speedup_data.append({
                        'n': n,
                        'vs Sort': f"{naive_time[0] / sort_time[0]:.1f}x",
                        'vs Hash': f"{naive_time[0] / hash_time[0]:.1f}x"
                    })
            
            df_speedup = pd.DataFrame(speedup_data)
            st.dataframe(df_speedup, hide_index=True, width='stretch', height=280)
            
            st.caption("Quantas vezes mais rápido são os algoritmos O(n²)")
        else:
            st.warning("Nenhum tamanho comum entre Naive e Otimizados")
    
    # Tabela completa de resultados
    st.markdown("### 📋 Tabela Completa de Resultados")
    
    df_display = df_results.copy()
    df_display['avg_time_ms'] = (df_display['avg_time'] * 1000).round(3)
    df_display['median_time_ms'] = (df_display['median_time'] * 1000).round(3)
    df_display['std_time_ms'] = (df_display['std_time'] * 1000).round(3)
    
    st.dataframe(
        df_display[['algorithm', 'n', 'avg_time_ms', 'median_time_ms', 'std_time_ms', 'trials', 'correct_found']],
        hide_index=True,
        width='stretch',
        height=400
    )
    
    # Download CSV
    st.markdown("### 💾 Download dos Resultados")
    
    csv = df_results.to_csv(index=False)
    st.download_button(
        label="📥 Baixar Resultados Completos (CSV)",
        data=csv,
        file_name=f"three_sum_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        width='stretch'
    )

# ==================== SEÇÃO DE EXPLICAÇÃO ====================

st.markdown("---")
st.markdown("### 🧠 Como Funcionam os Algoritmos")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class='algorithm-card'>
            <h4 style='color: #DC2626;'>🔴 Naive O(n³)</h4>
            <pre style='background: #F3F4F6; padding: 15px; border-radius: 5px; overflow-x: auto; font-size: 12px;'>
for i = 0 to n-3:
  for j = i+1 to n-2:
    for k = j+1 to n-1:
      if arr[i]+arr[j]+arr[k] = target:
        return (i, j, k)
            </pre>
            <p style='font-size: 14px; color: #6B7280; margin-top: 10px;'>
                ✗ Três loops aninhados<br>
                ✗ ~n³/6 comparações<br>
                ✗ Impraticável para n > 2000
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class='algorithm-card'>
            <h4 style='color: #059669;'>🟢 Sort + TwoPointer O(n²)</h4>
            <pre style='background: #F3F4F6; padding: 15px; border-radius: 5px; overflow-x: auto; font-size: 12px;'>
sort(arr)  # O(n log n)
for i = 0 to n-3:
  left = i+1, right = n-1
  while left < right:
    sum = arr[i]+arr[left]+arr[right]
    if sum = target: return
    if sum < target: left++
    else: right--
            </pre>
            <p style='font-size: 14px; color: #6B7280; margin-top: 10px;'>
                ✓ Ordena uma vez<br>
                ✓ Dois ponteiros eliminam 1 loop<br>
                ✓ ~n² comparações
            </p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class='algorithm-card'>
            <h4 style='color: #1E40AF;'>🔵 HashMap O(n²)</h4>
            <pre style='background: #F3F4F6; padding: 15px; border-radius: 5px; overflow-x: auto; font-size: 12px;'>
for i = 0 to n-1:
  need = target - arr[i]
  seen = {}
  for j = i+1 to n-1:
    comp = need - arr[j]
    if comp in seen:
      return (arr[i], arr[j], comp)
    seen.add(arr[j])
            </pre>
            <p style='font-size: 14px; color: #6B7280; margin-top: 10px;'>
                ✓ Usa tabela hash<br>
                ✓ Não precisa ordenar<br>
                ✓ ~n² comparações
            </p>
        </div>
    """, unsafe_allow_html=True)

# Insights e Conclusões
st.markdown("### 💡 Principais Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class='algorithm-card' style='background: linear-gradient(135deg, #FEF3C7 0%, #FCD34D 100%);'>
            <h4 style='color: #92400E; margin: 0;'>📈 Crescimento Assintótico</h4>
            <p style='color: #78350F; margin: 10px 0 5px 0; font-size: 14px;'>
                • <strong>O(n³):</strong> Cresce como o cubo de n<br>
                • <strong>O(n²):</strong> Cresce como o quadrado de n<br>
                • <strong>Diferença:</strong> Para n=1000, ~1000x mais rápido!
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class='algorithm-card' style='background: linear-gradient(135deg, #E0E7FF 0%, #A5B4FC 100%);'>
            <h4 style='color: #3730A3; margin: 0;'>⚖️ Sort vs HashMap</h4>
            <p style='color: #312E81; margin: 10px 0 5px 0; font-size: 14px;'>
                • <strong>Sort+TwoPointer:</strong> Melhor para arrays grandes<br>
                • <strong>HashMap:</strong> Não precisa ordenar, mas usa mais memória<br>
                • <strong>Na prática:</strong> Desempenho similar para a maioria dos casos
            </p>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <p style='text-align: center; color: #9CA3AF; font-size: 14px;'>
        💡 Experimento baseado no problema 3-SUM - Detecção de Fraudes em Transações Financeiras<br>
        Desenvolvido com Python, Streamlit e Plotly
    </p>
""", unsafe_allow_html=True)