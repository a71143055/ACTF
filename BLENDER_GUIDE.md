# ACTF Blender 시각화 가이드

ACTF (Android Cyborg Transformers) 시스템의 3D 모델을 Blender로 시각화하는 방법에 대한 완전한 가이드입니다.

## 📋 전체 실행 단계

### 1. ACTF 시스템 실행

```bash
cd "c:\Users\USER\OneDrive\바탕 화면\ACTF"
python actf_main.py
```

이 명령은 ACTF 메인 시스템을 초기화하고 시스템 진단 리포트를 출력합니다.

### 2. 통합 테스트 실행

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
- 모든 시각화 생성 (PNG 파일)

테스트 결과는 `test_report_[timestamp].json` 파일로 저장됩니다.

### 3. Blender용 3D 모델 내보내기

```bash
python blender_export.py
```

이 명령은 다음 파일을 `blender_exports/` 폴더에 생성합니다:
- `exoskeleton.obj` - 외골격 3D 모델
- `exoskeleton_metadata.json` - 외골격 메타데이터
- `endoskeleton.obj` - 내골격 3D 모델
- `endoskeleton_metadata.json` - 내골격 메타데이터

### 4. Blender로 모델 가져오기

#### 방법 A: 자동화 스크립트 사용 (권장)

1. Blender를 엽니다
2. 상단 탭에서 **Scripting** 워크스페이스를 선택합니다
3. **Open** 버튼을 클릭하고 `blender_import_script.py` 파일을 선택합니다
4. 스크립트 상단의 `import_path` 변수가 올바른 경로인지 확인합니다:
   ```python
   import_path = r"c:\Users\USER\OneDrive\바탕 화면\ACTF\blender_exports"
   ```
5. **Run Script** 버튼 (▶)을 클릭합니다

스크립트가 자동으로 다음을 설정합니다:
- 장면 초기화 (기본 큐브 삭제)
- 전문가급 조명 설정 (Key Light, Fill Light, Rim Light, Ambient Light)
- 카메라 설정
- 지면 평면
- 월드 환경 설정
- 렌더 설정
- OBJ 모델 가져오기 및 재질 적용

#### 방법 B: 수동 가져오기

1. Blender를 엽니다
2. **File > Import > Wavefront (.obj)**를 선택합니다
3. `blender_exports/exoskeleton.obj` 파일을 선택합니다
4. 동일한 과정으로 `endoskeleton.obj`를 가져옵니다
5. 재질을 수동으로 설정합니다

### 5. Blender에서 렌더링

자동화 스크립트를 사용한 경우:
1. **Z** 키를 눌러 렌더 모드로 전환합니다
2. **F12** 키를 눌러 렌더링합니다
3. 렌더링된 이미지를 저장하려면 **Image > Save As**를 선택합니다

## 🎨 Blender 기본 조작

- **G**: 객체 이동 (Grab)
- **R**: 객체 회전 (Rotate)
- **S**: 객체 크기 조절 (Scale)
- **X/Y/Z**: 축 제한 (G, R, S 후에 누름)
- **Tab**: 편집 모드/오브젝트 모드 전환
- **Z**: 쉐이딩 모드 전환
- **N**: 속성 패널 토글
- **T**: 툴셸프 토글

## 📁 프로젝트 구조

```
ACTF/
├── actf_main.py                 # 메인 시스템 모듈
├── neural_interface.py          # 신경 인터페이스 모듈
├── stem_cell_cultivation.py     # 줄기세포 배양 모듈
├── visualization.py             # 2D 시각화 모듈 (matplotlib)
├── blender_export.py            # Blender용 3D 내보내기 모듈
├── blender_import_script.py     # Blender 가져오기 스크립트
├── test_integration.py          # 통합 테스트 스크립트
├── visualizations/              # 2D 시각화 출력 폴더
│   ├── system_architecture.png
│   ├── exoskeleton_structure.png
│   ├── biological_systems.png
│   ├── stem_cell_cultivation.png
│   └── system_status_dashboard.png
├── blender_exports/             # Blender용 3D 모델 출력 폴더
│   ├── exoskeleton.obj
│   ├── exoskeleton_metadata.json
│   ├── endoskeleton.obj
│   └── endoskeleton_metadata.json
└── test_report_*.json           # 테스트 리포트 파일들
```

## 🔧 문제 해결

### OBJ 파일이 Blender로 가져오지 않는 경우

1. `blender_exports/` 폴더가 존재하는지 확인합니다
2. OBJ 파일이 실제로 생성되었는지 확인합니다
3. Blender 스크립트의 `import_path`가 올바른지 확인합니다

### 재질이 올바르게 적용되지 않는 경우

Blender 스크립트는 Eevee 렌더 엔진을 사용합니다. Cycles를 사용하려면 스크립트에서 다음을 수정합니다:

```python
bpy.context.scene.render.engine = 'CYCLES'
```

### 조명이 너무 밝거나 어두운 경우

`blender_import_script.py`에서 조명 강도를 조절합니다:

```python
key_light.data.energy = 3.0  # 값을 조절
fill_light.data.energy = 1.5  # 값을 조절
```

## 🎯 빠른 시작 (한 번에 모두 실행)

모든 단계를 한 번에 실행하려면:

```bash
# 1. 시스템 테스트 및 2D 시각화 생성
python test_integration.py

# 2. Blender용 3D 모델 내보내기
python blender_export.py

# 3. Blender 열고 스크립트 실행
# (Blender에서 blender_import_script.py 실행)
```

## 📊 생성된 파일 설명

### 2D 시각화 (visualization.py)
- **system_architecture.png**: 전체 시스템 아키텍처 다이어그램
- **exoskeleton_structure.png**: 외골격 구조 및 사양
- **biological_systems.png**: 내골격 생물학적 시스템
- **stem_cell_cultivation.png**: 줄기세포 배양 시스템 상태
- **system_status_dashboard.png**: 시스템 상태 대시보드

### 3D 모델 (blender_export.py)
- **exoskeleton.obj**: 외골격 3D 메쉬 (머리, 목, 몸통, 팔, 다리)
- **endoskeleton.obj**: 내골격 3D 메쉬 (뇌, 심장, 폐, 척추, 근육)

## 🎨 색상 스킴

Blender에서 사용되는 색상:

- **외골격**: #FF6B6B (빨간색)
- **내골격**: #4ECDC4 (청록색)
- **신경계**: #95E1D3 (연두색)
- **순환계**: #FF6B9D (분홍색)
- **호흡계**: #A8E6CF (연두색)
- **근육계**: #FFD3B6 (주황색)
- **감각계**: #FFAAA5 (연분홍색)
- **내분비계**: #FF8B94 (진분홍색)

## 📝 추가 정보

- **Blender 버전 요구사항**: Blender 3.0 이상
- **Python 버전**: Python 3.8 이상
- **OBJ 형식**: Wavefront OBJ (가장 널리 지원되는 3D 형식)
- **재질**: Blender Principled BSDF (PBR 기반)

---

작성일: 2026년 5월 19일
ACTF 프로젝트
