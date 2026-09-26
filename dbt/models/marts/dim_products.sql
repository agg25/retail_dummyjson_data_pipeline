select
    product_id,
    title,
    category,
    brand,
    price,
    rating,
    stock,
    availability_status
from {{ ref('stg_products') }}
