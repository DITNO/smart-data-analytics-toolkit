"""
SDA Toolkit - Streamlit Dashboard
"""

import sys
from pathlib import Path

# Add src/ to module search path so 'sda_toolkit' is found even when
# 'pip install -e .' hasn't been run (e.g. on Streamlit Cloud).
# Streamlit Cloud only runs requirements.txt, not the editable install.
_src_path = str(Path(__file__).resolve().parent / 'src')
if _src_path not in sys.path:
    sys.path.insert(0, _src_path)

import io, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd, streamlit as st
import sda_toolkit
from sda_toolkit import cleaning, analysis, report

st.set_page_config(page_title="SDA Toolkit", page_icon=chr(128202), layout="wide", initial_sidebar_state="expanded")

def _bar_chart(df,x,y): fig,ax=plt.subplots(figsize=(8,4)); ax.bar(df[x],df[y]); ax.set_xlabel(x); ax.set_ylabel(y); ax.set_title(f"{x} vs {y}"); plt.tight_layout(); return fig
def _line_chart(df,x,y): fig,ax=plt.subplots(figsize=(8,4)); ax.plot(df[x],df[y]); ax.set_xlabel(x); ax.set_ylabel(y); ax.set_title(f"{x} vs {y}"); plt.tight_layout(); return fig
def _histogram(df,c,b=20): fig,ax=plt.subplots(figsize=(8,4)); ax.hist(df[c],bins=b); ax.set_xlabel(c); ax.set_ylabel("Frequency"); ax.set_title(f"Dist of {c}"); plt.tight_layout(); return fig
def _scatter(df,x,y): fig,ax=plt.subplots(figsize=(8,4)); ax.scatter(df[x],df[y]); ax.set_xlabel(x); ax.set_ylabel(y); ax.set_title(f"Scatter {x} vs {y}"); plt.tight_layout(); return fig
def _pie(df,c): ct=df[c].value_counts(); fig,ax=plt.subplots(figsize=(6,6)); ax.pie(ct,labels=ct.index,autopct="%1.1f%%"); ax.set_title(f"Pie {c}"); plt.tight_layout(); return fig

for k in ["df_original","df_cleaned","file_name","stats","cleaning_applied"]:
  if k not in st.session_state: st.session_state[k] = None if k != "cleaning_applied" else False

st.title("SDA Toolkit")
st.markdown("Upload, clean, analyze, visualize, and export tabular data.")

with st.sidebar:
  st.header("Data Source")
  u = st.file_uploader("Upload CSV/Excel/JSON", type=["csv","xlsx","xls","json"])
  if u is not None:
    try:
      s = Path(u.name).suffix
      if s == ".csv": df = pd.read_csv(u)
      elif s in (".xlsx", ".xls"): df = pd.read_excel(u)
      elif s == ".json": df = pd.read_json(u)
      else: st.error("Unsupported " + s); df = None
      if df is not None and not df.empty:
        st.session_state.df_original = df.copy(); st.session_state.df_cleaned = df.copy()
        st.session_state.file_name = u.name; st.session_state.stats = analysis.summary_stats(df)
        st.session_state.cleaning_applied = False
        st.success("Loaded " + u.name + " (" + str(len(df)) + "r x " + str(len(df.columns)) + "c)")
      elif df is not None: st.warning("Empty file.")
    except Exception as e: st.error("Error: " + str(e))
  st.divider(); st.header("Cleaning")
  dd = st.checkbox("Drop duplicates", True)
  ms = st.selectbox("Missing strategy", ["mean","median","drop","fill"], 0)
  ft = st.checkbox("Auto-fix dtypes", True)
  if st.button("Apply Cleaning", type="primary", use_container_width=True):
    if st.session_state.df_original is not None:
      df = st.session_state.df_original.copy()
      if dd: df = cleaning.drop_duplicates(df)
      df = cleaning.handle_missing(df, strategy=ms)
      if ft: df = cleaning.fix_dtype(df)
      st.session_state.df_cleaned = df; st.session_state.stats = analysis.summary_stats(df)
      st.session_state.cleaning_applied = True; st.success("Cleaning applied!")
    else: st.warning("Upload first.")
  st.divider(); st.caption("v" + sda_toolkit.__version__)
  if st.button("Reset", use_container_width=True):
    for k in ["df_original","df_cleaned","file_name","stats"]: st.session_state[k] = None
    st.session_state.cleaning_applied = False; st.rerun()

