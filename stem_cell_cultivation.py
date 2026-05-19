"""
ACTF - 줄기세포 배양 시스템 모듈

이 모듈은 내골격의 생물학적 조직 배양 프로세스를 시뮬레이션합니다.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import random


class StemCellType(Enum):
    """줄기세포 타입"""
    EMBRYONIC = "embryonic"
    ADULT = "adult"
    INDUCED_PLURIPOTENT = "induced_pluripotent"


class CellDifferentiationType(Enum):
    """분화 유형"""
    MUSCLE = "muscle_cell"
    NEURON = "neuron"
    CARDIAC = "cardiac_cell"
    ENDOTHELIAL = "endothelial_cell"
    OSTEOCYTE = "osteocyte"
    FIBROBLAST = "fibroblast"


class BioreactorStatus(Enum):
    """생물반응기 상태"""
    STANDBY = "standby"
    CULTIVATION = "cultivation"
    DIFFERENTIATION = "differentiation"
    MATURATION = "maturation"
    READY_FOR_TRANSPLANT = "ready_for_transplant"
    ERROR = "error"


@dataclass
class CultivationParameters:
    """배양 파라미터"""
    temperature: float = 37.0  # °C
    ph_level: float = 7.4
    oxygen_concentration: float = 5.0  # %
    nutrient_density: float = 100.0  # %
    waste_product_level: float = 0.0  # %
    co2_concentration: float = 5.0  # %


@dataclass
class StemCell:
    """줄기세포"""
    cell_id: str
    cell_type: StemCellType
    target_differentiation: CellDifferentiationType
    creation_date: datetime
    division_count: int = 0
    health_status: float = 100.0  # 0-100%
    differentiation_progress: float = 0.0  # 0-100%
    
    def update_health(self, delta: float):
        """세포 건강도 업데이트"""
        self.health_status = max(0, min(100, self.health_status + delta))
    
    def divide(self) -> 'StemCell':
        """세포 분열"""
        new_cell = StemCell(
            cell_id=f"{self.cell_id}_daughter_{self.division_count}",
            cell_type=self.cell_type,
            target_differentiation=self.target_differentiation,
            creation_date=datetime.now(),
            division_count=self.division_count + 1
        )
        return new_cell


class Bioreactor:
    """생물반응기"""
    
    def __init__(self, reactor_id: str, capacity: int = 1000000):
        self.reactor_id = reactor_id
        self.capacity = capacity
        self.stem_cells: List[StemCell] = []
        self.parameters = CultivationParameters()
        self.status = BioreactorStatus.STANDBY
        self.creation_date = datetime.now()
        self.operation_hours: float = 0.0
        self.harvest_ready_cells: List[StemCell] = []
    
    def add_stem_cells(self, cells: List[StemCell]) -> bool:
        """줄기세포 추가"""
        if len(self.stem_cells) + len(cells) > self.capacity:
            return False
        self.stem_cells.extend(cells)
        return True
    
    def start_cultivation(self) -> bool:
        """배양 시작"""
        if self.status != BioreactorStatus.STANDBY:
            return False
        if len(self.stem_cells) == 0:
            return False
        
        self.status = BioreactorStatus.CULTIVATION
        return True
    
    def simulate_growth_cycle(self, hours: float = 24.0) -> Dict:
        """성장 사이클 시뮬레이션 (24시간 기준)"""
        self.operation_hours += hours
        results = {
            "duration_hours": hours,
            "cell_count_before": len(self.stem_cells),
            "divisions": 0,
            "health_degradation": []
        }
        
        if self.status in [BioreactorStatus.CULTIVATION, BioreactorStatus.DIFFERENTIATION]:
            new_cells = []
            
            for cell in self.stem_cells:
                # 환경 적응에 따른 건강도 변화
                health_delta = self._calculate_health_delta()
                cell.update_health(health_delta)
                
                # 세포 분열 확률
                if cell.health_status > 70 and random.random() < 0.3:
                    new_cell = cell.divide()
                    new_cells.append(new_cell)
                    results["divisions"] += 1
                
                # 분화 진행
                if self.status == BioreactorStatus.DIFFERENTIATION:
                    cell.differentiation_progress = min(
                        100.0,
                        cell.differentiation_progress + random.uniform(5, 15)
                    )
            
            # 새 세포 추가
            self.add_stem_cells(new_cells)
            
            # 수확 준비 상태 확인
            self._check_harvest_readiness()
            
            results["cell_count_after"] = len(self.stem_cells)
        
        return results
    
    def _calculate_health_delta(self) -> float:
        """건강도 변화 계산"""
        # 파라미터가 최적일 때 긍정적 변화
        delta = 0.0
        
        # 온도 영향
        if 36.5 <= self.parameters.temperature <= 37.5:
            delta += 2.0
        else:
            delta -= 3.0
        
        # pH 영향
        if 7.2 <= self.parameters.ph_level <= 7.6:
            delta += 1.5
        else:
            delta -= 2.5
        
        # 산소 농도 영향
        if 3.0 <= self.parameters.oxygen_concentration <= 7.0:
            delta += 1.5
        else:
            delta -= 2.0
        
        # 영양소 영향
        if self.parameters.nutrient_density >= 80.0:
            delta += 1.0
        else:
            delta -= 3.0
        
        # 폐기물 축적 영향
        if self.parameters.waste_product_level > 40.0:
            delta -= 4.0
        
        return delta
    
    def _check_harvest_readiness(self):
        """수확 준비 상태 확인"""
        ready_cells = []
        remaining_cells = []
        
        for cell in self.stem_cells:
            if cell.differentiation_progress >= 95.0 and cell.health_status >= 90.0:
                ready_cells.append(cell)
            else:
                remaining_cells.append(cell)
        
        if ready_cells:
            self.harvest_ready_cells.extend(ready_cells)
            self.stem_cells = remaining_cells
    
    def harvest_cells(self) -> List[StemCell]:
        """세포 수확"""
        harvested = self.harvest_ready_cells
        self.harvest_ready_cells = []
        return harvested
    
    def update_parameters(self, **kwargs):
        """배양 파라미터 업데이트"""
        for key, value in kwargs.items():
            if hasattr(self.parameters, key):
                setattr(self.parameters, key, value)
    
    def get_status(self) -> Dict:
        """현재 상태 반환"""
        return {
            "reactor_id": self.reactor_id,
            "status": self.status.value,
            "cell_count": len(self.stem_cells),
            "harvest_ready_count": len(self.harvest_ready_cells),
            "operation_hours": self.operation_hours,
            "parameters": {
                "temperature": self.parameters.temperature,
                "ph_level": self.parameters.ph_level,
                "oxygen_concentration": self.parameters.oxygen_concentration,
                "nutrient_density": self.parameters.nutrient_density,
                "waste_product_level": self.parameters.waste_product_level,
                "co2_concentration": self.parameters.co2_concentration
            }
        }


class StemCellCultivationSystem:
    """줄기세포 배양 시스템"""
    
    def __init__(self):
        self.system_id = "STEM_CULT_001"
        self.bioreactors: Dict[str, Bioreactor] = {}
        self.created_at = datetime.now()
        self.operation_log: List[Dict] = []
    
    def create_bioreactor(self, reactor_id: str, capacity: int = 1000000) -> Bioreactor:
        """생물반응기 생성"""
        reactor = Bioreactor(reactor_id, capacity)
        self.bioreactors[reactor_id] = reactor
        self.log_event(f"Created bioreactor {reactor_id} with capacity {capacity}")
        return reactor
    
    def initialize_cultivation(self, reactor_id: str, cell_type: StemCellType,
                             differentiation_target: CellDifferentiationType,
                             initial_cell_count: int = 10000) -> bool:
        """배양 초기화"""
        if reactor_id not in self.bioreactors:
            return False
        
        reactor = self.bioreactors[reactor_id]
        
        # 초기 줄기세포 생성
        initial_cells = [
            StemCell(
                cell_id=f"{reactor_id}_cell_{i}",
                cell_type=cell_type,
                target_differentiation=differentiation_target,
                creation_date=datetime.now()
            )
            for i in range(initial_cell_count)
        ]
        
        if not reactor.add_stem_cells(initial_cells):
            self.log_event(f"Failed to add cells to {reactor_id}")
            return False
        
        if not reactor.start_cultivation():
            self.log_event(f"Failed to start cultivation in {reactor_id}")
            return False
        
        self.log_event(
            f"Initialized cultivation in {reactor_id}: "
            f"{initial_cell_count} {cell_type.value} cells targeting {differentiation_target.value}"
        )
        return True
    
    def advance_cultivation(self, reactor_id: str, days: float = 1.0) -> Dict:
        """배양 진행"""
        if reactor_id not in self.bioreactors:
            return {"error": f"Reactor {reactor_id} not found"}
        
        reactor = self.bioreactors[reactor_id]
        hours = days * 24.0
        
        # 배양 사이클 시뮬레이션
        results = []
        for _ in range(int(days)):
            cycle_result = reactor.simulate_growth_cycle(24.0)
            results.append(cycle_result)
        
        self.log_event(
            f"Advanced cultivation in {reactor_id} by {days} days. "
            f"Total cells: {len(reactor.stem_cells)}"
        )
        
        return {
            "reactor_id": reactor_id,
            "days_advanced": days,
            "cycle_results": results,
            "current_status": reactor.get_status()
        }
    
    def start_differentiation(self, reactor_id: str) -> bool:
        """분화 시작"""
        if reactor_id not in self.bioreactors:
            return False
        
        reactor = self.bioreactors[reactor_id]
        if reactor.status != BioreactorStatus.CULTIVATION:
            return False
        
        reactor.status = BioreactorStatus.DIFFERENTIATION
        self.log_event(f"Started differentiation in {reactor_id}")
        return True
    
    def harvest_cells(self, reactor_id: str) -> Dict:
        """세포 수확"""
        if reactor_id not in self.bioreactors:
            return {"error": f"Reactor {reactor_id} not found"}
        
        reactor = self.bioreactors[reactor_id]
        harvested = reactor.harvest_cells()
        
        self.log_event(
            f"Harvested {len(harvested)} cells from {reactor_id}"
        )
        
        return {
            "reactor_id": reactor_id,
            "cells_harvested": len(harvested),
            "average_health": sum(c.health_status for c in harvested) / len(harvested) if harvested else 0
        }
    
    def log_event(self, event: str):
        """이벤트 로깅"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event
        }
        self.operation_log.append(log_entry)
        print(f"[STEM_CULT] {event}")
    
    def get_system_status(self) -> Dict:
        """시스템 전체 상태"""
        return {
            "system_id": self.system_id,
            "bioreactors": {
                rid: reactor.get_status()
                for rid, reactor in self.bioreactors.items()
            },
            "total_operation_hours": sum(
                r.operation_hours for r in self.bioreactors.values()
            ),
            "log_entries": len(self.operation_log)
        }


