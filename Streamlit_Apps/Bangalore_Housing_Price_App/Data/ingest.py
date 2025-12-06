import os

os.environ['KAGGLEHUB_CACHE'] = r"F:\Udemy\Git\ML Portfolio\Streamlit Apps\Bangalore Housing Price App\Data"

import kagglehub
path = kagglehub.dataset_download("amitabhajoy/bengaluru-house-price-data")