import re
import openai
from config import OPENAI_API_KEY, GPT_MODEL
from logger import log_interpretation, log_error

# OpenAI API 키 설정
openai.api_key = OPENAI_API_KEY

def remove_markup(text):
    """
    텍스트에서 마크다운, HTML 등의 마크업을 제거합니다.
    
    Args:
        text (str): 마크업이 포함된 텍스트
        
    Returns:
        str: 마크업이 제거된 텍스트
    """
    if not text:
        return text
    
    # 마크다운 코드 블록 제거
    text = re.sub(r"```(\w*)\n(.*?)\n```", r"\2", text, flags=re.DOTALL)
    
    # 인라인 코드 형식 제거
    text = re.sub(r"`([^`]*)`", r"\1", text)
    
    # 볼드 및 이탤릭체 제거
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    
    # 링크 형식 제거 [텍스트](링크)
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
    
    # HTML 태그 제거
    text = re.sub(r"<[^>]*>", "", text)
    
    # 불필요한 여러 줄바꿈 제거
    text = re.sub(r"\n{3,}", "\n\n", text)
    
    return text.strip()

def interpret_output(command, stdout, stderr, exit_code, user_input=None):
    """
    명령어 실행 결과를 해석합니다.
    
    Args:
        command (str): 실행된 명령어
        stdout (str): 표준 출력
        stderr (str): 표준 에러
        exit_code (int): 종료 코드
        user_input (str, optional): 사용자가 입력한 원래 자연어 질의
        
    Returns:
        tuple: (해석된 결과, 추가 명령어 제안 목록)
    """
    try:
        # 빈 출력이면 해석 생략
        if not stdout and not stderr:
            if exit_code == 0:
                return ("명령이 성공적으로 실행되었으나 출력이 없습니다.", [])
            else:
                return (f"명령이 실패했습니다. 종료 코드: {exit_code}", [])

        # GPT 프롬프트 구성
        prompt = f"""다음은 리눅스 명령어 실행 결과입니다. 사람이 이해하기 쉬운 문장으로 요약해주세요.

"""
        # 사용자 입력이 있는 경우 추가
        if user_input:
            prompt += f"""사용자 질의: {user_input}

"""

        prompt += f"""명령어: {command}

표준 출력(STDOUT):
{stdout}

표준 에러(STDERR):
{stderr}

종료 코드: {exit_code}

주의사항:
1. 정보를 간결하고 명확하게 요약해주세요.
2. 기술적인 용어는 필요 시 쉽게 풀어서 설명해주세요.
3. 명령어가 실패했다면 실패 이유를 설명해주세요.
4. 사용자 질의가 있는 경우, 질의 내용에 맞게 결과를 맞춤형으로 해석해주세요.
5. 한국어로 응답해주세요.
6. 마크다운 형식이나 HTML 태그를 사용하지 마세요.

결과를 분석하고 난 후, 사용자가 추가로 수행할 수 있는 관련 명령어를 3개 이내로 제안해주세요. 제안할 명령어가 없으면 빈 목록을 반환하세요.

예시 형식:
---
<해석 텍스트>
---
추가 명령어:
1. <첫 번째 명령어 설명>: <명령어>
2. <두 번째 명령어 설명>: <명령어>
3. <세 번째 명령어 설명>: <명령어>
"""

        # OpenAI API 호출
        response = openai.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": "당신은 리눅스 명령어 실행 결과를 사람이 이해하기 쉽게 해석하는 도우미입니다. 사용자의 질의 내용과 실행 결과를 고려하여 맥락에 맞는 응답을 제공합니다. 마크다운 형식이나 HTML 태그를 사용하지 마세요. 또한 사용자가 추가로 수행할 수 있는 관련 명령어를 제안해주세요."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        # 응답에서 해석 추출
        full_response = response.choices[0].message.content.strip()
        
        # 마크업 제거
        full_response = remove_markup(full_response)
        
        # 해석과 추가 명령어 분리
        interpretation, suggested_commands = parse_interpretation_and_suggestions(full_response)
        
        # 해석 결과 로깅
        log_interpretation(command, stdout, stderr, exit_code, interpretation)
        
        return (interpretation, suggested_commands)
    
    except Exception as e:
        error_msg = f"결과 해석 중 오류 발생: {str(e)}"
        log_error(error_msg)
        return (f"결과 해석에 실패했습니다: {str(e)}", [])

def parse_interpretation_and_suggestions(text):
    """
    해석 텍스트와 추가 명령어 제안을 분리합니다.
    
    Args:
        text (str): GPT의 전체 응답 텍스트
        
    Returns:
        tuple: (해석 텍스트, 추가 명령어 목록)
    """
    # 추가 명령어 패턴
    if "추가 명령어:" in text:
        parts = text.split("추가 명령어:", 1)
        interpretation = parts[0].strip()
        
        # 추가 명령어 파싱
        suggestions_text = parts[1].strip()
        suggestions = []
        
        # 번호가 붙은 항목 찾기
        lines = suggestions_text.split('\n')
        current_desc = ""
        current_cmd = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 숫자로 시작하는 줄 찾기 (예: "1. 설명: 명령어")
            match = re.match(r'^\d+\.\s+(.*?):\s+(.*)$', line)
            if match:
                desc, cmd = match.groups()
                suggestions.append({"description": desc.strip(), "command": cmd.strip()})
            # 콜론으로 구분된 설명과 명령어
            elif ":" in line:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    desc, cmd = parts
                    suggestions.append({"description": desc.strip(), "command": cmd.strip()})
        
        return interpretation, suggestions
    else:
        return text, [] 