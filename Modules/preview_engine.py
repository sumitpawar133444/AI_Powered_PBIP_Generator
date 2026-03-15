import streamlit as st
import pandas as pd
import numpy as np
try:
    import plotly.express as px
    import plotly.graph_objects as go

    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
from typing import Any, Dict, List, Optional

def render_preview_content(active_chat: Dict[str, Any], selected_page_idx: int = 0,is_full: bool = False, preview_key: str = "default") -> None:
    """
    Render the dashboard preview based on the chat's frontend_spec.

    """
    frontend = active_chat.get("frontend_spec")
    if not frontend:
        st.info("Start chatting to see your dashboard preview!")
        return

    title = frontend.get("title") or "Dashboard Preview"

    st.header(title)

    pages = frontend.get('pages', [])
    if not pages:
        st.info("No pages defined yet.")
        return

    # Get selected page visuals
    page_visuals = pages[selected_page_idx].get('visuals', [])

    if not page_visuals:
        st.info("No visuals on this page yet.")
        return

    pcolor = st.session_state.style_spec.get("primary_color", "#118DFF")
    scolor = st.session_state.style_spec.get("secondary_color", "#12239E")

    sorted_visuals = sorted(
        page_visuals,
        key=lambda v: (
            v.get('bounds', {}).get('y', 0),
            v.get('bounds', {}).get('x', 0)
        )
    )

    # Unique keys for KPI/chart containers
    kpi_types = ['card', 'kpi', 'gauge']
    kpis = [v for v in sorted_visuals if (v.get('type') or '').lower() in kpi_types]
    charts = [v for v in sorted_visuals if (v.get('type') or '').lower() not in kpi_types]

    kpi_key = f"kpis_{preview_key}_{selected_page_idx}"
    chart_key = f"charts_{preview_key}_{selected_page_idx}"

    with st.container(key=kpi_key):
        render_kpis(kpis, pcolor, is_full)

    with st.container(key=chart_key):
        render_charts(charts, pcolor, scolor, is_full)

    # Page footer info
    st.caption(f"Layout: {pages[selected_page_idx].get('layout', {}).get('type', 'default')} | {len(page_visuals)} visuals")


def render_kpis(page_visuals: List[Dict[str, Any]], pcolor: str, is_full: bool) -> None:
    """Render KPI/card visuals across responsive columns."""
    kpi_types = ['card', 'kpi', 'gauge']
    top_metrics = [v for v in page_visuals if (v.get('type') or '').lower() in kpi_types]
    if not top_metrics:
        return

    max_cols = 4 if is_full else 3
    num_cols = min(max_cols, max(1, len(top_metrics)))

    for i in range(0, len(top_metrics), num_cols):
        cols = st.columns(num_cols)
        for j in range(num_cols):
            if i + j < len(top_metrics):
                vis = top_metrics[i + j]
                with cols[j]:
                    render_single_kpi(vis, pcolor)

