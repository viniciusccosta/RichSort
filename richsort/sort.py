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

console = Console()


class SortTUI:
    def __init__(self):
        self.algorithms = [
            {"name": "🫧 Bubble Sort", "id": "bubble", "implemented": True},
            {"name": "🔄 Selection Sort", "id": "selection", "implemented": False},
            {"name": "📍 Insertion Sort", "id": "insertion", "implemented": False},
            {"name": "🚀 Quick Sort", "id": "quick", "implemented": False},
            {"name": "🔀 Merge Sort", "id": "merge", "implemented": False},
        ]

        self.test_cases = [
            {
                "name": "🎲 Caso Aleatório",
                "array": [10, 30, 20, 40, 5],
                "description": "Array com elementos em ordem aleatória",
            },
            {
                "name": "✅ Melhor Caso",
                "array": [1, 2, 3, 4, 5],
                "description": "Array já ordenado - mínimo de trocas",
            },
            {
                "name": "❌ Pior Caso",
                "array": [50, 40, 30, 20, 10],
                "description": "Array em ordem decrescente - máximo de trocas",
            },
            {
                "name": "🔄 Caso com Duplicatas",
                "array": [3, 1, 4, 1, 5, 9, 2, 6],
                "description": "Array com elementos repetidos",
            },
        ]

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

    def generate_bubble_sort_steps(
        self, input_array: List[int]
    ) -> List[Dict[str, Any]]:
        """Gera todos os passos do bubble sort para visualização"""
        steps = []
        array = input_array.copy()
        length = len(array)
        comparisons = 0
        swaps = 0

        # Passo inicial
        steps.append(
            {
                "type": "start",
                "content": self.create_step_content(
                    f"🫧 BUBBLE SORT\n\n"
                    f"Array inicial: {input_array}\n"
                    f"Tamanho: {length} elementos\n\n"
                    f"O Bubble Sort compara elementos adjacentes e os troca\n"
                    f"se estiverem fora de ordem.",
                    array,
                    -1,
                    -1,
                    comparisons,
                    swaps,
                ),
            }
        )

        # Iteração externa
        for step in range(length):
            steps.append(
                {
                    "type": "step_start",
                    "content": self.create_step_content(
                        f"PASSO {step + 1}/{length} - Estado atual",
                        array,
                        -1,
                        -1,
                        comparisons,
                        swaps,
                    ),
                }
            )

            houve_troca_no_passo = False

            # Iteração interna
            for index in range(length - step - 1):
                elemento = array[index]
                vizinho = array[index + 1]
                comparisons += 1

                # Mostra comparação
                steps.append(
                    {
                        "type": "comparison",
                        "content": self.create_step_content(
                            f"Comparando {elemento} (pos: {index}) com {vizinho} (pos: {index + 1})",
                            array,
                            index,
                            index + 1,
                            comparisons,
                            swaps,
                        ),
                    }
                )

                # Executa troca se necessário
                if elemento > vizinho:
                    array[index], array[index + 1] = array[index + 1], array[index]
                    swaps += 1
                    houve_troca_no_passo = True

                    steps.append(
                        {
                            "type": "swap",
                            "content": self.create_step_content(
                                f"✅ {elemento} > {vizinho} → TROCAR!",
                                array,
                                index,
                                index + 1,
                                comparisons,
                                swaps,
                                swapped=True,
                            ),
                        }
                    )
                else:
                    steps.append(
                        {
                            "type": "no_swap",
                            "content": self.create_step_content(
                                f"❌ {elemento} ≤ {vizinho} → não trocar",
                                array,
                                index,
                                index + 1,
                                comparisons,
                                swaps,
                            ),
                        }
                    )

            if not houve_troca_no_passo:
                steps.append(
                    {
                        "type": "early_finish",
                        "content": self.create_step_content(
                            "🎉 Nenhuma troca neste passo! Array está ordenado.",
                            array,
                            -1,
                            -1,
                            comparisons,
                            swaps,
                        ),
                    }
                )
                break

        # Resultado final
        steps.append(
            {
                "type": "final",
                "content": self.create_step_content(
                    f"🎉 ORDENAÇÃO CONCLUÍDA!\n\n"
                    f"Array final: {array}\n\n"
                    f"📊 Estatísticas:\n"
                    f"  • Comparações: {comparisons}\n"
                    f"  • Trocas: {swaps}\n"
                    f"  • Complexidade: O(n²) = O({length}²) = {length**2}",
                    array,
                    -1,
                    -1,
                    comparisons,
                    swaps,
                ),
            }
        )

        return steps

    def create_step_content(
        self,
        description: str,
        array: List[int],
        highlight1: int = -1,
        highlight2: int = -1,
        comparisons: int = 0,
        swaps: int = 0,
        swapped: bool = False,
    ) -> str:
        """Cria o conteúdo visual de um passo"""
        content = f"{description}\n\n"

        # Array visual
        visual_array = []
        for i, val in enumerate(array):
            if i == highlight1:
                if swapped:
                    visual_array.append(f"[green on white] {val} [/]")
                else:
                    visual_array.append(f"[magenta on white] {val} [/]")
            elif i == highlight2:
                if swapped:
                    visual_array.append(f"[green on white] {val} [/]")
                else:
                    visual_array.append(f"[cyan on white] {val} [/]")
            else:
                visual_array.append(f"[white] {val} [/]")

        content += f"Array: {' '.join(visual_array)}\n\n"
        content += f"📊 Comparações: {comparisons} | Trocas: {swaps}"

        return content

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

        # Executa o bubble sort com visualização
        bubble_sort(self.test_cases[self.selected_test_case]["array"])

        input("\n\nPressione Enter para voltar ao menu principal...")


