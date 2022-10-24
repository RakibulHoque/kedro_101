# kedro-101
Download Geo [Data](https://gadm.org/download_country.html)
## Installation
- Install [GDAL](https://opensourceoptions.com/blog/how-to-install-gdal-for-python-with-pip-on-windows/)
```
pip install extra_geo_packages\GDAL-3.4.3-cp39-cp39-win_amd64.whl
```
- Install [fiona](https://stackoverflow.com/questions/50876702/cant-install-fiona-on-windows)
```
pip install extra_geo_packages\Fiona-1.8.21-cp39-cp39-win_amd64.whl
```
- Install GeoPandas: 
```
pip install geopandas
```

## How to Run
### 00
cd _kedro && kedro run