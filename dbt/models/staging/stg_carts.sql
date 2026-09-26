select
    id as cart_id,
    userId as user_id,
    total,
    discountedTotal as discounted_total,
    totalProducts as total_products,
    totalQuantity as total_quantity
from {{ source('retail_dummyjson', 'raw_carts') }}
