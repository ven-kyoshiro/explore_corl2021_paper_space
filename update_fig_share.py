import pandas as pd
import plotly.graph_objects as go
import plotly.offline as offline


#mukais = [18,65,71,92,171,183,107]
path = "my_choices.txt"

with open(path) as f:
    s = f.read()
id_word = s.split("\n")
mukais = [int(w.strip()) for w in id_word[0].split(",")]
word = id_word[1].strip()

df = pd.read_csv("all_result_for_updatepy.csv")

df["mukai"] = [i in mukais for i in df["id"]]
df["category"] = [word in txt for txt in df["base_txt"]]
df["category"][df["mukai"]] = False

fig = go.Figure(go.Scatter(
    x = df["dim1"][~(df["mukai"]&df["category"])],
    y = df["dim2"][~(df["mukai"]&df["category"])],
    hovertemplate =
    '%{hovertext}<extra></extra>',
    text = df["best_kw"][~(df["mukai"]&df["category"])],
    hovertext = df["disp_txt"][~(df["mukai"]&df["category"])],
    showlegend = False,mode = "markers+text", textposition='top center'))

fig.add_trace(go.Scatter(
    x = df["dim1"][df["mukai"]],
    y = df["dim2"][df["mukai"]],
    hovertemplate =
    '%{hovertext}',
    text = df["best_kw"][df["mukai"]],
    hovertext = df["disp_txt"][df["mukai"]],
    showlegend = False,mode = "markers+text", textposition='top center'))

fig.add_trace(go.Scatter(
    x = df["dim1"][df["category"]],
    y = df["dim2"][df["category"]],
    hovertemplate =
    '%{hovertext}',
    text = df["best_kw"][df["category"]],
    hovertext = df["disp_txt"][df["category"]],
    showlegend = False,mode = "markers+text", textposition='top center'))


fig.update_layout(width=2000, height=2000,xaxis=dict(title='dim1'),
        yaxis=dict(title='dim2',scaleanchor="x", scaleratio=1),)

offline.plot(fig, filename='corl_allpaper.html')
df[["id","Title","OR Link","Keyword","Abstract"]][df["mukai"]].to_csv("my_choices_summary.csv")

