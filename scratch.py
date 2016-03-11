from create_ponds import *
from arcpy import env
import posixpath as os
import arcpy

env.overWriteOutput = True

root_dir = ('E:/_data/welikia/beaver_ponds')
watershed_dir = os.join(root_dir, 'WATERSHED_BURNED_STREAMS')
flow_accumulation = os.join(watershed_dir, 'flow_accumulation', 'flow_accumulation.shp')

# num_points = 300
# minimum_distance = 800
# out_path = os.join(watershed_dir, 'outputs')
# out_name = os.join(watershed_dir, 'outputs', 'pond_points', 'pond_points.shp')
#
# arcpy.CreateRandomPoints_management(out_path=out_path,
#                                     out_name=out_name,
#                                     constraining_feature_class=flow_accumulation,
#                                     number_of_points_or_field=num_points)

LANDSCAPE_POND_FREQ = 200

env.workspace = os.join(watershed_dir, 'outputs')

print env.workspace

age_raster = arcpy.Raster(os.join(root_dir, '_test', 'pond_age_01.tif'))

succession_out = os.join(root_dir, '_test', 'succession')
#
# arcpy.BuildRasterAttributeTable_management("pond_count", "Overwrite")
#
# import random
pond_count = os.join(root_dir, '_test', 'pond_count.tif')
#
# start_age = calculate_start_age(pond_count)
#
# start_age.save(os.join(root_dir,'_test', 'start_age.tif'))

# age = arcpy.sa.Raster(os.join(root_dir,'_test', 'start_age.tif'))
#
# for year in range(21):
#     landcover = succession(age)
#     age += 1
#     landcover.save(os.join(succession_out, 'landcover_%s.tif' % year))

# Inputs
flow_direction = os.join(watershed_dir, 'flow_direction', 'flow_direction.tif')

DEM = os.join(watershed_dir, 'fill', 'UPLAND_DEM_BURNED_STREAMS_5m_FILL.tif')

landcover = os.join(root_dir, '_test', 'landcover.tif')

suitable_streams = os.join(root_dir, '_test', 'suitability_surface.tif')

suitability_points = os.join(root_dir, '_test', 'suitability_points.shp')

pond_points = os.join(root_dir, '_test', 'outputs', 'pond_points.shp')

temp_point = os.join(root_dir, '_test', 'temp_point.shp')

output_dir = os.join(root_dir, '_test', 'outputs')

start_age = os.join(root_dir, '_test', 'start_age.tif')

sum_ponds_binary = os.join(root_dir, '_test', 'sum_pond_binary.tif')

# start

# coordinate_list = dam_points_coordinates(pond_points)
# print coordinate_list
# active_ponds = count_ponds(pond_count)
#
# carrying_capacity = 150

# if active_ponds < carrying_capacity:
#
#     print 'number of active ponds below carrying capacity, creating new ponds'
#
#     num_new_ponds = carrying_capacity - active_ponds
#
#     calculate_suitability(suitable_streams, landcover, suitability_points)
#
#     assign_pond_locations(constraint=suitability_points,
#                           num_points=num_new_ponds
#                           )
#
#     coordinate_list = dam_points_coordinates(pond_points)
#
#     for p, i in zip(coordinate_list, range(len(coordinate_list))):
#
#         print 'calculating pond %s' % i
#
#         if arcpy.Exists(temp_point):
#             arcpy.Delete_management(temp_point)
#
#         pond = create_pond(dem=DEM,
#                            flow_direction=flow_direction,
#                            coordinates=p,
#                            temp_point=temp_point)
#
#         out_path = os.join(output_dir, ('pond_%s.tif' % i))
#         pond.save(out_path)
#
#     # sum ponds into single raster
#     env.workspace = os.join(output_dir)
#
#     print env.workspace
#
#     l = arcpy.ListRasters()
#
#     sum = arcpy.Raster(l[0])
#
#     for r in l[1:]:
#         print r
#         sum += arcpy.Raster(r)
#
#     sum.save('sum_ponds.tif')

# start_age = arcpy.Raster(start_age)
# sum_ponds_binary = arcpy.Raster(sum_ponds_binary)
#
# x = update_time_since_disturbance(start_age, sum_ponds_binary)
#
# x.save(os.join(root_dir, '_test', 'time_since_disturbance.tif'))
#
# import numpy
# random.choice
# numpy.abs()
# output_dir = os.join(root_dir, '_test', 'outputs')
# ponds = arcpy.Raster(os.join(output_dir, 'ponds.tif'))
#
# pond_count, region_group = count_ponds(ponds)
#
# time_since_disturbance = initial_time_since_disturbance(region_group)
#
# time_since_disturbance.save(os.join(output_dir, 'time_since_last_disturbance.tif'))

x = 'adslfj'

if type(x) == str:
    print "x is a string"