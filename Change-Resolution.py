import os
import re
from InquirerPy import inquirer
from InquirerPy.validator import NumberValidator
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

ASCII_ART = """
 ██████╗██╗  ██╗ █████╗ ███╗   ██╗ ██████╗ ███████╗
██╔════╝██║  ██║██╔══██╗████╗  ██║██╔════╝ ██╔════╝
██║     ███████║███████║██╔██╗ ██║██║  ███╗█████╗  
██║     ██╔══██║██╔══██║██║╚██╗██║██║   ██║██╔══╝  
╚██████╗██║  ██║██║  ██║██║ ╚████║╚██████╔╝███████╗
 ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝
                                                     
██████╗ ███████╗███████╗ ██████╗ ██╗     ██╗   ██╗████████╗██╗ ██████╗ ███╗   ██╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗██║     ██║   ██║╚══██╔══╝██║██╔═══██╗████╗  ██║
██████╔╝█████╗  ███████╗██║   ██║██║     ██║   ██║   ██║   ██║██║   ██║██╔██╗ ██║
██╔══██╗██╔══╝  ╚════██║██║   ██║██║     ██║   ██║   ██║   ██║██║   ██║██║╚██╗██║
██║  ██║███████╗███████║╚██████╔╝███████╗╚██████╔╝   ██║   ██║╚██████╔╝██║ ╚████║
╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚══════╝ ╚═════╝    ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
"""

def obter_monitores():
    saida = os.popen('xrandr').read()
    monitores = []
    
    for linha in saida.split('\n'):
        if ' connected' in linha and not 'disconnected' in linha:
            monitor = linha.split()[0]
            monitores.append(monitor)
    
    return monitores

def obter_resolucoes_por_monitor(monitor):
    saida = os.popen('xrandr').read()
    resolucoes = []
    capturando = False
    
    for linha in saida.split('\n'):
        if monitor in linha and ' connected' in linha:
            capturando = True
            continue
        
        if capturando:
            if linha and not linha.startswith(' '):
                break
            
            match = re.search(r'(\d{3,5}x\d{3,5})\s+(\d+\.\d+)', linha)
            if match:
                resolucao = match.group(1)
                hz = match.group(2)
                atual = '*' in linha
                resolucoes.append({
                    'resolucao': resolucao,
                    'hz': hz,
                    'atual': atual,
                    'display': f"{resolucao} @ {hz}Hz" + (" [ATUAL]" if atual else "")
                })
    
    return resolucoes

def criar_resolucao_customizada(largura, altura, hz):
    console.print(f"\n[yellow]Criando resolução customizada {largura}x{altura} @ {hz}Hz...[/yellow]")
    
    cvt_output = os.popen(f'cvt {largura} {altura} {hz}').read()
    
    modeline_match = re.search(r'Modeline\s+".*?"\s+(.*)', cvt_output)
    if not modeline_match:
        console.print("[red]Erro ao gerar modeline![/red]")
        return None
    
    modeline = modeline_match.group(1)
    mode_name = f"{largura}x{altura}_{hz}"
    
    console.print(f"[green]Modeline gerado:[/green] {modeline}")
    
    return mode_name, modeline

def aplicar_resolucao_customizada(monitor, largura, altura, hz):
    mode_name, modeline = criar_resolucao_customizada(largura, altura, hz)
    
    if not mode_name:
        return False
    
    console.print(f"\n[cyan]Adicionando novo modo...[/cyan]")
    os.system(f'xrandr --newmode "{mode_name}" {modeline}')
    
    console.print(f"[cyan]Vinculando modo ao monitor {monitor}...[/cyan]")
    os.system(f'xrandr --addmode {monitor} "{mode_name}"')
    
    console.print(f"[cyan]Aplicando resolução...[/cyan]")
    os.system(f'xrandr --output {monitor} --mode "{mode_name}"')
    
    console.print(f"[green]✓ Resolução {largura}x{altura} @ {hz}Hz aplicada com sucesso![/green]")
    return True

def aplicar_resolucao_existente(monitor, resolucao, hz):
    console.print(f"\n[cyan]Aplicando resolução {resolucao} @ {hz}Hz...[/cyan]")
    os.system(f'xrandr --output {monitor} --mode {resolucao} --rate {hz}')
    console.print(f"[green]✓ Resolução aplicada com sucesso![/green]")

def main():
    console.clear()
    console.print(f"[cyan]{ASCII_ART}[/cyan]")
    console.print(Panel.fit("[bold green]Bem-vindo ao Customizador de Resolução![/bold green]", border_style="green"))
    
    monitores = obter_monitores()
    
    if not monitores:
        console.print("[red]Nenhum monitor detectado![/red]")
        return
    
    if len(monitores) > 1:
        monitor = inquirer.select(
            message="Selecione o monitor:",
            choices=monitores
        ).execute()
    else:
        monitor = monitores[0]
        console.print(f"\n[green]Monitor detectado:[/green] {monitor}")
    
    resolucoes = obter_resolucoes_por_monitor(monitor)
    
    if resolucoes:
        table = Table(title=f"\n📺 Resoluções Disponíveis para {monitor}", show_header=True, header_style="bold magenta")
        table.add_column("Resolução", style="cyan")
        table.add_column("Hz", style="yellow")
        table.add_column("Status", style="green")
        
        for r in resolucoes:
            status = "★ ATUAL" if r['atual'] else ""
            table.add_row(r['resolucao'], r['hz'] + " Hz", status)
        
        console.print(table)
    
    opcao = inquirer.select(
        message="\nO que deseja fazer?",
        choices=[
            "Usar resolução existente",
            "Criar resolução customizada",
            "Sair"
        ]
    ).execute()
    
    if opcao == "Sair":
        console.print("\n[yellow]Até logo![/yellow]")
        return
    
    if opcao == "Usar resolução existente":
        if not resolucoes:
            console.print("[red]Nenhuma resolução disponível![/red]")
            return
        
        escolha = inquirer.select(
            message="Selecione a resolução:",
            choices=[r['display'] for r in resolucoes]
        ).execute()
        
        for r in resolucoes:
            if r['display'] == escolha:
                aplicar_resolucao_existente(monitor, r['resolucao'], r['hz'])
                break
    
    elif opcao == "Criar resolução customizada":
        largura = inquirer.number(
            message="Largura:",
            validate=NumberValidator()
        ).execute()
        
        altura = inquirer.number(
            message="Altura:",
            validate=NumberValidator()
        ).execute()
        
        hz = inquirer.number(
            message="Taxa de atualização em Hz:",
            validate=NumberValidator(),
            default=60
        ).execute()
        
        aplicar_resolucao_customizada(monitor, int(largura), int(altura), int(hz))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Operação cancelada pelo usuário.[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Erro: {e}[/red]")
