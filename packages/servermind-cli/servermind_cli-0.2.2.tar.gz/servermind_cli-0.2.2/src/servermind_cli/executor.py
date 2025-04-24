import subprocess
import sys
from logger import log_execution, log_error
from interpreter import interpret_output, remove_markup
import click

# remove_markup 함수를 interpreter 모듈에서 임포트
try:
    from interpreter import remove_markup
except ImportError:
    # 임포트 실패 시 간단한 버전의 함수 정의
    def remove_markup(text):
        return text

def execute_command(command, user_input=None):
    """
    단일 명령어를 실행합니다.
    
    Args:
        command (str): 실행할 명령어
        user_input (str, optional): 사용자가 입력한 원래 자연어 질의
        
    Returns:
        tuple: (실행 성공 여부, 반환 코드, 표준 출력, 표준 에러, (해석, 추가 명령어 제안))
    """
    try:
        # 명령어 실행 (셸 모드 활성화)
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 표준 출력과 표준 에러 수집
        stdout, stderr = process.communicate()
        return_code = process.returncode
        
        # 실행 결과 로깅
        log_execution(command, return_code, stdout, stderr)
        
        # 결과 해석
        interpretation_result = interpret_output(command, stdout, stderr, return_code, user_input)
        
        return True, return_code, stdout, stderr, interpretation_result
    
    except Exception as e:
        error_msg = f"명령어 실행 중 오류 발생: {str(e)}"
        log_error(error_msg)
        return False, -1, "", error_msg, ("실행에 실패했습니다.", [])

def execute_commands(commands, explain=True, output_options=None, user_input=None, suggestion_depth=0):
    """
    여러 명령어를 순차적으로 실행합니다.
    
    Args:
        commands (list): 실행할 명령어 목록
        explain (bool): 결과 해석을 출력할지 여부
        output_options (dict): 출력 항목 설정 옵션
            - show_command (bool): 명령어 출력 여부
            - show_result (bool): 실행 결과 출력 여부
            - show_error (bool): 오류 출력 여부
            - show_interpretation (bool): 결과 해석 출력 여부
        user_input (str, optional): 사용자가 입력한 원래 자연어 질의
        suggestion_depth (int, optional): 현재 추가 명령어 실행 깊이 (재귀 제한용)
        
    Returns:
        list: 각 명령어의 실행 결과 목록
    """
    # 옵션 기본값 설정
    if output_options is None:
        output_options = {
            "show_command": True,
            "show_result": True,
            "show_error": True,
            "show_interpretation": explain
        }
    
    results = []
    
    for i, command in enumerate(commands):
        # 명령어 출력
        if output_options.get("show_command", True):
            click.echo(click.style("\n[명령어 실행]", fg="blue", bold=True))
            click.echo(f"> {command}")
        
        # 명령어 실행
        success, return_code, stdout, stderr, interpretation_result = execute_command(command, user_input)
        
        # 해석과 추가 명령어 제안 분리
        if isinstance(interpretation_result, tuple) and len(interpretation_result) == 2:
            interpretation, suggested_commands = interpretation_result
        else:
            interpretation, suggested_commands = interpretation_result, []
        
        # 결과 저장
        results.append({
            "command": command,
            "success": success,
            "return_code": return_code,
            "stdout": stdout,
            "stderr": stderr,
            "interpretation": interpretation,
            "suggested_commands": suggested_commands
        })
        
        # 표준 출력 출력
        if stdout and output_options.get("show_result", True):
            click.echo(click.style("\n[실행 결과]", fg="green"))
            click.echo(stdout.rstrip())
        
        # 표준 에러 출력
        if stderr and output_options.get("show_error", True):
            click.echo(click.style("\n[오류 출력]", fg="red"))
            click.echo(stderr.rstrip(), err=True)
        
        # 결과 해석 출력
        if interpretation and output_options.get("show_interpretation", explain):
            click.echo(click.style("\n[결과 해석]", fg="yellow", bold=True))
            # 마크업이 이미 제거되었지만, 한 번 더 확인
            clean_interpretation = remove_markup(interpretation)
            # 결과 해석 출력
            click.echo(clean_interpretation)
            
            # 추가 명령어 제안 출력
            if suggested_commands and len(suggested_commands) > 0 and suggestion_depth < 2:
                click.echo(click.style("\n[추가 명령어 제안]", fg="cyan", bold=True))
                for idx, suggestion in enumerate(suggested_commands):
                    click.echo(f"{idx+1}. {suggestion['description']}: {click.style(suggestion['command'], fg='green')}")
                
                # 향상된 명령어 선택 인터페이스
                click.echo(click.style("\n실행할 명령어 번호를 입력하거나, 자연어로 새 명령어를 입력하세요. 종료하려면 'q'를 입력하세요.", fg="cyan"))
                response = click.prompt("", prompt_suffix="> ", show_default=False, default="", show_choices=False)
                
                # 사용자 응답 처리
                if response.lower() == 'q':
                    # 종료
                    return results
                
                # 제안된 명령어 번호를 입력한 경우
                try:
                    choice = int(response)
                    if 1 <= choice <= len(suggested_commands):
                        selected_command = suggested_commands[choice-1]["command"]
                        click.echo(click.style(f"\n선택한 명령어: {selected_command}", fg="green"))
                        
                        # 재귀적으로 명령어 실행
                        new_output_options = output_options.copy()
                        execute_commands([selected_command], explain=explain, output_options=new_output_options, user_input=None, suggestion_depth=suggestion_depth+1)
                    else:
                        click.echo(click.style(f"오류: 유효한 번호를 입력해주세요 (1-{len(suggested_commands)})", fg="red"))
                except ValueError:
                    # 번호가 아닌 경우 자연어 명령어로 간주
                    from translator import translate_to_command
                    
                    click.echo(click.style(f"\n입력한 명령어: {response}", fg="blue"))
                    new_commands = translate_to_command(response)
                    
                    if new_commands:
                        # 새 명령어 실행
                        click.echo(click.style(f"변환된 명령어: {new_commands[0]}", fg="green"))
                        new_output_options = output_options.copy()
                        execute_commands(new_commands, explain=explain, output_options=new_output_options, user_input=response, suggestion_depth=suggestion_depth+1)
                    else:
                        click.echo(click.style("명령어를 생성할 수 없습니다. 다른 표현으로 시도해보세요.", fg="red"))
        
        # 실행 실패 시 사용자에게 물어보기
        if (not success or return_code != 0) and i < len(commands) - 1:
            error_msg = click.style(f"\n명령어 실행 실패: {command}", fg="red")
            if output_options.get("show_error", True):
                click.echo(error_msg, err=True)
            
            if click.confirm(click.style("다음 명령어를 계속 실행하시겠습니까?", fg="yellow"), default=False):
                continue
            else:
                break
    
    return results 