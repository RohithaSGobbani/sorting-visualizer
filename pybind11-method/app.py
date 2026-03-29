import streamlit as st
import plotly.graph_objects as go
import time
import random
import sorting_engine  


ALGO_INFO = {
    "Bubble Sort": {"time": "O(n²)", "space": "O(1)"},
    "Selection Sort": {"time": "O(n²)", "space": "O(1)"},
    "Insertion Sort": {"time": "O(n²)", "space": "O(1)"},
    "Merge Sort": {"time": "O(n log n)", "space": "O(n)"},
    "Quick Sort": {"time": "O(n log n)", "space": "O(log n)"},
}

st.set_page_config(page_title="High-Performance Visualizer", layout="wide")


algo_choice = st.sidebar.selectbox(
    "Select Algorithm",
    ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort"],
)
st.title(f"{algo_choice}")
info = ALGO_INFO.get(algo_choice, {"time": "N/A", "space": "N/A"})

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Time Complexity", value=info["time"])
with col2:
    st.metric(label="Space Complexity", value=info["space"])

st.markdown("---")
st.subheader("Native C++ & Pybind11")
num_elements = st.sidebar.slider("Elements", 5, 100, 20)
speed = st.sidebar.slider("Delay (sec)", 0.0, 0.5, 0.05)

if "data" not in st.session_state or len(st.session_state.data) != num_elements:
    st.session_state.data = random.sample(range(1, 101), num_elements)

if st.sidebar.button("Shuffle Data"):
    st.session_state.data = random.sample(range(1, 101), num_elements)
    st.rerun()


def draw_bars(arr, highlights=[-1, -1]):
    """Returns a high-quality Plotly chart for static states."""
    colors = ["#1f77b4"] * len(arr)
    for idx in highlights:
        if 0 <= idx < len(arr):
            colors[idx] = "#d62728"

    fig = go.Figure(data=[go.Bar(y=arr, marker_color=colors)])
    fig.update_layout(
        template="plotly_dark",
        yaxis=dict(range=[0, 110], fixedrange=True),
        xaxis=dict(fixedrange=True),
        height=400,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
    )
    return fig


placeholder = st.empty()


def ui_callback(current_array, idx1, idx2):
    """
    Called by C++ during swaps.
    Uses bar_chart for speed and to eliminate flickering.
    """

    placeholder.bar_chart(current_array)
    time.sleep(speed)


placeholder.plotly_chart(
    draw_bars(st.session_state.data),
    use_container_width=True,
    config={"displayModeBar": False},
    key="initial_chart",
)

if st.button("Start Sorting"):
    if algo_choice == "Bubble Sort":
        result = sorting_engine.bubble_sort(st.session_state.data, ui_callback)
    elif algo_choice == "Selection Sort":
        result = sorting_engine.selection_sort(st.session_state.data, ui_callback)
    elif algo_choice == "Insertion Sort":
        result = sorting_engine.insertion_sort(st.session_state.data, ui_callback)
    elif algo_choice == "Merge Sort":
        result = sorting_engine.merge_sort(st.session_state.data, ui_callback)
    elif algo_choice == "Quick Sort":
        result = sorting_engine.quick_sort(st.session_state.data, ui_callback)

    if result is not None:
        st.session_state.data = result
        placeholder.plotly_chart(
            draw_bars(st.session_state.data),
            use_container_width=True,
            key="final_sorted_chart",
        )
        st.success(f"{algo_choice} Complete!")
