from create_ponds import *
from arcpy import env
import posixpath as os

env.overWriteOutput = True

# PATHS
root_dir = 'E:/_data/welikia/beaver_ponds'
watershed_dir = os.join(root_dir, 'WATERSHED_BURNED_STREAMS')
flow_direction = os.join(watershed_dir, 'flow_direction', 'flow_direction.tif')
DEM = os.join(watershed_dir, 'fill', 'UPLAND_DEM_BURNED_STREAMS_5m_FILL.tif' )
pour_points = os.join(root_dir, 'pour_points_01.shp')
output_dir = os.join(watershed_dir, 'outputs')

# create coordinate list from pour points feature
coordinate_list = dam_points_coordinates(pour_points)

# iterate through points and create ponds
for p, i in zip(coordinate_list, range(len(coordinate_list))):
    print 'calculating pond %s' % i
    temp_point = os.join(output_dir, 'temp_point.shp')

    if arcpy.Exists(temp_point):
        arcpy.Delete_management(temp_point)

    pond = create_pond(dem=DEM,
                       flow_direction=flow_direction,
                       coordinates=p,
                       temp_point=temp_point)

    out_path = os.join(output_dir, ('pond_%s.tif' % i))
    pond.save(out_path)

# sum ponds into single raster
env.workspace = os.join(output_dir)

print env.workspace

l = arcpy.ListRasters()

sum = arcpy.Raster(l[0])

for r in l[1:]:
    print r
    sum += arcpy.Raster(r)

sum.save('sum_ponds.tif')