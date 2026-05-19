"""
ACTF - Blender 3D Export Module

3D geometry generation and export for Blender visualization.
Supports OBJ format export for exoskeleton and endoskeleton components.
"""

import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple
import json
from datetime import datetime


class BlenderGeometryExporter:
    """3D geometry exporter for Blender"""
    
    def __init__(self, output_dir: str = "./blender_exports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.vertices: List[Tuple[float, float, float]] = []
        self.faces: List[Tuple[int, int, int]] = []
        self.normals: List[Tuple[float, float, float]] = []
        self.uvs: List[Tuple[float, float]] = []
    
    def clear_geometry(self):
        """Clear all geometry data"""
        self.vertices = []
        self.faces = []
        self.normals = []
        self.uvs = []
    
    def add_cube(self, center: Tuple[float, float, float], 
                 size: Tuple[float, float, float], 
                 name: str = ""):
        """Add a cube to the geometry"""
        cx, cy, cz = center
        sx, sy, sz = size
        
        # 8 vertices of a cube
        base_vertices = [
            (cx - sx/2, cy - sy/2, cz - sz/2),  # 0
            (cx + sx/2, cy - sy/2, cz - sz/2),  # 1
            (cx + sx/2, cy + sy/2, cz - sz/2),  # 2
            (cx - sx/2, cy + sy/2, cz - sz/2),  # 3
            (cx - sx/2, cy - sy/2, cz + sz/2),  # 4
            (cx + sx/2, cy - sy/2, cz + sz/2),  # 5
            (cx + sx/2, cy + sy/2, cz + sz/2),  # 6
            (cx - sx/2, cy + sy/2, cz + sz/2),  # 7
        ]
        
        vertex_offset = len(self.vertices)
        self.vertices.extend(base_vertices)
        
        # 12 faces (triangles)
        base_faces = [
            (0, 1, 2), (0, 2, 3),  # front
            (4, 5, 6), (4, 6, 7),  # back
            (0, 1, 5), (0, 5, 4),  # bottom
            (2, 3, 7), (2, 7, 6),  # top
            (0, 3, 7), (0, 7, 4),  # left
            (1, 2, 6), (1, 6, 5),  # right
        ]
        
        self.faces.extend([tuple(v + vertex_offset for v in face) for face in base_faces])
    
    def add_sphere(self, center: Tuple[float, float, float], 
                   radius: float, 
                   segments: int = 16,
                   rings: int = 12):
        """Add a sphere to the geometry"""
        cx, cy, cz = center
        vertex_offset = len(self.vertices)
        
        # Generate vertices
        for i in range(rings + 1):
            lat = np.pi * i / rings
            for j in range(segments):
                lon = 2 * np.pi * j / segments
                
                x = cx + radius * np.sin(lat) * np.cos(lon)
                y = cy + radius * np.cos(lat)
                z = cz + radius * np.sin(lat) * np.sin(lon)
                
                self.vertices.append((x, y, z))
        
        # Generate faces
        for i in range(rings):
            for j in range(segments):
                p1 = i * segments + j
                p2 = i * segments + (j + 1) % segments
                p3 = (i + 1) * segments + (j + 1) % segments
                p4 = (i + 1) * segments + j
                
                self.faces.append((p1 + vertex_offset, p2 + vertex_offset, p3 + vertex_offset))
                self.faces.append((p1 + vertex_offset, p3 + vertex_offset, p4 + vertex_offset))
    
    def add_cylinder(self, center: Tuple[float, float, float],
                     radius: float,
                     height: float,
                     segments: int = 16,
                     axis: str = 'y'):
        """Add a cylinder to the geometry"""
        cx, cy, cz = center
        vertex_offset = len(self.vertices)
        
        if axis == 'y':
            # Vertical cylinder
            for i in range(segments):
                angle = 2 * np.pi * i / segments
                x = cx + radius * np.cos(angle)
                z = cz + radius * np.sin(angle)
                
                # Bottom vertex
                self.vertices.append((x, cy - height/2, z))
                # Top vertex
                self.vertices.append((x, cy + height/2, z))
            
            # Side faces
            for i in range(segments):
                p1 = 2 * i
                p2 = 2 * ((i + 1) % segments)
                p3 = 2 * ((i + 1) % segments) + 1
                p4 = 2 * i + 1
                
                self.faces.append((p1 + vertex_offset, p2 + vertex_offset, p3 + vertex_offset))
                self.faces.append((p1 + vertex_offset, p3 + vertex_offset, p4 + vertex_offset))
            
            # Bottom cap
            bottom_center = len(self.vertices)
            self.vertices.append((cx, cy - height/2, cz))
            for i in range(segments):
                p1 = 2 * i
                p2 = 2 * ((i + 1) % segments)
                self.faces.append((bottom_center + vertex_offset, p2 + vertex_offset, p1 + vertex_offset))
            
            # Top cap
            top_center = len(self.vertices)
            self.vertices.append((cx, cy + height/2, cz))
            for i in range(segments):
                p1 = 2 * i + 1
                p2 = 2 * ((i + 1) % segments) + 1
                self.faces.append((top_center + vertex_offset, p1 + vertex_offset, p2 + vertex_offset))
        
        elif axis == 'x':
            # Horizontal cylinder (along X axis)
            for i in range(segments):
                angle = 2 * np.pi * i / segments
                y = cy + radius * np.cos(angle)
                z = cz + radius * np.sin(angle)
                
                # Bottom vertex
                self.vertices.append((cx - height/2, y, z))
                # Top vertex
                self.vertices.append((cx + height/2, y, z))
            
            # Side faces
            for i in range(segments):
                p1 = 2 * i
                p2 = 2 * ((i + 1) % segments)
                p3 = 2 * ((i + 1) % segments) + 1
                p4 = 2 * i + 1
                
                self.faces.append((p1 + vertex_offset, p2 + vertex_offset, p3 + vertex_offset))
                self.faces.append((p1 + vertex_offset, p3 + vertex_offset, p4 + vertex_offset))
            
            # Bottom cap
            bottom_center = len(self.vertices)
            self.vertices.append((cx - height/2, cy, cz))
            for i in range(segments):
                p1 = 2 * i
                p2 = 2 * ((i + 1) % segments)
                self.faces.append((bottom_center + vertex_offset, p2 + vertex_offset, p1 + vertex_offset))
            
            # Top cap
            top_center = len(self.vertices)
            self.vertices.append((cx + height/2, cy, cz))
            for i in range(segments):
                p1 = 2 * i + 1
                p2 = 2 * ((i + 1) % segments) + 1
                self.faces.append((top_center + vertex_offset, p1 + vertex_offset, p2 + vertex_offset))
    
    def add_capsule(self, center: Tuple[float, float, float],
                    radius: float,
                    height: float,
                    segments: int = 16):
        """Add a capsule (cylinder with hemispherical ends)"""
        cx, cy, cz = center
        
        # Middle cylinder
        cylinder_height = height - 2 * radius
        if cylinder_height > 0:
            self.add_cylinder(center, radius, cylinder_height, segments, axis='y')
        
        # Top hemisphere
        top_center = (cx, cy + cylinder_height/2, cz)
        self.add_sphere(top_center, radius, segments, segments//2)
        
        # Bottom hemisphere
        bottom_center = (cx, cy - cylinder_height/2, cz)
        self.add_sphere(bottom_center, radius, segments, segments//2)
    
    def export_obj(self, filename: str, object_name: str = "ACTF_Object"):
        """Export geometry to OBJ file"""
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            # Header
            f.write(f"# ACTF 3D Model Export\n")
            f.write(f"# Generated: {datetime.now().isoformat()}\n")
            f.write(f"# Object: {object_name}\n")
            f.write(f"# Vertices: {len(self.vertices)}\n")
            f.write(f"# Faces: {len(self.faces)}\n")
            f.write("\n")
            
            # Object name
            f.write(f"o {object_name}\n")
            
            # Vertices
            for v in self.vertices:
                f.write(f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
            
            # Faces (OBJ uses 1-based indexing)
            for face in self.faces:
                f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")
        
        print(f"✓ Exported OBJ file: {filepath}")
        return filepath
    
    def export_metadata(self, filename: str, metadata: Dict):
        """Export metadata as JSON"""
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Exported metadata: {filepath}")
        return filepath


class ACTFBlenderExporter:
    """ACTF-specific Blender exporter"""
    
    def __init__(self, output_dir: str = "./blender_exports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.color_scheme = {
            "exoskeleton": (1.0, 0.42, 0.42),  # RGB for #FF6B6B
            "endoskeleton": (0.31, 0.8, 0.78),  # RGB for #4ECDC4
            "nervous": (0.58, 0.88, 0.83),  # RGB for #95E1D3
            "circulatory": (1.0, 0.42, 0.62),  # RGB for #FF6B9D
            "respiratory": (0.66, 0.9, 0.81),  # RGB for #A8E6CF
            "muscular": (1.0, 0.83, 0.71),  # RGB for #FFD3B6
            "sensory": (1.0, 0.67, 0.65),  # RGB for #FFAAA5
            "endocrine": (1.0, 0.55, 0.58),  # RGB for #FF8B94
        }
    
    def export_exoskeleton(self):
        """Export exoskeleton 3D model"""
        exporter = BlenderGeometryExporter(self.output_dir)
        
        # Head (sphere)
        exporter.add_sphere((0, 1.7, 0), 0.15, segments=24, rings=16)
        
        # Neck (cylinder)
        exporter.add_cylinder((0, 1.5, 0), 0.08, 0.15, segments=16, axis='y')
        
        # Torso (box)
        exporter.add_cube((0, 1.2, 0), (0.4, 0.5, 0.25))
        
        # Left arm
        exporter.add_cylinder((-0.3, 1.3, 0), 0.06, 0.4, segments=16, axis='x')
        exporter.add_cylinder((-0.7, 1.3, 0), 0.05, 0.35, segments=16, axis='x')
        
        # Right arm
        exporter.add_cylinder((0.3, 1.3, 0), 0.06, 0.4, segments=16, axis='x')
        exporter.add_cylinder((0.7, 1.3, 0), 0.05, 0.35, segments=16, axis='x')
        
        # Left leg
        exporter.add_cylinder((-0.12, 0.85, 0), 0.07, 0.5, segments=16, axis='y')
        exporter.add_cylinder((-0.12, 0.4, 0), 0.06, 0.45, segments=16, axis='y')
        
        # Right leg
        exporter.add_cylinder((0.12, 0.85, 0), 0.07, 0.5, segments=16, axis='y')
        exporter.add_cylinder((0.12, 0.4, 0), 0.06, 0.45, segments=16, axis='y')
        
        # Export
        obj_file = exporter.export_obj("exoskeleton.obj", "ACTF_Exoskeleton")
        
        # Metadata
        metadata = {
            "object_name": "ACTF_Exoskeleton",
            "component_type": "exoskeleton",
            "material": "Graphene Polymer LCD",
            "color": self.color_scheme["exoskeleton"],
            "parts": [
                {"name": "head", "type": "sphere", "position": [0, 1.7, 0], "radius": 0.15},
                {"name": "neck", "type": "cylinder", "position": [0, 1.5, 0], "radius": 0.08, "height": 0.15},
                {"name": "torso", "type": "cube", "position": [0, 1.2, 0], "size": [0.4, 0.5, 0.25]},
                {"name": "left_arm_upper", "type": "cylinder", "position": [-0.3, 1.3, 0], "radius": 0.06, "length": 0.4},
                {"name": "left_arm_lower", "type": "cylinder", "position": [-0.7, 1.3, 0], "radius": 0.05, "length": 0.35},
                {"name": "right_arm_upper", "type": "cylinder", "position": [0.3, 1.3, 0], "radius": 0.06, "length": 0.4},
                {"name": "right_arm_lower", "type": "cylinder", "position": [0.7, 1.3, 0], "radius": 0.05, "length": 0.35},
                {"name": "left_leg_upper", "type": "cylinder", "position": [-0.12, 0.85, 0], "radius": 0.07, "length": 0.5},
                {"name": "left_leg_lower", "type": "cylinder", "position": [-0.12, 0.4, 0], "radius": 0.06, "length": 0.45},
                {"name": "right_leg_upper", "type": "cylinder", "position": [0.12, 0.85, 0], "radius": 0.07, "length": 0.5},
                {"name": "right_leg_lower", "type": "cylinder", "position": [0.12, 0.4, 0], "radius": 0.06, "length": 0.45},
            ]
        }
        exporter.export_metadata("exoskeleton_metadata.json", metadata)
        
        return obj_file
    
    def export_endoskeleton(self):
        """Export endoskeleton 3D model"""
        exporter = BlenderGeometryExporter(self.output_dir)
        
        # Brain (sphere in head)
        exporter.add_sphere((0, 1.75, 0), 0.12, segments=24, rings=16)
        
        # Heart (sphere in chest)
        exporter.add_sphere((0.05, 1.25, 0.05), 0.08, segments=20, rings=16)
        
        # Lungs (two spheres)
        exporter.add_sphere((-0.08, 1.2, 0), 0.1, segments=20, rings=16)
        exporter.add_sphere((0.08, 1.2, 0), 0.1, segments=20, rings=16)
        
        # Spine (series of spheres)
        for i in range(10):
            y = 1.6 - i * 0.12
            exporter.add_sphere((0, y, 0), 0.03, segments=12, rings=8)
        
        # Muscle groups (simplified as capsules)
        exporter.add_capsule((-0.3, 1.3, 0), 0.04, 0.35, segments=12)
        exporter.add_capsule((0.3, 1.3, 0), 0.04, 0.35, segments=12)
        exporter.add_capsule((-0.12, 0.65, 0), 0.05, 0.4, segments=12)
        exporter.add_capsule((0.12, 0.65, 0), 0.05, 0.4, segments=12)
        
        # Export
        obj_file = exporter.export_obj("endoskeleton.obj", "ACTF_Endoskeleton")
        
        # Metadata
        metadata = {
            "object_name": "ACTF_Endoskeleton",
            "component_type": "endoskeleton",
            "material": "Biological Tissue",
            "color": self.color_scheme["endoskeleton"],
            "systems": [
                {"name": "nervous_system", "type": "sphere", "position": [0, 1.75, 0], "radius": 0.12},
                {"name": "circulatory_system", "type": "sphere", "position": [0.05, 1.25, 0.05], "radius": 0.08},
                {"name": "respiratory_system_left", "type": "sphere", "position": [-0.08, 1.2, 0], "radius": 0.1},
                {"name": "respiratory_system_right", "type": "sphere", "position": [0.08, 1.2, 0], "radius": 0.1},
                {"name": "muscular_system", "type": "capsules", "count": 4},
            ]
        }
        exporter.export_metadata("endoskeleton_metadata.json", metadata)
        
        return obj_file
    
    def export_complete_system(self):
        """Export complete ACTF system"""
        print("\n" + "="*60)
        print("Exporting ACTF System for Blender")
        print("="*60)
        
        # Export exoskeleton
        print("\n[1/2] Exporting Exoskeleton...")
        exo_file = self.export_exoskeleton()
        
        # Export endoskeleton
        print("\n[2/2] Exporting Endoskeleton...")
        endo_file = self.export_endoskeleton()
        
        print("\n" + "="*60)
        print(f"✓ Export complete!")
        print(f"  Output directory: {self.output_dir}")
        print(f"  Files created:")
        print(f"    - exoskeleton.obj")
        print(f"    - exoskeleton_metadata.json")
        print(f"    - endoskeleton.obj")
        print(f"    - endoskeleton_metadata.json")
        print("="*60)
        
        return {
            "exoskeleton": exo_file,
            "endoskeleton": endo_file
        }


# ============================================================================
# Main execution
# ============================================================================

if __name__ == "__main__":
    print("ACTF Blender Export Module")
    print("="*60)
    
    exporter = ACTFBlenderExporter()
    exporter.export_complete_system()
    
    print("\n✓ Ready for Blender import!")
    print("  Use the Blender import script to load these models.")
