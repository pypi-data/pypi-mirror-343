import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Rich 콘솔 인스턴스 생성
console = Console()

def print_command_preview(commands, output_options=None):
    """
    변환된 명령어 미리보기를 출력합니다.
    
    Args:
        commands (list): 변환된 명령어 목록
        output_options (dict): 출력 항목 설정 옵션
    """
    # 기본 출력 옵션 설정
    if output_options is None:
        output_options = {"show_command": True}
    
    # 명령어를 표시하지 않는 경우 미리보기도 표시하지 않음
    if not output_options.get("show_command", True):
        return
        
    table = Table(title="실행 예정 명령어")
    table.add_column("순서", style="cyan")
    table.add_column("명령어", style="green")
    
    for i, cmd in enumerate(commands, 1):
        table.add_row(str(i), cmd)
    
    console.print(table)

def print_dangerous_warning(commands, output_options=None):
    """
    위험한 명령어에 대한 경고를 출력합니다.
    
    Args:
        commands (list): 위험한 명령어 목록
        output_options (dict): 출력 항목 설정 옵션
    """
    # 기본 출력 옵션 설정
    if output_options is None:
        output_options = {"show_error": True}
    
    # 오류를 표시하지 않는 경우 경고도 표시하지 않음
    if not output_options.get("show_error", True):
        return
        
    warning_text = "\n".join([f"- {cmd}" for cmd in commands])
    
    panel = Panel(
        f"다음 명령어는 위험하여 실행이 차단되었습니다:\n\n{warning_text}\n\n강제 실행하려면 --yes 옵션을 사용하세요.",
        title="[bold red]위험 경고[/bold red]",
        border_style="red"
    )
    
    console.print(panel)

def print_execution_result(result, output_options=None):
    """
    명령어 실행 결과를 출력합니다.
    
    Args:
        result (dict): 명령어 실행 결과
        output_options (dict): 출력 항목 설정 옵션
    """
    # 기본 출력 옵션 설정
    if output_options is None:
        output_options = {"show_result": True}
    
    # 결과를 표시하지 않는 경우 실행 결과도 표시하지 않음
    if not output_options.get("show_result", True):
        return
        
    if result["success"] and result["return_code"] == 0:
        status = "[bold green]성공[/bold green]"
    else:
        status = "[bold red]실패[/bold red]"
    
    panel = Panel(
        f"명령어: {result['command']}\n상태: {status}\n반환 코드: {result['return_code']}",
        title="[bold blue]실행 결과[/bold blue]",
        border_style="blue"
    )
    
    console.print(panel)

def ensure_env_file():
    """
    .env 파일이 없는 경우 생성합니다.
    """
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write("# ServerMind 환경 설정\n")
            f.write("OPENAI_API_KEY=your_api_key_here\n")
            f.write("GPT_MODEL=gpt-4\n")
            f.write("LOG_FILE=history.log\n")
        
        console.print("[yellow]새 .env 파일이 생성되었습니다. OpenAI API 키를 설정해주세요.[/yellow]") 