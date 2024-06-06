import boto3
import rasterio
import numpy as np
import requests
from rasterio.transform import from_origin

# AWS S3 setup
s3_client = boto3.client('s3')
bucket_name = 'your-bucket-name'

# NASA Earthdata API configuration
nasa_api_url = 'https://earthdata.nasa.gov/api-endpoint'
nasa_api_key = 'YOUR_NASA_API_KEY'
raw_data_path = '/tmp/raw_data.tif'
preprocessed_data_path = '/tmp/preprocessed_data.tif'
ndvi_path = '/tmp/ndvi.tif'

# Function to download data
def download_nasa_data(api_url, save_path, api_key):
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    response = requests.get(api_url, headers=headers)
    with open(save_path, 'wb') as file:
        file.write(response.content)
    print("Data downloaded.")

# Function to preprocess data
def preprocess_data(input_path, output_path):
    with rasterio.open(input_path) as src:
        data = src.read()
        # Example preprocessing: normalize data
        data = (data - np.min(data)) / (np.max(data) - np.min(data))
        with rasterio.open(output_path, 'w', **src.meta) as dst:
            dst.write(data)
    print("Data preprocessed.")

# Function to calculate NDVI
def calculate_ndvi(nir_band, red_band):
    ndvi = (nir_band - red_band) / (nir_band + red_band)
    return ndvi

# Function to create a raster file
def create_raster(data, save_path, transform, crs):
    with rasterio.open(
        save_path, 'w', driver='GTiff', height=data.shape[0], width=data.shape[1],
        count=1, dtype=data.dtype, crs=crs, transform=transform
    ) as dst:
        dst.write(data, 1)
    print("NDVI raster created.")

# Main pipeline function
def run_pipeline():
    # Step 1: Download data from NASA
    download_nasa_data(nasa_api_url, raw_data_path, nasa_api_key)

    # Step 2: Preprocess data
    preprocess_data(raw_data_path, preprocessed_data_path)

    # Step 3: Calculate NDVI
    with rasterio.open(preprocessed_data_path) as src:
        red_band = src.read(1)  # assuming band 1 is red
        nir_band = src.read(2)  # assuming band 2 is NIR
        ndvi = calculate_ndvi(nir_band, red_band)

    # Step 4: Create NDVI raster file
    transform = from_origin(-124.7844079, 24.396308, 10, 10)
    crs = 'EPSG:4326'
    create_raster(ndvi, ndvi_path, transform, crs)

    # Step 5: Upload to AWS S3
    s3_client.upload_file(ndvi_path, bucket_name, 'ndvi.tif')
    print("Raster file uploaded to S3.")

if __name__ == '__main__':
    run_pipeline()
