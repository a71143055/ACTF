"""
ACTF - 통합 테스트 및 데모 스크립트

전체 시스템의 동작을 검증하는 포괄적인 테스트 스위트
"""

import sys
import json
from datetime import datetime
from typing import Dict, List

# 모듈 임포트
try:
    from actf_main import ACTFMainController
    from stem_cell_cultivation import (
        StemCellCultivationSystem,
        StemCellType,
        CellDifferentiationType
    )
    from neural_interface import BrainComputerInterface
    from visualization import ACTFVisualizer
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all ACTF modules are in the same directory")
    sys.exit(1)


class ACTFIntegrationTest:
    """ACTF 통합 테스트"""
    
    def __init__(self):
        self.test_results: List[Dict] = []
        self.start_time = datetime.now()
    
    def log_test(self, test_name: str, passed: bool, details: str = ""):
        """테스트 결과 로깅"""
        result = {
            "test_name": test_name,
            "passed": passed,
            "timestamp": datetime.now().isoformat(),
            "details": details
        }
        self.test_results.append(result)
        status_symbol = "[OK]" if passed else "[FAIL]"
        print(f"{status_symbol} {test_name}")
        if details:
            print(f"  └─ {details}")
    
    def test_exoskeleton_initialization(self) -> bool:
        """외골격 초기화 테스트"""
        print("\n[TEST 1] Exoskeleton Initialization")
        print("-" * 60)
        
        try:
            actf = ACTFMainController()
            actf_exoskeleton = actf.exoskeleton
            
            # 외골격 부위 검증
            assert actf_exoskeleton.head is not None
            assert actf_exoskeleton.torso is not None
            assert actf_exoskeleton.left_arm is not None
            assert actf_exoskeleton.right_arm is not None
            assert actf_exoskeleton.left_leg is not None
            assert actf_exoskeleton.right_leg is not None
            
            self.log_test(
                "Exoskeleton structure validation",
                True,
                f"6 body parts detected, {actf_exoskeleton.total_joints} joints"
            )
            
            # 관절 검증
            assert actf_exoskeleton.left_arm.joints is not None
            assert len(actf_exoskeleton.left_arm.joints) > 0
            
            self.log_test(
                "Joint structure validation",
                True,
                f"Arm joints: {len(actf_exoskeleton.left_arm.joints)}"
            )
            
            return True
        except Exception as e:
            self.log_test("Exoskeleton initialization", False, str(e))
            return False
    
    def test_endoskeleton_initialization(self) -> bool:
        """내골격 초기화 테스트"""
        print("\n[TEST 2] Endoskeleton Initialization")
        print("-" * 60)
        
        try:
            actf = ACTFMainController()
            actf_endoskeleton = actf.endoskeleton
            
            # 생물 시스템 검증
            systems = [
                ("Nervous System", actf_endoskeleton.nervous_system),
                ("Circulatory System", actf_endoskeleton.circulatory_system),
                ("Respiratory System", actf_endoskeleton.respiratory_system),
                ("Muscular System", actf_endoskeleton.muscular_system),
                ("Sensory System", actf_endoskeleton.sensory_system),
                ("Endocrine System", actf_endoskeleton.endocrine_system)
            ]
            
            for system_name, system in systems:
                assert system is not None
                self.log_test(
                    f"{system_name} validation",
                    True,
                    f"Health status: {system.health_index}%"
                )
            
            return True
        except Exception as e:
            self.log_test("Endoskeleton initialization", False, str(e))
            return False
    
    def test_system_initialization(self) -> bool:
        """전체 시스템 초기화 테스트"""
        print("\n[TEST 3] Full System Initialization")
        print("-" * 60)
        
        try:
            actf = ACTFMainController()
            
            if actf.initialize():
                self.log_test(
                    "System initialization",
                    True,
                    "All components initialized successfully"
                )
                return True
            else:
                self.log_test("System initialization", False, "Initialization failed")
                return False
        except Exception as e:
            self.log_test("System initialization", False, str(e))
            return False
    
    def test_stem_cell_cultivation(self) -> bool:
        """줄기세포 배양 테스트"""
        print("\n[TEST 4] Stem Cell Cultivation")
        print("-" * 60)
        
        try:
            cultivation = StemCellCultivationSystem()
            
            # 생물반응기 생성
            reactor = cultivation.create_bioreactor("TEST_REACTOR", capacity=100000)
            self.log_test(
                "Bioreactor creation",
                True,
                "Test reactor created with 100k capacity"
            )
            
            # 배양 초기화
            success = cultivation.initialize_cultivation(
                "TEST_REACTOR",
                StemCellType.ADULT,
                CellDifferentiationType.MUSCLE,
                initial_cell_count=10000
            )
            self.log_test(
                "Cultivation initialization",
                success,
                "10k muscle cells initialized"
            )
            
            if not success:
                return False
            
            # 배양 진행
            for day in [10, 20, 30]:
                result = cultivation.advance_cultivation("TEST_REACTOR", days=10.0)
                cells = result['current_status']['cell_count']
                self.log_test(
                    f"Cultivation at day {day}",
                    True,
                    f"Cell count: {cells}"
                )
            
            # 분화 시작
            success = cultivation.start_differentiation("TEST_REACTOR")
            self.log_test(
                "Differentiation start",
                success,
                "Differentiation phase initiated"
            )
            
            # 추가 배양
            for day in range(1, 4):
                cultivation.advance_cultivation("TEST_REACTOR", days=20.0)
            
            # 수확
            harvest = cultivation.harvest_cells("TEST_REACTOR")
            self.log_test(
                "Cell harvest",
                harvest['cells_harvested'] > 0,
                f"{harvest['cells_harvested']} cells harvested"
            )
            
            return True
        except Exception as e:
            self.log_test("Stem cell cultivation", False, str(e))
            return False
    
    def test_neural_interface(self) -> bool:
        """신경 인터페이스 테스트"""
        print("\n[TEST 5] Neural Interface")
        print("-" * 60)
        
        try:
            bci = BrainComputerInterface()
            
            # 신경 인터페이스 등록
            main_interface = bci.register_neural_interface("MAIN_INTERFACE")
            self.log_test(
                "Neural interface registration",
                True,
                "Main interface registered"
            )
            
            # 인터페이스 초기화
            if bci.initialize_interfaces():
                self.log_test(
                    "Interface connection",
                    True,
                    "All interfaces connected"
                )
            else:
                self.log_test("Interface connection", False, "Connection failed")
                return False
            
            # 운동 명령 테스트
            result = bci.send_command_to_motor_system("arm_flexor", 75.0)
            self.log_test(
                "Motor command",
                result['status'] == 'sent',
                f"Latency: {result['latency_ms']:.2f}ms"
            )
            
            # 감각 입력 테스트
            result = bci.receive_sensory_data("visual", 80.0)
            self.log_test(
                "Sensory input",
                result['status'] == 'received',
                f"Visual input processed: {result['processed']}"
            )
            
            # 인지 부하 테스트
            bci.update_cognitive_load(65.0)
            self.log_test(
                "Cognitive load",
                bci.cognitive_load == 65.0,
                f"Load set to {bci.cognitive_load}%"
            )
            
            return True
        except Exception as e:
            self.log_test("Neural interface", False, str(e))
            return False
    
    def test_system_diagnostics(self) -> bool:
        """시스템 진단 테스트"""
        print("\n[TEST 6] System Diagnostics")
        print("-" * 60)
        
        try:
            actf = ACTFMainController()
            if not actf.initialize():
                self.log_test("System diagnostics", False, "System init failed")
                return False
            
            # 진단 수행
            diagnosis = actf.diagnose()
            
            # 외골격 진단
            exo_parts = diagnosis['exoskeleton']['body_parts']
            self.log_test(
                "Exoskeleton diagnostics",
                len(exo_parts) == 6,
                f"6 body parts diagnosed"
            )
            
            # 내골격 진단
            endo_systems = diagnosis['endoskeleton']['biological_systems']
            self.log_test(
                "Endoskeleton diagnostics",
                len(endo_systems) == 6,
                f"6 biological systems diagnosed"
            )
            
            return True
        except Exception as e:
            self.log_test("System diagnostics", False, str(e))
            return False
    
    def run_all_tests(self) -> Dict:
        """모든 테스트 실행"""
        print("\n" + "=" * 80)
        print("ACTF COMPREHENSIVE INTEGRATION TEST SUITE")
        print("=" * 80)
        
        tests = [
            self.test_exoskeleton_initialization,
            self.test_endoskeleton_initialization,
            self.test_system_initialization,
            self.test_stem_cell_cultivation,
            self.test_neural_interface,
            self.test_system_diagnostics
        ]
        
        for test in tests:
            try:
                test()
            except Exception as e:
                print(f"✗ Test {test.__name__} failed with exception: {e}")
        
        # 결과 요약
        return self.generate_report()
    
    def generate_report(self) -> Dict:
        """테스트 리포트 생성"""
        passed = sum(1 for r in self.test_results if r['passed'])
        total = len(self.test_results)
        
        report = {
            "test_summary": {
                "total_tests": total,
                "passed": passed,
                "failed": total - passed,
                "success_rate": (passed / total * 100) if total > 0 else 0,
                "duration_seconds": (datetime.now() - self.start_time).total_seconds()
            },
            "test_results": self.test_results
        }
        
        return report
    
    def print_report(self, report: Dict):
        """리포트 출력"""
        print("\n" + "=" * 80)
        print("TEST RESULTS SUMMARY")
        print("=" * 80)
        
        summary = report['test_summary']
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['passed']}")
        print(f"Failed: {summary['failed']}")
        print(f"Success Rate: {summary['success_rate']:.1f}%")
        print(f"Duration: {summary['duration_seconds']:.2f} seconds")
        
        if summary['failed'] == 0:
            print("\n✓ ALL TESTS PASSED!")
        else:
            print(f"\n✗ {summary['failed']} test(s) failed")


def main():
    """메인 실행 함수"""
    # 테스트 실행
    tester = ACTFIntegrationTest()
    report = tester.run_all_tests()
    tester.print_report(report)
    
    # JSON 형식 리포트 저장
    report_filename = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_filename, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n리포트가 저장되었습니다: {report_filename}")
    
    # 시각화 생성
    print("\n" + "="*80)
    print("Generating Visualizations...")
    print("="*80)
    
    visualizer = ACTFVisualizer(output_dir="./visualizations")
    
    # 시스템 데이터 수집
    actf = ACTFMainController()
    actf.initialize()
    diagnosis = actf.diagnose()
    
    # 줄기세포 배양 시스템 데이터
    cultivation = StemCellCultivationSystem()
    stem_status = cultivation.get_system_status()
    
    # BCI 데이터
    bci = BrainComputerInterface()
    bci.register_neural_interface("MAIN_INTERFACE")
    bci.initialize_interfaces()
    bci_status = bci.get_full_status()
    
    # 모든 시각화 생성
    visualizer.generate_all_visualizations(
        diagnosis=diagnosis,
        stem_status=stem_status,
        bci_status=bci_status
    )
    
    print("\n✓ All visualizations completed successfully!")


if __name__ == "__main__":
    main()
