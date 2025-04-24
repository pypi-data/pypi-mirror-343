# ServerMind CLI v0.2

자연어 입력 기반 리눅스 명령어 변환 및 결과 해석 시스템

## 소개

ServerMind CLI는 개발자가 한국어 및 영어 등의 자연어를 입력하면, 이를 리눅스 명령어로 변환하고 실행하는 도구입니다. GPT API를 활용하여 자연어를 명령어로 변환하고, 위험한 명령어에 대한 검증을 수행합니다. v0.2부터는 명령어 실행 결과를 사람이 이해하기 쉬운 형태로 해석하는 기능이 추가되었습니다.

## 기능

- 자연어 입력을 리눅스 명령어로 변환
- 위험한 명령어 감지 및 차단 (--yes 옵션으로 강제 실행 가능)
- 명령어 미리보기 (--preview 옵션)
- 다단계 명령어 순차 실행
- 입력값/명령/결과 로깅
- **신규:** 명령어 실행 결과 자연어 해석 (--explain/--no-explain 옵션)

## 설치 방법

### 요구 사항

- Python 3.8 이상
- Ubuntu 20.04 이상 (다른 리눅스 배포판에서도 작동할 수 있음)

### 설치

```bash
# 저장소 클론
git clone https://github.com/bssoft/servermind.git
cd servermind

# 패키지 설치
pip install -r requirements.txt

# .env 파일 설정 (첫 실행 시 자동 생성)
# OpenAI API 키 설정 필요
```

## 사용 방법

```bash
# 기본 사용법 (결과 해석 포함)
servermind "현재 폴더 확인"
# 또는 (bs는 servermind의 별칭)
bs "현재 폴더 확인"

# 위험 명령어 미리보기
servermind --preview "모든 로그 파일 삭제"

# 위험 명령어 강제 실행
servermind --yes "모든 로그 파일 삭제"

# 다단계 명령어 예시
servermind "git clone 하고 cd 후 npm install"

# 해석 기능 비활성화
servermind --no-explain "디스크 사용량 확인"

# 여러 옵션 함께 사용
servermind --preview --yes "위험한 명령어 미리보기"
```

## 출력 예시

```
[INFO] 요청: '현재 디렉토리에 뭐가 있는지 보여줘'
[INFO] 변환된 명령어: 'ls -al'

[명령어 실행]
> ls -al

[실행 결과]
drwxr-xr-x 5 user user 4096 Apr 23 12:34 .
drwxr-xr-x 3 user user 4096 Apr 23 11:45 ..
-rwxr-xr-x 1 user user 2345 Apr 23 12:30 main.py
-rw-r--r-- 1 user user  243 Apr 23 12:15 .env
-rw-r--r-- 1 user user 1234 Apr 23 12:00 history.log

[결과 해석]
현재 디렉토리에는 숨김 폴더 두 개를 포함하여 총 5개의 항목이 있습니다. 주요 파일로는 'main.py' (실행 권한 있음), '.env' 및 'history.log' 등이 있습니다.
```

## 주의 사항

- 위험한 명령어는 기본적으로 차단됩니다. 강제 실행이 필요한 경우 `--yes` 옵션을 사용하세요.
- 항상 `--preview` 옵션으로 실행될 명령어를 미리 확인하는 것이 좋습니다.
- API 호출 비용이 발생할 수 있습니다.
- 결과 해석 기능은 기본적으로 활성화되어 있으며, 비활성화하려면 `--no-explain` 옵션을 사용하세요.
- **중요:** 옵션(--preview, --yes, --no-explain 등)은 항상 명령어 텍스트 앞에 위치해야 합니다.

## 로그 확인

명령어 실행 기록은 `history.log` 파일에 저장됩니다. 로그 위치는 `.env` 파일에서 변경할 수 있습니다.
v0.2부터는 명령어 실행 결과 해석도 로그에 포함됩니다.

## 라이선스

MIT 라이선스 