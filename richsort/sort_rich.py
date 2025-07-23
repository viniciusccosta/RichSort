import sys
from time import sleep
from typing import Any, Dict, List

from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .algorithms import get_algorithm_visualizer, get_available_algorithms
from .test_cases import get_test_cases

console = Console()


class SortTUI:
    def __init__(self):
        self.algorithms = get_available_algorithms()
        self.test_cases = get_test_cases()

        self.selected_algorithm = 0
        self.selected_test_case = 0
        self.current_step = 0
        self.sort_steps = []
        self.is_running = False

    def create_layout(self):
        """Cria o layout da TUI"""
        layout = Layout()

        # Divide em header e body
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=3),
        )

        # Divide o body em left e right
        layout["body"].split_row(
            Layout(name="left", ratio=1), Layout(name="right", ratio=2)
        )

        # Divide o left em algorithms e test_cases
        layout["left"].split_column(
            Layout(name="algorithms", ratio=1), Layout(name="test_cases", ratio=1)
        )

        return layout

    def render_header(self):
        """Renderiza o cabeçalho"""
        return Panel(
            Align.center(
                Text(
                    "🚀 RichSort - Visualizador de Algoritmos de Ordenação",
                    style="bold cyan",
                )
            ),
            style="blue",
        )

    def render_footer(self):
        """Renderiza o rodapé com comandos"""
        commands = (
            "[yellow]↑↓[/] Navegar | [yellow]Tab[/] Trocar painel | "
            "[yellow]Enter[/] Executar | [yellow]Space[/] Pausar/Continuar | [yellow]R[/] Reset | [yellow]Q[/] Sair"
        )
        return Panel(Align.center(commands), style="green")

    def render_algorithms_panel(self):
        """Renderiza o painel de algoritmos"""
        table = Table(show_header=False, box=None, padding=(0, 1))

        for i, algo in enumerate(self.algorithms):
            if i == self.selected_algorithm:
                if algo["implemented"]:
                    table.add_row(f"► [bold cyan]{algo['name']}[/]")
                else:
                    table.add_row(f"► [bold red]{algo['name']} (Em breve)[/]")
            else:
                if algo["implemented"]:
                    table.add_row(f"  [white]{algo['name']}[/]")
                else:
                    table.add_row(f"  [dim]{algo['name']} (Em breve)[/]")

        return Panel(
            table,
            title="🧮 Algoritmos",
            border_style="cyan" if self.selected_panel == "algorithms" else "dim",
        )

    def render_test_cases_panel(self):
        """Renderiza o painel de casos de teste"""
        table = Table(show_header=False, box=None, padding=(0, 1))

        for i, test_case in enumerate(self.test_cases):
            if i == self.selected_test_case:
                table.add_row(f"► [bold yellow]{test_case['name']}[/]")
                table.add_row(f"   [dim]{test_case['description']}[/]")
                table.add_row(f"   [cyan]Array: {test_case['array']}[/]")
            else:
                table.add_row(f"  [white]{test_case['name']}[/]")

        return Panel(
            table,
            title="📋 Casos de Teste",
            border_style="yellow" if self.selected_panel == "test_cases" else "dim",
        )

    def render_main_panel(self):
        """Renderiza o painel principal com a execução do algoritmo"""
        if not self.sort_steps:
            return Panel(
                Align.center(
                    Text(
                        "Pressione Enter para executar o algoritmo selecionado\n\n"
                        f"Algoritmo: {self.algorithms[self.selected_algorithm]['name']}\n"
                        f"Caso de Teste: {self.test_cases[self.selected_test_case]['name']}",
                        style="dim",
                        justify="center",
                    )
                ),
                title="📊 Execução do Algoritmo",
                border_style="magenta",
            )

        # Se temos passos, mostra o passo atual
        if self.current_step < len(self.sort_steps):
            step_data = self.sort_steps[self.current_step]
            content = step_data["content"]
        else:
            content = "Execução concluída!"

        progress = (
            f"Passo {self.current_step + 1}/{len(self.sort_steps)}"
            if self.sort_steps
            else ""
        )

        return Panel(
            content,
            title=f"📊 Execução do Algoritmo - {progress}",
            border_style="magenta",
        )

    def run(self):
        """Executa a TUI"""
        self.selected_panel = "algorithms"

        console.clear()
        console.print(
            "[bold cyan]🚀 RichSort - Visualizador de Algoritmos de Ordenação[/]"
        )
        console.print("[dim]Versão TUI simplificada[/]\n")

        while True:
            # Mostra o estado atual
            console.print("─" * 80)
            console.print(
                f"[bold]Algoritmo selecionado:[/] {self.algorithms[self.selected_algorithm]['name']}"
            )
            console.print(
                f"[bold]Caso de teste selecionado:[/] {self.test_cases[self.selected_test_case]['name']}"
            )
            console.print(
                f"[dim]Array: {self.test_cases[self.selected_test_case]['array']}[/]"
            )
            console.print("─" * 80)

            # Menu de opções
            console.print("\n[bold cyan]Opções:[/]")
            console.print("1. Mudar algoritmo")
            console.print("2. Mudar caso de teste")
            console.print("3. Executar algoritmo")
            console.print("4. Sair")

            choice = input("\nSua escolha (1-4): ").strip()

            if choice == "1":
                self.select_algorithm()
            elif choice == "2":
                self.select_test_case()
            elif choice == "3":
                self.execute_algorithm()
            elif choice == "4":
                console.print("[bold green]👋 Obrigado por usar o RichSort![/]")
                break
            else:
                console.print("[red]Opção inválida![/]")

            console.clear()

    def select_algorithm(self):
        """Permite selecionar um algoritmo"""
        console.print("\n[bold cyan]Algoritmos disponíveis:[/]")
        for i, algo in enumerate(self.algorithms):
            status = "✅" if algo["implemented"] else "🚧"
            marker = "►" if i == self.selected_algorithm else " "
            console.print(f"{marker} {i + 1}. {status} {algo['name']}")

        try:
            choice = int(input("\nEscolha um algoritmo (número): ")) - 1
            if 0 <= choice < len(self.algorithms):
                if self.algorithms[choice]["implemented"]:
                    self.selected_algorithm = choice
                    console.print(
                        f"[green]✅ Algoritmo selecionado: {self.algorithms[choice]['name']}[/]"
                    )
                else:
                    console.print(
                        "[yellow]⚠️ Este algoritmo ainda não foi implementado![/]"
                    )
            else:
                console.print("[red]Opção inválida![/]")
        except ValueError:
            console.print("[red]Por favor, digite um número válido![/]")

        input("\nPressione Enter para continuar...")

    def select_test_case(self):
        """Permite selecionar um caso de teste"""
        console.print("\n[bold cyan]Casos de teste disponíveis:[/]")
        for i, test_case in enumerate(self.test_cases):
            marker = "►" if i == self.selected_test_case else " "
            console.print(f"{marker} {i + 1}. {test_case['name']}")
            console.print(f"   {test_case['description']}")
            console.print(f"   Array: {test_case['array']}\n")

        try:
            choice = int(input("Escolha um caso de teste (número): ")) - 1
            if 0 <= choice < len(self.test_cases):
                self.selected_test_case = choice
                console.print(
                    f"[green]✅ Caso selecionado: {self.test_cases[choice]['name']}[/]"
                )
            else:
                console.print("[red]Opção inválida![/]")
        except ValueError:
            console.print("[red]Por favor, digite um número válido![/]")

        input("\nPressione Enter para continuar...")

    def execute_algorithm(self):
        """Executa o algoritmo selecionado"""
        if not self.algorithms[self.selected_algorithm]["implemented"]:
            console.print("[red]Este algoritmo ainda não foi implementado![/]")
            input("Pressione Enter para continuar...")
            return

        console.clear()
        console.rule(
            f"🚀 Executando {self.algorithms[self.selected_algorithm]['name']}"
        )
        console.print(
            f"[yellow]Caso de teste:[/] {self.test_cases[self.selected_test_case]['name']}"
        )
        console.print(
            f"[yellow]Array inicial:[/] {self.test_cases[self.selected_test_case]['array']}\n"
        )

        # Execute algorithm using the shared algorithm module
        algorithm_id = self.algorithms[self.selected_algorithm]["id"]
        try:
            visualizer = get_algorithm_visualizer(algorithm_id)
            output = visualizer.sort_complete(
                self.test_cases[self.selected_test_case]["array"]
            )
            console.print(output)
        except (ValueError, NotImplementedError) as e:
            console.print(f"[red]Erro: {str(e)}[/]")

        input("\n\nPressione Enter para voltar ao menu principal...")


def main():
    """Entry point for the Rich-based TUI application."""
    try:
        tui = SortTUI()
        tui.run()
    except KeyboardInterrupt:
        console.print("\n[bold green]👋 Obrigado por usar o RichSort![/]")
        sys.exit(0)


if __name__ == "__main__":
    main()