# ============================================================================
# 테스트 예제
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("Stem Cell Cultivation System Test")
    print("=" * 80)
    print()
    
    # 시스템 생성
    cultivation_system = StemCellCultivationSystem()
    
    # 생물반응기 생성
    print("1. Creating bioreactors...")
    reactor_muscle = cultivation_system.create_bioreactor("REACTOR_MUSCLE_001", capacity=5000000)
    reactor_neuron = cultivation_system.create_bioreactor("REACTOR_NEURON_001", capacity=3000000)
    print()
    
    # 배양 초기화
    print("2. Initializing cultivations...")
    cultivation_system.initialize_cultivation(
        "REACTOR_MUSCLE_001",
        StemCellType.ADULT,
        CellDifferentiationType.MUSCLE,
        initial_cell_count=50000
    )
    cultivation_system.initialize_cultivation(
        "REACTOR_NEURON_001",
        StemCellType.INDUCED_PLURIPOTENT,
        CellDifferentiationType.NEURON,
        initial_cell_count=30000
    )
    print()
    
    # 배양 진행
    print("3. Running cultivation cycles (30 days)...")
    for day in range(1, 4):
        print(f"\n--- Day {day * 10} ---")
        result_muscle = cultivation_system.advance_cultivation(
            "REACTOR_MUSCLE_001",
            days=10.0
        )
        result_neuron = cultivation_system.advance_cultivation(
            "REACTOR_NEURON_001",
            days=10.0
        )
        print(f"Muscle reactor: {result_muscle['current_status']['cell_count']} cells")
        print(f"Neuron reactor: {result_neuron['current_status']['cell_count']} cells")
    
    print()
    
    # 분화 시작
    print("4. Starting differentiation...")
    cultivation_system.start_differentiation("REACTOR_MUSCLE_001")
    cultivation_system.start_differentiation("REACTOR_NEURON_001")
    print()
    
    # 추가 배양
    print("5. Advancing differentiation (60 days)...")
    for day in range(1, 7):
        cultivation_system.advance_cultivation("REACTOR_MUSCLE_001", days=10.0)
        cultivation_system.advance_cultivation("REACTOR_NEURON_001", days=10.0)
    print()
    
    # 수확
    print("6. Harvesting cells...")
    harvest_muscle = cultivation_system.harvest_cells("REACTOR_MUSCLE_001")
    harvest_neuron = cultivation_system.harvest_cells("REACTOR_NEURON_001")
    print(f"Muscle cells harvested: {harvest_muscle['cells_harvested']}")
    print(f"Neuron cells harvested: {harvest_neuron['cells_harvested']}")
    print()
    
    # 시스템 상태
    print("=" * 80)
    print("System Status Summary")
    print("=" * 80)
    import json
    print(json.dumps(cultivation_system.get_system_status(), indent=2, ensure_ascii=False))
