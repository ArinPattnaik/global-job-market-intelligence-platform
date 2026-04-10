"""
Page 7: Universal Data Analyzer
==================================
Upload any CSV/Excel dataset for automatic intelligent analysis.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

st.set_page_config(page_title="Data Analyzer | GJMIP", page_icon="📤", layout="wide")

with st.sidebar:
    if st.button("⬅️ Back to Home", use_container_width=True):
        st.switch_page("app.py")

COLORS = ["#667EEA", "#764BA2", "#48BB78", "#ED8936", "#E53E3E",
          "#38B2AC", "#D69E2E", "#9F7AEA", "#FC8181", "#4FD1C5"]

# ── Header ───────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom: 8px;">
    <span style="font-size: 2rem; font-weight: 800; color: #E6EDF3;">📤 Universal Data Analyzer</span>
    <span style="color: #8B949E; font-size: 0.9rem; margin-left: 12px;">
        Upload any dataset for instant AI-powered analysis
    </span>
</div>
""", unsafe_allow_html=True)

# ── File Upload ──────────────────────────────────────────────────────
st.markdown("")

uploaded_file = st.file_uploader(
    "Upload your dataset (CSV or Excel, max 50MB)",
    type=["csv", "xlsx", "xls"],
    help="Supported formats: CSV, XLSX, XLS. The analyzer will auto-detect column types and generate appropriate visualizations.",
)

if uploaded_file is None:
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(102,126,234,0.06) 0%, rgba(118,75,162,0.04) 100%);
                border: 1px solid rgba(102,126,234,0.12); border-radius: 16px;
                padding: 60px 40px; text-align: center; margin-top: 20px;">
        <div style="font-size: 4rem; margin-bottom: 16px;">📊</div>
        <div style="font-size: 1.4rem; font-weight: 700; color: #E6EDF3; margin-bottom: 10px;">
            Drop Any Dataset Here
        </div>
        <div style="font-size: 0.95rem; color: #8B949E; line-height: 1.7; max-width: 500px; margin: 0 auto;">
            Upload a CSV or Excel file and get instant analysis including:<br>
            <strong style="color: #667EEA;">Smart KPIs</strong> · 
            <strong style="color: #764BA2;">Auto Charts</strong> · 
            <strong style="color: #48BB78;">Distributions</strong> · 
            <strong style="color: #ED8936;">Correlations</strong> · 
            <strong style="color: #E53E3E;">Time Series</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Load Data ────────────────────────────────────────────────────────
@st.cache_data
def load_uploaded_file(file_data, file_name):
    try:
        if file_name.endswith((".xlsx", ".xls")):
            return pd.read_excel(BytesIO(file_data))
        else:
            try:
                return pd.read_csv(BytesIO(file_data))
            except UnicodeDecodeError:
                return pd.read_csv(BytesIO(file_data), encoding="latin-1")
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return pd.DataFrame()


file_bytes = uploaded_file.read()
df = load_uploaded_file(file_bytes, uploaded_file.name)

if df.empty:
    st.error("Could not parse the uploaded file. Please check the format.")
    st.stop()

# ── Column Type Detection ────────────────────────────────────────────
def detect_column_types(df):
    """Auto-detect column types for smart visualization."""
    types = {
        "numeric": [],
        "categorical": [],
        "datetime": [],
        "text": [],
        "boolean": [],
    }

    for col in df.columns:
        # Try datetime
        if df[col].dtype == "datetime64[ns]" or "date" in col.lower() or "time" in col.lower():
            try:
                pd.to_datetime(df[col], errors="raise")
                types["datetime"].append(col)
                continue
            except (ValueError, TypeError):
                pass

        # Numeric
        if pd.api.types.is_numeric_dtype(df[col]):
            if df[col].nunique() <= 2:
                types["boolean"].append(col)
            else:
                types["numeric"].append(col)
            continue

        # Categorical vs Text
        if pd.api.types.is_string_dtype(df[col]) or pd.api.types.is_object_dtype(df[col]):
            nunique = df[col].nunique()
            if nunique <= 30:
                types["categorical"].append(col)
            else:
                # Check if it's a date hidden as string
                try:
                    pd.to_datetime(df[col].dropna().head(20), errors="raise")
                    types["datetime"].append(col)
                except (ValueError, TypeError):
                    types["text"].append(col)
            continue

        types["text"].append(col)

    return types


col_types = detect_column_types(df)

# Convert detected datetime columns
for col in col_types["datetime"]:
    try:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    except Exception:
        pass

# ── Dataset Overview ─────────────────────────────────────────────────
st.markdown("")
st.markdown("### 📋 Dataset Overview")

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.metric("Rows", f"{len(df):,}")
with k2:
    st.metric("Columns", f"{len(df.columns)}")
with k3:
    st.metric("Numeric", f"{len(col_types['numeric'])}")
with k4:
    st.metric("Categorical", f"{len(col_types['categorical'])}")
with k5:
    missing_pct = df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100
    st.metric("Missing %", f"{missing_pct:.1f}%")