def bubble_sort(input_array: list[int]) -> list[int]:
    """
    Bubble Sort - O algoritmo de ordenação mais simples!

    Como funciona:
    1. Compara elementos adjacentes
    2. Troca se estiverem fora de ordem
    3. Repete até que nenhuma troca seja necessária

    Complexidade: O(n²) no pior caso
    """

    # Copiando o array para não alterar o array original
    array = input_array.copy()

    # Tamanho total:
    length = len(array)

    # Estatísticas para fins didáticos
    comparisons = 0
    swaps = 0

    # Cabeçalho explicativo
    explanation = Panel(
        "[bold cyan]🫧 BUBBLE SORT[/]\n\n"
        "[white]O Bubble Sort compara elementos adjacentes e os troca se estiverem\n"
        "fora de ordem. Como as bolhas que sobem na água, os elementos\n"
        "maiores 'borbulham' para o final da lista.[/]\n\n"
        f"[yellow]📊 Array inicial: {input_array}[/]\n"
        f"[yellow]📏 Tamanho: {length} elementos[/]",
        title="🎯 Algoritmo de Ordenação",
        border_style="blue",
    )
    console.print(explanation)
    console.print(f"Ordenando {array}...")

    # Iteração externa:
    for step in range(length):
        console.print(
            f"\n[bold blue]🔄 PASSO {step + 1}/{length}[/] - Estado atual: {array}"
        )
        if step == 0:
            console.print(
                "[dim]💡 A cada passo, o maior elemento restante irá para sua posição final[/]"
            )

        # Flag para detectar se houve trocas neste passo
        houve_troca_no_passo = False

        # Iteração interna (até o penúltimo elemento NÃO ordenado):
        for index in range(length - step - 1):
            # Elemento a ser analisado:
            elemento = array[index]
            comparisons += 1

            console.print(
                f"\n\t\t[white]🔍 Comparando {elemento} (pos: {index}) com seu vizinho...[/]"
            )
            visual_array = [
                (
                    f"[magenta on white]{array[i]}[/]"
                    if i == index
                    else (
                        f"[cyan on white]{array[i]}[/]"
                        if i == index + 1
                        else (
                            f"[dim]{array[i]}[/]"
                            if i >= length - step
                            else f"[white]{array[i]}[/]"
                        )
                    )
                )
                for i in range(length)
            ]
            console.print(f"\t\t\tArray: {visual_array}")
            if step > 0:
                console.print(
                    f"\t\t\t[dim]Últimos {step} elementos já estão ordenados ✅[/]"
                )

            # Vizinho a ser comparado:
            index_vizinho = index + 1
            vizinho = array[index_vizinho]

            # Comparação
            trocou = False
            if elemento > vizinho:
                array[index], array[index + 1] = array[index + 1], array[index]
                swaps += 1
                trocou = True
                houve_troca_no_passo = True
                console.print(f"\t\t\t[green]✅ {elemento} > {vizinho} → TROCAR![/]")
            else:
                console.print(f"\t\t\t[red]❌ {elemento} ≤ {vizinho} → não trocar[/]")

            # Array após iteração interna:
            visual_array = []
            for i in range(length):
                if trocou and i == index:
                    cor = "green on white"
                elif trocou and i == index_vizinho:
                    cor = "green on white"
                elif i >= length - step:
                    cor = "dim"
                else:
                    cor = "white"

                visual_array.append(f"[{cor}]{array[i]}[/]")
            console.print(f"\t\t\tResultado: {visual_array}")

        if not houve_troca_no_passo:
            console.print(
                f"\n\t[yellow]🎉 Nenhuma troca neste passo! Array pode estar ordenado.[/]"
            )

        # # Otimização: se não houve trocas, o array já está ordenado
        # if not houve_troca_no_passo:
        #     if verbose:
        #         console.print(
        #             f"[bold green]✨ Array ordenado antes do tempo! Paramos aqui.[/]"
        #         )
        #     break

    # Resultado:
    console.print()
    summary = Panel(
        f"[bold green]🎉 ORDENAÇÃO CONCLUÍDA![/]\n\n"
        f"[white]Array final: [bold cyan]{array}[/][/]\n\n"
        f"[white]📊 Estatísticas:[/]\n"
        f"[white]  • Comparações: [yellow]{comparisons}[/][/]\n"
        f"[white]  • Trocas realizadas: [yellow]{swaps}[/][/]\n",
        title="📈 Relatório Final",
        border_style="green",
    )
    console.print(summary)

    return array


if __name__ == "__main__":
    try:
        tui = SortTUI()
        tui.run()
    except KeyboardInterrupt:
        console.print("\n[bold green]👋 Obrigado por usar o RichSort![/]")
        sys.exit(0)