if st.session_state.df_original is None:
  c1,c2,c3 = st.columns(3)
  c1.info("Upload a file")
  c2.markdown("CSV, Excel, JSON")
  c3.markdown("1.Upload 2.Clean 3.Analyze 4.Download"); st.stop()

df = st.session_state.df_cleaned; orig = st.session_state.df_original; stats = st.session_state.stats
t1,t2,t3,t4 = st.tabs(["Preview","Analysis","Charts","Report"])

with t1:
  st.subheader("Dataset Preview")
  c1,c2,c3,c4 = st.columns(4)
  c1.metric("Original", len(orig))
  c2.metric("Cleaned", len(df), delta=len(df)-len(orig))
  c3.metric("Columns", len(df.columns))
  c4.metric("Missing", int(df.isnull().sum().sum()))
  with st.expander("Raw data", False): st.dataframe(orig, use_container_width=True)
  with st.expander("Cleaned data", True): st.dataframe(df, use_container_width=True)
  ct = pd.DataFrame({"Column": df.columns, "Dtype": [str(d) for d in df.dtypes], "Non-Null": df.notna().sum().values, "Null": df.isna().sum().values})
  st.dataframe(ct, use_container_width=True, hide_index=True)

with t2:
  st.subheader("Summary Stats")
  if stats is not None and not stats.empty: st.dataframe(stats, use_container_width=True)
  else: st.info("No numeric cols.")
  st.divider(); st.subheader("Correlation")
  corr = analysis.correlation_matrix(df)
  if corr is not None and not corr.empty: st.dataframe(corr.style.background_gradient(cmap="coolwarm"), use_container_width=True)
  else: st.info("Not enough numeric cols.")
  st.divider(); st.subheader("Outliers (IQR)")
  ol = analysis.detect_outliers(df)
  if ol: st.dataframe(pd.DataFrame(list(ol.items()), columns=["Col","Count"]), use_container_width=True, hide_index=True)
  else: st.info("No numeric cols.")
  st.divider(); st.subheader("Value Counts")
  c = st.selectbox("Column", df.columns.tolist(), key="vc")
  cnt = df[c].value_counts().reset_index(); cnt.columns = [c, "Count"]
  st.dataframe(cnt, use_container_width=True, hide_index=True)

with t3:
  st.subheader("Charts")
  ct = st.selectbox("Type", ["Bar","Line","Histogram","Scatter","Pie"], 0)
  nc = df.select_dtypes(include="number").columns.tolist()
  cc = df.select_dtypes(exclude="number").columns.tolist()
  gen = st.button("Generate", type="primary")
  if ct == "Bar":
    x = st.selectbox("X", cc + df.columns.tolist()); y = st.selectbox("Y", nc)
    if gen and x and y: f = _bar_chart(df,x,y); st.pyplot(f); plt.close(f)
  elif ct == "Line":
    x = st.selectbox("X", df.columns.tolist()); y = st.selectbox("Y", nc)
    if gen and x and y: f = _line_chart(df,x,y); st.pyplot(f); plt.close(f)
  elif ct == "Histogram":
    c = st.selectbox("Column", nc); b = st.slider("Bins", 5, 100, 20)
    if gen and c: f = _histogram(df,c,bins=b); st.pyplot(f); plt.close(f)
  elif ct == "Scatter":
    x = st.selectbox("X", nc); y = st.selectbox("Y", nc, index=min(1,len(nc)-1))
    if gen and x and y: f = _scatter(df,x,y); st.pyplot(f); plt.close(f)
  elif ct == "Pie":
    c = st.selectbox("Column", cc + df.columns.tolist())
    if gen and c: f = _pie(df,c); st.pyplot(f); plt.close(f)

with t4:
  st.subheader("Export")
  buf = io.BytesIO(); df.to_csv(buf, index=False)
  fn = st.session_state.file_name
  st.download_button("Download CSV", buf.getvalue(), Path(fn).stem + "_cleaned.csv", "text/csv", use_container_width=True)
  st.divider()
  if stats is not None and not stats.empty:
    rl = ["=== Summary Stats ===\n"]
    for cn, cs in stats.items():
      rl.append("Column: " + str(cn)); rl.append("-" * (len(str(cn)) + 8))
      for sn, sv in cs.items(): rl.append("  " + str(sn) + ": " + str(sv))
      rl.append("")
    rt = "\n".join(rl)
  else: rt = "No stats available."
  st.download_button("Download Report", rt, Path(fn).stem + "_summary.txt", "text/plain", use_container_width=True)
