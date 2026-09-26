select
    c.cart_id as order_id,
    c.user_id,
    u.first_name || ' ' || u.last_name as customer_name,
    c.total,
    c.discounted_total,
    c.total_products,
    c.total_quantity
from {{ ref('stg_carts') }} c
left join {{ ref('stg_users') }} u
    on c.user_id = u.user_id
