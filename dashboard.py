import pandas as pd
import dash
from dash import dcc, html, dash_table
import plotly.express as px

# === 1. Загружаем данные из CSV (экспорт из Google Sheets) ===
df = pd.read_csv("data.csv")
# Печатаем список колонок
#print("Колонки в файле:")
#print(df.columns.tolist())

# Печатаем первые 5 строк
#print("\nПервые строки таблицы:")
#print(df.head())
# Проверим названия колонок (переименуйте под ваши реальные в файле)
# Например: Source, Spend, Clicks, Leads, Sales, Revenue

# === 2. Приводим к нужным колонкам ===

rename_map = {
"traffic_source": "Source",
"costs": "Spend",
"clicks": "Clicks",
"leads": "Leads",
"orders": "Sales",
"revenue": "Revenue"
}

df = df.rename(columns=rename_map)

# === 2. Считаем метрики ===
df_summary = df.groupby("Source", as_index=False).sum()

# Добавляем вычисляемые поля
if "Leads" in df_summary.columns:
    df_summary["CPL"] = df_summary.apply(lambda x: x["Spend"] / x["Leads"] if x["Leads"] > 0 else None, axis=1)
if "Sales" in df_summary.columns:
    df_summary["CPO"] = df_summary.apply(lambda x: x["Spend"] / x["Sales"] if x["Sales"] > 0 else None, axis=1)
if "Revenue" in df_summary.columns:
    df_summary["ROAS"] = df_summary.apply(lambda x: x["Revenue"] / x["Spend"] if x["Spend"] > 0 else None, axis=1)

# Оставляем только агрегированные колонки
cols_show = ["Source", "Spend", "Clicks", "Leads", "Sales", "Revenue", "CPL", "CPO", "ROAS"]
df_summary = df_summary[[c for c in cols_show if c in df_summary.columns]]
# === 3. Создаём дашборд ===
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("📊 Маркетинговый дашборд", style={"textAlign": "center"}),

    # Таблица с метриками
    dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df_summary.columns],
        data=df_summary.round(2).to_dict("records"),
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "center", "padding": "5px"},
        style_header={"backgroundColor": "#f4f4f4", "fontWeight": "bold"}
    ),

    html.Br(),

    # График расходов по источникам
    dcc.Graph(
        figure=px.bar(df_summary, x="Source", y="Spend", title="Расходы по источникам", text_auto=True)
    ),

    # График заявок и продаж (если есть)
    dcc.Graph(
        figure=px.bar(df_summary, x="Source", y=[col for col in ["Leads", "Sales"] if col in df_summary.columns],
                      barmode="group", title="Заявки и продажи")
    ),

    # ROAS
    dcc.Graph(
        figure=px.bar(df_summary, x="Source", y="ROAS", title="ROAS по источникам", text_auto=True)
    ) if "ROAS" in df_summary.columns else html.Div()
])

if __name__ == "__main__":
    app.run(debug=True)