# Column type badges
st.markdown("")
type_colors = {
    "numeric": "#667EEA", "categorical": "#48BB78",
    "datetime": "#ED8936", "text": "#9F7AEA", "boolean": "#D69E2E",
}
badges_html = ""
for type_name, cols in col_types.items():
    color = type_colors.get(type_name, "#8B949E")
    for col in cols:
        badges_html += (
            f'<span style="display:inline-block; padding:3px 10px; margin:3px; '
            f'border-radius:12px; font-size:0.72rem; font-weight:500; '
            f'background:rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.12); '
            f'color:{color}; border:1px solid {color}30;">'
            f'{col} ({type_name})</span>'
        )

st.markdown(f'<div style="margin-bottom: 16px;">{badges_html}</div>', unsafe_allow_html=True)

# ── Data Preview ─────────────────────────────────────────────────────
with st.expander("📄 Data Preview", expanded=True):
    st.dataframe(df.head(100), use_container_width=True, hide_index=True)

# ── Summary Statistics ───────────────────────────────────────────────
with st.expander("📊 Summary Statistics", expanded=False):
    st.dataframe(df.describe(include="all").round(2), use_container_width=True)

# ── Auto Visualizations ─────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📈 Auto-Generated Visualizations")

tabs_list = []
if col_types["numeric"]:
    tabs_list.append("Distributions")
if col_types["categorical"]:
    tabs_list.append("Categories")
if len(col_types["numeric"]) >= 2:
    tabs_list.append("Correlations")
if col_types["datetime"] and col_types["numeric"]:
    tabs_list.append("Time Series")
if len(col_types["numeric"]) >= 2:
    tabs_list.append("Scatter Explorer")

if not tabs_list:
    st.info("No suitable columns detected for auto-visualization.")
    st.stop()

tabs = st.tabs(tabs_list)
tab_idx = 0

# ── Distributions Tab ───────────────────────────────────────────────
if "Distributions" in tabs_list:
    with tabs[tab_idx]:
        st.markdown("#### Numeric Distributions")
        sel_num_cols = st.multiselect(
            "Select columns to visualize",
            col_types["numeric"],
            default=col_types["numeric"][:4],
            key="dist_cols",
        )

        if sel_num_cols:
            n_cols = min(len(sel_num_cols), 2)
            for i in range(0, len(sel_num_cols), 2):
                cols = st.columns(n_cols)
                for j, col_name in enumerate(sel_num_cols[i:i+2]):
                    with cols[j]:
                        fig = px.histogram(
                            df, x=col_name, nbins=40,
                            color_discrete_sequence=["#667EEA"],
                            template="plotly_dark",
                            marginal="box",
                        )
                        fig.update_layout(
                            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                            font=dict(family="Inter", color="#E6EDF3"),
                            margin=dict(l=0, r=0, t=30, b=0), height=300,
                            title=dict(text=col_name, font=dict(size=14)),
                            xaxis=dict(gridcolor="rgba(102,126,234,0.06)"),
                            yaxis=dict(gridcolor="rgba(102,126,234,0.06)"),
                            showlegend=False,
                        )
                        st.plotly_chart(fig, use_container_width=True)
    tab_idx += 1

# ── Categories Tab ───────────────────────────────────────────────────
if "Categories" in tabs_list:
    with tabs[tab_idx]:
        st.markdown("#### Categorical Distributions")
        sel_cat_cols = st.multiselect(
            "Select columns",
            col_types["categorical"],
            default=col_types["categorical"][:4],
            key="cat_cols",
        )

        if sel_cat_cols:
            for i in range(0, len(sel_cat_cols), 2):
                cols = st.columns(2)
                for j, col_name in enumerate(sel_cat_cols[i:i+2]):
                    if i + j >= len(sel_cat_cols):
                        break
                    with cols[j]:
                        val_counts = df[col_name].value_counts().head(20).reset_index()
                        val_counts.columns = [col_name, "Count"]

                        if len(val_counts) <= 8:
                            fig = px.pie(
                                val_counts, values="Count", names=col_name,
                                hole=0.45, color_discrete_sequence=COLORS,
                                template="plotly_dark",
                            )
                        else:
                            fig = px.bar(
                                val_counts, x="Count", y=col_name, orientation="h",
                                color="Count",
                                color_continuous_scale=["#1a1f2e", "#667EEA", "#764BA2"],
                                template="plotly_dark",
                            )
                            fig.update_layout(coloraxis_showscale=False)

                        fig.update_layout(
                            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                            font=dict(family="Inter", color="#E6EDF3"),
                            margin=dict(l=0, r=0, t=30, b=0), height=350,
                            title=dict(text=col_name, font=dict(size=14)),
                            showlegend=True if len(val_counts) <= 8 else False,
                        )
                        st.plotly_chart(fig, use_container_width=True)
    tab_idx += 1

