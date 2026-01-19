import json
import os
import subprocess
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

console = Console()
LABS_FILE = "labs.json"
PRACTICE_DIR = "lab_practice"

def load_labs():
    if not os.path.exists(LABS_FILE):
        return []
    with open(LABS_FILE, 'r') as f:
        return json.load(f)

def ensure_practice_dir(sub_dir):
    path = os.path.join(os.getcwd(), PRACTICE_DIR, sub_dir)
    os.makedirs(path, exist_ok=True)
    return path

def run_shell_command(command, cwd):
    try:
        # Use bash if available, else standard shell
        # We explicitly use bash as the user requested unix commands
        result = subprocess.run(
            ["bash", "-c", command],
            cwd=cwd,
            capture_output=True,
            text=True
        )
        if result.stdout:
            console.print(result.stdout, style="green")
        if result.stderr:
            console.print(result.stderr, style="red")
    except FileNotFoundError:
        console.print("[bold red]Error:[/bold red] 'bash' not found. Please ensure Git Bash or WSL is installed and in your PATH.")
    except Exception as e:
        console.print(f"[bold red]Execution Error:[/bold red] {e}")

def practice_loop(lab, task):
    lab_dir = ensure_practice_dir(f"lab_{lab['id']}")
    console.print(Panel(f"[bold blue]Practice Mode: {lab['title']}[/bold blue]\n[yellow]Task: {task['description']}[/yellow]\n\n[bold white]Entering Bash Shell...[/bold white]\nType 'exit' to return to the menu.\nWorking Directory: {lab_dir}\n\n[dim]Tip: You can use 'nano' or 'vim' here to write your scripts![/dim]", expand=False))

    try:
        # Spawn an interactive bash shell in the lab directory
        # This allows interactive tools like nano/vi to work
        subprocess.call(["bash"], cwd=lab_dir)
    except FileNotFoundError:
        console.print("[bold red]Error:[/bold red] 'bash' not found. Please ensure Git Bash or WSL is installed.")
    except Exception as e:
        console.print(f"[bold red]Error launching shell:[/bold red] {e}")

    console.print("\n[bold yellow]Session ended. Returning to menu...[/bold yellow]")

def main():
    labs = load_labs()
    
    while True:
        console.clear()
        console.print("")
        console.print("[bold magenta]  ╔══════════════════════════════════════════╗[/bold magenta]")
        console.print("[bold magenta]  ║[/bold magenta]  [bold cyan]█▀▀█ █▀▀▄ ▀▀▀ █▀▀█ █▀▀[/bold cyan]                 [bold magenta]║[/bold magenta]")
        console.print("[bold magenta]  ║[/bold magenta]  [bold cyan]█▄▄█ █  █ ▀█▀ █  █ ▀▀█[/bold cyan]                 [bold magenta]║[/bold magenta]")
        console.print("[bold magenta]  ║[/bold magenta]  [bold cyan]▀  ▀ ▀▀▀  ▀▀▀ ▀▀▀▀ ▀▀▀[/bold cyan]                 [bold magenta]║[/bold magenta]")
        console.print("[bold magenta]  ║[/bold magenta]  [dim]═══════════════════════[/dim]                 [bold magenta]║[/bold magenta]")
        console.print("[bold magenta]  ║[/bold magenta]     [dim]Adi's Operating System Lab Tool[/dim]    [bold magenta]║[/bold magenta]")
        console.print("[bold magenta]  ╚══════════════════════════════════════════╝[/bold magenta]")
        console.print("")
        console.print(Panel("[bold magenta]OS Lab Practice Tool[/bold magenta]\n[dim]Select a lab to practice Unix/Linux commands[/dim]"))
        
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("ID", style="dim", width=6)
        table.add_column("Title")
        
        for lab in labs:
            table.add_row(str(lab['id']), lab['title'])
            
        console.print(table)
        
        choice = Prompt.ask("[bold]Select Lab ID[/bold] (or 'r' for Reference, 'q' to quit)", default="1")
        
        if choice.lower() == 'q':
            console.print("Goodbye!")
            break
        
        if choice.lower() == 'r':
            if os.path.exists("reference.txt"):
                with open("reference.txt", "r") as f:
                    console.print(Panel(f.read(), title="Appendix 1: Unix Commands", border_style="green"))
            else:
                console.print("[red]Reference file not found.[/red]")
            Prompt.ask("Press Enter to continue...")
            continue
            
        selected_lab = next((l for l in labs if str(l['id']) == choice), None)
        
        if selected_lab:
            console.print(f"\n[bold green]Selected: {selected_lab['title']}[/bold green]")
            # Show tasks
            t_table = Table(show_header=True)
            t_table.add_column("Task ID", style="bold yellow")
            t_table.add_column("Description")
            
            for task in selected_lab['tasks']:
                t_table.add_row(task['id'], task['description'])
            
            console.print(t_table)
            
            task_choice = Prompt.ask("Select Task ID to practice (or 'all' to just open shell)", default="all")
            
            # Find task or checking for 'all'
            selected_task = next((t for t in selected_lab['tasks'] if str(t['id']) == task_choice), None)
            
            if selected_task:
                practice_loop(selected_lab, selected_task)
            elif task_choice == 'all':
                 practice_loop(selected_lab, {"description": "Free Practice", "id": "all"})
            else:
                console.print("[red]Invalid Task ID[/red]")
                
        else:
            console.print("[red]Invalid Lab ID[/red]")

if __name__ == "__main__":
    main()
