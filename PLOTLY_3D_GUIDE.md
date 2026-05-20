# ACTF Plotly 3D 시각화 가이드

ACTF (Android Cyborg Transformers) 시스템의 3D 모델을 Plotly로 시각화하는 방법에 대한 완전한 가이드입니다.

## 📋 전체 실행 단계

### 1. Plotly 설치

```bash
pip install plotly
```

### 2. ACTF 시스템 실행

```bash
cd "c:\Users\USER\OneDrive\바탕 화면\ACTF"
python actf_main.py
```

이 명령은 ACTF 메인 시스템을 초기화하고 시스템 진단 리포트를 출력합니다.

### 3. 통합 테스트 실행 (Plotly 3D 포함)

```bash
python test_integration.py
```

이 명령은 다음을 수행합니다:
- 외골격 시스템 초기화 테스트
- 내골격 시스템 초기화 테스트
- 전체 시스템 초기화 테스트
- 줄기세포 배양 시스템 테스트
- 신경 인터페이스 테스트
- 시스템 진단 테스트
- 2D 시각화 생성 (PNG 파일)
- **Plotly 3D 시각화 생성 (HTML 파일)**

테스트 결과는 `test_report_[timestamp].json` 파일로 저장됩니다.

### 4. Plotly 3D 시각화만 생성

```bash
python plotly_3d_viz.py
```

이 명령은 다음 HTML 파일들을 `plotly_3d/` 폴더에 생성합니다:
- `exoskeleton_3d.html` - 외골격 3D 모델
- `endoskeleton_3d.html` - 내골격 3D 모델
- `complete_system_3d.html` - 전체 시스템 3D 모델

### 5. 3D 시각화 보기

생성된 HTML 파일을 웹 브라우저로 엽니다:
- Chrome, Firefox, Edge, Safari 등 어떤 브라우저든 가능
- 파일을 더블 클릭하거나 브라우저로 드래그 앤 드롭

## 🎨 Plotly 3D 인터랙티브 기능

HTML 파일을 브라우저에서 열면 다음 기능을 사용할 수 있습니다:

- **회전**: 마우스로 드래그하여 3D 모델 회전
- **줌**: 마우스 휠로 줌 인/아웃
- **패닝**: 마우스 오른쪽 버튼으로 드래그하여 이동
- **호버**: 부품 위에 마우스를 올리면 이름 표시
- **범례 클릭**: 특정 부품 표시/숨기기

## 📁 프로젝트 구조

```
ACTF/
├── actf_main.py                 # 메인 시스템 모듈
├── neural_interface.py          # 신경 인터페이스 모듈
├── stem_cell_cultivation.py     # 줄기세포 배양 모듈
├── visualization.py             # 2D 시각화 모듈 (matplotlib)
├── plotly_3d_viz.py             # Plotly 3D 시각화 모듈
├── test_integration.py          # 통합 테스트 스크립트
├── visualizations/              # 2D 시각화 출력 폴더
│   ├── system_architecture.png
│   ├── exoskeleton_structure.png
│   ├── biological_systems.png
│   ├── stem_cell_cultivation.png
│   └── system_status_dashboard.png
├── plotly_3d/                   # Plotly 3D 시각화 출력 폴더
│   ├── exoskeleton_3d.html
│   ├── endoskeleton_3d.html
│   └── complete_system_3d.html
└── test_report_*.json           # 테스트 리포트 파일들
```

## 🔧 Plotly vs Blender 장단점

### Plotly 장점
- ✅ 브라우저에서 바로 실행 (별도 소프트웨어 불필요)
- ✅ 인터랙티브 3D (회전, 줌, 패닝)
- ✅ HTML 파일로 공유 용이
- ✅ 설치가 간단 (pip install plotly)
- ✅ Python 코드로 직접 제어 가능
- ✅ 가벼움 (빠른 로딩)

### Blender 장점
- ✅ 전문가급 3D 모델링
- ✅ 고급 렌더링 (Cycles, Eevee)
- ✅ 애니메이션 지원
- ✅ 물리 시뮬레이션
- ✅ 더 정교한 모델링 도구

