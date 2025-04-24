#!/usr/bin/env python3
import sys
import click
from translator import translate_to_command
from filter import filter_commands
from executor import execute_commands
from utils import print_command_preview, print_dangerous_warning, ensure_env_file
from logger import log_command, log_error, enable_console_logging, disable_console_logging

@click.command(context_settings=dict(help_option_names=['-h', '--help'], ignore_unknown_options=False))
@click.option("--preview", is_flag=True, help="명령어만 출력하고 실행하지 않습니다.")
@click.option("--yes", is_flag=True, help="위험한 명령어도 실행합니다.")
@click.option("--explain/--no-explain", default=True, help="명령어 실행 결과를 해석합니다. (기본값: 활성화)")
@click.option("--show-info/--no-info", default=False, help="정보 메시지를 출력합니다. (기본값: 비활성화)")
@click.option("--show-command/--no-command", default=True, help="실행할 명령어를 출력합니다. (기본값: 활성화)")
@click.option("--show-result/--no-result", default=True, help="명령어 실행 결과를 출력합니다. (기본값: 활성화)")
@click.option("--show-error/--no-error", default=False, help="오류 메시지를 출력합니다. (기본값: 비활성화)")
@click.option("--show-log/--no-log", default=False, help="로그 메시지를 콘솔에 출력합니다. (기본값: 비활성화)")
@click.option("--show-all", is_flag=True, help="모든 출력을 활성화합니다.")
@click.argument("input_text", required=True, nargs=-1)
def main(input_text, preview, yes, explain, show_info, show_command, show_result, show_error, show_log, show_all):
    """
    ServerMind CLI v0.2 - 자연어 입력 기반 리눅스 명령어 변환 및 결과 해석 시스템
    
    자연어로 입력하면 리눅스 명령어로 변환하여 실행하고 결과를 해석합니다.
    여러 명령어는 \n으로 구분하여 순차적으로 실행할 수 있습니다.
    
    예시:
    \b
    servermind "현재 폴더 확인"
    servermind "파일 목록 확인\\n용량이 큰 파일 찾기"
    servermind --preview "모든 log 파일 삭제"
    servermind --yes "위험한 명령어 실행"
    servermind --no-explain "디스크 사용량 확인"
    servermind --show-info --show-error "선택적으로 출력하기"
    servermind --show-all "모든 정보 출력하기"
    servermind --show-log "로그 메시지도 콘솔에 출력하기"
    """
    try:
        # --show-all 옵션이 활성화되면 모든 출력 옵션 활성화
        if show_all:
            show_info = True
            show_command = True
            show_result = True
            show_error = True
            show_log = True
        
        # 로그 출력 설정
        if show_log:
            enable_console_logging()
        else:
            disable_console_logging()
        
        # .env 파일 확인
        ensure_env_file()
        
        # 입력 텍스트 결합
        text = " ".join(input_text)
        
        # 사용자 요청 출력
        if show_info:
            click.echo(click.style("[INFO]", fg="blue") + f" 요청: '{text}'")
        
        # GPT를 통한 명령어 변환
        commands = translate_to_command(text)
        
        if not commands:
            error_msg = " 명령어를 생성할 수 없습니다. 다른 표현으로 시도해보세요."
            log_error(f"명령어 생성 실패: {text}")
            # 명령어 생성 실패는 중요한 오류이므로 항상 표시
            click.echo(click.style("[ERROR]", fg="red") + error_msg, err=True)
            sys.exit(1)
        
        # 명령어 로깅
        for cmd in commands:
            log_command(text, cmd)
            
        # 변환된 명령어 출력
        if show_info:
            if len(commands) == 1:
                click.echo(click.style("[INFO]", fg="blue") + f" 변환된 명령어: '{commands[0]}'")
            else:
                click.echo(click.style("[INFO]", fg="blue") + f" 변환된 명령어 {len(commands)}개:")
                for i, cmd in enumerate(commands):
                    click.echo(click.style(f"  {i+1}.", fg="blue") + f" {cmd}")
        
        # 위험 명령어 필터링
        is_safe, filtered_commands = filter_commands(text, commands, force=yes)
        
        # 출력 옵션 설정
        output_options = {
            "show_command": show_command,
            "show_result": show_result,
            "show_error": show_error,
            "show_interpretation": explain
        }
        
        # 미리보기 모드
        if preview:
            print_command_preview(filtered_commands, output_options=output_options)
            return
        
        # 위험 명령어 처리
        if not is_safe:
            print_dangerous_warning(filtered_commands, output_options=output_options)
            return
        
        # 명령어 실행
        execute_commands(filtered_commands, explain=explain, output_options=output_options, user_input=text, suggestion_depth=0)
    
    except Exception as e:
        error_msg = f" 오류 발생: {str(e)}"
        log_error(error_msg.strip())
        # 예외 오류는 중요한 오류이므로 항상 표시
        click.echo(click.style("[ERROR]", fg="red") + error_msg, err=True)
        sys.exit(1)

if __name__ == "__main__":
    main() 