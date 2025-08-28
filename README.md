# dashboard
## Описание задачи
Построение дешборда на основе данных маркентинговой аналитики в формате csv
с исползованием Python, Pandas и Dash.
Отображаются следующие показатели:
1. Рекламные источники.
2. Расходы, клики по этим источникам;
3. Заявки, стоимость заявки;
4. Продажи, стоимость продажи и ROAS.

## Показатели входных данных:
- date
- traffic_source
- search_engine
- referral_source
- utm_source
- utm_medium
- utm_campaign
- utm_term
- utm_content
- start_url
- costs
- impressions
- clicks
- visits
- deal_id
- product_name
- city
- manager
- form
- leads
- q_leads
- orders
- revenue

## Установка
pip install pandas dash plotly

## Запуск
python3 dashboard.py