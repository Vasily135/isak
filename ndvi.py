import rasterio
from rasterio import plot
import numpy

img_b3='LE07_L1TP_199026_20020830_20170214_01_T1_B3.tif'
img_b4='LE07_L1TP_199026_20020830_20170214_01_T1_B4.tif'

if __name__ == '__main__':
    band_red = rasterio.open(img_b3)
    band_nir = rasterio.open(img_b4)
    red = band_red.read(1).astype('float64')
    nir = band_nir.read(1).astype('float64')
    ndvi = numpy.where((nir + red) == 0., 0, (nir - red) / (nir + red))
    ndvi_to_write = rasterio.open('output.jpg', 'w', driver='Gtiff', width=band_red.width, height=band_red.height,
                                  count=1, crs=band_red.crs, transform=band_red.transform, dtype='float64')
    ndvi_to_write.write(ndvi, 1)
    ndvi_to_write.close()

    ndvi = rasterio.open('output.jpg')
    #plot.show(ndvi, cmap='Greys_r')
    plot.show(ndvi, cmap='RdYlGn')