def render_single_kpi(vis: Dict[str, Any], pcolor: str) -> None:
    """Render a single KPI/card with mocked values."""
    title = vis.get("displayName") or vis.get("name") or "Metric"
    v_type = (vis.get("type") or "").lower()
    is_kpi = v_type == "kpi"

    val = int(np.random.randint(100, 999))
    target = int(np.random.randint(100, 999))

    if is_kpi and target != 0:
        pct = ((val / target) - 1) * 100
        value_text = f"{val} ({pct:.1f}%)"
        goal_line = f'<br><small style="color: #999;">Goal: {target}</small>'
    else:
        value_text = str(val)
        goal_line = ""

    st.markdown(
        f"""
        <div style="
            border-left: 4px solid {pcolor};
            padding: 10px;
            background: #fdfdfd;
            border: 1px solid #eee;
            border-radius: 4px;
            margin-bottom: 10px;
        ">
            <small style="color: #666; font-weight: bold; word-wrap: break-word;">
                {title}
            </small><br>
            <span style="font-size: 1.5rem; color: {pcolor}; font-weight: bold;">
                {value_text}
            </span>
            {goal_line}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_charts(page_visuals: List[Dict[str, Any]], pcolor: str, scolor: str, is_full: bool) -> None:
    """Render chart-like visuals in a grid."""
    charts = page_visuals
    if not charts:
        return

    max_cols = 3 if is_full else 2
    chart_cols = min(max_cols, max(1, len(charts)))

    for i in range(0, len(charts), chart_cols):
        cols = st.columns(chart_cols)
        for j in range(chart_cols):
            if i + j >= len(charts):
                break

            vis = charts[i + j]
            with cols[j]:
                with st.container(border=True):
                    _render_single_chart(vis, pcolor, scolor)


def _render_single_chart(
    vis: Dict[str, Any],
    p_color: str,
    s_color: str,
) -> None:
    """Render a single visual with mocked data, based on its type."""
    title = vis.get("displayName") or vis.get("name") or "Untitled"
    raw_type = (vis.get("type") or "barChart").lower()
    v_type = raw_type.replace("chart", "").replace(" ", "")
    v_dims = vis.get("dimensions") or ["Category"]
    v_meas = vis.get("measures") or ["Value"]

    # Extract properties
    props = vis.get("properties", {})
    orientation = props.get("orientation", "vertical")

    st.markdown(f"**{title}**")

    dummy_df = pd.DataFrame()
    map_data = None

    try:
        if v_type in {"scatter", "bubble"}:
            dim = v_dims[0]
            m1 = v_meas[0] if len(v_meas) > 0 else "X"
            m2 = v_meas[1] if len(v_meas) > 1 else "Y"
            m3 = v_meas[2] if len(v_meas) > 2 else "Size"

            dummy_df = pd.DataFrame(
                {
                    dim: ["A", "B", "C", "D", "E"],
                    m1: np.random.randint(10, 100, 5),
                    m2: np.random.randint(10, 100, 5),
                    m3: np.random.randint(10, 100, 5),
                }
            ).set_index(dim)

        elif v_type in {"table", "matrix"}:
            dim = v_dims[0]
            dummy_data = {dim: ["North", "South", "East", "West"]}
            for m in v_meas:
                dummy_data[m] = np.random.randint(1000, 5000, 4)
            dummy_df = pd.DataFrame(dummy_data)

        elif v_type == "heatmap":
            dim1 = v_dims[0]
            dim2 = v_dims[1] if len(v_dims) > 1 else "SubCategory"
            meas = v_meas[0]
            dummy_df = pd.DataFrame(
                {
                    dim1: ["Mon", "Tue", "Wed", "Mon", "Tue", "Wed"],
                    dim2: ["A", "A", "A", "B", "B", "B"],
                    meas: np.random.randint(10, 100, 6),
                }
            )

        elif v_type == "gauge":
            meas = v_meas[0]
            dummy_df = pd.DataFrame({meas: [np.random.randint(40, 95)]})

        elif v_type == "waterfall":
            df = pd.DataFrame(
                {
                    "Stage": ["Start", "A", "B", "C", "D", "Total"],
                    "Value": [100, 30, -20, 40, -10, 0],
                }
            )
            if PLOTLY_AVAILABLE:
                fig = go.Figure(
                    go.Waterfall(
                        orientation="v",
                        measure=[
                            "relative",
                            "relative",
                            "relative",
                            "relative",
                            "relative",
                            "total",
                        ],
                        x=df["Stage"],
                        y=df["Value"],
                        connector={"line": {"color": "rgb(63, 63, 63)"}},
                        increasing={"marker": {"color": p_color}},
                        decreasing={"marker": {"color": s_color}},
                    )
                )
                fig.update_layout(
                    height=200,
                    margin=dict(t=10, b=10, l=10, r=10),
                )
                st.plotly_chart(fig, use_container_width=True)

        elif v_type == "funnel":
            dummy_df = pd.DataFrame(
                {"Stage": ["Leads", "Quotes", "Orders", "Payments"], "Value": [1000, 600, 400, 200]}
            )
            if PLOTLY_AVAILABLE:
                fig = px.funnel(
                    dummy_df, x="Value", y="Stage", color_discrete_sequence=[p_color]
                )
                fig.update_layout(
                    height=200,
                    margin=dict(t=10, b=10, l=10, r=10),
                    showlegend=False,
                )
                st.plotly_chart(fig, use_container_width=True)

        elif v_type == "map":
            map_data = pd.DataFrame(
                {
                    "latitude": np.random.uniform(34.0, 36.0, 10),
                    "longitude": np.random.uniform(-119.0, -117.0, 10),
                    "size": np.random.randint(100, 1000, 10),
                }
            )

        elif v_type == "slicer":
            st.multiselect(
                f"Select {v_dims[0]}",
                ["Option A", "Option B", "Option C"],
                default=["Option A"],
            )
            st.caption("Visuals on this page will filter based on selection.")

        elif v_type == "ribbon":
            dummy_df = pd.DataFrame(
                {
                    "Month": ["Jan", "Feb", "Mar", "Apr"],
                    "A": [10, 20, 15, 25],
                    "B": [20, 10, 25, 15],
                }
            ).set_index("Month")

        elif v_type in {"bar", "column"}:
            dim = v_dims[0]
            meas = v_meas[0]
            dummy_df = pd.DataFrame(
                {
                    dim: ["A", "B", "C"],
                    meas: np.random.randint(10, 100, size=3),
                }
            ).set_index(dim)

        else:  # line, area, pie, donut, or unknown
            dim = v_dims[0]
            meas = v_meas[0]
            dummy_df = pd.DataFrame(
                {
                    dim: ["A", "B", "C", "D", "E"],
                    meas: np.random.randint(10, 100, size=5),
                }
            ).set_index(dim)

    except Exception as exc:
        st.error(f"Error mocking data: {exc}")
        dummy_df = pd.DataFrame()

    _draw_chart_from_dummy(
        v_type=v_type,
        dummy_df=dummy_df,
        map_data=map_data,
        v_dims=v_dims,
        v_meas=v_meas,
        p_color=p_color,
        s_color=s_color,
        orientation=orientation
    )

    st.caption(
        f"🔗 `{vis.get('table', 'TBD')} | Dims: {len(v_dims)} | Meas: {len(v_meas)}`"
    )


def _draw_chart_from_dummy(
    v_type: str,
    dummy_df: pd.DataFrame,
    map_data: pd.DataFrame | None,
    v_dims: List[str],
    v_meas: List[str],
    p_color: str,
    s_color: str,
    orientation="vertical"
) -> None:
    """Given dummy data and type, draw an appropriate preview chart."""
    if v_type == "waterfall" or dummy_df.empty and v_type not in {"map", "slicer"}:
        # waterfall already rendered in _render_single_chart when Plotly is available
        if dummy_df.empty and v_type not in {"map", "slicer"}:
            st.info(f"Previewing '{v_type}' as empty visual.")
        return

    if v_type in {"bar", "column"}:
        is_horizontal = (v_type == "bar") or (orientation == "horizontal")
        st.bar_chart(
            dummy_df,
            height=200,
            horizontal=is_horizontal,
        )

    elif v_type == "line":
        st.line_chart(dummy_df, height=200)

    elif v_type == "area":
        st.area_chart(dummy_df, height=200)

    elif v_type in {"scatter", "bubble"}:
        st.scatter_chart(dummy_df, height=200)

    elif v_type in {"table", "matrix"}:
        st.dataframe(dummy_df, use_container_width=True, height=200)

    elif v_type == "ribbon":
        st.area_chart(dummy_df, height=200)

    elif v_type == "map" and map_data is not None:
        st.map(map_data, size="size", height=200)

    elif v_type in {"pie", "donut"} and PLOTLY_AVAILABLE:
        df_pie = dummy_df.reset_index()
        hole_size = 0.5 if v_type == "donut" else 0.0
        fig = px.pie(
            df_pie,
            names=df_pie.columns[0],
            values=df_pie.columns[1],
            hole=hole_size,
        )
        fig.update_traces(
            marker=dict(
                colors=[p_color, s_color, "#87CEEB", "#B0E0E6", "#4682B4"]
            )
        )
        fig.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            height=200,
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    elif v_type == "gauge" and PLOTLY_AVAILABLE:
        val = float(dummy_df.iloc[0, 0])
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=val,
                title={"text": v_meas[0], "font": {"size": 12}},
                gauge={"axis": {"range": [None, 100]}, "bar": {"color": p_color}},
            )
        )
        fig.update_layout(margin=dict(t=30, b=20, l=20, r=20), height=200)
        st.plotly_chart(fig, use_container_width=True)

    elif v_type == "heatmap" and PLOTLY_AVAILABLE:
        fig = px.density_heatmap(
            dummy_df,
            x=dummy_df.columns[0],
            y=dummy_df.columns[1],
            z=dummy_df.columns[2],
            color_continuous_scale="Blues",
        )
        fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=200)
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info(f"Previewing '{v_type}' as table.")
        st.dataframe(dummy_df, use_container_width=True, height=180)