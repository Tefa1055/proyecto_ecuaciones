import io
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# CONFIGURACIÓN GENERAL DEL DASHBOARD
# ============================================================
st.set_page_config(
    page_title="Simulador MAS Masa-Resorte",
    page_icon="🌀",
    layout="wide"
)


# ============================================================
# ESTILOS VISUALES
# ============================================================
st.markdown(
    """
    <style>
        [data-testid="stAppViewContainer"] {
            background-color: #0b1020;
        }

        [data-testid="stSidebar"] {
            background-color: #1f2433;
        }

        .titulo-principal {
            font-size: 34px;
            font-weight: 800;
            color: #7c3aed;
            margin-bottom: 0px;
        }

        .subtitulo {
            font-size: 16px;
            color: #d1d5db;
            margin-top: 4px;
            margin-bottom: 20px;
        }

        .tarjeta {
            background-color: #ffffff;
            padding: 18px;
            border-radius: 16px;
            box-shadow: 0px 4px 14px rgba(76, 29, 149, 0.12);
            border: 1px solid #e9d5ff;
            margin-bottom: 16px;
            color: #1f2937 !important;
        }

        .tarjeta * {
            color: #1f2937 !important;
        }

        .tarjeta-morada {
            background: linear-gradient(135deg, #6d28d9, #4c1d95);
            padding: 18px;
            border-radius: 16px;
            color: white !important;
            box-shadow: 0px 4px 14px rgba(76, 29, 149, 0.25);
            margin-bottom: 16px;
        }

        .tarjeta-morada * {
            color: white !important;
        }

        .texto-metrica {
            font-size: 14px;
            opacity: 0.95;
            margin-bottom: 4px;
        }

        .valor-metrica {
            font-size: 28px;
            font-weight: 800;
        }

        .formula {
            background-color: #ede9fe;
            color: #4c1d95 !important;
            padding: 12px;
            border-radius: 12px;
            font-weight: 700;
            text-align: center;
            margin-bottom: 10px;
        }

        .nota {
            background-color: #fefce8;
            border-left: 5px solid #eab308;
            padding: 12px;
            border-radius: 10px;
            color: #78350f !important;
            font-size: 15px;
        }

        .nota * {
            color: #78350f !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FUNCIONES DEL MODELO FÍSICO
# ============================================================
def calcular_mas(masa, constante, amplitud, tiempo_total, puntos, fase):
    omega = np.sqrt(constante / masa)
    periodo = 2 * np.pi * np.sqrt(masa / constante)
    frecuencia = 1 / periodo

    tiempo = np.linspace(0, tiempo_total, puntos)

    posicion = amplitud * np.cos(omega * tiempo + fase)
    velocidad = -amplitud * omega * np.sin(omega * tiempo + fase)
    aceleracion = -amplitud * (omega ** 2) * np.cos(omega * tiempo + fase)

    return tiempo, posicion, velocidad, aceleracion, omega, periodo, frecuencia


def crear_grafica(tiempo, posicion, velocidad, aceleracion, tipo_grafica):
    figura, eje = plt.subplots(figsize=(11, 4.8))

    if tipo_grafica == "Posición, velocidad y aceleración":
        eje.plot(tiempo, posicion, label="Posición x(t) [m]", linewidth=2)
        eje.plot(tiempo, velocidad, label="Velocidad v(t) [m/s]", linewidth=2)
        eje.plot(tiempo, aceleracion, label="Aceleración a(t) [m/s²]", linewidth=2)
        eje.set_title("Posición, velocidad y aceleración del MAS")

    elif tipo_grafica == "Solo posición":
        eje.plot(tiempo, posicion, label="Posición x(t) [m]", linewidth=2)
        eje.set_title("Posición vs tiempo")

    elif tipo_grafica == "Solo velocidad":
        eje.plot(tiempo, velocidad, label="Velocidad v(t) [m/s]", linewidth=2)
        eje.set_title("Velocidad vs tiempo")

    elif tipo_grafica == "Solo aceleración":
        eje.plot(tiempo, aceleracion, label="Aceleración a(t) [m/s²]", linewidth=2)
        eje.set_title("Aceleración vs tiempo")

    eje.set_xlabel("Tiempo (s)")
    eje.set_ylabel("Magnitud")
    eje.grid(True, alpha=0.35)
    eje.legend(loc="upper right")

    figura.tight_layout()
    return figura


def crear_animacion_estatica(posicion_actual, amplitud_referencia):
    figura, eje = plt.subplots(figsize=(7, 4.2))

    eje.set_xlim(-2.5, 2.5)
    eje.set_ylim(-2.8, 1.2)
    eje.axis("off")

    y_soporte = 0.8
    y_equilibrio = -1.0

    amplitud_segura = max(abs(amplitud_referencia), 0.01)
    escala = 1.2 / amplitud_segura
    y_masa = y_equilibrio - posicion_actual * escala
    y_masa = max(-2.2, min(0.2, y_masa))

    eje.plot([-1.2, 1.2], [y_soporte, y_soporte], linewidth=4)

    vueltas = 10
    x_resorte = []
    y_resorte = []

    for i in range(vueltas + 1):
        if i == 0:
            x = 0
        elif i == vueltas:
            x = 0
        else:
            x = -0.25 if i % 2 == 0 else 0.25

        y = y_soporte - (i / vueltas) * (y_soporte - y_masa + 0.25)
        x_resorte.append(x)
        y_resorte.append(y)

    eje.plot(x_resorte, y_resorte, linewidth=2)

    ancho_masa = 0.75
    alto_masa = 0.55

    rectangulo = plt.Rectangle(
        (-ancho_masa / 2, y_masa - alto_masa),
        ancho_masa,
        alto_masa,
        fill=True,
        alpha=0.45
    )
    eje.add_patch(rectangulo)

    eje.text(
        0,
        y_masa - alto_masa / 2,
        "m",
        ha="center",
        va="center",
        fontsize=14,
        fontweight="bold"
    )

    eje.axhline(y_equilibrio, linestyle="--", linewidth=1, alpha=0.7)
    eje.text(-2.2, y_equilibrio + 0.08, "equilibrio", fontsize=10)

    eje.set_title("Representación visual del sistema masa–resorte")

    figura.tight_layout()
    return figura

def crear_animacion_html(amplitud, omega, fase, tiempo_total):
    html = f"""
    <div style="
        width:100%;
        background:#ffffff;
        border-radius:18px;
        padding:18px;
        box-shadow:0px 4px 14px rgba(76, 29, 149, 0.18);
        border:1px solid #e9d5ff;
    ">
        <svg id="svg-mas" viewBox="0 0 850 390" width="100%" height="390">
            <rect x="0" y="0" width="850" height="390" rx="18" fill="#ffffff"></rect>

            <text x="425" y="32" text-anchor="middle"
                  font-size="22" font-weight="bold" fill="#4c1d95">
                Animación automática del sistema masa–resorte
            </text>

            <line x1="300" y1="70" x2="550" y2="70"
                  stroke="#1f2937" stroke-width="6" stroke-linecap="round"></line>

            <polyline id="resorte"
                      points=""
                      fill="none"
                      stroke="#f97316"
                      stroke-width="4"
                      stroke-linejoin="round"></polyline>

            <rect id="masa"
                  x="365"
                  y="210"
                  width="120"
                  height="65"
                  rx="6"
                  fill="#bfdbfe"
                  stroke="#2563eb"
                  stroke-width="3"></rect>

            <text id="texto-masa"
                  x="425"
                  y="250"
                  text-anchor="middle"
                  font-size="24"
                  font-weight="bold"
                  fill="#1e3a8a">m</text>

            <line x1="90" y1="245" x2="760" y2="245"
                  stroke="#a78bfa"
                  stroke-width="2"
                  stroke-dasharray="8 8"></line>

            <text x="110" y="235"
                  font-size="16"
                  fill="#6d28d9">equilibrio</text>

            <text id="info-tiempo"
                  x="425"
                  y="350"
                  text-anchor="middle"
                  font-size="18"
                  font-weight="bold"
                  fill="#4c1d95">
                t = 0.00 s
            </text>

            <text id="info-posicion"
                  x="425"
                  y="375"
                  text-anchor="middle"
                  font-size="15"
                  fill="#1f2937">
                x(t) = 0.0000 m
            </text>
        </svg>
    </div>

    <script>
        const A = {float(amplitud)};
        const omega = {float(omega)};
        const fase = {float(fase)};
        const tiempoTotal = {float(tiempo_total)};

        const soporteY = 70;
        const equilibrioY = 245;
        const escala = 65 / Math.max(Math.abs(A), 0.01);

        const resorte = document.getElementById("resorte");
        const masa = document.getElementById("masa");
        const textoMasa = document.getElementById("texto-masa");
        const infoTiempo = document.getElementById("info-tiempo");
        const infoPosicion = document.getElementById("info-posicion");

        function limitar(valor, minimo, maximo) {{
            return Math.max(minimo, Math.min(maximo, valor));
        }}

        function generarPuntosResorte(yMasa) {{
            let puntos = "";
            const xCentro = 425;
            const vueltas = 12;
            const yFinal = yMasa;
            const separacion = (yFinal - soporteY) / vueltas;

            puntos += xCentro + "," + soporteY + " ";

            for (let i = 1; i <= vueltas; i++) {{
                let x = (i % 2 === 0) ? xCentro - 35 : xCentro + 35;
                let y = soporteY + i * separacion;
                puntos += x + "," + y + " ";
            }}

            puntos += xCentro + "," + yFinal;
            return puntos;
        }}

        let inicio = null;

        function animar(timestamp) {{
            if (!inicio) {{
                inicio = timestamp;
            }}

            const tiempoTranscurrido = (timestamp - inicio) / 1000;
            const t = tiempoTranscurrido % tiempoTotal;

            const posicion = A * Math.cos(omega * t + fase);

            let yMasa = equilibrioY + posicion * escala;
            yMasa = limitar(yMasa, 130, 285);

            resorte.setAttribute("points", generarPuntosResorte(yMasa));

            masa.setAttribute("y", yMasa);
            textoMasa.setAttribute("y", yMasa + 40);

            infoTiempo.textContent = "t = " + t.toFixed(2) + " s";
            infoPosicion.textContent = "x(t) = " + posicion.toFixed(4) + " m";

            requestAnimationFrame(animar);
        }}

        requestAnimationFrame(animar);
    </script>
    """

    return html

def convertir_datos_csv(tiempo, posicion, velocidad, aceleracion):
    contenido = "tiempo,posicion,velocidad,aceleracion\n"

    for i in range(len(tiempo)):
        contenido += (
            f"{tiempo[i]:.6f},"
            f"{posicion[i]:.6f},"
            f"{velocidad[i]:.6f},"
            f"{aceleracion[i]:.6f}\n"
        )

    return contenido.encode("utf-8")


def convertir_figura_png(figura):
    buffer = io.BytesIO()
    figura.savefig(buffer, format="png", bbox_inches="tight", dpi=180)
    buffer.seek(0)
    return buffer


# ============================================================
# ENCABEZADO
# ============================================================
st.markdown(
    """
    <div class="titulo-principal">
        Simulador educativo del sistema masa–resorte
    </div>
    <div class="subtitulo">
        Modelo de Movimiento Armónico Simple inspirado en los principios mecánicos de Leonardo da Vinci.
        Permite modificar masa, constante elástica, amplitud, fase y tiempo para visualizar el comportamiento del sistema.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PANEL LATERAL
# ============================================================
st.sidebar.title("⚙️ Parámetros del sistema")

st.sidebar.markdown("Modifica los valores para simular el movimiento.")

masa = st.sidebar.number_input(
    "Masa m (kg)",
    min_value=0.01,
    value=1.0,
    step=0.1
)

constante = st.sidebar.number_input(
    "Constante elástica k (N/m)",
    min_value=0.01,
    value=4.0,
    step=0.5
)

amplitud = st.sidebar.number_input(
    "Amplitud A (m)",
    min_value=0.01,
    value=0.5,
    step=0.1
)

tiempo_total = st.sidebar.number_input(
    "Tiempo total de simulación (s)",
    min_value=1.0,
    value=10.0,
    step=1.0
)

puntos = st.sidebar.slider(
    "Puntos de simulación",
    min_value=100,
    max_value=3000,
    value=600,
    step=100
)

fase = st.sidebar.number_input(
    "Fase inicial φ (rad)",
    value=0.0,
    step=0.1
)

tipo_grafica = st.sidebar.radio(
    "Gráfica a mostrar",
    [
        "Posición, velocidad y aceleración",
        "Solo posición",
        "Solo velocidad",
        "Solo aceleración"
    ]
)


# ============================================================
# CÁLCULO PRINCIPAL
# ============================================================
tiempo, posicion, velocidad, aceleracion, omega, periodo, frecuencia = calcular_mas(
    masa,
    constante,
    amplitud,
    tiempo_total,
    puntos,
    fase
)


# ============================================================
# MÉTRICAS PRINCIPALES
# ============================================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="tarjeta-morada">
            <div class="texto-metrica">Frecuencia angular</div>
            <div class="valor-metrica">ω = {omega:.4f}</div>
            <div>rad/s</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="tarjeta-morada">
            <div class="texto-metrica">Período</div>
            <div class="valor-metrica">T = {periodo:.4f}</div>
            <div>segundos</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="tarjeta-morada">
            <div class="texto-metrica">Frecuencia</div>
            <div class="valor-metrica">f = {frecuencia:.4f}</div>
            <div>Hz</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="tarjeta-morada">
            <div class="texto-metrica">Ecuación usada</div>
            <div style="font-size: 17px; font-weight: 800;">
                x(t) = {amplitud:.2f} cos({omega:.2f}t + {fase:.2f})
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PESTAÑAS DEL DASHBOARD
# ============================================================
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📈 Gráfica del MAS",
        "🌀 Sistema masa–resorte",
        "📘 Modelo matemático",
        "📊 Datos"
    ]
)


