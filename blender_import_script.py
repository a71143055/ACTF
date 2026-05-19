"""
ACTF Blender Import Script

This script should be run in Blender's Scripting tab to import
the exported ACTF 3D models and set up the scene.

Instructions:
1. Open Blender
2. Go to the Scripting workspace
3. Open this script (File > Open)
4. Update the import_path variable to point to your blender_exports folder
5. Click "Run Script" button

Requirements:
- Blender 3.0 or later
"""

import bpy
import os
import json
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

# Update this path to point to your blender_exports folder
# Use forward slashes or double backslashes for Windows paths
import_path = r"c:\Users\USER\OneDrive\바탕 화면\ACTF\blender_exports"

# Color scheme (RGB values, 0-1 range)
COLOR_SCHEME = {
    "exoskeleton": (1.0, 0.42, 0.42, 1.0),  # #FF6B6B
    "endoskeleton": (0.31, 0.8, 0.78, 1.0),  # #4ECDC4
    "nervous": (0.58, 0.88, 0.83, 1.0),  # #95E1D3
    "circulatory": (1.0, 0.42, 0.62, 1.0),  # #FF6B9D
    "respiratory": (0.66, 0.9, 0.81, 1.0),  # #A8E6CF
    "muscular": (1.0, 0.83, 0.71, 1.0),  # #FFD3B6
    "sensory": (1.0, 0.67, 0.65, 1.0),  # #FFAAA5
    "endocrine": (1.0, 0.55, 0.58, 1.0),  # #FF8B94
}


# ============================================================================
# SCENE SETUP FUNCTIONS
# ============================================================================

def clear_scene():
    """Clear the current scene (remove default cube)"""
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()
    
    # Remove lights and camera if they exist
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
        if obj.type in ['LIGHT', 'CAMERA']:
            obj.select_set(True)
    bpy.ops.object.delete()


def setup_lighting():
    """Set up professional lighting for the scene"""
    # Clear existing lights
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
        if obj.type == 'LIGHT':
            obj.select_set(True)
    bpy.ops.object.delete()
    
    # Key light (main light)
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
    key_light = bpy.context.active_object
    key_light.name = "Key_Light"
    key_light.data.energy = 3.0
    key_light.data.shadow_soft_size = 0.5
    
    # Fill light (softer light from opposite side)
    bpy.ops.object.light_add(type='SUN', location=(-5, 3, 8))
    fill_light = bpy.context.active_object
    fill_light.name = "Fill_Light"
    fill_light.data.energy = 1.5
    fill_light.data.shadow_soft_size = 0.3
    
    # Rim light (back light for edge definition)
    bpy.ops.object.light_add(type='SUN', location=(0, -5, 5))
    rim_light = bpy.context.active_object
    rim_light.name = "Rim_Light"
    rim_light.data.energy = 1.0
    rim_light.data.shadow_soft_size = 0.2
    
    # Ambient light (soft overall illumination)
    bpy.ops.object.light_add(type='AREA', location=(0, 0, 5))
    ambient_light = bpy.context.active_object
    ambient_light.name = "Ambient_Light"
    ambient_light.data.energy = 0.5
    ambient_light.data.size = 10
    ambient_light.rotation_euler = (0, 0, 0)


def setup_camera():
    """Set up camera for optimal viewing"""
    bpy.ops.object.camera_add(location=(3, -5, 2.5))
    camera = bpy.context.active_object
    camera.name = "ACTF_Camera"
    
    # Point camera at the origin
    camera.rotation_euler = (1.2, 0, 0.5)
    
    # Set as active camera
    bpy.context.scene.camera = camera
    
    # Adjust camera settings
    camera.data.lens = 50  # 50mm lens
    camera.data.sensor_fit = 'HORIZONTAL'


def setup_material(name, color):
    """Create a material with the given color"""
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    
    # Get the material nodes
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    
    # Clear default nodes
    nodes.clear()
    
    # Create nodes
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    output_node.location = (400, 0)
    
    principled_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled_node.location = (0, 0)
    
    # Set color
    principled_node.inputs['Base Color'].default_value = color
    principled_node.inputs['Metallic'].default_value = 0.3
    principled_node.inputs['Roughness'].default_value = 0.4
    
    # Link nodes
    links.new(principled_node.outputs['BSDF'], output_node.inputs['Surface'])
    
    return material


