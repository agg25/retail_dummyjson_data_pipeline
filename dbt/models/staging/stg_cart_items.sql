select
    cart_id,
    user_id,
    product_id,
    title,
    price,
    quantity,
    total,
    discountPercentage as discount_percentage,
    discountedTotal as discounted_total,
    thumbnail
from {{ source('retail_dummyjson', 'raw_cart_items') }}
