import streamlit as st
import itertools, math, json
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def dist(a, b):
    d = math.hypot(a[0]-b[0], a[1]-b[1])
    return 0.0 if abs(d) < 1e-12 else d

def p_center(coords, p):
    D = {(i, j): dist(coords[i], coords[j]) for i in coords for j in coords}
    best_combo, best_z = None, float("inf")
    for combo in itertools.combinations(coords.keys(), p):
        max_d = max(min(D[(i, j)] for i in combo) for j in coords)
        if max_d < best_z:
            best_z, best_combo = max_d, combo
    return best_combo, best_z

def nCr(n, r):
    from math import comb
    return comb(n, r)

def validate(coords, p, max_n=25):
    # Basic input validation for safe use
    if not coords:
        raise ValueError("No neighborhood coordinates provided.")
    if any(not isinstance(k, int) for k in coords.keys()):
        raise ValueError("Keys in 'coords' must be integers (e.g., '1','2',...).")
    if any(len(v)!=2 or any(not isinstance(x,(int,float)) for x in v) for v in coords.values()):
        raise ValueError("Each coordinate must be a numeric pair [x, y] (km).")
    n = len(coords)
    if p < 1:
        raise ValueError("Number of stations p must be ≥ 1.")
    if p > n:
        raise ValueError(f"p={p} cannot exceed number of neighborhoods n={n}.")
    if n > max_n:
        raise ValueError(f"Too many locations (n={n}). Try n ≤ {max_n}.")
    if nCr(n, p) > 2_000_000:
        st.warning("Large search space (n choose p). Computation may be slow.")

# Visualization
def visualize(coords, combo, z):
    fig, ax = plt.subplots(figsize=(6,6))
    xs, ys = zip(*coords.values())
    ax.scatter(xs, ys, c='#444', s=70, label="Neighborhoods", zorder=3)
    for i in combo:
        ax.scatter(coords[i][0], coords[i][1], c='#d62828', s=130, marker='^',
                   edgecolors='white', linewidths=1.5,
                   label="Emergency Station" if i==combo[0] else "")
        circ = Circle(coords[i], radius=z, fill=False, ls='--', color='#d62828', alpha=0.5)
        ax.add_patch(circ)
    for j in coords:
        nearest = min(combo, key=lambda i: dist(coords[i], coords[j]))
        ax.plot([coords[j][0], coords[nearest][0]],
                [coords[j][1], coords[nearest][1]],
                lw=0.9, color='#999', alpha=0.5)
    ax.set_facecolor('#f8f9fa')
    ax.set_title(f"Emergency Station Coverage  (p={len(combo)},  z*={z:.2f} km)", fontsize=14, pad=10)
    ax.legend(frameon=False, loc='upper right')
    ax.axis('equal')
    ax.grid(True, alpha=0.2)
    st.pyplot(fig)

# Streamlit UI
st.set_page_config(page_title="Emergency Station Optimizer", page_icon="🚒", layout="centered")

st.markdown("<h2 style='text-align:center; color:#333;'>🚒 Emergency Station Optimization</h2>", unsafe_allow_html=True)
st.caption("Determine optimal locations for emergency stations so every neighborhood is within the minimum possible **maximum response distance**.")

tab1, tab2 = st.tabs(["🏙️ Input Data","📈 Results & Visualization"])

with tab1:
    st.markdown("### 📍 Define Neighborhood Coordinates")
    mode = st.radio("Choose input type:", ["Manual", "JSON file/text"])
    coords = {}
    if mode == "Manual":
        n = st.number_input("Number of neighborhoods", 2, 20, 6)
        cols = st.columns(2)
        for i in range(1, n+1):
            x = cols[0].number_input(f"X{i} (km)", value=float(i*5-5))
            y = cols[1].number_input(f"Y{i} (km)", value=float((i%3)*5))
            coords[i] = (x, y)
        p = st.number_input("Number of emergency stations (p)", 1, n, 2)
    else:
        example = '{\n  "coords": {"1": [0,0], "2": [0,10], "3": [10,0], "4": [10,10], "5": [20,5], "6": [30,8]},\n  "p": 2\n}'
        data = st.text_area("Paste JSON data:", example, height=150)
        try:
            js = json.loads(data)
            coords = {int(k): tuple(v) for k,v in js["coords"].items()}
            p = int(js["p"])
            st.success(f"Loaded {len(coords)} neighborhoods (p={p}).")
        except Exception as e:
            st.error(f"Invalid JSON → {e}")
            coords, p = {}, 0

    run = st.button("🚀 Compute Optimal Station Placement")

with tab2:
    if run and coords:
        try:
            validate(coords, p)
            combo, z = p_center(coords, p)
            c1, c2 = st.columns(2)
            with c1: st.metric("Stations Opened", str(combo))
            with c2: st.metric("Max Response Distance z*", f"{z:.2f} km")
            st.markdown("#### Neighborhood Assignments")
            for j in coords:
                nearest = min(combo, key=lambda i: dist(coords[i], coords[j]))
                st.write(f"Neighborhood **{j}** → Station **{nearest}**  (distance {dist(coords[nearest], coords[j]):.2f} km)")
            st.markdown("---")
            visualize(coords, combo, z)
        except Exception as e:
            st.error(str(e))
    else:
        st.info("Enter data and click *Compute Optimal Station Placement* in the Input tab.")
