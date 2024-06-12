import pandas as pd
import numpy as np

# Simulate customer journey data
np.random.seed(42)
num_records = 10000  # Increase the number of records for more complexity
start_date = pd.Timestamp('2018-01-01')
end_date = pd.Timestamp('2023-01-01')

# Create a function to generate realistic data
def generate_realistic_data(num_records):
    customer_ids = np.random.randint(1, 1001, num_records)
    stages = np.random.choice(['Awareness', 'Consideration', 'Decision'], num_records, p=[0.5, 0.3, 0.2])
    segments = np.random.choice(['frequent', 'one_time'], num_records, p=[0.7, 0.3])
    conversion_rates = np.where(stages == 'Awareness', np.random.uniform(0.05, 0.1, num_records),
                                np.where(stages == 'Consideration', np.random.uniform(0.1, 0.2, num_records),
                                         np.random.uniform(0.2, 0.3, num_records)))
    click_through_rates = np.where(stages == 'Awareness', np.random.uniform(0.05, 0.1, num_records),
                                   np.where(stages == 'Consideration', np.random.uniform(0.1, 0.2, num_records),
                                            np.random.uniform(0.2, 0.3, num_records)))
    engagement_scores = np.where(segments == 'frequent', np.random.uniform(50, 100, num_records),
                                 np.random.uniform(20, 50, num_records))
    bounce_rates = np.where(stages == 'Decision', np.random.uniform(20, 40, num_records), np.random.uniform(40, 80, num_records))
    page_views = np.where(stages == 'Awareness', np.random.randint(20, 40, num_records),
                         np.where(stages == 'Consideration', np.random.randint(30, 60, num_records), np.random.randint(40, 80, num_records)))
    timestamps = pd.to_datetime(np.random.randint(start_date.value // 10**9, end_date.value // 10**9, num_records), unit='s')
    
    # Add retention data
    retention_periods = np.random.randint(1, 365, num_records)  # Retention period in days
    retention_rates = np.where(segments == 'frequent', np.random.uniform(0.5, 0.9, num_records), 
                               np.random.uniform(0.1, 0.5, num_records))  # Higher retention rates for frequent

    data = pd.DataFrame({
        'customer_id': customer_ids,
        'stage': stages,
        'segment': segments,
        'conversion_rate': conversion_rates,
        'click_through_rate': click_through_rates,
        'engagement_score': engagement_scores,
        'bounce_rate': bounce_rates,
        'page_views': page_views,
        'timestamp': timestamps,
        'retention_period': retention_periods,
        'retention_rate': retention_rates
    })
    
    return data

data = generate_realistic_data(num_records)
data.to_csv('customer_journey_data.csv', index=False)
