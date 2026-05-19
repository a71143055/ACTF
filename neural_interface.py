"""
ACTF - 신경 인터페이스 시스템 모듈

뇌와 사이보그 본체 간의 신호 통신을 관리합니다.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import random


class SignalType(Enum):
    """신경 신호 유형"""
    MOTOR_COMMAND = "motor_command"
    SENSORY_INPUT = "sensory_input"
    AUTONOMIC = "autonomic"
    COGNITIVE = "cognitive"


class NeuralFrequency(Enum):
    """신경 신호 주파수대"""
    DELTA = "delta"      # 0.5-4 Hz (sleep)
    THETA = "theta"      # 4-8 Hz (drowsiness)
    ALPHA = "alpha"      # 8-12 Hz (relaxation)
    BETA = "beta"        # 12-30 Hz (conscious activity)
    GAMMA = "gamma"      # 30-100 Hz (cognitive processing)


@dataclass
class NeuralSignal:
    """신경 신호"""
    signal_id: str
    signal_type: SignalType
    frequency_band: NeuralFrequency
    amplitude: float  # μV (microvolt)
    source_region: str  # 뇌의 영역
    timestamp: datetime
    latency: float = 10.0  # ms
    
    def to_dict(self) -> Dict:
        """딕셔너리 변환"""
        return {
            "signal_id": self.signal_id,
            "signal_type": self.signal_type.value,
            "frequency_band": self.frequency_band.value,
            "amplitude_uv": self.amplitude,
            "source_region": self.source_region,
            "latency_ms": self.latency,
            "timestamp": self.timestamp.isoformat()
        }


class MotorCommand(NeuralSignal):
    """운동 명령"""
    
    def __init__(self, command_id: str, target_muscle_group: str, force: float):
        super().__init__(
            signal_id=command_id,
            signal_type=SignalType.MOTOR_COMMAND,
            frequency_band=NeuralFrequency.BETA,
            amplitude=random.uniform(50, 200),
            source_region="Motor Cortex",
            timestamp=datetime.now(),
            latency=random.uniform(8, 15)
        )
        self.target_muscle_group = target_muscle_group
        self.force = force  # 0-100%
        self.execution_status = "pending"
    
    def execute(self) -> bool:
        """명령 실행"""
        self.execution_status = "executed"
        return True
    
    def to_dict(self) -> Dict:
        """딕셔너리 변환"""
        data = super().to_dict()
        data.update({
            "target_muscle_group": self.target_muscle_group,
            "force_percent": self.force,
            "execution_status": self.execution_status
        })
        return data


class SensoryInput(NeuralSignal):
    """감각 입력"""
    
    def __init__(self, input_id: str, sensory_type: str, intensity: float):
        super().__init__(
            signal_id=input_id,
            signal_type=SignalType.SENSORY_INPUT,
            frequency_band=NeuralFrequency.ALPHA,
            amplitude=random.uniform(30, 150),
            source_region="Sensory Cortex",
            timestamp=datetime.now(),
            latency=random.uniform(5, 20)
        )
        self.sensory_type = sensory_type  # visual, auditory, tactile, proprioceptive
        self.intensity = intensity  # 0-100%
        self.processed = False
    
    def process(self) -> bool:
        """감각 정보 처리"""
        self.processed = True
        return True
    
    def to_dict(self) -> Dict:
        """딕셔너리 변환"""
        data = super().to_dict()
        data.update({
            "sensory_type": self.sensory_type,
            "intensity": self.intensity,
            "processed": self.processed
        })
        return data


class NeuralInterface:
    """신경 인터페이스"""
    
    def __init__(self, interface_id: str):
        self.interface_id = interface_id
        self.connection_status = False
        self.signal_buffer: List[NeuralSignal] = []
        self.processed_signals: List[NeuralSignal] = []
        self.latency_ms: float = 10.0
        self.error_rate: float = 0.0  # %
        self.bandwidth_mhz: float = 100.0  # MHz
        self.signal_count = 0
    
    def connect(self) -> bool:
        """신경계 연결"""
        # 연결 검증 프로세스
        connection_checks = [
            self._check_electrode_impedance(),
            self._check_signal_quality(),
            self._check_bandwidth()
        ]
        
        self.connection_status = all(connection_checks)
        return self.connection_status
    
    def _check_electrode_impedance(self) -> bool:
        """전극 임피던스 확인"""
        impedance = random.uniform(1, 100)  # kΩ
        return 1 < impedance < 100
    
    def _check_signal_quality(self) -> bool:
        """신호 품질 확인"""
        snr = random.uniform(10, 50)  # dB
        return snr > 15
    
    def _check_bandwidth(self) -> bool:
        """대역폭 확인"""
        return self.bandwidth_mhz >= 50
    
    def send_motor_command(self, target_muscle: str, force: float) -> MotorCommand:
        """운동 명령 전송"""
        command = MotorCommand(
            command_id=f"CMD_{self.signal_count:06d}",
            target_muscle_group=target_muscle,
            force=force
        )
        self.signal_count += 1
        
        if self.connection_status:
            command.execute()
            self.processed_signals.append(command)
        else:
            self.signal_buffer.append(command)
        
        return command
    
    def receive_sensory_input(self, sensory_type: str, intensity: float) -> SensoryInput:
        """감각 입력 수신"""
        sensor_input = SensoryInput(
            input_id=f"SENS_{self.signal_count:06d}",
            sensory_type=sensory_type,
            intensity=intensity
        )
        self.signal_count += 1
        
        if self.connection_status:
            sensor_input.process()
            self.processed_signals.append(sensor_input)
        else:
            self.signal_buffer.append(sensor_input)
        
        return sensor_input
    
    def flush_buffer(self) -> int:
        """버퍼 플러시"""
        flushed = len(self.signal_buffer)
        for signal in self.signal_buffer:
            if isinstance(signal, MotorCommand):
                signal.execute()
            elif isinstance(signal, SensoryInput):
                signal.process()
            self.processed_signals.append(signal)
        self.signal_buffer.clear()
        return flushed
    
    def get_status(self) -> Dict:
        """인터페이스 상태"""
        return {
            "interface_id": self.interface_id,
            "connection_status": self.connection_status,
            "latency_ms": self.latency_ms,
            "error_rate_percent": self.error_rate,
            "bandwidth_mhz": self.bandwidth_mhz,
            "signal_buffer_size": len(self.signal_buffer),
            "processed_signals": len(self.processed_signals),
            "total_signals": self.signal_count
        }


class BrainComputerInterface:
    """뇌-컴퓨터 인터페이스 시스템"""
    
    def __init__(self):
        self.bci_id = "BCI_MAIN_001"
        self.created_at = datetime.now()
        self.neural_interfaces: Dict[str, NeuralInterface] = {}
        self.active_commands: List[MotorCommand] = []
        self.sensory_buffer: List[SensoryInput] = []
        self.cognitive_load: float = 0.0  # 0-100%
        self.system_log: List[Dict] = []
        self.performance_metrics = {
            "total_commands": 0,
            "successful_commands": 0,
            "total_inputs": 0,
            "processed_inputs": 0,
            "average_latency_ms": 0.0
        }
    
    def register_neural_interface(self, interface_id: str) -> NeuralInterface:
        """신경 인터페이스 등록"""
        interface = NeuralInterface(interface_id)
        self.neural_interfaces[interface_id] = interface
        self.log_event(f"Registered neural interface: {interface_id}")
        return interface
    
    def initialize_interfaces(self) -> bool:
        """모든 인터페이스 초기화"""
        self.log_event("Initializing neural interfaces...")
        
        success_count = 0
        for interface_id, interface in self.neural_interfaces.items():
            if interface.connect():
                self.log_event(f"Interface {interface_id} connected successfully")
                success_count += 1
            else:
                self.log_event(f"Interface {interface_id} connection failed")
        
        return success_count == len(self.neural_interfaces)
    
    def send_command_to_motor_system(self, muscle_group: str, force: float) -> Dict:
        """운동계에 명령 전송"""
        # 기본 인터페이스를 통해 명령 전송
        main_interface = self.neural_interfaces.get("MAIN_INTERFACE")
        if not main_interface or not main_interface.connection_status:
            return {"status": "failed", "reason": "No active interface"}
        
        command = main_interface.send_motor_command(muscle_group, force)
        self.active_commands.append(command)
        self.performance_metrics["total_commands"] += 1
        
        if command.execution_status == "executed":
            self.performance_metrics["successful_commands"] += 1
        
        self.log_event(
            f"Sent motor command: {muscle_group} with force {force}%"
        )
        
        return {
            "status": "sent",
            "command_id": command.signal_id,
            "latency_ms": command.latency,
            "execution_status": command.execution_status
        }
    
    def receive_sensory_data(self, sensory_type: str, intensity: float) -> Dict:
        """감각 데이터 수신"""
        main_interface = self.neural_interfaces.get("MAIN_INTERFACE")
        if not main_interface:
            return {"status": "failed", "reason": "No interface available"}
        
        sensory_input = main_interface.receive_sensory_input(sensory_type, intensity)
        self.sensory_buffer.append(sensory_input)
        self.performance_metrics["total_inputs"] += 1
        
        if sensory_input.processed:
            self.performance_metrics["processed_inputs"] += 1
        
        self.log_event(
            f"Received sensory input: {sensory_type} with intensity {intensity}%"
        )
        
        return {
            "status": "received",
            "input_id": sensory_input.signal_id,
            "latency_ms": sensory_input.latency,
            "processed": sensory_input.processed
        }
    
    def update_cognitive_load(self, new_load: float):
        """인지 부하 업데이트"""
        self.cognitive_load = max(0, min(100, new_load))
        
        if self.cognitive_load > 80:
            self.log_event("WARNING: High cognitive load detected")
        elif self.cognitive_load > 60:
            self.log_event("CAUTION: Moderate cognitive load")
    
    def log_event(self, event: str):
        """이벤트 로깅"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event
        }
        self.system_log.append(log_entry)
        print(f"[BCI] {event}")
    
    def get_performance_report(self) -> Dict:
        """성능 리포트"""
        if self.performance_metrics["total_commands"] > 0:
            success_rate = (
                self.performance_metrics["successful_commands"] /
                self.performance_metrics["total_commands"] * 100
            )
        else:
            success_rate = 0
        
        if self.performance_metrics["total_inputs"] > 0:
            process_rate = (
                self.performance_metrics["processed_inputs"] /
                self.performance_metrics["total_inputs"] * 100
            )
        else:
            process_rate = 0
        
        return {
            "total_commands": self.performance_metrics["total_commands"],
            "command_success_rate": success_rate,
            "total_inputs": self.performance_metrics["total_inputs"],
            "input_process_rate": process_rate,
            "cognitive_load": self.cognitive_load,
            "interfaces_status": {
                iid: interface.get_status()
                for iid, interface in self.neural_interfaces.items()
            }
        }
    
    def get_full_status(self) -> Dict:
        """전체 상태"""
        return {
            "bci_id": self.bci_id,
            "created_at": self.created_at.isoformat(),
            "active_commands": len(self.active_commands),
            "sensory_buffer_size": len(self.sensory_buffer),
            "cognitive_load": self.cognitive_load,
            "performance": self.get_performance_report(),
            "log_entries": len(self.system_log)
        }


