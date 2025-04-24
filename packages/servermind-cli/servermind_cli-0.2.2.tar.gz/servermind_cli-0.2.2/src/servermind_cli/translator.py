import json
import re
import openai
from config import OPENAI_API_KEY, GPT_MODEL
from logger import log_error

# OpenAI API 키 설정
openai.api_key = OPENAI_API_KEY

def translate_to_command(input_text):
    """
    자연어를 리눅스 명령어로 변환합니다.
    
    Args:
        input_text (str): 자연어 입력
        
    Returns:
        list: 변환된 명령어 목록
    """
    try:
        # GPT 프롬프트 구성
        prompt = f"""다음 문장을 Linux 명령으로 변환해줘. 

규칙:
1. 설명 없이 오직 명령어만 제공할 것
2. 코드 블록(```)을 사용하지 말 것
3. 명령이 하나 이상일 경우 줄바꿈(\\n)으로 구분하거나 JSON 배열로 제공할 것
4. 명령어는 셸에서 바로 실행 가능한 형태여야 함

입력자 문장: {input_text}"""
        
        # OpenAI API 호출
        response = openai.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": "당신은 자연어를 정확한 리눅스 명령어로 변환하는 도우미입니다. 형식에 맞게 명령어만 출력하세요."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=300
        )
        
        # 응답에서 명령어 추출
        output = response.choices[0].message.content.strip()
        
        # 명령어 파싱
        return parse_commands(output)
    
    except Exception as e:
        log_error(f"명령어 변환 중 오류 발생: {str(e)}")
        return []

def parse_commands(output):
    """
    GPT 응답에서 명령어를 파싱합니다.
    JSON 형식 또는 줄바꿈으로 구분된 명령어를 처리합니다.
    
    Args:
        output (str): GPT 응답
        
    Returns:
        list: 명령어 목록
    """
    # 마크다운 코드 블록 제거
    output = re.sub(r"```(?:bash|shell)?|```", "", output).strip()
    
    # 문자열에 포함된 \n을 실제 줄바꿈으로 변환
    output = output.replace('\\n', '\n')
    
    # JSON 형식인지 확인
    try:
        json_data = json.loads(output)
        if isinstance(json_data, list):
            return json_data
        return [output]
    except json.JSONDecodeError:
        pass
    
    # 줄바꿈으로 구분된 명령어 처리
    return parse_multi_commands(output)

def parse_multi_commands(output):
    """
    줄바꿈으로 구분된 명령어를 처리합니다.
    번호가 붙은 단계별 명령어 (예: 1. git clone...)도 처리합니다.
    
    Args:
        output (str): 줄바꿈으로 구분된 명령어
        
    Returns:
        list: 명령어 목록
    """
    lines = output.strip().split("\n")
    cmds = []
    for line in lines:
        line = line.strip()
        if line == "" or line.startswith("```") or line == "```": 
            continue
        # 번호가 붙은 형식 제거 (예: "1. git clone" -> "git clone")
        line = re.sub(r"^\d+\.\s*", "", line)
        cmds.append(line.strip())
    
    # 빈 명령어 항목 제거
    return [cmd for cmd in cmds if cmd] 