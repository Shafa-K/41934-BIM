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

# Your script goes here
import ifcopenshell

# We'll first define a dictionary that shows wall types and their corresponding prices, these are 'random' prices, ideally it'll be more accurate prices from SIGMA or likewise.
custom_wall_prices = {
    "Basic Wall:VE20-3": 1210.00,
    "Basic Wall:VE20-0": 1210.00,
    "Basic Wall:VE20-S22-0": 1210.00,
    "Basic Wall:VE20-S22-1": 1210.00,
    "Basic Wall:VE20-DS22-1": 1210.00,
    "Basic Wall:VE20-DS22-0": 1210.00,
    "Basic Wall:FS50": 1242.00,
    "Basic Wall:FS70": 1242.00,
    "Basic Wall:FS110": 1242.00,
    "Basic Wall:FS30": 1242.00,
    "Basic Wall:FSS20": 1278.00,
    "Basic Wall:VG20": 1200.00,
    "Basic Wall:VG25": 1200.00,
    "Basic Wall:VG20-1": 1200.00,
    "Basic Wall:FP100": 1278.00,
    "Basic Wall:FP150": 1278.00,
    "Basic Wall:FSP36": 1278.00,
    "Basic Wall:FP120": 1278.00,
    "Basic Wall:FSP100": 1278.00,
    "Basic Wall:FP140/200": 1050.00,
    "Basic Wall:FSG70": 1278.00,
    "Basic Wall:FP100/240": 1278.00,
    "Basic Wall:FSP42": 1278.00,
    "Basic Wall:VE20-1": 1210.00,
    "Basic Wall:FP200": 1300.00,
    "Basic Wall:FSG50": 1280.00,
    "Basic Wall:VG30": 1210.00,
    "Basic Wall:FBJ50": 1210.00,
    "Basic Wall:FBJ30-0": 1210.00,
    "Basic Wall:IH25": 4.5,
    "Basic Wall:IH30": 5.2,
    "Basic Wall:IH15": 3.8,
    "Basic Wall:IH20": 5.0,
    "Basic Wall:IH11": 3.8,
    "Basic Wall:IH14": 3.8,
    "Basic Wall:IH10": 3.8,
    "Basic Wall:VG425-2": 1310,
    "Basic Wall:VG425-1": 1310.00,
    "Basic Wall:VG35": 1310.00,
    "Basic Wall:FSG100": 1278.00,
    "Basic Wall:FSG140/200": 1278.00,
    "Basic Wall:FBJ30-1": 1278.00,
    "Basic Wall:FSG120": 1278.0,
    "Basic Wall:FSG110": 1278.00,}

# The same is done for beams, where we make a dictionary that maps beam types to their corresponding prices
custom_beam_prices = {
    "XXX_SF_Opsvejst I-profil_m. db.hylde:SB11": 180.00,
    "IPE-Beams:SB26": 150.00,
    "Rectangular and Square Hollow Sections:SB14": 200.00,
    "XXX_SF_Opsvejst I-profil_ensidig:SB03": 150.00,
    "XXX_SF_Opsvejst I-profil:SB01": 80.00,
    "H-Wide Flange Beams:SB09": 250.00,
    "XXX_SF_Opsvejst I-profil:SB02": 180.00,
    "XXX_SF_Opsvejst I-profil_ensidig m.hylde:SB15": 180.00,
    "XXX_SF_Opsvejst I-profil_m. db.hylde:SB12": 180.00,
    "XXX_SF_Opsvejst I-profil_m. db.hylde:SB05": 180.00,
    "XXX_SF_Opsvejst I-profil_m. db.hylde:SB06": 180.00,
    "H-Wide Flange Beams:SB04": 200.00,
    "H-Wide Flange Beams:SB08": 200.00,
    "Rectangular and Square Hollow Sections:SB13": 150.00,
    "XXX_SF_Opsvejst I-profil_ensidig m.hylde:SB07": 180.00,
    "XXX_SF_Opsvejst I-profil:SB16": 180.00,
    "H-Wide Flange Beams:SB30": 250.00,
    "Rectangular and Square Hollow Sections:SB40": 200.00,
    "SHS-Square Hollow Section:SB41": 200.00,
    "HEB-profil m. underflange:SB30-1": 350.00,
    "XXX_SF_Opsvejst I-profil:SB19": 180.00,
    "SHS-Square Hollow Section:SB17": 250.00,
    "H-Wide Flange Beams:SB18": 200.00,
    "XXX_SF_L-Angles:SB20": 250.00,
    "XXX_SF_U-Parallel Flange Channels:SB21": 200.00,
    "H-Wide Flange Beams:SB22": 250.00,
    "IPE-Beams:SB24": 320.00,
    "H-Wide Flange Beams:SB23": 200.00,
    "U-Parallel Flange Channels:SB25": 250.00,
    "IPE-Beams:SB27": 200.00,
    "Rectangular and Square Hollow Sections:SB10": 200.00,
    "H-Wide Flange Beams:SB28": 250.00,
    "IPE-Beams:SB29": 200.00,}

# Define a dictionary for columns
custom_column_prices = {
    "SE_Betonsøjle_Element:SE36-2": 1200.00,
    "SE_Betonsøjle_Element:SE100/36-0": 1200.00,
    "SE_Betonsøjle_Element:SE42": 1280.00,
    "SE_Betonsøjle_Element:SE36-1": 1280.00,
    "SE_Betonsøjle_Element:SE36-0": 1280.00,
    "SE_Betonsøjle_Element m. top udsparing:SE100/36-1": 1180.00,
    "SHS-Square Hollow Section-Column:SS01": 400.00,
    "Opstropning_60mm:SS04": 400.00,
    "SHS-Square Hollow Section-Column:SS02": 250.00,
    "SHS-Square Hollow Section-Column:SS03": 250.00,}

