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
    # 1. Start with a list of blue for every bar
    colors = ["#1f77b4"] * len(arr)

    # 2. If C++ tells us it's swapping index 5 and 6, change those to red
    for idx in highlights:
        if 0 <= idx < len(arr):
            colors[idx] = "#d62728"

    # 3. Tell Plotly to draw the bars using those specific colors
    fig = go.Figure(data=[go.Bar(y=arr, marker_color=colors)])

    # 4. Make it look "Dark Mode" and sleek
    fig.update_layout(template="plotly_dark", yaxis=dict(range=[0, 110]))
    return fig


placeholder = st.empty()

if st.button("Start Sorting"):
    # 1. Build the terminal command: ['./engine', '10', '42', '5'...]
    cmd = ["./bub"] + [str(x) for x in st.session_state.data]

    # 2. Run the C++ binary and open the "Pipe"
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)

    # 3. Listen to C++ line-by-line
    for line in process.stdout:
        # line looks like: "10,5,42|1,2"
        raw_array, raw_idxs = line.strip().split("|")

        # 4. Convert text back to Python lists
        current_array = [int(x) for x in raw_array.split(",")]
        current_idxs = [int(x) for x in raw_idxs.split(",")]

        # 5. Redraw the chart in the placeholder
        placeholder.plotly_chart(draw_bars(current_array, current_idxs))

        # 6. Pause for a split second so humans can see it
        time.sleep(speed)
