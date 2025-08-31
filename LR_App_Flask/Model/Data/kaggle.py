import os
os.environ["KAGGLEHUB_CACHE"] = r"F:\Udemy\Git\ML Portfolio\LR_App_Flask\Model\Data"
import kagglehub

path = kagglehub.dataset_download("shalmamuji/electricity-cost-prediction-dataset")

print(path)