# ============================================================
# TAB 1: GRÁFICA
# ============================================================
with tab1:
    st.markdown("### Visualización gráfica del Movimiento Armónico Simple")

    figura_grafica = crear_grafica(
        tiempo,
        posicion,
        velocidad,
        aceleracion,
        tipo_grafica
    )

    st.pyplot(figura_grafica, width="stretch")

    png_grafica = convertir_figura_png(figura_grafica)

    st.download_button(
        label="📥 Descargar gráfica en PNG",
        data=png_grafica,
        file_name="grafica_masa_resorte_mas.png",
        mime="image/png"
    )


# ============================================================
# TAB 2: ANIMACIÓN VISUAL
# ============================================================
# ============================================================
# TAB 2: ANIMACIÓN VISUAL
# ============================================================
# ============================================================
# TAB 2: ANIMACIÓN VISUAL
# ============================================================
with tab2:
    st.markdown("### Simulación visual automática del resorte y la masa")

    st.markdown(
        """
        <div class="nota">
            La animación se mueve automáticamente según la ecuación del Movimiento Armónico Simple.
            El resorte y la masa cambian de posición de acuerdo con x(t) = A cos(ωt + φ).
        </div>
        """,
        unsafe_allow_html=True
    )

    html_animacion = crear_animacion_html(
        amplitud,
        omega,
        fase,
        tiempo_total
    )

    components.html(
        html_animacion,
        height=460,
        scrolling=False
    )

    st.markdown("### Valores en un instante seleccionado")

    tiempo_animado = st.slider(
        "Selecciona un tiempo para ver los valores físicos",
        min_value=0.0,
        max_value=float(tiempo_total),
        value=0.0,
        step=float(tiempo_total / 200)
    )

    posicion_actual = amplitud * np.cos(omega * tiempo_animado + fase)
    velocidad_actual = -amplitud * omega * np.sin(omega * tiempo_animado + fase)
    aceleracion_actual = -amplitud * (omega ** 2) * np.cos(omega * tiempo_animado + fase)

    col_estado_1, col_estado_2, col_estado_3, col_estado_4 = st.columns(4)

    with col_estado_1:
        st.markdown(
            f"""
            <div class="tarjeta">
                <h4>Tiempo</h4>
                <h3>{tiempo_animado:.3f} s</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_estado_2:
        st.markdown(
            f"""
            <div class="tarjeta">
                <h4>Posición</h4>
                <h3>{posicion_actual:.4f} m</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_estado_3:
        st.markdown(
            f"""
            <div class="tarjeta">
                <h4>Velocidad</h4>
                <h3>{velocidad_actual:.4f} m/s</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_estado_4:
        st.markdown(
            f"""
            <div class="tarjeta">
                <h4>Aceleración</h4>
                <h3>{aceleracion_actual:.4f} m/s²</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

# ============================================================
# TAB 3: MODELO MATEMÁTICO
# ============================================================
with tab3:
    st.markdown("### Modelo físico y matemático del sistema")

    col_teoria_1, col_teoria_2 = st.columns(2)

    with col_teoria_1:
        st.markdown(
            """
            <div class="tarjeta">
                <h4 style="color:#4c1d95;">Ley de Hooke</h4>
                <div class="formula">F = -kx</div>
                <p>
                    La fuerza restauradora del resorte es proporcional al desplazamiento
                    y actúa en sentido contrario al movimiento.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="tarjeta">
                <h4 style="color:#4c1d95;">Segunda ley de Newton</h4>
                <div class="formula">m · d²x/dt² = -kx</div>
                <p>
                    Al aplicar la segunda ley de Newton, se obtiene una ecuación diferencial
                    que describe el comportamiento dinámico de la masa.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_teoria_2:
        st.markdown(
            """
            <div class="tarjeta">
                <h4 style="color:#4c1d95;">Ecuación diferencial del MAS</h4>
                <div class="formula">d²x/dt² + (k/m)x = 0</div>
                <p>
                    Esta ecuación diferencial lineal de segundo orden permite modelar
                    el Movimiento Armónico Simple del sistema masa–resorte.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="tarjeta">
                <h4 style="color:#4c1d95;">Solución del sistema</h4>
                <div class="formula">x(t) = A cos(ωt + φ)</div>
                <p><b>ω = √(k/m)</b> = {omega:.4f} rad/s</p>
                <p><b>T = 2π√(m/k)</b> = {periodo:.4f} s</p>
                <p><b>f = 1/T</b> = {frecuencia:.4f} Hz</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div class="nota">
            Interpretación: si aumenta la masa, el período crece y el sistema oscila más lento.
            Si aumenta la constante elástica del resorte, el período disminuye y el sistema oscila más rápido.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# TAB 4: DATOS
# ============================================================
with tab4:
    st.markdown("### Tabla de datos de la simulación")

    datos = {
        "Tiempo (s)": tiempo,
        "Posición x(t) [m]": posicion,
        "Velocidad v(t) [m/s]": velocidad,
        "Aceleración a(t) [m/s²]": aceleracion
    }

    st.dataframe(datos, width="stretch")

    csv = convertir_datos_csv(tiempo, posicion, velocidad, aceleracion)

    st.download_button(
        label="📥 Descargar datos en CSV",
        data=csv,
        file_name="datos_simulacion_masa_resorte.csv",
        mime="text/csv"
    )


# ============================================================
# PIE DE PÁGINA
# ============================================================
st.markdown("---")
st.markdown(
    """
    <p style="text-align:center; color:#4c1d95; font-weight:600;">
        Simulador educativo masa–resorte | Movimiento Armónico Simple | Proyecto de cálculo y física
    </p>
    """,
    unsafe_allow_html=True
)