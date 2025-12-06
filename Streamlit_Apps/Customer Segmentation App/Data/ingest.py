import os
os.environ['KAGGLEHUB_CACHE'] = r'F:\Udemy\Git\ML Portfolio\Streamlit Apps\Customer Segmentation App\Data'

import kagglehub

path = kagglehub.dataset_download()

print('Data has successfully loaded into desired path 🎉')