import streamlit as st
import subprocess
import plotly.graph_objects as go
import time
import random

st.set_page_config(page_title="Sorting Visualizer", layout="wide")
st.title("C++ & Streamlit Sorting Visualizer")

num_ele = st.sidebar.slider("Number of elements:", 5, 5, 20)
speed = st.sidebar.slider("Speed(Delay):", 0.01, 0.5, 0.1)

if "data" not in st.session_state:
    st.session_state.data = random.sample(range(1, 101), num_ele)

if st.sidebar.button("Shuffle"):
    st.session_state.data = random.sample(range(1, 101), num_ele)


def draw_bars(arr, highlights=[-1, -1]):

    colors = ["#1f77b4"] * len(arr)

    for idx in highlights:
        if 0 <= idx < len(arr):
            colors[idx] = "#d62728"

    fig = go.Figure(data=[go.Bar(y=arr, marker_color=colors)])

    fig.update_layout(template="plotly_dark", yaxis=dict(range=[0, 110]))
    return fig


placeholder = st.empty()

if st.button("Start Sorting"):

    cmd = ["./bub"] + [str(x) for x in st.session_state.data]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)

    for line in process.stdout:
       
        raw_array, raw_idxs = line.strip().split("|")


        current_array = [int(x) for x in raw_array.split(",")]
        current_idxs = [int(x) for x in raw_idxs.split(",")]

  
        placeholder.plotly_chart(draw_bars(current_array, current_idxs))

        time.sleep(speed)
