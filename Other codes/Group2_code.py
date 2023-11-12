from pathlib import Path
import ifcopenshell

modelname = "LLYN_STRU"

try:
    dir_path = Path(__file__).parent
    model_url = Path.joinpath(dir_path, 'model', modelname).with_suffix('.ifc')
    model = ifcopenshell.open(model_url)
except OSError:
    try:
        import bpy
        model_url = Path.joinpath(Path(bpy.context.space_data.text.filepath).parent, 'model', modelname).with_suffix('.ifc')
        model = ifcopenshell.open(model_url)
    except OSError:
        print(f"ERROR: please check your model folder : {model_url} does not exist")

# Our script for finding the dimensions of structural elements in the building, to use them to calculate the cost:

import ifcopenshell.util.element

# First we'll define a function to process elements and update the total volumes and areas dictionaries
def process_elements(elements, object_type_attribute, property_set_name, total_volumes_dict):
    for element in elements:
        object_type = getattr(element, object_type_attribute)
        psets = ifcopenshell.util.element.get_psets(element)

        if object_type:
            if property_set_name in psets:
                net_volume = psets[property_set_name].get("NetVolume")

                if net_volume:
                    volume_value = net_volume

                    if object_type in total_volumes_dict:
                        total_volumes_dict[object_type] += volume_value
                    else:
                        total_volumes_dict[object_type] = volume_value
            

# Now we can retrieve information for walls, by first creating dictionaries to store the volumes:
walls = model.by_type("IfcWall")
wall_volumes = {}
total_wall_volumes_by_object_type = {}

# Now we will go through each wall to find its volume.
for wall in walls:
    psets = ifcopenshell.util.element.get_psets(wall)
    
    if "Qto_WallBaseQuantities" in psets:
        net_volume = psets["Qto_WallBaseQuantities"].get("NetVolume")
        
        if net_volume:
            wall_type = wall.Name
           
            if wall_type in wall_volumes:
                wall_volumes[wall_type] += net_volume
            else:
                wall_volumes[wall_type] = net_volume


# We find the volumes for each wall type
for wall_type, volume in wall_volumes.items():
    print(f"Wall Type: {wall_type}, Net Volume: {volume} cubic meters")
    
# Now we will process walls to find the total volume for each wall type:
process_elements(walls, "ObjectType", "Qto_WallBaseQuantities", total_wall_volumes_by_object_type)

# And print the combined net volume for each wall type
print("Total Net Volumes by Object Type for Walls:")
for object_type, total_volume in total_wall_volumes_by_object_type.items():
    print(f"Object Type: {object_type}, Total Net Volume: {total_volume} cubic meters")


# Now the same for columns, first Retrieve information for columns by creating dicts:
columns = model.by_type("IfcColumn")
column_volumes = {}
total_column_volumes_by_object_type = {}

# going through each column to find its volume.
for column in columns:
    psets = ifcopenshell.util.element.get_psets(column)
    
    if "Qto_ColumnBaseQuantities" in psets:
        net_volume = psets["Qto_ColumnBaseQuantities"].get("NetVolume")
        
        if net_volume:
            column_type = column.Name
            
            if column_type in column_volumes:
                column_volumes[column_type] += net_volume
            else:
                column_volumes[column_type] = net_volume

# The net volumes for each column type
print("Column Volumes by Type:")
for column_type, volume in column_volumes.items():
    print(f"Column Type: {column_type}, Net Volume: {volume} cubic meters")

# Processing the columns
process_elements(columns, "ObjectType", "Qto_ColumnBaseQuantities", total_column_volumes_by_object_type)

# the combined net volume for the columns types.
print("Total Net Volumes by Object Type for Columns:")
for object_type, total_volume in total_column_volumes_by_object_type.items():
    print(f"Object Type: {object_type}, Total Net Volume: {total_volume} cubic meters")

# Again retrieving information

beams = model.by_type("IfcBeam")
beam_volumes = {}
total_beam_volumes_by_object_type = {}

# As well as finding the volume for beams.
for beam in beams:
    psets = ifcopenshell.util.element.get_psets(beam)
    
    if "Qto_BeamBaseQuantities" in psets:
        net_volume = psets["Qto_BeamBaseQuantities"].get("NetVolume")
        
        if net_volume:
            beam_type = beam.Name
            
            if beam_type in beam_volumes:
                beam_volumes[beam_type] += net_volume
            else:
                beam_volumes[beam_type] = net_volume

# the net volumes for each beam type
print("Beam Volumes by Type:")
for beam_type, volume in beam_volumes.items():
    print(f"Beam Type: {beam_type}, Net Volume: {volume} cubic meters")

# Process beams
process_elements(beams, "ObjectType", "Qto_BeamBaseQuantities", total_beam_volumes_by_object_type)

# the total net volume for all beams types
print("Total Net Volumes by Object Type for Beams:")
for object_type, total_volume in total_beam_volumes_by_object_type.items():
    print(f"Object Type: {object_type}, Total Net Volume: {total_volume} cubic meters")


# For the slab we'll do the same but instead of net volume we'll find the net area:
slabs = model.by_type("IfcSlab")
slab_areas = {}
total_slab_areas_by_object_type = {}

#The function for net area:

def process_elements(elements, object_type_attribute, property_set_name, total_areas_dict):
    for element in elements:
        object_type = getattr(element, object_type_attribute)
        psets = ifcopenshell.util.element.get_psets(element)

        if object_type:
            if property_set_name in psets:
                net_area = psets[property_set_name].get("NetArea")

                if net_area:
                    area_value = net_area

                    if object_type in total_areas_dict:
                        total_areas_dict[object_type] += area_value
                    else:
                        total_areas_dict[object_type] = area_value
                        
# Let's do the same for slabs.
for slab in slabs:
    psets = ifcopenshell.util.element.get_psets(slab)
    
    if "Qto_SlabBaseQuantities" in psets:
        net_area = psets["Qto_SlabBaseQuantities"].get("NetArea")
        
        if net_area:
            slab_type = slab.Name
            
            if slab_type in slab_areas:
                slab_areas[slab_type] += net_area
            else:
                slab_areas[slab_type] = net_area

# Find the net areas for each slab type
print("Slab Net Areas by Type:")
for slab_type, area in slab_areas.items():
    print(f"Slab Type: {slab_type}, Net Area: {area} square meters")

# The process for slabs
process_elements(slabs, "ObjectType", "Qto_SlabBaseQuantities", total_slab_areas_by_object_type)

# As well as the combined net area for all slabs
print("Total Net Areas by Object Type for Slabs:")
for object_type, total_area in total_slab_areas_by_object_type.items():
    print(f"Object Type: {object_type}, Total Net Area: {total_area} square meters")
