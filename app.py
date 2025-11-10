# app.py
import streamlit as st
from data_processing import full_pipeline
from viz_helpers import galactic_scatter, flux_histogram, flux_corr_heatmap, sed_plot, plot_3d
import time

# --- Page setup ---
st.set_page_config(
    page_title="Planck CMB Explorer ",
    layout="wide",
    page_icon="",
    initial_sidebar_state="expanded"
)

# --- Animated Cosmic Background ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

html, body, [class*="stApp"] {
    overflow: hidden;
    font-family: 'Orbitron', sans-serif;
}

#starfield {
    position: fixed;
    top: 0;
    left: 0;
    z-index: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
}

.main-content {
    position: relative;
    z-index: 10;
    padding: 1.5rem 2rem;
    background: rgba(0, 0, 0, 0.65);
    border-radius: 20px;
    box-shadow: 0px 0px 20px rgba(0, 255, 255, 0.3);
}

h1, h2, h3, h4, h5, h6, p, label, span {
    color: #f0f0f0 !important;
    text-shadow: 0 0 8px rgba(0,255,255,0.2);
}

.stExpander {
    background: rgba(15, 15, 30, 0.8) !important;
    border-radius: 12px;
    padding: 5px;
}
</style>

<canvas id="starfield"></canvas>

<script>
const canvas = document.getElementById('starfield');
const ctx = canvas.getContext('2d');
let stars = [];
const numStars = 300;

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
function createStars() {
    stars = [];
    for (let i = 0; i < numStars; i++) {
        stars.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            z: Math.random() * canvas.width
        });
    }
}
function moveStars() {
    for (let i = 0; i < numStars; i++) {
        stars[i].z -= 2;
        if (stars[i].z <= 0) stars[i].z = canvas.width;
    }
}
function drawStars() {
    // Clear canvas without black overlay
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Optional cosmic gradient background
    const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
    gradient.addColorStop(0, "#0a0a1a");
    gradient.addColorStop(1, "#0d0d40");
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    const cx = canvas.width / 2;
    const cy = canvas.height / 2;
    for (let i = 0; i < numStars; i++) {
        const k = 128.0 / stars[i].z;
        const px = stars[i].x * k + cx;
        const py = stars[i].y * k + cy;
        if (px >= 0 && px <= canvas.width && py >= 0 && py <= canvas.height) {
            const size = (1 - stars[i].z / canvas.width) * 2;
            ctx.fillStyle = "white";
            ctx.beginPath();
            ctx.arc(px, py, size, 0, 2 * Math.PI);
            ctx.fill();
        }
    }
}
function animate() {
    moveStars();
    drawStars();
    requestAnimationFrame(animate);
}

resizeCanvas();
createStars();
animate();
window.onresize = resizeCanvas;
</script>
""", unsafe_allow_html=True)

# --- Main App Content ---
st.markdown("<div class='main-content'>", unsafe_allow_html=True)

st.title(" **Planck Cosmic Microwave Background Explorer**")
st.markdown("""
Explore the **Planck Space Observatory** data and visualize the **CMB sources**,  
their **flux variations**, and **galactic positions** in interactive 3D space.
""")

# --- Load and process data ---
@st.cache_data
def load_data():
    raw, processed = full_pipeline("planck.csv")
    return raw, processed

with st.spinner(" Loading and processing Planck dataset..."):
    time.sleep(1.2)
    raw_df, df = load_data()
st.success(" Dataset ready for exploration!")

# --- Sidebar controls ---
st.sidebar.header(" Filters & Controls")
band_options = ["total_flux"] + [f"flux{i}" for i in range(1, 10)]
color_by = st.sidebar.selectbox("Color by:", band_options)
minv = float(df[color_by].min(skipna=True))
maxv = float(df[color_by].max(skipna=True))
flux_range = st.sidebar.slider("Flux range", minv, maxv, (minv, maxv))
glon_range = st.sidebar.slider("Galactic Longitude range", 0.0, 360.0, (0.0, 360.0))
glat_range = st.sidebar.slider("Galactic Latitude range", -90.0, 90.0, (-30.0, 30.0))
only_reliable = st.sidebar.checkbox("Only reliable sources", True)

# --- Data filtering ---
f = df.copy()
f = f[(f[color_by] >= flux_range[0]) & (f[color_by] <= flux_range[1])]
f = f[(f['glon'] >= glon_range[0]) & (f['glon'] <= glon_range[1])]
f = f[(f['glat'] >= glat_range[0]) & (f['glat'] <= glat_range[1])]
if only_reliable and 'reliable' in f.columns:
    f = f[f['reliable']]

# --- Layout ---
col1, col2 = st.columns([2, 1])

# --- Left Column ---
with col1:
    st.subheader(" Galactic Sky Map")
    fig_map = galactic_scatter(f, color_col=color_by, title=f"Sky Map Colored by {color_by}")
    st.plotly_chart(fig_map, use_container_width=True)

    st.subheader(" Flux Distribution")
    st.plotly_chart(flux_histogram(f, col=color_by), use_container_width=True)

    st.subheader(" Flux Correlation Heatmap")
    st.plotly_chart(flux_corr_heatmap(df), use_container_width=True)

# --- Right Column ---
with col2:
    st.subheader(" Spectral Energy Distribution (SED)")
    idx = st.number_input("Choose source index:", min_value=0, max_value=max(0, len(df)-1), value=0)
    st.plotly_chart(sed_plot(df, int(idx)), use_container_width=True)

    st.subheader(" 3D Galactic Visualization")
    st.plotly_chart(plot_3d(f), use_container_width=True)

# --- Before/After ---
st.markdown("---")
with st.expander(" Show Raw Dataset Sample (Before Cleaning)"):
    st.dataframe(raw_df.head(), height=200)

with st.expander(" Show Processed Dataset Sample (After Cleaning)"):
    st.dataframe(df.head(), height=200)

# --- Sidebar Downloads & Metrics ---
st.sidebar.header(" Export Cleaned Data")
csv = df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button("⬇ Download Cleaned CSV", csv, "planck_cleaned.csv", "text/csv")

st.sidebar.header(" Dataset Summary")
st.sidebar.metric("Original Rows", len(raw_df))
st.sidebar.metric("After Cleaning", len(df))
st.sidebar.metric("Filtered Displayed", len(f))

st.sidebar.markdown("---")
st.sidebar.caption("Developed by Siddhant Rana  | NMIMS Chandigarh | Planck Mission Project")

st.markdown("</div>", unsafe_allow_html=True)
