
import hashlib
from pathlib import Path
import geopandas as gpd
from shapely.geometry.point import Point

from app.model.functions import get_id


def id_to_gid(_dict,root_id):
    gid = get_id(f"{root_id}{_dict.pop('id')}")
    _dict['properties']['__pgrass_gid'] = gid
    return {'_id':gid, **_dict}



def md5_for_file(f, block_size=2**20):
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()

def is_point(geometry):
    return isinstance(geometry, Point)


def read_kml(file):
    import fiona
    gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
    return gpd.read_file(file, driver='KML')
    
def read_gpd(file):
    return gpd.read_file(file) 



def read_file(file):
    match Path(file.filename).suffix.capitalize():
        case '.kml':
            gdf = read_kml(file.file)
        case  _:
            gdf = read_gpd(file.file) 
    return gdf