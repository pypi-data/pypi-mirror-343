# py-sodas-sdk

SODAS 프레임워크를 위한 공식 Python SDK입니다.
이 SDK를 통해 데이터셋의 메타데이터를 효율적으로 관리하고 표준화된 방식으로 처리할 수 있습니다.
DCAT(Data Catalog Vocabulary) 표준을 기반으로 하여 데이터셋의 메타데이터를 체계적으로 관리할 수 있습니다.

## 설치 방법

```bash
pip install py-sodas-sdk
```

## 주요 기능

- 데이터셋 메타데이터 생성 및 관리 (DCAT 기반)
- 다국어 메타데이터 지원 (제목, 설명, 키워드 등)
- 프로파일 기반의 메타데이터 스키마 관리
- 리소스 설명자를 통한 데이터 리소스 관리
- 버전 관리 및 이력 추적

## 핵심 컴포넌트

### API 초기화

SDK를 사용하기 전에 반드시 API URL을 초기화해야 합니다:

```python
from sodas_sdk import configure_api_url

DATAHUB_API_URL = "http://sodas-profile.example.com"
GOVERNANCE_API_URL = "http://api.example.com"

configure_api_url(DATAHUB_API_URL, GOVERNANCE_API_URL)
```

### Dataset

데이터셋의 메타데이터를 관리하는 핵심 클래스입니다.

```python
from sodas_sdk import Dataset,Distribution

dataset = Dataset()
# 기본 메타데이터 설정
dataset.set_title("데이터셋 제목")
dataset.set_description("데이터셋 설명")

# 다국어 지원
dataset.set_title("English Title", "en")
dataset.set_description("English Description", "en")

# 기타 메타데이터
dataset.type = "http://purl.org/dc/dcmitype/Dataset"
dataset.access_rights = "http://purl.org/eprint/accessRights/OpenAccess"
dataset.lincense = "http://creativecommons.org/licenses/by/4.0/"\

# 디스트리뷰션
distribution = dataset.create_distribution()
distribution.set_title("디스트리뷰션 제목")
distribution.set_description("디스트리뷰션 설명")
# 파일을 업로드하는 경우
if file exists:
    distribution.set_uploading_data("상대경로")
# download_url이 존재하는 경우
if downlod url exists:
    distribution.download_url = "https://DOWNLOAD_URL"

#만약 버킷 정보를 입력하고 싶으면 다음과 같이 합니다.
Distribution.configure_bucket_name("bucket")
# dataset에서 db_record api를 호출하면 distribution은 자동호출됩니다.
await dataset.create_db_record()
# dataset과 distribution은 백엔드와 통신 후 정보를 업데이트합니다.
# 파일 설정시 파일을 업로드하고 download_url이 생깁니다.
downnload_url = distribution.download_url
```

### DatasetSeries

데이터셋들의 집합을 관리합니다.
데이터셋은 단 하나의 데이터셋 시리즈에만 들어갈 수 있으며(1:N),
현재는 데이터셋 시리즈는 데이터셋 시리즈에 들어가지 못합니다.

```python
from sodas_sdk import DatasetSeries
# 처음 데이터 활용
creating_series = DatasetSeries()

dataset1 = await Dataset.get_db_record(dataset1_ID)
dataset2 = await Dataset.get_db_record(dataset2_ID)

creating_series.append_series_member(dataset1)
creating_series.append_series_member(dataset2)

await creating_series.create_db_record()

# 이후 만들어진 데이터셋 시리즈 활용. create_db_record 이후 똑같은 프로세스로 활용 가능합니다.
updating_series = await DatasetSeries.get_db_record(existing_series.id)
appending_dataset = await Dataset.get_db_record(exsiting_dataset.id)
updating_series.append_series_member(appending_dataset)

await updating_series.update_db_record()
```

### Profile

```python
from sodas_sdk import Profile,Dataset
# 처음 데이터 활용
existing_dataset = await Dataset.get_db_record(existing_dataset_id)

dcatProfile = await Profile.get_db_record(exsiting_dataset.profile_iri)
dataProfile = await Profile.get_db_record(existing_dataset.conforms_to)

mapping_value = dataProfile.get_template_descriptor_value_of_role(ResourceDescriptorRole.MAPPING)
schema_value = dataProfile.get_template_descriptor_value_of_role(ResourceDescriptorRole.SCHEMA)
```

### ResourceDescriptor

데이터 리소스의 구조와 특성을 기술하는 클래스입니다.
