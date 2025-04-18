import pandas as pd
import plotly.graph_objects as go
from itertools import tee

pathways = pd.read_csv("course_pathways.csv")
catalog = pd.read_csv("course_catalog_by_major.csv")

# Normalize text fields for consistent matching
for df, cols in [(pathways, ["Program", "Major"]), (catalog, ["Major", "Type"])]:
    for col in cols:
        df[col] = df[col].str.strip().str.lower()

target_majors = ["data science", "artificial intelligence", "cybersecurity"]
df = pathways[(pathways["Program"] == "cecs") & (pathways["Major"].isin(target_majors))].copy()

reqd_lookup = (
    catalog[catalog["Type"] == "required"]
    .groupby("Major")["Course"]
    .apply(set)
    .to_dict()
)

df["Course"] = df["CoursePath"].str.split("->")
df_long = df.explode("Course")
df_long["Course"] = df_long["Course"].str.strip()

# Keep only the required courses for each student
df_long = df_long[df_long.apply(lambda row: row["Course"] in reqd_lookup.get(row["Major"], set()), axis=1)]

# Reassemble each student’s required-course sequence
seqs = (
    df_long.groupby("StudentID")["Course"]
    .apply(list)
    .reset_index(name="ReqSeq")
)

# Extract consecutive course transitions for Sankey links
def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

transitions = [pair for seq in seqs["ReqSeq"] for pair in pairwise(seq)]
trans_df = (
    pd.DataFrame(transitions, columns=["source", "target"] )  
    .value_counts()
    .reset_index(name="count")
)

# Map each course name to a unique node index
nodes = pd.unique(trans_df[["source", "target"]].values.ravel())
node_index = {course: idx for idx, course in enumerate(nodes)}
trans_df["source_idx"] = trans_df["source"].map(node_index)
trans_df["target_idx"] = trans_df["target"].map(node_index)

scale_factor = 8
values = trans_df["count"] / scale_factor

# Sankey diagram
fig = go.Figure(go.Sankey(
    arrangement="snap",
    node=dict(
        pad=30,
        thickness=24,
        line=dict(color="black", width=0.5),
        label=list(nodes),
        align='center'
    ),
    link=dict(
        arrowlen=315,
        source=trans_df["source_idx"],
        target=trans_df["target_idx"],
        value=values,
        color="rgba(100,100,100,0.4)"
    )
))

fig.update_layout(
    title_text="CECS Required-course Pathways",
    font=dict(size=10),
    margin=dict(l=40, r=40, t=60, b=40),
    width=2700,
    height=1000
)

# Export the results
fig.write_image("sankey_diagram.png")  