def import_obj_file(filepath, object_name, material_name):
    """Import an OBJ file and apply material"""
    # Import the OBJ file
    bpy.ops.import_scene.obj(filepath=filepath)
    
    # Get the imported object
    imported_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
    
    if imported_objects:
        obj = imported_objects[0]
        obj.name = object_name
        
        # Create and apply material
        material = setup_material(material_name, COLOR_SCHEME.get(material_name, (0.8, 0.8, 0.8, 1.0)))
        
        # Assign material to object
        if obj.data.materials:
            obj.data.materials[0] = material
        else:
            obj.data.materials.append(material)
        
        return obj
    return None


def setup_ground_plane():
    """Add a ground plane for reference"""
    bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, -0.1))
    ground = bpy.context.active_object
    ground.name = "Ground_Plane"
    
    # Create ground material
    material = setup_material("Ground_Material", (0.2, 0.2, 0.2, 1.0))
    material.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.8
    
    if ground.data.materials:
        ground.data.materials[0] = material
    else:
        ground.data.materials.append(material)


def setup_world_environment():
    """Set up world environment for better rendering"""
    world = bpy.context.scene.world
    if world is None:
        world = bpy.data.worlds.new("ACTF_World")
        bpy.context.scene.world = world
    
    world.use_nodes = True
    nodes = world.node_tree.nodes
    links = world.node_tree.links
    
    # Clear default nodes
    nodes.clear()
    
    # Create background node
    bg_node = nodes.new(type='ShaderNodeBackground')
    bg_node.location = (0, 0)
    bg_node.inputs['Color'].default_value = (0.1, 0.1, 0.15, 1.0)
    bg_node.inputs['Strength'].default_value = 1.0
    
    # Create output node
    output_node = nodes.new(type='ShaderNodeOutputWorld')
    output_node.location = (400, 0)
    
    # Link nodes
    links.new(bg_node.outputs['Background'], output_node.inputs['Surface'])


def setup_render_settings():
    """Configure render settings for quality"""
    # Use Eevee for fast preview or Cycles for quality
    bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
    
    # Set resolution
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    
    # Enable shadows
    bpy.context.scene.eevee.use_shadow_cube_map = True
    bpy.context.scene.eevee.shadow_cube_size = 2048
    
    # Enable ambient occlusion
    bpy.context.scene.eevee.use_gtao = True
    bpy.context.scene.eevee.gtao_distance = 0.5
    bpy.context.scene.eevee.gtao_factor = 1.0


# ============================================================================
# MAIN IMPORT FUNCTION
# ============================================================================

def import_actf_models():
    """Import all ACTF models"""
    # Check if import path exists
    if not os.path.exists(import_path):
        print(f"Error: Import path does not exist: {import_path}")
        print("Please update the import_path variable in this script.")
        return False
    
    print("="*60)
    print("Importing ACTF Models into Blender")
    print("="*60)
    
    # Clear scene
    print("\n[1/7] Clearing scene...")
    clear_scene()
    
    # Set up lighting
    print("[2/7] Setting up lighting...")
    setup_lighting()
    
    # Set up camera
    print("[3/7] Setting up camera...")
    setup_camera()
    
    # Set up world environment
    print("[4/7] Setting up environment...")
    setup_world_environment()
    
    # Set up ground plane
    print("[5/7] Setting up ground plane...")
    setup_ground_plane()
    
    # Import exoskeleton
    exo_path = os.path.join(import_path, "exoskeleton.obj")
    if os.path.exists(exo_path):
        print("[6/7] Importing exoskeleton...")
        import_obj_file(exo_path, "ACTF_Exoskeleton", "exoskeleton")
    else:
        print(f"Warning: Exoskeleton file not found: {exo_path}")
    
    # Import endoskeleton
    endo_path = os.path.join(import_path, "endoskeleton.obj")
    if os.path.exists(endo_path):
        print("[7/7] Importing endoskeleton...")
        import_obj_file(endo_path, "ACTF_Endoskeleton", "endoskeleton")
    else:
        print(f"Warning: Endoskeleton file not found: {endo_path}")
    
    # Configure render settings
    print("\n[Configuring render settings...]")
    setup_render_settings()
    
    print("\n" + "="*60)
    print("✓ Import complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Press 'Z' to toggle render mode")
    print("2. Use 'G' to grab/move objects")
    print("3. Use 'R' to rotate objects")
    print("4. Use 'S' to scale objects")
    print("5. Press 'F12' to render the scene")
    print("="*60)
    
    return True


# ============================================================================
# EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Only run if in Blender
    try:
        import_actf_models()
    except NameError:
        print("This script must be run inside Blender.")
        print("Open Blender, go to Scripting workspace, and run this script.")
