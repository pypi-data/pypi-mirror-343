import re
from logger import log_command

# 위험한 명령어 패턴 목록
DANGEROUS_PATTERNS = [
    r"rm\s+-rf\s+/", r"shutdown", r"reboot", r":\(\)\s*{\s*:.*};",
    r"mkfs", r"dd\s+if=", r"mv\s+/", r">\s+/dev/sda", r"chmod\s+000"
]

def is_dangerous_command(command):
    """명령어가 위험한지 검사합니다."""
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, command):
            return True
    return False

def filter_commands(input_text, commands, force=False):
    """
    명령어 목록을 검사하고 위험한 명령어가 있는지 확인합니다.
    
    Args:
        input_text (str): 원본 자연어 입력
        commands (list): 변환된 명령어 목록
        force (bool): --yes 플래그 여부
        
    Returns:
        tuple: (안전한지 여부, 명령어 목록)
    """
    dangerous_commands = []
    
    # 단일 명령어를 리스트로 변환
    if isinstance(commands, str):
        commands = [commands]
    
    # 각 명령어 검사
    for cmd in commands:
        if is_dangerous_command(cmd):
            log_command(input_text, cmd, is_dangerous=True)
            dangerous_commands.append(cmd)
    
    # 위험한 명령어가 있고 force가 False면 실행 불가
    if dangerous_commands and not force:
        return False, dangerous_commands
    
    return True, commands 