from pyproj import CRS, Transformer, exceptions


def convert_crs(lasx, lasy, epsg_num_in, epsg_num_out):
    if epsg_num_in is epsg_num_out:
        return lasx, lasy

    crs_in = CRS.from_epsg(epsg_num_in)
    crs_out = CRS.from_epsg(epsg_num_out)
    transformer = Transformer.from_crs(crs_from=crs_in, crs_to=crs_out)

    nx, ny = transformer.transform(lasx, lasy)
    return nx, ny

def convert_crs_individual_values(value, epsg_num_in, epsg_num_out):
    if epsg_num_in is epsg_num_out:
        return value

    crs_in = CRS.from_epsg(epsg_num_in)
    crs_out = CRS.from_epsg(epsg_num_out)
    transformer = Transformer.from_crs(crs_from=crs_in, crs_to=crs_out)

    val = transformer.transform(value)
    return val
