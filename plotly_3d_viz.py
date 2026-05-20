"""
ACTF - Plotly 3D Visualization Module

Interactive 3D visualization using Plotly for the ACTF system.
Generates HTML files that can be viewed in any browser.
"""

import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple
import json
from datetime import datetime


class Plotly3DVisualizer:
    """Plotly-based 3D visualizer for ACTF system"""
    
    def __init__(self, output_dir: str = "./plotly_3d"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.color_scheme = {
            "exoskeleton": "#FF6B6B",
            "endoskeleton": "#4ECDC4",
            "nervous": "#95E1D3",
            "circulatory": "#FF6B9D",
            "respiratory": "#A8E6CF",
            "muscular": "#FFD3B6",
            "sensory": "#FFAAA5",
            "endocrine": "#FF8B94",
        }
    
    def create_sphere(self, center: Tuple[float, float, float], 
                     radius: float, 
                     color: str,
                     name: str,
                     segments: int = 20):
        """Create 3D sphere mesh data"""
        cx, cy, cz = center
        
        # Generate sphere vertices
        phi = np.linspace(0, np.pi, segments)
        theta = np.linspace(0, 2 * np.pi, segments)
        phi, theta = np.meshgrid(phi, theta)
        
        x = cx + radius * np.sin(phi) * np.cos(theta)
        y = cy + radius * np.cos(phi)
        z = cz + radius * np.sin(phi) * np.sin(theta)
        
        return go.Surface(
            x=x, y=y, z=z,
            colorscale=[[0, color], [1, color]],
            showscale=False,
            name=name,
            opacity=0.9
        )
    
    def create_cylinder(self, center: Tuple[float, float, float],
                       radius: float,
                       height: float,
                       color: str,
                       name: str,
                       axis: str = 'y',
                       segments: int = 20):
        """Create 3D cylinder mesh data"""
        cx, cy, cz = center
        
        if axis == 'y':
            # Vertical cylinder
            theta = np.linspace(0, 2 * np.pi, segments)
            y_vals = np.linspace(cy - height/2, cy + height/2, segments)
            theta, y_vals = np.meshgrid(theta, y_vals)
            
            x = cx + radius * np.cos(theta)
            z = cz + radius * np.sin(theta)
            y = y_vals
            
        elif axis == 'x':
            # Horizontal cylinder
            theta = np.linspace(0, 2 * np.pi, segments)
            x_vals = np.linspace(cx - height/2, cx + height/2, segments)
            theta, x_vals = np.meshgrid(theta, x_vals)
            
            y = cy + radius * np.cos(theta)
            z = cz + radius * np.sin(theta)
            x = x_vals
        
        return go.Surface(
            x=x, y=y, z=z,
            colorscale=[[0, color], [1, color]],
            showscale=False,
            name=name,
            opacity=0.9
        )
    
    def create_box(self, center: Tuple[float, float, float],
                   size: Tuple[float, float, float],
                   color: str,
                   name: str):
        """Create 3D box mesh data"""
        cx, cy, cz = center
        sx, sy, sz = size
        
        # Create box vertices
        x = np.array([
            [cx - sx/2, cx + sx/2],
            [cx - sx/2, cx + sx/2]
        ])
        y = np.array([
            [cy - sy/2, cy - sy/2],
            [cy + sy/2, cy + sy/2]
        ])
        z = np.array([
            [cz - sz/2, cz - sz/2],
            [cz + sz/2, cz + sz/2]
        ])
        
        return go.Surface(
            x=x, y=y, z=z,
            colorscale=[[0, color], [1, color]],
            showscale=False,
            name=name,
            opacity=0.9
        )
    
    def visualize_exoskeleton_3d(self):
        """Create 3D visualization of exoskeleton"""
        fig = go.Figure()
        
        # Head (sphere)
        fig.add_trace(self.create_sphere(
            (0, 1.7, 0), 0.15, self.color_scheme["exoskeleton"], "Head"
        ))
        
        # Neck (cylinder)
        fig.add_trace(self.create_cylinder(
            (0, 1.5, 0), 0.08, 0.15, self.color_scheme["exoskeleton"], "Neck", axis='y'
        ))
        
        # Torso (box)
        fig.add_trace(self.create_box(
            (0, 1.2, 0), (0.4, 0.5, 0.25), self.color_scheme["exoskeleton"], "Torso"
        ))
        
        # Left arm
        fig.add_trace(self.create_cylinder(
            (-0.3, 1.3, 0), 0.06, 0.4, self.color_scheme["exoskeleton"], "Left Arm Upper", axis='x'
        ))
        fig.add_trace(self.create_cylinder(
            (-0.7, 1.3, 0), 0.05, 0.35, self.color_scheme["exoskeleton"], "Left Arm Lower", axis='x'
        ))
        
        # Right arm
        fig.add_trace(self.create_cylinder(
            (0.3, 1.3, 0), 0.06, 0.4, self.color_scheme["exoskeleton"], "Right Arm Upper", axis='x'
        ))
        fig.add_trace(self.create_cylinder(
            (0.7, 1.3, 0), 0.05, 0.35, self.color_scheme["exoskeleton"], "Right Arm Lower", axis='x'
        ))
        
        # Left leg
        fig.add_trace(self.create_cylinder(
            (-0.12, 0.85, 0), 0.07, 0.5, self.color_scheme["exoskeleton"], "Left Leg Upper", axis='y'
        ))
        fig.add_trace(self.create_cylinder(
            (-0.12, 0.4, 0), 0.06, 0.45, self.color_scheme["exoskeleton"], "Left Leg Lower", axis='y'
        ))
        
        # Right leg
        fig.add_trace(self.create_cylinder(
            (0.12, 0.85, 0), 0.07, 0.5, self.color_scheme["exoskeleton"], "Right Leg Upper", axis='y'
        ))
        fig.add_trace(self.create_cylinder(
            (0.12, 0.4, 0), 0.06, 0.45, self.color_scheme["exoskeleton"], "Right Leg Lower", axis='y'
        ))
        
        # Layout
        fig.update_layout(
            title="ACTF Exoskeleton - 3D Visualization",
            scene=dict(
                xaxis_title='X (m)',
                yaxis_title='Y (m)',
                zaxis_title='Z (m)',
                camera=dict(
                    eye=dict(x=2, y=2, z=2)
                )
            ),
            width=1000,
            height=800
        )
        
        # Save as HTML
        filepath = self.output_dir / "exoskeleton_3d.html"
        fig.write_html(str(filepath))
        print(f"✓ Exoskeleton 3D visualization saved: {filepath}")
        
        return filepath
    
    def visualize_endoskeleton_3d(self):
        """Create 3D visualization of endoskeleton"""
        fig = go.Figure()
        
        # Brain (sphere in head)
        fig.add_trace(self.create_sphere(
            (0, 1.75, 0), 0.12, self.color_scheme["nervous"], "Brain"
        ))
        
        # Heart (sphere in chest)
        fig.add_trace(self.create_sphere(
            (0.05, 1.25, 0.05), 0.08, self.color_scheme["circulatory"], "Heart"
        ))
        
        # Lungs (two spheres)
        fig.add_trace(self.create_sphere(
            (-0.08, 1.2, 0), 0.1, self.color_scheme["respiratory"], "Left Lung"
        ))
        fig.add_trace(self.create_sphere(
            (0.08, 1.2, 0), 0.1, self.color_scheme["respiratory"], "Right Lung"
        ))
        
        # Spine (series of spheres)
        for i in range(10):
            y = 1.6 - i * 0.12
            fig.add_trace(self.create_sphere(
                (0, y, 0), 0.03, self.color_scheme["endoskeleton"], f"Vertebra {i+1}"
            ))
        
        # Muscle groups (simplified as cylinders)
        fig.add_trace(self.create_cylinder(
            (-0.3, 1.3, 0), 0.04, 0.35, self.color_scheme["muscular"], "Left Arm Muscle", axis='x'
        ))
        fig.add_trace(self.create_cylinder(
            (0.3, 1.3, 0), 0.04, 0.35, self.color_scheme["muscular"], "Right Arm Muscle", axis='x'
        ))
        fig.add_trace(self.create_cylinder(
            (-0.12, 0.65, 0), 0.05, 0.4, self.color_scheme["muscular"], "Left Leg Muscle", axis='y'
        ))
        fig.add_trace(self.create_cylinder(
            (0.12, 0.65, 0), 0.05, 0.4, self.color_scheme["muscular"], "Right Leg Muscle", axis='y'
        ))
        
        # Layout
        fig.update_layout(
            title="ACTF Endoskeleton - 3D Visualization",
            scene=dict(
                xaxis_title='X (m)',
                yaxis_title='Y (m)',
                zaxis_title='Z (m)',
                camera=dict(
                    eye=dict(x=2, y=2, z=2)
                )
            ),
            width=1000,
            height=800
        )
        
        # Save as HTML
        filepath = self.output_dir / "endoskeleton_3d.html"
        fig.write_html(str(filepath))
        print(f"✓ Endoskeleton 3D visualization saved: {filepath}")
        
        return filepath
    
    def visualize_complete_system_3d(self):
        """Create 3D visualization of complete ACTF system"""
        fig = go.Figure()
        
        # Exoskeleton (semi-transparent)
        # Head
        fig.add_trace(self.create_sphere(
            (0, 1.7, 0), 0.16, self.color_scheme["exoskeleton"], "Exo Head"
        ))
        
        # Neck
        fig.add_trace(self.create_cylinder(
            (0, 1.5, 0), 0.09, 0.15, self.color_scheme["exoskeleton"], "Exo Neck", axis='y'
        ))
        
        # Torso
        fig.add_trace(self.create_box(
            (0, 1.2, 0), (0.42, 0.52, 0.27), self.color_scheme["exoskeleton"], "Exo Torso"
        ))
        
        # Arms
        fig.add_trace(self.create_cylinder(
            (-0.3, 1.3, 0), 0.07, 0.4, self.color_scheme["exoskeleton"], "Exo Left Arm", axis='x'
        ))
        fig.add_trace(self.create_cylinder(
            (0.3, 1.3, 0), 0.07, 0.4, self.color_scheme["exoskeleton"], "Exo Right Arm", axis='x'
        ))
        
        # Legs
        fig.add_trace(self.create_cylinder(
            (-0.12, 0.85, 0), 0.08, 0.5, self.color_scheme["exoskeleton"], "Exo Left Leg", axis='y'
        ))
        fig.add_trace(self.create_cylinder(
            (0.12, 0.85, 0), 0.08, 0.5, self.color_scheme["exoskeleton"], "Exo Right Leg", axis='y'
        ))
        
        # Endoskeleton (internal organs)
        # Brain
        fig.add_trace(self.create_sphere(
            (0, 1.75, 0), 0.12, self.color_scheme["nervous"], "Brain"
        ))
        
        # Heart
        fig.add_trace(self.create_sphere(
            (0.05, 1.25, 0.05), 0.08, self.color_scheme["circulatory"], "Heart"
        ))
        
        # Lungs
        fig.add_trace(self.create_sphere(
            (-0.08, 1.2, 0), 0.1, self.color_scheme["respiratory"], "Left Lung"
        ))
        fig.add_trace(self.create_sphere(
            (0.08, 1.2, 0), 0.1, self.color_scheme["respiratory"], "Right Lung"
        ))
        
        # Spine
        for i in range(10):
            y = 1.6 - i * 0.12
            fig.add_trace(self.create_sphere(
                (0, y, 0), 0.03, self.color_scheme["endoskeleton"], f"Vertebra {i+1}"
            ))
        
        # Layout
        fig.update_layout(
            title="ACTF Complete System - 3D Visualization",
            scene=dict(
                xaxis_title='X (m)',
                yaxis_title='Y (m)',
                zaxis_title='Z (m)',
                camera=dict(
                    eye=dict(x=2.5, y=2.5, z=2.5)
                )
            ),
            width=1200,
            height=900
        )
        
        # Save as HTML
        filepath = self.output_dir / "complete_system_3d.html"
        fig.write_html(str(filepath))
        print(f"✓ Complete system 3D visualization saved: {filepath}")
        
        return filepath
    
    def generate_all_3d_visualizations(self):
        """Generate all 3D visualizations"""
        print("\n" + "="*60)
        print("Generating Plotly 3D Visualizations")
        print("="*60)
        
        # Exoskeleton
        print("\n[1/3] Generating exoskeleton 3D visualization...")
        self.visualize_exoskeleton_3d()
        
        # Endoskeleton
        print("\n[2/3] Generating endoskeleton 3D visualization...")
        self.visualize_endoskeleton_3d()
        
        # Complete system
        print("\n[3/3] Generating complete system 3D visualization...")
        self.visualize_complete_system_3d()
        
        print("\n" + "="*60)
        print(f"✓ All 3D visualizations saved to: {self.output_dir}")
        print("="*60)
        print("\nTo view the visualizations:")
        print("1. Open the HTML files in your web browser")
        print("2. You can rotate, zoom, and pan the 3D models")
        print("3. Hover over parts to see their names")
        print("="*60)


# ============================================================================
# Main execution
# ============================================================================

if __name__ == "__main__":
    print("ACTF Plotly 3D Visualization Module")
    print("="*60)
    
    visualizer = Plotly3DVisualizer()
    visualizer.generate_all_3d_visualizations()
    
    print("\n✓ 3D visualizations ready!")
    print("  Open the HTML files in your browser to view them.")
