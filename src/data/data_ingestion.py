# data ingestion
import os
import yaml
import logging
from src.logger import logging
import kagglehub
import shutil
import os

# def download_data_from_kaggle(kaggle_dataset_name,path):

#     cached_path = kagglehub.dataset_download(kaggle_dataset_name)

#     logging.info("The default kaggle downloaded path: %s",cached_path)

#     # Copy dataset to your preferred location
#     # shutil.copytree(cached_path, destination, dirs_exist_ok=True)
#     shutil.move(cached_path, path)

#     logging.info("Data has been moved to: %s",path)

import os
import shutil
import logging

def download_data_from_kaggle(kaggle_dataset_name, path):
    chest_xray_folder = os.path.join(path, "chest_xray")

    # Check if the chest_xray folder already exists
    if os.path.exists(chest_xray_folder):
        user_input = input(f"The folder '{chest_xray_folder}' already exists. Do you want to download it again? (y/n): ")
        if user_input.lower() != 'y':
            logging.info("Download skipped by user.")
            return

    # Proceed to download from Kaggle
    cached_path = kagglehub.dataset_download(kaggle_dataset_name)
    logging.info("The default kaggle downloaded path: %s", cached_path)

    # Move dataset to the desired path
    if os.path.exists(path):
        shutil.rmtree(path)  # Remove existing path to avoid overwrite issues
    shutil.move(cached_path, path)

    logging.info("Data has been moved to: %s", path)

def load_params(params_path: str) -> dict:
    """Load parameters from a YAML file."""
    try:
        with open(params_path, 'r') as file:
            params = yaml.safe_load(file)
        logging.debug('Parameters retrieved from %s', params_path)
        return params
    except FileNotFoundError:
        logging.error('File not found: %s', params_path)
        raise
    except yaml.YAMLError as e:
        logging.error('YAML error: %s', e)
        raise
    except Exception as e:
        logging.error('Unexpected error: %s', e)
        raise

def main():
    try:
        params = load_params(params_path='params.yaml')
        kaggle_dataset_name = params['data_ingestion']['kaggle_dataset_name']
        path_to_store_data = params['data_ingestion']['path_to_store_data']
        # kaggle_data_path = "paultimothymooney/chest-xray-pneumonia"
        download_data_from_kaggle(kaggle_dataset_name,path_to_store_data)
    except Exception as e:
        logging.error('Failed to complete the data ingestion process: %s', e)
        print(f"Error: {e}")

if __name__ == '__main__':
    main()