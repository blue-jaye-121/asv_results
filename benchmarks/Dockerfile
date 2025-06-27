FROM python:3.12

RUN pip install --no-cache-dir matplotlib netcdf4 numpy pandas pint pooch pyproj scipy traitlets xarray asv

RUN groupadd -g 3300 metpy && \
    useradd -m -u 3300 -g metpy metpy
 
USER metpy
 
WORKDIR /home/metpy
