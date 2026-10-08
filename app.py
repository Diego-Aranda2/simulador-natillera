import streamlit as st
import pandas as pd

# ------------------------
# CONFIGURACIÓN
# ------------------------

st.set_page_config(
    page_title="La Natillera",
    page_icon="💰",
    layout="wide"
)

# ------------------------
# FORMATO PESOS COLOMBIA
# ------------------------

def cop(valor):
    return f"$ {valor:,.0f}".replace(",", ".")

# ------------------------
# LOGO
# ------------------------

col_logo, col_titulo = st.columns([1,4])

with col_logo:
    try:
        st.image("logo.png", width=150)
    except:
        pass

with col_titulo:
    st.markdown(
        """
        <h1 style='color:#F57C00;margin-bottom:0px;'>
        SIMULADOR DE CRÉDITO
        </h1>
        """,
        unsafe_allow_html=True
    )

st.divider()

# ------------------------
# FORMULARIO
# ------------------------

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown("### 💵 Valor del préstamo")

monto = st.slider(
    "",
    min_value=100000,
    max_value=3000000,
    value=100000,
    step=100000
)

st.success(f"Valor seleccionado: {cop(monto)}")

with col2:

    meses = st.selectbox(
        "📅 Plazo",
        [1,2,3,4,5,6,7,8,9,10,11,12]
    )

with col3:

    modalidad = st.selectbox(
        "📋 Tipo de pago",
        [
            "Capital + Interés",
            "Solo interés y capital al final"
        ]
    )

# ------------------------
# BOTÓN SIMULAR
# ------------------------
if monto <= 0:
    st.error("El valor del préstamo debe ser desde $100.000")
    st.stop()
simular = st.button(
    "CALCULAR SIMULACIÓN",
    use_container_width=True
)

if simular:

    tasa = 0.04

    registros = []

    total_intereses = 0
    total_pagado = 0

    # ------------------------------------------------
    # CAPITAL + INTERÉS SOBRE SALDO
    # ------------------------------------------------

    if modalidad == "Capital + Interés":

        saldo = monto
        capital = monto / meses

        for cuota in range(1, meses + 1):

            interes = saldo * tasa

            cuota_total = capital + interes

            saldo_final = saldo - capital

            registros.append([
                cuota,
                round(capital),
                round(interes),
                round(cuota_total),
                round(max(saldo_final, 0))
            ])

            total_intereses += interes
            total_pagado += cuota_total

            saldo = saldo_final

    # ------------------------------------------------
    # SOLO INTERÉS
    # ------------------------------------------------

    else:

        for cuota in range(1, meses + 1):

            interes = monto * tasa

            if cuota < meses:

                capital = 0
                cuota_total = interes
                saldo_final = monto

            else:

                capital = monto
                cuota_total = monto + interes
                saldo_final = 0

            registros.append([
                cuota,
                round(capital),
                round(interes),
                round(cuota_total),
                round(saldo_final)
            ])

            total_intereses += interes
            total_pagado += cuota_total

    # ------------------------
    # TABLA
    # ------------------------

    df = pd.DataFrame(
        registros,
        columns=[
            "Cuota",
            "Capital",
            "Interés",
            "Valor Cuota",
            "Saldo"
        ]
    )

    st.divider()

    st.subheader("📊 Resumen de la Simulación")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Valor Prestado",
        cop(monto)
    )

    c2.metric(
        "Total Intereses",
        cop(total_intereses)
    )

    c3.metric(
        "Total a Pagar",
        cop(total_pagado)
    )

    st.divider()

    vista = df.copy()

    for columna in [
        "Capital",
        "Interés",
        "Valor Cuota",
        "Saldo"
    ]:

        vista[columna] = vista[columna].apply(cop)

    st.subheader("📅 Tabla de Amortización")

    st.dataframe(
        vista,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.success(
        f"Total del crédito: {cop(total_pagado)}"
    )

    st.markdown(
        """
        ---
        **Tasa aplicada:** 4% mensual sobre saldo.

        **La presente simulación es informativa y puede variar según las condiciones definitivas del crédito.**
        """
    )
    st.link_button(
    "📝 SOLICITAR CRÉDITO",
    "https://forms.gle/4cYrjJpmZjZswSFF7",
    use_container_width=True
)