# ── Correlations Tab ─────────────────────────────────────────────────
if "Correlations" in tabs_list:
    with tabs[tab_idx]:
        st.markdown("#### Correlation Matrix")
        num_df = df[col_types["numeric"]].select_dtypes(include=[np.number])
        if len(num_df.columns) >= 2:
            corr = num_df.corr().round(3)
            fig = px.imshow(
                corr.values,
                x=corr.columns.tolist(),
                y=corr.index.tolist(),
                color_continuous_scale=["#E53E3E", "#0E1117", "#48BB78"],
                zmin=-1, zmax=1,
                template="plotly_dark",
                aspect="auto",
                text_auto=".2f",
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color="#E6EDF3"),
                margin=dict(l=0, r=0, t=10, b=0),
                height=max(350, len(corr.columns) * 40),
            )
            st.plotly_chart(fig, use_container_width=True)

            # Top correlations
            st.markdown("##### Top Correlations")
            pairs = []
            for i in range(len(corr.columns)):
                for j in range(i+1, len(corr.columns)):
                    pairs.append({
                        "Column A": corr.columns[i],
                        "Column B": corr.columns[j],
                        "Correlation": corr.iloc[i, j],
                    })
            pairs_df = pd.DataFrame(pairs).sort_values("Correlation", key=abs, ascending=False).head(10)
            st.dataframe(pairs_df, use_container_width=True, hide_index=True)
    tab_idx += 1

# ── Time Series Tab ──────────────────────────────────────────────────
if "Time Series" in tabs_list:
    with tabs[tab_idx]:
        st.markdown("#### Time Series Analysis")
        date_col = st.selectbox("Date Column", col_types["datetime"], key="ts_date")
        value_col = st.selectbox("Value Column", col_types["numeric"], key="ts_value")

        if date_col and value_col:
            ts_df = df[[date_col, value_col]].dropna().sort_values(date_col)

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=ts_df[date_col], y=ts_df[value_col],
                mode="lines", fill="tonexty",
                line=dict(color="#667EEA", width=2),
                fillcolor="rgba(102,126,234,0.1)",
            ))
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color="#E6EDF3"),
                margin=dict(l=0, r=0, t=10, b=0), height=350,
                xaxis=dict(gridcolor="rgba(102,126,234,0.06)"),
                yaxis=dict(gridcolor="rgba(102,126,234,0.06)", title=value_col),
                hovermode="x unified",
            )
            st.plotly_chart(fig, use_container_width=True)

            # Aggregated view
            if len(ts_df) > 30:
                st.markdown("##### Aggregated (Monthly Mean)")
                monthly = ts_df.set_index(date_col).resample("M")[value_col].mean().reset_index()
                fig2 = px.bar(
                    monthly, x=date_col, y=value_col,
                    color_discrete_sequence=["#764BA2"],
                    template="plotly_dark",
                )
                fig2.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Inter", color="#E6EDF3"),
                    margin=dict(l=0, r=0, t=10, b=0), height=300,
                    xaxis=dict(gridcolor="rgba(102,126,234,0.06)"),
                    yaxis=dict(gridcolor="rgba(102,126,234,0.06)"),
                    showlegend=False,
                )
                st.plotly_chart(fig2, use_container_width=True)
    tab_idx += 1

# ── Scatter Explorer Tab ────────────────────────────────────────────
if "Scatter Explorer" in tabs_list:
    with tabs[tab_idx]:
        st.markdown("#### Scatter Plot Explorer")
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            x_col = st.selectbox("X Axis", col_types["numeric"], index=0, key="scatter_x")
        with sc2:
            y_idx = min(1, len(col_types["numeric"]) - 1)
            y_col = st.selectbox("Y Axis", col_types["numeric"], index=y_idx, key="scatter_y")
        with sc3:
            color_options = ["None"] + col_types["categorical"][:10]
            color_col = st.selectbox("Color by", color_options, key="scatter_color")

        if x_col and y_col:
            scatter_kwargs = {
                "data_frame": df,
                "x": x_col,
                "y": y_col,
                "template": "plotly_dark",
                "opacity": 0.6,
            }
            if color_col != "None":
                scatter_kwargs["color"] = color_col
                scatter_kwargs["color_discrete_sequence"] = COLORS
            else:
                scatter_kwargs["color_discrete_sequence"] = ["#667EEA"]

            fig = px.scatter(**scatter_kwargs)
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color="#E6EDF3"),
                margin=dict(l=0, r=0, t=10, b=0), height=450,
                xaxis=dict(gridcolor="rgba(102,126,234,0.06)"),
                yaxis=dict(gridcolor="rgba(102,126,234,0.06)"),
            )
            st.plotly_chart(fig, use_container_width=True)

# ── Download Processed Data ─────────────────────────────────────────
st.markdown("---")
st.markdown("### 💾 Export")

col_dl1, col_dl2, _ = st.columns([1, 1, 4])
with col_dl1:
    csv_data = df.to_csv(index=False)
    st.download_button(
        "📥 Download as CSV",
        data=csv_data,
        file_name="analyzed_data.csv",
        mime="text/csv",
    )
with col_dl2:
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Data")
        df.describe(include="all").to_excel(writer, sheet_name="Statistics")
    st.download_button(
        "📥 Download as Excel",
        data=buffer.getvalue(),
        file_name="analyzed_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
