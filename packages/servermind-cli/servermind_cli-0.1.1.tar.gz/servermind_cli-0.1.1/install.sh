#!/bin/bash

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 로고 출력
echo -e "${GREEN}"
echo "  ____                          __  __ _           _ "
echo " / ___|  ___ _ ____   _____ _ __|  \/  (_)_ __   __| |"
echo " \\___ \\ / _ \\ '_ \\ \\ / / _ \\ '__| |\/| | | '_ \\ / _\` |"
echo "  ___) |  __/ | | \\ V /  __/ |  | |  | | | | | | (_| |"
echo " |____/ \\___|_| |_|\\_/ \\___|_|  |_|  |_|_|_| |_|\\__,_|"
echo -e "${NC}"
echo "ServerMind CLI v0.2 설치 스크립트"
echo "================================="

CURRENT_DIR=$(pwd)

# 기존 설치 확인 및 제거
check_existing_installation() {
    echo -e "${YELLOW}[0/7] 기존 설치 확인 중...${NC}"
    local commands=("servermind" "bs")
    local installation_found=false
    
    # 기존 심볼릭 링크 확인
    for cmd in "${commands[@]}"; do
        if [ -f "/usr/local/bin/$cmd" ]; then
            installation_found=true
            echo -e "${YELLOW}기존 $cmd 설치가 발견되었습니다.${NC}"
        fi
    done

    # 기존 가상환경 확인
    if [ -d "$CURRENT_DIR/venv" ]; then
        installation_found=true
        echo -e "${YELLOW}기존 가상환경이 발견되었습니다.${NC}"
    fi

    # conda 환경 확인
    if command -v conda &> /dev/null; then
        if conda env list | grep -q "^servermind "; then
            installation_found=true
            echo -e "${YELLOW}기존 conda 환경이 발견되었습니다.${NC}"
        fi
    fi

    if [ "$installation_found" = true ]; then
        echo -e "${YELLOW}기존 설치를 제거하시겠습니까? (y/n)${NC}"
        read -r response
        if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            remove_existing_installation
        else
            echo -e "${YELLOW}기존 설치를 유지합니다. 일부 문제가 발생할 수 있습니다.${NC}"
        fi
    else
        echo -e "${GREEN}기존 설치가 없습니다. 새로 설치를 진행합니다.${NC}"
    fi
}

# 기존 설치 제거
remove_existing_installation() {
    echo -e "${YELLOW}기존 설치 제거 중...${NC}"
    
    # 심볼릭 링크 제거
    for cmd in servermind bs; do
        if [ -f "/usr/local/bin/$cmd" ]; then
            echo -e "${YELLOW}$cmd 심볼릭 링크 제거 중...${NC}"
            sudo rm "/usr/local/bin/$cmd"
        fi
    done
    
    # 가상환경 제거
    if [ -d "$CURRENT_DIR/venv" ]; then
        echo -e "${YELLOW}가상환경 제거 중...${NC}"
        rm -rf "$CURRENT_DIR/venv"
    fi
    
    # conda 환경 제거
    if command -v conda &> /dev/null; then
        if conda env list | grep -q "^servermind "; then
            echo -e "${YELLOW}conda 환경 제거 중...${NC}"
            conda env remove -n servermind -y
        fi
    fi
    
    echo -e "${GREEN}기존 설치가 제거되었습니다.${NC}"
}

# conda 설치 확인
check_conda() {
    if command -v conda &> /dev/null; then
        return 0
    else
        return 1
    fi
}

# conda 환경 생성 및 활성화
setup_conda_env() {
    local env_name="servermind"
    echo -e "${YELLOW}conda 환경 생성 중...${NC}"

    if conda env list | grep -q "^$env_name "; then
        echo -e "${YELLOW}기존 conda 환경이 존재합니다. 삭제 중...${NC}"
        conda env remove -n $env_name -y
    fi

    conda create -n $env_name python=3.8 -y
    source $(conda info --base)/etc/profile.d/conda.sh
    conda activate $env_name

    VENV_PATH="$(conda info --base)/envs/$env_name"
    echo -e "${GREEN}conda 환경 생성 완료${NC}"
}

