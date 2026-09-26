select
    category,
    count(distinct cart_id) as orders,
    sum(quantity) as units_sold,
    round(sum(line_total), 2) as revenue,
    round(sum(line_discounted_total), 2) as discounted_revenue
from {{ ref('int_order_lines') }}
group by category
order by revenue desc
