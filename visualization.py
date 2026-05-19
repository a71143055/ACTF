"""
ACTF - 시각화 모듈

시스템의 상태, 구조, 성능 지표를 시각적으로 표현합니다.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, FancyArrowPatch
import numpy as np
from datetime import datetime
import json
from typing import Dict, List, Tuple
import io
from pathlib import Path

# 한글 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False


class ACTFVisualizer:
    """ACTF 시스템 시각화 클래스"""
    
    def __init__(self, output_dir: str = "."):
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
            "success": "#2ecc71",
            "warning": "#f39c12",
            "error": "#e74c3c"
        }
    
    def visualize_system_architecture(self):
        """전체 시스템 아키텍처 시각화"""
        fig, ax = plt.subplots(1, 1, figsize=(14, 10))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # 제목
        ax.text(5, 9.5, 'ACTF System Architecture', 
                fontsize=20, fontweight='bold', ha='center')
        
        # 외골격 시스템
        exo_box = FancyBboxPatch((0.5, 5.5), 4, 2.5, 
                                 boxstyle="round,pad=0.1", 
                                 edgecolor='black', 
                                 facecolor=self.color_scheme["exoskeleton"],
                                 alpha=0.7, linewidth=2)
        ax.add_patch(exo_box)
        ax.text(2.5, 7.5, 'Exoskeleton System', fontsize=12, fontweight='bold', ha='center')
        ax.text(2.5, 7, '• Graphene Polymer LCD', fontsize=9, ha='center')
        ax.text(2.5, 6.6, '• 12 Joints', fontsize=9, ha='center')
        ax.text(2.5, 6.2, '• 6 Body Parts', fontsize=9, ha='center')
        ax.text(2.5, 5.8, '• Carbon Nanotube Coating', fontsize=9, ha='center')
        
        # 내골격 시스템
        endo_box = FancyBboxPatch((5.5, 5.5), 4, 2.5,
                                 boxstyle="round,pad=0.1",
                                 edgecolor='black',
                                 facecolor=self.color_scheme["endoskeleton"],
                                 alpha=0.7, linewidth=2)
        ax.add_patch(endo_box)
        ax.text(7.5, 7.5, 'Endoskeleton System', fontsize=12, fontweight='bold', ha='center')
        ax.text(7.5, 7, '• Nervous System', fontsize=9, ha='center')
        ax.text(7.5, 6.6, '• Circulatory System', fontsize=9, ha='center')
        ax.text(7.5, 6.2, '• Muscular System', fontsize=9, ha='center')
        ax.text(7.5, 5.8, '• 6 Biological Systems', fontsize=9, ha='center')
        
        # 중앙 제어부
        brain_circle = Circle((5, 4), 0.8, color='#FFD700', alpha=0.8, edgecolor='black', linewidth=2)
        ax.add_patch(brain_circle)
        ax.text(5, 4, 'Brain\nControl', fontsize=10, fontweight='bold', ha='center', va='center')
        
        # 화살표
        arrow1 = FancyArrowPatch((2.5, 5.5), (4.5, 4.8),
                                arrowstyle='->', mutation_scale=20, linewidth=2, color='black')
        arrow2 = FancyArrowPatch((7.5, 5.5), (5.5, 4.8),
                                arrowstyle='->', mutation_scale=20, linewidth=2, color='black')
        ax.add_patch(arrow1)
        ax.add_patch(arrow2)
        
        # 신경 인터페이스
        neural_box = FancyBboxPatch((2, 2), 6, 1.2,
                                    boxstyle="round,pad=0.1",
                                    edgecolor='black',
                                    facecolor='#E8DAEF',
                                    alpha=0.7, linewidth=2)
        ax.add_patch(neural_box)
        ax.text(5, 2.9, 'Brain-Computer Interface (BCI)', fontsize=11, fontweight='bold', ha='center')
        ax.text(5, 2.4, 'Motor Commands | Sensory Inputs | Cognitive Load', fontsize=9, ha='center')
        
        arrow3 = FancyArrowPatch((5, 3.2), (5, 3.2),
                                arrowstyle='->', mutation_scale=20, linewidth=2, color='black')
        ax.add_patch(arrow3)
        
        # 줄기세포 배양 시스템
        stem_box = FancyBboxPatch((2, 0.3), 6, 1.2,
                                  boxstyle="round,pad=0.1",
                                  edgecolor='black',
                                  facecolor='#F5D76E',
                                  alpha=0.7, linewidth=2)
        ax.add_patch(stem_box)
        ax.text(5, 1.2, 'Stem Cell Cultivation System', fontsize=11, fontweight='bold', ha='center')
        ax.text(5, 0.7, 'Bioreactors | Cell Growth | Differentiation | Harvesting', fontsize=9, ha='center')
        
        plt.tight_layout()
        filepath = self.output_dir / "system_architecture.png"
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"✓ System architecture visualization saved: {filepath}")
        plt.close()
    
    def visualize_exoskeleton_structure(self):
        """외골격 구조 시각화"""
        fig, ax = plt.subplots(1, 1, figsize=(12, 14))
        ax.set_xlim(-3, 3)
        ax.set_ylim(-7, 7)
        ax.axis('off')
        
        # 제목
        ax.text(0, 6.5, 'Exoskeleton Structure', 
                fontsize=18, fontweight='bold', ha='center')
        
        # 머리
        head = Circle((0, 5), 0.6, color=self.color_scheme["exoskeleton"], 
                      alpha=0.8, edgecolor='black', linewidth=2)
        ax.add_patch(head)
        ax.text(0, 5, 'HEAD', fontsize=9, ha='center', va='center', fontweight='bold')
        
        # 몸통
        torso = Rectangle((-0.4, 3.5), 0.8, 1.2, 
                         color=self.color_scheme["exoskeleton"],
                         alpha=0.8, edgecolor='black', linewidth=2)
        ax.add_patch(torso)
        ax.text(0, 4.1, 'TORSO', fontsize=9, ha='center', va='center', fontweight='bold')
        
        # 왼쪽 팔
        left_arm = Rectangle((-1.5, 3.7), 1, 0.4,
                            color=self.color_scheme["exoskeleton"],
                            alpha=0.8, edgecolor='black', linewidth=2)
        ax.add_patch(left_arm)
        ax.text(-1, 3.9, 'L-ARM', fontsize=8, ha='center', va='center', fontweight='bold')
        
        # 오른쪽 팔
        right_arm = Rectangle((0.5, 3.7), 1, 0.4,
                             color=self.color_scheme["exoskeleton"],
                             alpha=0.8, edgecolor='black', linewidth=2)
        ax.add_patch(right_arm)
        ax.text(1, 3.9, 'R-ARM', fontsize=8, ha='center', va='center', fontweight='bold')
        
        # 왼쪽 다리
        left_leg = Rectangle((-0.3, 1.5), 0.25, 2,
                            color=self.color_scheme["exoskeleton"],
                            alpha=0.8, edgecolor='black', linewidth=2)
        ax.add_patch(left_leg)
        ax.text(-0.18, 2.5, 'L-LEG', fontsize=8, ha='center', fontweight='bold')
        
        # 오른쪽 다리
        right_leg = Rectangle((0.05, 1.5), 0.25, 2,
                             color=self.color_scheme["exoskeleton"],
                             alpha=0.8, edgecolor='black', linewidth=2)
        ax.add_patch(right_leg)
        ax.text(0.18, 2.5, 'R-LEG', fontsize=8, ha='center', fontweight='bold')
        
        # 주요 사양
        specs_text = """
        Materials:
        • Graphene Polymer LCD (Core)
        • Carbon Nanotube (Reinforcement)
        
        Specifications:
        • Total Joints: 12
        • Tensile Strength: 135-150 GPa
        • Thermal Conductivity: 3500-5000 W/mK
        • Weight: ~50-70% of body weight
        """
        ax.text(-2.8, -2.5, specs_text, fontsize=9, 
               verticalalignment='top', family='monospace',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        filepath = self.output_dir / "exoskeleton_structure.png"
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"✓ Exoskeleton structure visualization saved: {filepath}")
        plt.close()
    
    def visualize_biological_systems(self):
        """생물학적 시스템 시각화"""
        fig, ax = plt.subplots(1, 1, figsize=(14, 10))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # 제목
        ax.text(5, 9.5, 'Endoskeleton - Biological Systems', 
                fontsize=18, fontweight='bold', ha='center')
        
        systems = [
            ("Nervous System", 1, 7.5, self.color_scheme["nervous"]),
            ("Circulatory System", 4, 7.5, self.color_scheme["circulatory"]),
            ("Respiratory System", 7, 7.5, self.color_scheme["respiratory"]),
            ("Muscular System", 1, 4.5, self.color_scheme["muscular"]),
            ("Sensory System", 4, 4.5, self.color_scheme["sensory"]),
            ("Endocrine System", 7, 4.5, self.color_scheme["endocrine"])
        ]
        
        for name, x, y, color in systems:
            box = FancyBboxPatch((x-0.9, y-0.6), 1.8, 1.2,
                                boxstyle="round,pad=0.08",
                                edgecolor='black',
                                facecolor=color,
                                alpha=0.7, linewidth=2)
            ax.add_patch(box)
            ax.text(x, y, name, fontsize=10, fontweight='bold', 
                   ha='center', va='center')
        
        # 상세 정보
        details = """
        NERVOUS SYSTEM
        • Neurons: 86 billion
        • Synapses: 7 trillion
        • Signal Latency: 10 ms
        
        CIRCULATORY SYSTEM
        • Heart Rate: 72 bpm
        • Blood Pressure: 120/80 mmHg
        • O2 Saturation: 98%
        
        RESPIRATORY SYSTEM
        • Breathing Rate: 16 breaths/min
        • Lung Capacity: 6000 ml
        • O2 Intake: 250 ml/min
        
        MUSCULAR SYSTEM
        • Muscle Mass: 40 kg
        • Muscle Groups: 680
        • Strength Index: 100% (+ mech. enhancement)
        
        SENSORY SYSTEM
        • Visual Acuity: 1.0 (20/20)
        • Hearing Range: 20-20000 Hz
        • Touch Sensors: 5M receptors
        
        ENDOCRINE SYSTEM
        • Glands: 7 major
        • Hormone Levels: Balanced
        • Metabolic Rate: 1700 kcal/day
        """
        
        ax.text(5, 2.5, details, fontsize=8, verticalalignment='center',
               ha='center', family='monospace',
               bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))
        
        plt.tight_layout()
        filepath = self.output_dir / "biological_systems.png"
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"✓ Biological systems visualization saved: {filepath}")
        plt.close()
    
    def visualize_system_status(self, diagnosis: Dict):
        """시스템 상태 시각화 (진단 데이터 기반)"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('ACTF System Status Dashboard', fontsize=16, fontweight='bold')
        
        # 1. 외골격 부위별 건강도
        ax = axes[0, 0]
        exo_data = diagnosis['exoskeleton']['body_parts']
        parts_names = [part['part_type'] for part in exo_data]
        parts_health = [part['health'] for part in exo_data]
        
        colors = [self.color_scheme["success"] if h >= 80 else 
                 self.color_scheme["warning"] if h >= 60 else 
                 self.color_scheme["error"] for h in parts_health]
        
        bars1 = ax.bar(range(len(parts_names)), parts_health, color=colors, edgecolor='black', linewidth=1.5)
        ax.set_ylabel('Health Status (%)', fontweight='bold')
        ax.set_title('Exoskeleton - Body Parts Health', fontweight='bold')
        ax.set_xticks(range(len(parts_names)))
        ax.set_xticklabels([p.replace('_', ' ').title() for p in parts_names], rotation=45, ha='right')
        ax.set_ylim(0, 105)
        ax.grid(axis='y', alpha=0.3)
        
        for bar, health in zip(bars1, parts_health):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{health:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # 2. 내골격 시스템 건강도
        ax = axes[0, 1]
        endo_data = diagnosis['endoskeleton']['biological_systems']
        systems_names = [sys['system_id'].split('_')[0] for sys in endo_data]
        systems_health = [sys['health'] for sys in endo_data]
        
        colors = [self.color_scheme["success"] if h >= 80 else 
                 self.color_scheme["warning"] if h >= 60 else 
                 self.color_scheme["error"] for h in systems_health]
        
        bars2 = ax.bar(range(len(systems_names)), systems_health, color=colors, edgecolor='black', linewidth=1.5)
        ax.set_ylabel('Health Status (%)', fontweight='bold')
        ax.set_title('Endoskeleton - Biological Systems Health', fontweight='bold')
        ax.set_xticks(range(len(systems_names)))
        ax.set_xticklabels(systems_names, rotation=45, ha='right')
        ax.set_ylim(0, 105)
        ax.grid(axis='y', alpha=0.3)
        
        for bar, health in zip(bars2, systems_health):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{health:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # 3. 총 관절 수와 센서 수
        ax = axes[1, 0]
        total_joints = diagnosis['exoskeleton']['total_joints']
        categories = ['Joints', 'Bio-Systems']
        values = [total_joints, len(endo_data)]
        colors_pie = [self.color_scheme["exoskeleton"], self.color_scheme["endoskeleton"]]
        
        wedges, texts, autotexts = ax.pie(values, labels=categories, autopct='%1.0f',
                                           colors=colors_pie, explode=(0.05, 0.05),
                                           startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
        ax.set_title('System Component Count', fontweight='bold')
        
        # 4. 시스템 상태 요약
        ax = axes[1, 1]
        ax.axis('off')
        
        summary_text = f"""
        SYSTEM STATUS SUMMARY
        
        System ID: {diagnosis['system_id']}
        Status: {diagnosis['system_status'].upper()}
        Operation Time: {diagnosis['operation_time_seconds']:.1f} seconds
        
        EXOSKELETON:
        • Total Joints: {total_joints}
        • Body Parts: {len(exo_data)}
        • Avg Health: {np.mean(parts_health):.1f}%
        
        ENDOSKELETON:
        • Biological Systems: {len(endo_data)}
        • Avg Health: {np.mean(systems_health):.1f}%
        
        LOG ENTRIES: {diagnosis['log_entries']}
        """
        
        ax.text(0.1, 0.9, summary_text, fontsize=10, verticalalignment='top',
               family='monospace', transform=ax.transAxes,
               bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
        
        plt.tight_layout()
        filepath = self.output_dir / "system_status_dashboard.png"
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"✓ System status dashboard saved: {filepath}")
        plt.close()
    
    def visualize_stem_cell_cultivation(self, system_status: Dict):
        """줄기세포 배양 시각화"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Stem Cell Cultivation System', fontsize=16, fontweight='bold')
        
        bioreactors = system_status.get('bioreactors', {})
        
        if not bioreactors:
            ax = axes[0, 0]
            ax.text(0.5, 0.5, 'No bioreactor data available', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=12)
            plt.tight_layout()
            filepath = self.output_dir / "stem_cell_cultivation.png"
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            return
        
        # 1. 생물반응기별 세포 수
        ax = axes[0, 0]
        reactor_names = list(bioreactors.keys())
        cell_counts = [bioreactors[r]['cell_count'] for r in reactor_names]
        
        bars = ax.barh(reactor_names, cell_counts, color='#A8E6CF', edgecolor='black', linewidth=1.5)
        ax.set_xlabel('Cell Count', fontweight='bold')
        ax.set_title('Cells per Bioreactor', fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        
        for i, (bar, count) in enumerate(zip(bars, cell_counts)):
            ax.text(count, i, f'  {count:,}', va='center', fontweight='bold')
        
        # 2. 생물반응기별 상태
        ax = axes[0, 1]
        statuses = [bioreactors[r]['status'] for r in reactor_names]
        status_colors = {
            'standby': '#95a5a6',
            'cultivation': '#3498db',
            'differentiation': '#f39c12',
            'maturation': '#27ae60',
            'ready_for_transplant': '#2ecc71',
            'error': '#e74c3c'
        }
        
        colors = [status_colors.get(s, '#95a5a6') for s in statuses]
        bars = ax.bar(reactor_names, [1]*len(reactor_names), color=colors, edgecolor='black', linewidth=2)
        ax.set_ylabel('Status', fontweight='bold')
        ax.set_title('Bioreactor Status', fontweight='bold')
        ax.set_ylim(0, 1.5)
        ax.set_yticks([])
        
        for bar, status in zip(bars, statuses):
            ax.text(bar.get_x() + bar.get_width()/2., 0.5, 
                   status.replace('_', '\n').title(),
                   ha='center', va='center', fontweight='bold', fontsize=9)
        
        # 3. 배양 파라미터
        ax = axes[1, 0]
        ax.axis('off')
        
        if reactor_names:
            first_reactor = bioreactors[reactor_names[0]]
            params = first_reactor.get('parameters', {})
            
            param_text = f"""
            CULTIVATION PARAMETERS
            
            Temperature: {params.get('temperature', 'N/A')} °C
            pH Level: {params.get('ph_level', 'N/A')}
            O2 Concentration: {params.get('oxygen_concentration', 'N/A')} %
            Nutrient Density: {params.get('nutrient_density', 'N/A')} %
            Waste Product: {params.get('waste_product_level', 'N/A')} %
            CO2 Concentration: {params.get('co2_concentration', 'N/A')} %
            """
            
            ax.text(0.1, 0.9, param_text, fontsize=10, verticalalignment='top',
                   family='monospace', transform=ax.transAxes,
                   bbox=dict(boxstyle='round', facecolor='#F5D76E', alpha=0.5))
        
        # 4. 운영 시간
        ax = axes[1, 1]
        operation_hours = system_status.get('total_operation_hours', 0)
        
        days = int(operation_hours // 24)
        hours = int(operation_hours % 24)
        
        time_text = f"""
        SYSTEM OPERATION TIME
        
        Total Hours: {operation_hours:.1f}
        Days: {days}
        Hours: {hours}
        
        LOG ENTRIES: {system_status.get('log_entries', 0)}
        """
        
        ax.text(0.5, 0.5, time_text, fontsize=11, verticalalignment='center',
               ha='center', family='monospace', transform=ax.transAxes,
               bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5),
               fontweight='bold')
        ax.axis('off')
        
        plt.tight_layout()
        filepath = self.output_dir / "stem_cell_cultivation.png"
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"✓ Stem cell cultivation visualization saved: {filepath}")
        plt.close()
    
    def visualize_neural_interface(self, bci_status: Dict):
        """신경 인터페이스 시각화"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Brain-Computer Interface (BCI) Status', fontsize=16, fontweight='bold')
        
        performance = bci_status.get('performance', {})
        
        # 1. 명령 성공률
        ax = axes[0, 0]
        total_commands = performance.get('total_commands', 1)
        successful_commands = performance.get('successful_commands', 0)
        
        if total_commands > 0:
            success_rate = max(0, min(100, (successful_commands / total_commands) * 100))
            failed_rate = 100 - success_rate
        else:
            success_rate = 50
            failed_rate = 50
        
        # 유효한 값만 사용
        if success_rate > 0 and failed_rate > 0:
            sizes = [success_rate, failed_rate]
            colors = [self.color_scheme["success"], self.color_scheme["error"]]
            wedges, texts, autotexts = ax.pie(sizes, labels=['Successful', 'Failed'],
                                               autopct='%1.1f%%', colors=colors,
                                               startangle=90, textprops={'fontweight': 'bold'})
        else:
            ax.text(0.5, 0.5, 'No command data', ha='center', va='center', transform=ax.transAxes)
        
        ax.set_title(f'Motor Commands (Total: {total_commands})', fontweight='bold')
        
        # 2. 감각 입력 처리율
        ax = axes[0, 1]
        total_inputs = performance.get('total_inputs', 1)
        processed_inputs = performance.get('processed_inputs', 0)
        
        if total_inputs > 0:
            process_rate = max(0, min(100, (processed_inputs / total_inputs) * 100))
            failed_rate = 100 - process_rate
        else:
            process_rate = 50
            failed_rate = 50
        
        # 유효한 값만 사용
        if process_rate > 0 and failed_rate > 0:
            sizes = [process_rate, failed_rate]
            colors = [self.color_scheme["success"], self.color_scheme["warning"]]
            wedges, texts, autotexts = ax.pie(sizes, labels=['Processed', 'Pending'],
                                               autopct='%1.1f%%', colors=colors,
                                               startangle=90, textprops={'fontweight': 'bold'})
        else:
            ax.text(0.5, 0.5, 'No input data', ha='center', va='center', transform=ax.transAxes)
        
        ax.set_title(f'Sensory Inputs (Total: {total_inputs})', fontweight='bold')
        
        # 3. 인터페이스 상태
        ax = axes[1, 0]
        ax.axis('off')
        
        interface_text = f"""
        NEURAL INTERFACES STATUS
        
        BCI ID: {bci_status.get('bci_id', 'N/A')}
        Active Commands: {bci_status.get('active_commands', 0)}
        Sensory Buffer: {bci_status.get('sensory_buffer_size', 0)}
        Cognitive Load: {bci_status.get('cognitive_load', 0):.1f}%
        
        PERFORMANCE METRICS:
        • Total Commands: {total_commands}
        • Command Success Rate: {success_rate:.1f}%
        • Total Inputs: {total_inputs}
        • Input Process Rate: {process_rate:.1f}%
        
        Avg Latency: {performance.get('average_latency_ms', 0):.2f} ms
        """
        
        ax.text(0.1, 0.9, interface_text, fontsize=9, verticalalignment='top',
               family='monospace', transform=ax.transAxes,
               bbox=dict(boxstyle='round', facecolor='#E8DAEF', alpha=0.5))
        
        # 4. 인지 부하 게이지
        ax = axes[1, 1]
        cognitive_load = bci_status.get('cognitive_load', 0)
        
        # 배경
        ax.barh(['Cognitive\nLoad'], [100], color='#ecf0f1', edgecolor='black', linewidth=2)
        
        # 현재 부하
        load_color = self.color_scheme["success"] if cognitive_load < 50 else \
                    self.color_scheme["warning"] if cognitive_load < 80 else \
                    self.color_scheme["error"]
        ax.barh(['Cognitive\nLoad'], [cognitive_load], color=load_color, edgecolor='black', linewidth=2)
        
        ax.set_xlim(0, 100)
        ax.set_xlabel('Load Level (%)', fontweight='bold')
        
        if cognitive_load > 0:
            ax.text(cognitive_load/2, 0, f'{cognitive_load:.1f}%', 
                   va='center', ha='center', fontweight='bold', fontsize=12, color='white')
        else:
            ax.text(50, 0, '0.0%', va='center', ha='center', fontweight='bold', fontsize=12)
        
        ax.set_title('Current Cognitive Load', fontweight='bold')
        
        plt.tight_layout()
        filepath = self.output_dir / "neural_interface_status.png"
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"✓ Neural interface visualization saved: {filepath}")
        plt.close()
    
    def generate_all_visualizations(self, diagnosis: Dict = None, 
                                   stem_status: Dict = None,
                                   bci_status: Dict = None):
        """모든 시각화 생성"""
        print("\n" + "="*60)
        print("Generating ACTF Visualizations")
        print("="*60)
        
        # 기본 시각화
        self.visualize_system_architecture()
        self.visualize_exoskeleton_structure()
        self.visualize_biological_systems()
        
        # 데이터 기반 시각화
        if diagnosis:
            self.visualize_system_status(diagnosis)
        
        if stem_status:
            self.visualize_stem_cell_cultivation(stem_status)
        
        if bci_status:
            self.visualize_neural_interface(bci_status)
        
        print("="*60)
        print(f"✓ All visualizations saved to: {self.output_dir}")
        print("="*60)


# ============================================================================
# 테스트 및 실행
# ============================================================================

if __name__ == "__main__":
    print("ACTF Visualization Module Test")
    print("="*60)
    
    # 시각화 도구 생성
    visualizer = ACTFVisualizer(output_dir="./visualizations")
    
    # 기본 시각화만 생성
    visualizer.visualize_system_architecture()
    visualizer.visualize_exoskeleton_structure()
    visualizer.visualize_biological_systems()
    
    print("\n✓ Basic visualizations completed!")
    print("  Output directory: ./visualizations/")