# As well as slabs 
custom_slab_prices = {
    "Floor:DS01": 1400.00,
    "Floor:DE22": 1400.00,
    "Floor:DK20-1": 1400.00,
    "Floor:DS02": 1580.00,  # Add prices for other slab types as needed
    "(12).6 Brøndfundament:BF150": 1210.00,
    "(12).6 Brøndfundament:BF100": 1210.00,
    "(12).6 Brøndfundament:BF150-1": 1210.00,
    "Floor:DK20-3": 1180.00,
    "Floor:IH45": 2000.00,
    "Floor:DK5": 1400.00,
    "Floor:DK22": 1400.00,
    "Floor:FPL30": 2000.00,
    "Floor:DK20-2": 1400.00,
    "Floor:DE18": 1210.00,
    "Floor:DK18": 1210.00,
    "Floor:DK12": 1200.00,
    "Floor:DK15": 1210.00,
    "Floor:DK20-0": 1400.00,
    "(12).6 Brøndfundament:BF60-0": 1210.00,
    "(12).6 Brøndfundament:BF60-1": 1210.00,
    "(12).6 Brøndfundament:BF60-2": 1210.00,
    "Structural Foundations 1:Structural Foundations 1": 1110.00,
    "Floor:DK16": 1210.00,
    "Floor:DK10": 1210.00,
    "Floor:DK17": 1210.00,}


# First, we'll define a function to process elements and update the total volumes, areas, and materials dictionaries
def process_elements(elements, object_type_attribute, property_set_name, total_values_dict, total_materials_dict, custom_prices):
    for element in elements:
        object_type = getattr(element, object_type_attribute)
        psets = ifcopenshell.util.element.get_psets(element)

        if object_type:
            if property_set_name in psets:
                value = psets[property_set_name].get("NetVolume") or psets[property_set_name].get("NetArea")

                if value:
                    if object_type in total_values_dict:
                        total_values_dict[object_type] += value
                    else:
                        total_values_dict[object_type] = value

                    # Retrieve and print the materials for each object type
                    materials = ifcopenshell.util.element.get_materials(element)
                    if object_type in total_materials_dict:
                        total_materials_dict[object_type].extend(materials)
                    else:
                        total_materials_dict[object_type] = materials

                    # We make it check custom price exists for this object type
                    price = custom_prices.get(object_type)
                    if price:
                        total_price = price * value  # Multiply price with volume/area to get total cost

                        # Get the material of the element
                        element_material = ifcopenshell.util.element.get_material(element)

                        if element_material:
                            # Then we create a new property set and add it to the material
                            new_material_pset = ifcopenshell.api.run(
                                "pset.add_pset", model, product=element_material, name="CustomProperties")

                            if new_material_pset:
                                # Edit the property set by providing a dictionary with the properties to define
                                ifcopenshell.api.run(
                                    "pset.edit_pset",
                                    model,
                                    pset=new_material_pset,
                                    properties={"Price": total_price},)

                                # And then we want to only print the price for each object type once
                                if object_type not in printed_object_types:
                                    print(
                                        f"Object Type: {object_type}, Total Net Value: {value}, "
                                        f"Price: {price} /m3 DKK, Total Price: {total_price} DKK, Materials: {materials}")
                                    printed_object_types.add(object_type)
                            else:
                                print(f"Error: Failed to create a new property set for {element}")
                        else:
                            print(f"Error: Element {element} has no associated material.")

# Now we create dictionaries to store materials, volumes/areas, and materials by object type
element_materials_walls = {}
element_volumes_walls = {}
total_element_materials_by_object_type_walls = {}

element_materials_beams = {}
element_volumes_beams = {}
total_element_materials_by_object_type_beams = {}

element_materials_columns = {}
element_volumes_columns = {}
total_element_materials_by_object_type_columns = {}

element_materials_slabs = {}
element_areas_slabs = {}
total_element_materials_by_object_type_slabs = {}

# To keep track of printed object types, we'll create a set
printed_object_types = set()

# We'll process walls to find the total volume and materials for each object type 
process_elements(
    model.by_type("IfcWall"),
    "ObjectType",
    "Qto_WallBaseQuantities",
    total_element_materials_by_object_type_walls,
    element_materials_walls,
    custom_wall_prices,)

# The same process for beams to find the total volume and materials for each object type
process_elements(
    model.by_type("IfcBeam"),
    "ObjectType",
    "Qto_BeamBaseQuantities",
    total_element_materials_by_object_type_beams,
    element_materials_beams,
    custom_beam_prices,)

# As well as columns 
process_elements(
    model.by_type("IfcColumn"),
    "ObjectType",
    "Qto_ColumnBaseQuantities",
    total_element_materials_by_object_type_columns,
    element_materials_columns,
    custom_column_prices,)

# We'll also process slabs, but here we'll find the total area and materials for each object type
process_elements(
    model.by_type("IfcSlab"),
    "ObjectType",
    "Qto_SlabBaseQuantities",
    total_element_materials_by_object_type_slabs,
    element_materials_slabs,
    custom_slab_prices,
)
# Now we can save the modified model to a new file in the same directory
new_model_url = model_url.parent / f"{modelname}_modified.ifc"

model.write(new_model_url)

print(f"Custom properties with prices added. Modified model saved to {new_model_url}.")