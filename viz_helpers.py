# viz_helpers.py
import plotly.express as px
import plotly.graph_objects as go

def galactic_scatter(df, color_col='total_flux', title=None, bg_image=None):
    fig = px.scatter(df, x='glon', y='glat', color=color_col,
                     hover_data=['name','ra','dec','total_flux','brightness_class'],
                     color_continuous_scale='plasma', title=title or f"Galactic Map colored by {color_col}")
    fig.update_layout(yaxis=dict(autorange='reversed'))
    if bg_image:
        fig.update_layout(images=[dict(source=bg_image, xref="paper", yref="paper",
                                      x=0, y=1, sizex=1, sizey=1, xanchor="left", yanchor="top", opacity=0.15)])
    return fig

def flux_histogram(df, col='total_flux', bins=60):
    return px.histogram(df, x=col, nbins=bins, title=f"Histogram of {col}")

def flux_corr_heatmap(df, flux_cols=None):
    if flux_cols is None:
        flux_cols = [f"flux{i}" for i in range(1,10) if f"flux{i}" in df.columns]
    corr = df[flux_cols].corr()
    fig = px.imshow(corr, text_auto=True, aspect="auto", title="Correlation between flux bands", color_continuous_scale='RdBu')
    return fig

def sed_plot(df, idx, flux_cols=None):
    if flux_cols is None:
        flux_cols = [f"flux{i}" for i in range(1,10) if f"flux{i}" in df.columns]
    row = df.reset_index(drop=True).iloc[idx]
    freqs = list(range(1, len(flux_cols)+1))
    values = [row[c] for c in flux_cols]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=freqs, y=values, mode='markers+lines'))
    fig.update_layout(title=f"SED for {row.get('name','source')}", xaxis_title="Band index (proxy)", yaxis_title="Flux")
    return fig

def plot_3d(df, x='ra', y='dec', z='total_flux'):
    return px.scatter_3d(df, x=x, y=y, z=z, color='brightness_class', hover_name='name', title="3D brightness cloud")