# 기존 설치 확인 및 제거
check_existing_installation

# [1/7] Python 버전 확인
echo -e "${YELLOW}[1/7] Python 버전 확인 중...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3가 설치되어 있지 않습니다.${NC}"
    if check_conda; then
        echo -e "${YELLOW}conda를 사용하여 Python 3.8을 설치합니다.${NC}"
        setup_conda_env
    else
        echo -e "${RED}Python 3.8 이상이 필요하며 설치할 수 있는 방법이 없습니다. conda 또는 pyenv 설치를 권장합니다.${NC}"
        exit 1
    fi
else
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    if [[ $(echo "$PYTHON_VERSION 3.8" | awk '{if ($1 < $2) print 1; else print 0}') -eq 1 ]]; then
        echo -e "${RED}Python 3.8 이상이 필요합니다. 현재 버전: $PYTHON_VERSION${NC}"
        if check_conda; then
            echo -e "${YELLOW}conda를 사용하여 Python 3.8을 설치합니다.${NC}"
            setup_conda_env
        else
            echo -e "${RED}Python 3.8 이상이 필요하며 설치할 수 있는 방법이 없습니다. conda 또는 pyenv 설치를 권장합니다.${NC}"
            exit 1
        fi
    else
        echo -e "${GREEN}Python $PYTHON_VERSION 확인 완료${NC}"
        VENV_PATH="$CURRENT_DIR/venv"
    fi
fi

# [2/7] 가상환경 생성
if [[ "$VENV_PATH" == "$CURRENT_DIR/venv" ]]; then
    echo -e "${YELLOW}[2/7] venv 가상환경 생성 중...${NC}"
    if ! python3 -m venv venv; then
        echo -e "${RED}venv 생성 실패${NC}"
        exit 1
    fi
    source venv/bin/activate
    echo -e "${GREEN}venv 가상환경 생성 완료${NC}"
else
    echo -e "${GREEN}conda 환경 활성화됨: $VENV_PATH${NC}"
fi

# [3/7] 패키지 설치
echo -e "${YELLOW}[3/7] 필요한 패키지 설치 중...${NC}"
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}패키지 설치 완료${NC}"

# [4/7] 실행 권한 설정
echo -e "${YELLOW}[4/7] 실행 권한 설정 중...${NC}"
chmod +x main.py
echo -e "${GREEN}main.py 실행 권한 설정 완료${NC}"

# [5/7] 실행 스크립트 생성
echo -e "${YELLOW}[5/7] 실행 스크립트 생성 중...${NC}"

# conda 환경과 일반 가상환경에 따라 다른 스크립트 생성
if [[ "$VENV_PATH" == "$CURRENT_DIR/venv" ]]; then
    # 일반 venv 가상환경용 스크립트
    SCRIPT_CONTENT=$(cat << 'EOL'
#!/bin/bash
# 현재 스크립트의 디렉토리 경로
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# 가상환경 활성화
source "$SCRIPT_DIR/activate"
# main.py 실행
exec python "$SCRIPT_DIR/../../main.py" "$@"
EOL
)
else
    # conda 환경용 스크립트
    CONDA_BASE=$(conda info --base)
    SCRIPT_CONTENT=$(cat << EOL
#!/bin/bash
# conda 환경 활성화
source "${CONDA_BASE}/etc/profile.d/conda.sh"
conda activate servermind
# main.py 실행
exec python "${CURRENT_DIR}/main.py" "\$@"
EOL
)
fi

# 디렉토리 생성 확인
mkdir -p "$VENV_PATH/bin"

# servermind 스크립트 생성
echo -e "$SCRIPT_CONTENT" > "$VENV_PATH/bin/servermind"
chmod +x "$VENV_PATH/bin/servermind"

