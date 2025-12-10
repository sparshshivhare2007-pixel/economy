# helpers/__init__.py

# -------------------- IMPORTS FROM DATABASE --------------------
from database.users import (
    get_user,
    users,
    user_db,
    add_group_id,
    is_group_open,
    set_group_status,
    is_protected,
    format_delta
)

# -------------------- UTILITY: RANDOM PERCENTAGE --------------------
import random

def random_percentage():
    return random.randint(1, 100)
