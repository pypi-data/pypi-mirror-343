#!/bin/bash

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 현재 디렉토리 경로
CURRENT_DIR=$(pwd)

# 로고 출력
echo -e "${GREEN}"
echo "  ____                          __  __ _           _ "
echo " / ___|  ___ _ ____   _____ _ __|  \/  (_)_ __   __| |"
echo " \\___ \\ / _ \\ '_ \\ \\ / / _ \\ '__| |\/| | | '_ \\ / _\` |"
echo "  ___) |  __/ | | \\ V /  __/ |  | |  | | | | | | (_| |"
echo " |____/ \\___|_| |_|\\_/ \\___|_|  |_|  |_|_|_| |_|\\__,_|"
echo -e "${NC}"
echo "ServerMind CLI v0.2 실행 스크립트"
echo "================================="

# 가상환경 확인 및 활성화 함수
activate_environment() {
    # local venv 환경 확인
    if [ -d "$CURRENT_DIR/venv" ]; then
        echo -e "${GREEN}로컬 가상환경을 활성화합니다...${NC}"
        source "$CURRENT_DIR/venv/bin/activate"
        VENV_TYPE="venv"
        return 0
    fi
    
    # conda 환경 확인
    if command -v conda &> /dev/null; then
        if conda env list | grep -q "^servermind "; then
            echo -e "${GREEN}conda 환경을 활성화합니다...${NC}"
            source "$(conda info --base)/etc/profile.d/conda.sh"
            conda activate servermind
            VENV_TYPE="conda"
            return 0
        fi
    fi
    
    # 가상환경이 없는 경우
    return 1
}

# 가상환경 활성화
if ! activate_environment; then
    # 가상환경이 없는 경우 설치 스크립트 실행
    echo -e "${YELLOW}가상환경이 존재하지 않습니다. 설치를 시작합니다...${NC}"
    
    if [ -f "$CURRENT_DIR/install.sh" ]; then
        chmod +x "$CURRENT_DIR/install.sh"
        "$CURRENT_DIR/install.sh"
        
        # 설치 후 다시 활성화 시도
        if ! activate_environment; then
            echo -e "${RED}가상환경 활성화에 실패했습니다.${NC}"
            exit 1
        fi
    else
        echo -e "${RED}설치 스크립트(install.sh)를 찾을 수 없습니다.${NC}"
        exit 1
    fi
fi

# 가상환경이 성공적으로 활성화되었는지 확인
if [ "$VENV_TYPE" = "venv" ]; then
    echo -e "${GREEN}✓ 가상환경(venv)이 성공적으로 활성화되었습니다.${NC}"
elif [ "$VENV_TYPE" = "conda" ]; then
    echo -e "${GREEN}✓ conda 환경(servermind)이 성공적으로 활성화되었습니다.${NC}"
fi

# Python 버전 출력
PYTHON_VERSION=$(python --version)
echo -e "${BLUE}사용 중인 Python: $PYTHON_VERSION${NC}"

# 환경 변수 확인
if [ -f "$CURRENT_DIR/.env" ]; then
    echo -e "${GREEN}✓ .env 파일이 존재합니다.${NC}"
else
    echo -e "${YELLOW}⚠ .env 파일이 없습니다. API 키 설정이 필요할 수 있습니다.${NC}"
fi

# 사용 방법 안내
echo -e "\n${YELLOW}사용 방법:${NC}"
echo -e "  ${GREEN}기본 사용법:${NC}"
echo -e "    servermind \"현재 폴더 확인\""
echo -e "    bs \"현재 폴더 확인\""
echo -e "  ${GREEN}옵션 사용법:${NC}"
echo -e "    servermind --preview \"모든 로그 파일 삭제\""
echo -e "    servermind --no-explain \"디스크 사용량 확인\""

echo -e "\n${GREEN}ServerMind CLI를 사용할 준비가 되었습니다!${NC}"
echo -e "${YELLOW}이 터미널 세션에서 명령어를 실행해 보세요.${NC}" 