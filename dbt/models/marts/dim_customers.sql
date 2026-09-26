select
    user_id,
    first_name,
    last_name,
    first_name || ' ' || last_name as full_name,
    email,
    phone,
    gender,
    age,
    role
from {{ ref('stg_users') }}