# ============================================================================
# 테스트 예제
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("Brain-Computer Interface System Test")
    print("=" * 80)
    print()
    
    # BCI 시스템 생성
    bci = BrainComputerInterface()
    
    # 신경 인터페이스 등록
    print("1. Registering neural interfaces...")
    main_interface = bci.register_neural_interface("MAIN_INTERFACE")
    sensory_interface = bci.register_neural_interface("SENSORY_INTERFACE")
    print()
    
    # 인터페이스 초기화
    print("2. Initializing interfaces...")
    if bci.initialize_interfaces():
        print("✓ All interfaces initialized successfully")
    else:
        print("✗ Some interfaces failed to initialize")
    print()
    
    # 운동 명령 전송
    print("3. Sending motor commands...")
    muscles = ["arm_flexor", "arm_extensor", "leg_quadriceps", "leg_hamstring"]
    for muscle in muscles:
        result = bci.send_command_to_motor_system(muscle, force=random.uniform(30, 90))
        print(f"   {muscle}: {result['execution_status']}")
    print()
    
    # 감각 입력 수신
    print("4. Receiving sensory inputs...")
    sensory_types = ["visual", "auditory", "tactile", "proprioceptive"]
    for sensory_type in sensory_types:
        result = bci.receive_sensory_data(sensory_type, intensity=random.uniform(50, 100))
        print(f"   {sensory_type}: processed={result['processed']}")
    print()
    
    # 인지 부하 업데이트
    print("5. Updating cognitive load...")
    for load in [30, 60, 85, 40]:
        bci.update_cognitive_load(load)
        print(f"   Cognitive load set to {load}%")
    print()
    
    # 성능 리포트
    print("=" * 80)
    print("Performance Report")
    print("=" * 80)
    import json
    print(json.dumps(bci.get_full_status(), indent=2, ensure_ascii=False))
