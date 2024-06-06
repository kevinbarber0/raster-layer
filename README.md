# Tree Canopy Coverage Data Pipeline

This project creates a data pipeline to build a raster file representing tree canopy coverage across the United States. The pipeline processes raw remote sensing data, calculates NDVI (Normalized Difference Vegetation Index), and generates a raster file. The final output is uploaded to an AWS S3 bucket.

## Prerequisites

- Python 3.x
- AWS CLI configured with necessary permissions
- Required Python packages:
  - rasterio
  - boto3
  - numpy
  - requests

Install the required packages:

```bash
pip install rasterio boto3 numpy requests
```

Running the Pipeline:

```bash
python main.py
```
