import pandas as pd

data = {
        'order_id': [1, 2, 3],
        'customer_id': [1, 2, 3],
        'created_at': ['2025-01-01', '2025-01-25', '2025-01-30']
    }

df = pd.DataFrame(data)
print("Customer orders:")
print(df)