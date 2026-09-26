select
    ci.cart_id,
    ci.user_id,
    ci.product_id,
    ci.title as product_title,
    ci.quantity,
    ci.price,
    ci.total as line_total,
    ci.discounted_total as line_discounted_total,
    p.category,
    p.brand,
    c.total as cart_total,
    c.discounted_total as cart_discounted_total
from {{ ref('stg_cart_items') }} ci
left join {{ ref('stg_products') }} p
    on ci.product_id = p.product_id
left join {{ ref('stg_carts') }} c
    on ci.cart_id = c.cart_id