# bs 스크립트 생성 (동일한 내용)
echo -e "$SCRIPT_CONTENT" > "$VENV_PATH/bin/bs"
chmod +x "$VENV_PATH/bin/bs"

echo -e "${GREEN}실행 스크립트 생성 완료${NC}"

# [6/7] 심볼릭 링크 생성
echo -e "${YELLOW}[6/7] 심볼릭 링크 생성 중...${NC}"
for cmd in servermind bs; do
    if [ -f "/usr/local/bin/$cmd" ]; then
        echo -e "${YELLOW}기존 $cmd 심볼릭 링크 삭제 중...${NC}"
        sudo rm "/usr/local/bin/$cmd"
    fi
    sudo ln -s "$VENV_PATH/bin/$cmd" "/usr/local/bin/$cmd"
    sudo chmod +x "/usr/local/bin/$cmd"
done

echo -e "${GREEN}심볼릭 링크 생성 완료${NC}"

# [7/7] .env 설정
echo -e "${YELLOW}[7/7] 환경 설정 파일 확인 중...${NC}"
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}.env 파일이 없습니다. 생성 중...${NC}"
    cat > .env << EOL
# ServerMind 환경 설정
OPENAI_API_KEY=your_api_key_here
GPT_MODEL=gpt-4
LOG_FILE=history.log
DEFAULT_LANGUAGE=ko
EOL
    echo -e "${GREEN}.env 파일 생성 완료${NC}"
    echo -e "${YELLOW}OpenAI API 키를 .env 파일에 설정해주세요.${NC}"
else
    echo -e "${GREEN}.env 파일이 이미 존재합니다.${NC}"
    if ! grep -q "DEFAULT_LANGUAGE" .env; then
        echo -e "${YELLOW}DEFAULT_LANGUAGE 설정이 없습니다. 추가 중...${NC}"
        echo "DEFAULT_LANGUAGE=ko" >> .env
    fi
fi

# 완료 메시지
echo -e "\n${GREEN}ServerMind CLI v0.2 설치가 완료되었습니다!${NC}"
echo -e "${BLUE}새로운 기능: 명령어 실행 결과 해석 기능이 추가되었습니다.${NC}"
echo -e "\n${YELLOW}사용 방법:${NC}"
echo -e "  ${GREEN}기본 사용법:${NC}"
echo -e "    servermind \"현재 폴더 확인\""
echo -e "    bs \"현재 폴더 확인\""
echo -e "  ${GREEN}옵션 사용법:${NC}"
echo -e "    servermind --preview \"모든 로그 파일 삭제\""
echo -e "    servermind --yes \"위험한 명령어 실행\""
echo -e "    servermind --no-explain \"디스크 사용량 확인\""
echo -e "    servermind --preview --yes \"위험한 명령어 미리보기\""

if [[ "$VENV_PATH" == "$CURRENT_DIR/venv" ]]; then
    echo -e "\n${YELLOW}가상환경 관리:${NC}"
    echo -e "  ${GREEN}가상환경 활성화:${NC}"
    echo -e "    source venv/bin/activate"
    echo -e "  ${GREEN}가상환경 비활성화:${NC}"
    echo -e "    deactivate"
else
    echo -e "\n${YELLOW}conda 환경 관리:${NC}"
    echo -e "  ${GREEN}conda 환경 활성화:${NC}"
    echo -e "    conda activate servermind"
    echo -e "  ${GREEN}conda 환경 비활성화:${NC}"
    echo -e "    conda deactivate"
fi

echo -e "\n${YELLOW}문제가 발생한 경우:${NC}"
echo -e "  1. .env 파일에 OPENAI_API_KEY가 올바르게 설정되어 있는지 확인하세요."
echo -e "  2. 가상환경이 활성화되어 있는지 확인하세요."
echo -e "  3. ./install.sh 를 다시 실행하세요."
