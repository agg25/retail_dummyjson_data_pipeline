select
    id as user_id,
    firstName as first_name,
    lastName as last_name,
    age,
    gender,
    email,
    phone,
    username,
    birthDate as birth_date,
    bloodGroup as blood_group,
    height,
    weight,
    eyeColor as eye_color,
    university,
    role
from {{ source('retail_dummyjson', 'raw_users') }}
