FROM python:3.12

WORKDIR /usr/src/app
RUN pip install --no-cache-dir matplotlib netcdf4 numpy pandas pint pooch pyproj scipy traitlets xarray

COPY src/metpy .

CMD [ "python", "src/metpy" ] 