### Plotly 단점
- ❌ Blender만큼 정교한 모델링 불가
- ❌ 고급 렌더링 기능 부족
- ❌ 애니메이션 제한적

### Blender 단점
- ❌ 대형 소프트웨어 (설치 필요)
- ❌ 학습 곡선이 높음
- ❌ Python 스크립트로 자동화 필요

## 📊 생성된 파일 설명

### 2D 시각화 (visualization.py)
- **system_architecture.png**: 전체 시스템 아키텍처 다이어그램
- **exoskeleton_structure.png**: 외골격 구조 및 사양
- **biological_systems.png**: 내골격 생물학적 시스템
- **stem_cell_cultivation.png**: 줄기세포 배양 시스템 상태
- **system_status_dashboard.png**: 시스템 상태 대시보드

### 3D 시각화 (plotly_3d_viz.py)
- **exoskeleton_3d.html**: 외골격 3D 모델 (머리, 목, 몸통, 팔, 다리)
- **endoskeleton_3d.html**: 내골격 3D 모델 (뇌, 심장, 폐, 척추, 근육)
- **complete_system_3d.html**: 전체 시스템 3D 모델 (외골격 + 내골격)

## 🎨 색상 스킴

Plotly 3D에서 사용되는 색상:

- **외골격**: #FF6B6B (빨간색)
- **내골격**: #4ECDC4 (청록색)
- **신경계**: #95E1D3 (연두색)
- **순환계**: #FF6B9D (분홍색)
- **호흡계**: #A8E6CF (연두색)
- **근육계**: #FFD3B6 (주황색)
- **감각계**: #FFAAA5 (연분홍색)
- **내분비계**: #FF8B94 (진분홍색)

## 🎯 빠른 시작 (한 번에 모두 실행)

모든 단계를 한 번에 실행하려면:

```bash
# Plotly 설치 (처음 한 번만)
pip install plotly

# 시스템 테스트 및 모든 시각화 생성 (2D + 3D)
python test_integration.py
```

또는 3D 시각화만:

```bash
python plotly_3d_viz.py
```

## 🔍 문제 해결

### Plotly가 설치되지 않은 경우

```bash
pip install plotly
```

### HTML 파일이 열리지 않는 경우

1. 파일이 실제로 생성되었는지 확인
2. 브라우저가 HTML 파일을 지원하는지 확인
3. 파일을 다른 브라우저로 열어보기

### 3D 모델이 너무 느린 경우

- 브라우저를 최신 버전으로 업데이트
- GPU 가속이 활성화되어 있는지 확인
- 다른 브라우저 시도 (Chrome 권장)

### 색상이 올바르게 표시되지 않는 경우

`plotly_3d_viz.py`의 `color_scheme` 딕셔너리를 확인하고 수정합니다.

## 📝 추가 정보

- **Plotly 버전 요구사항**: Plotly 5.0 이상
- **Python 버전**: Python 3.8 이상
- **브라우저 호환성**: Chrome, Firefox, Edge, Safari (최신 버전 권장)
- **파일 형식**: HTML (모든 브라우저에서 지원)

## 🚀 고급 사용법

### Python 코드에서 직접 3D 시각화 생성

```python
from plotly_3d_viz import Plotly3DVisualizer

# 시각화 도구 생성
visualizer = Plotly3DVisualizer(output_dir="./my_3d_viz")

# 특정 시각화만 생성
visualizer.visualize_exoskeleton_3d()
visualizer.visualize_endoskeleton_3d()
visualizer.visualize_complete_system_3d()
```

### Jupyter Notebook에서 사용

```python
from plotly_3d_viz import Plotly3DVisualizer
import plotly.graph_objects as go

visualizer = Plotly3DVisualizer()
fig = visualizer.visualize_exoskeleton_3d()
fig.show()  # Jupyter에서 직접 표시
```

### 색상 스킴 커스터마이징

```python
visualizer = Plotly3DVisualizer()
visualizer.color_scheme["exoskeleton"] = "#00FF00"  # 녹색으로 변경
visualizer.visualize_exoskeleton_3d()
```

---

작성일: 2026년 5월 21일
ACTF 프로젝트
