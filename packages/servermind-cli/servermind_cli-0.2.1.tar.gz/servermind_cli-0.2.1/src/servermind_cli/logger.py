import logging
import json
from datetime import datetime
from config import LOG_FILE

# 로거 설정
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 콘솔 핸들러 생성 (기본적으로 비활성화)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(message)s')
console.setFormatter(console_formatter)

# 기본적으로는 콘솔 로깅을 추가하지 않음
# logging.getLogger('').addHandler(console)

def enable_console_logging():
    """콘솔 로깅을 활성화합니다."""
    if console not in logging.getLogger('').handlers:
        logging.getLogger('').addHandler(console)

def disable_console_logging():
    """콘솔 로깅을 비활성화합니다."""
    if console in logging.getLogger('').handlers:
        logging.getLogger('').removeHandler(console)

def log_command(input_text, translated_command, is_dangerous=False):
    """자연어 입력과 변환된 명령어 로깅"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "input": input_text,
        "command": translated_command,
        "is_dangerous": is_dangerous
    }
    logging.info(json.dumps(log_entry, ensure_ascii=False))
    return log_entry

def log_execution(command, return_code, stdout, stderr):
    """명령어 실행 결과 로깅"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "command": command,
        "return_code": return_code,
        "stdout": stdout,
        "stderr": stderr
    }
    logging.info(json.dumps(log_entry, ensure_ascii=False))
    return log_entry

def log_interpretation(command, stdout, stderr, exit_code, interpretation):
    """명령어 실행 결과 해석 로깅"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "command": command,
        "stdout": stdout,
        "stderr": stderr,
        "exit_code": exit_code,
        "interpretation": interpretation
    }
    logging.info(json.dumps(log_entry, ensure_ascii=False))
    return log_entry

def log_error(error_message):
    """에러 로깅"""
    logging.error(error_message) 