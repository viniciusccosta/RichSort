import sys
from typing import Any, Dict, List

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, ScrollableContainer, Vertical
from textual.reactive import reactive
from textual.widgets import Footer, Header, ListItem, ListView, Static

console = Console()


class AlgorithmList(ListView):
    """Widget for displaying and selecting sorting algorithms."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.algorithms = [
            {"name": "🫧 Bubble Sort", "id": "bubble", "implemented": True},
            {"name": "🔄 Selection Sort", "id": "selection", "implemented": False},
            {"name": "📍 Insertion Sort", "id": "insertion", "implemented": False},
            {"name": "🚀 Quick Sort", "id": "quick", "implemented": False},
            {"name": "🔀 Merge Sort", "id": "merge", "implemented": False},
        ]

    def compose(self) -> ComposeResult:
        for algo in self.algorithms:
            if algo["implemented"]:
                yield ListItem(Static(algo["name"]), name=algo["id"])
            else:
                yield ListItem(
                    Static(f"[dim]{algo['name']} (Em breve)[/]"), name=algo["id"]
                )


class TestCaseList(ListView):
    """Widget for displaying and selecting test cases."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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

    def compose(self) -> ComposeResult:
        for i, test_case in enumerate(self.test_cases):
            content = f"{test_case['name']}\n[dim]{test_case['description']}[/]\n[cyan]Array: {test_case['array']}[/]"
            yield ListItem(Static(content), name=f"test_{i}")


class ExecutionPanel(ScrollableContainer):
    """Main panel for displaying algorithm execution."""

    execution_output = reactive("")
    # can_focus = True  # Make the panel focusable - but not via tab

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_algorithm = None
        self.current_test_case = None
        self.content_widget = Static("")

    def on_mount(self) -> None:
        """Mount the content widget inside the scroll view."""
        self.mount(self.content_widget)
        # Initialize with waiting state content
        self.update_content()

    def render_content(self) -> str:
        """Return the content to be displayed."""
        if self.execution_output:
            return self.execution_output
        elif self.current_algorithm and self.current_test_case:
            return self._render_ready_state()
        else:
            return self._render_waiting_state()

    def watch_execution_output(self, old_value: str, new_value: str) -> None:
        """Update the content when execution_output changes."""
        self.update_content()

    def update_content(self) -> None:
        """Update the scrollable content."""
        content = self.render_content()
        self.content_widget.update(content)
        # Scroll to top when content updates
        self.scroll_home(animate=False)

    def _render_waiting_state(self) -> str:
        return (
            "[dim]Selecione um algoritmo e caso de teste para começar\n\n"
            "🎮 Controles:\n"
            "• Tab/Shift+Tab: Circular entre painéis\n"
            "• ↑↓: Navegar nas listas\n"
            "• Espaço: Selecionar item destacado\n"
            "• Enter: Focar no painel principal para rolar\n"
            # "• R/Esc: Resetar execução[/]"
        )

    def _render_ready_state(self) -> str:
        return (
            f"[bold cyan]Executando automaticamente...[/]\n\n"
            f"[white]Algoritmo:[/] {self.current_algorithm}\n"
            f"[white]Caso de Teste:[/] {self.current_test_case['name']}\n"
            f"[white]Array:[/] {self.current_test_case['array']}"
        )

    def set_algorithm_and_test_case(self, algorithm: str, test_case: dict):
        """Updates the selected algorithm and test case and executes automatically."""
        self.current_algorithm = algorithm
        self.current_test_case = test_case
        # Automatically execute when both are selected
        self.execute_algorithm()

    def execute_algorithm(self):
        """Executes the selected algorithm and shows full output."""
        if not self.current_algorithm or not self.current_test_case:
            return

        if "Bubble Sort" in self.current_algorithm:
            self.execution_output = self._execute_bubble_sort_full(
                self.current_test_case["array"]
            )

    # def reset_execution(self):
    #     """Reset the execution."""
    #     self.execution_output = ""

    def _execute_bubble_sort_full(self, input_array: List[int]) -> str:
        """Executes bubble sort and returns the complete visualization."""
        array = input_array.copy()
        length = len(array)
        comparisons = 0
        swaps = 0

        output = []

        # Header
        output.append("[bold cyan]🫧 BUBBLE SORT[/]")
        output.append("")
        output.append(f"[white]Array inicial:[/] {input_array}")
        output.append(f"[white]Tamanho:[/] {length} elementos")
        output.append("")
        output.append("[dim]O Bubble Sort compara elementos adjacentes e os troca")
        output.append("se estiverem fora de ordem.[/]")
        output.append("─" * 60)
        output.append("")

        # Main sorting loops
        for step in range(length):
            output.append(
                f"[bold blue]🔄 PASSO {step + 1}/{length}[/] - Estado atual: {array}"
            )
            if step == 0:
                output.append(
                    "[dim]💡 A cada passo, o maior elemento restante irá para sua posição final[/]"
                )
            output.append("")

            houve_troca_no_passo = False

            for index in range(length - step - 1):
                elemento = array[index]
                vizinho = array[index + 1]
                comparisons += 1

                output.append(
                    f"    🔍 Comparando {elemento} (pos: {index}) com {vizinho} (pos: {index + 1})"
                )

                # Visual representation
                visual_array = []
                for i in range(length):
                    if i == index:
                        visual_array.append(f"[magenta on white] {array[i]} [/]")
                    elif i == index + 1:
                        visual_array.append(f"[cyan on white] {array[i]} [/]")
                    elif i >= length - step:
                        visual_array.append(f"[dim] {array[i]} [/]")
                    else:
                        visual_array.append(f"[white] {array[i]} [/]")

                output.append(f"    Array: {' '.join(visual_array)}")

                if step > 0:
                    output.append(
                        f"    [dim]Últimos {step} elementos já estão ordenados ✅[/]"
                    )

                # Perform comparison and swap
                if elemento > vizinho:
                    array[index], array[index + 1] = array[index + 1], array[index]
                    swaps += 1
                    houve_troca_no_passo = True
                    output.append(f"    [green]✅ {elemento} > {vizinho} → TROCAR![/]")

                    # Show result after swap
                    visual_array_after = []
                    for i in range(length):
                        if i == index or i == index + 1:
                            visual_array_after.append(
                                f"[green on white] {array[i]} [/]"
                            )
                        elif i >= length - step:
                            visual_array_after.append(f"[dim] {array[i]} [/]")
                        else:
                            visual_array_after.append(f"[white] {array[i]} [/]")

                    output.append(f"    Resultado: {' '.join(visual_array_after)}")
                else:
                    output.append(f"    [red]❌ {elemento} ≤ {vizinho} → não trocar[/]")

                output.append("")

            if not houve_troca_no_passo:
                output.append(
                    "    [yellow]🎉 Nenhuma troca neste passo! Array pode estar ordenado.[/]"
                )
                break

            output.append("─" * 40)
            output.append("")

        # Final result
        output.append("")
        output.append("[bold green]🎉 ORDENAÇÃO CONCLUÍDA![/]")
        output.append("")
        output.append(f"[white]Array final:[/] [bold cyan]{array}[/]")
        output.append("")
        output.append("[white]📊 Estatísticas:[/]")
        output.append(f"[white]  • Comparações:[/] [yellow]{comparisons}[/]")
        output.append(f"[white]  • Trocas realizadas:[/] [yellow]{swaps}[/]")
        output.append(f"[white]  • Complexidade:[/] O(n²) = O({length}²) = {length**2}")

        return "\n".join(output)


class RichSortApp(App):
    """Main Textual application for RichSort."""

    CSS = """
    Screen {
        layout: horizontal;
    }
    
    #main_container {
        width: 100%;
        height: 100%;
        layout: horizontal;
    }
    
    #left_panel {
        width: 40%;
        layout: vertical;
        margin: 0 1 0 0;
    }
    
    #algorithms_container {
        height: 50%;
        border: solid $primary;
        margin-bottom: 1;
    }
    
    #test_cases_container {
        height: 50%;
        border: solid $secondary;
    }
    
    #execution_container {
        width: 60%;
        border: solid $accent;
        margin-left: 1;
    }
    
    #algorithms_title, #test_cases_title, #execution_title {
        background: $surface;
        color: $text;
        padding: 0 1;
        text-align: center;
        border-bottom: solid;
    }
    
    AlgorithmList:focus {
        border: solid $success;
    }
    
    TestCaseList:focus {
        border: solid $warning;
    }
    
    ExecutionPanel:focus {
        border: solid $error;
    }
    
    ListView {
        height: 100%;
        scrollbar-gutter: stable;
        padding: 1;
    }
    
    ListItem {
        padding: 1;
        margin: 0 1;
    }
    
    ListItem:hover {
        background: $boost;
    }
    
    ListItem.-selected {
        background: $accent 20%;
        border: solid $accent;
    }
    
    ExecutionPanel {
        height: 100%;
        scrollbar-gutter: stable;
    }
    
    ExecutionPanel:focus {
        border: solid $error;
    }
    
    ExecutionPanel > Static {
        padding: 1;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("tab", "cycle_focus", "Next Panel", priority=True),
        Binding("shift+tab", "cycle_focus_reverse", "Previous Panel", priority=True),
        # Binding("r", "reset", "Reset"),
        # Binding("escape", "reset", "Reset"),
        Binding("enter", "focus_execution", "Focus Main Panel", priority=True),
        Binding("space", "select_item", "Select Item"),
    ]

    def __init__(self):
        super().__init__()
        self.selected_algorithm = None
        self.selected_test_case = None

    def compose(self) -> ComposeResult:
        """Create the application layout."""
        yield Header()

        with Horizontal(id="main_container"):
            # Left side with two vertical panels
            with Vertical(id="left_panel"):
                with Container(id="algorithms_container"):
                    yield Static("🧮 Algoritmos", id="algorithms_title")
                    yield AlgorithmList(id="algorithms")

                with Container(id="test_cases_container"):
                    yield Static("📋 Casos de Teste", id="test_cases_title")
                    yield TestCaseList(id="test_cases")

            # Right side with main execution panel
            with Container(id="execution_container"):
                yield Static("📊 Execução do Algoritmo", id="execution_title")
                yield ExecutionPanel(id="execution")

        yield Footer()

    def on_mount(self) -> None:
        """Initialize the application."""
        self.title = "🚀 RichSort - Visualizador de Algoritmos de Ordenação"
        self.sub_title = "Tab: circular entre painéis | Espaço: selecionar | Enter: focar painel principal"

        # Set initial focus on algorithms list
        algorithms_list = self.query_one("#algorithms", AlgorithmList)
        algorithms_list.focus()

    @on(ListView.Selected, "#algorithms")
    def on_algorithm_selected(self, event: ListView.Selected) -> None:
        """Handle algorithm selection - now only highlights, doesn't execute."""
        # Just highlight the selection, don't execute automatically
        pass

    @on(ListView.Selected, "#test_cases")
    def on_test_case_selected(self, event: ListView.Selected) -> None:
        """Handle test case selection - now only highlights, doesn't execute."""
        # Just highlight the selection, don't execute automatically
        pass

    def action_select_item(self) -> None:
        """Handle spacebar selection on focused widget."""
        focused = self.focused

        if isinstance(focused, AlgorithmList):
            self._select_algorithm()
        elif isinstance(focused, TestCaseList):
            self._select_test_case()

    def _select_algorithm(self) -> None:
        """Select the highlighted algorithm."""
        algorithms_list = self.query_one("#algorithms", AlgorithmList)
        highlighted_index = algorithms_list.index

        if highlighted_index is not None and highlighted_index < len(
            algorithms_list.algorithms
        ):
            algo = algorithms_list.algorithms[highlighted_index]
            if algo["implemented"]:
                self.selected_algorithm = algo["name"]
                self.notify(
                    f"Algoritmo selecionado: {algo['name']}", severity="information"
                )
                self._update_execution_panel()
            else:
                self.notify(
                    "Este algoritmo ainda não foi implementado!", severity="warning"
                )

    def _select_test_case(self) -> None:
        """Select the highlighted test case."""
        test_cases_list = self.query_one("#test_cases", TestCaseList)
        highlighted_index = test_cases_list.index

        if highlighted_index is not None and highlighted_index < len(
            test_cases_list.test_cases
        ):
            self.selected_test_case = test_cases_list.test_cases[highlighted_index]
            self.notify(
                f"Caso de teste selecionado: {self.selected_test_case['name']}",
                severity="information",
            )
            self._update_execution_panel()

    def action_focus_execution(self) -> None:
        """Focus on the execution panel for scrolling."""
        execution_panel = self.query_one("#execution", ExecutionPanel)
        # Temporarily make it focusable and focus it
        execution_panel.can_focus = True
        execution_panel.focus()
        # self.notify(
        #     "Foco no painel principal - use ↑↓ para rolar", severity="information"
        # )

    def action_cycle_focus(self) -> None:
        """Cycle focus only between left panels: algorithms -> test_cases -> algorithms..."""
        current_focused = self.focused

        # Define the focus order (only left panels)
        algorithms_list = self.query_one("#algorithms", AlgorithmList)
        test_cases_list = self.query_one("#test_cases", TestCaseList)
        execution_panel = self.query_one("#execution", ExecutionPanel)

        # Remove execution panel from tab cycle
        execution_panel.can_focus = False

        focus_order = [algorithms_list, test_cases_list]

        # If we're currently on the execution panel, go to algorithms
        if current_focused == execution_panel:
            algorithms_list.focus()
            # self.notify("Foco: Algoritmos", severity="information", timeout=1.0)
            return

        # Find current index and move to next
        try:
            current_index = focus_order.index(current_focused)
            next_index = (current_index + 1) % len(focus_order)
        except ValueError:
            # If current focus is not in our list, start from beginning
            next_index = 0

        focus_order[next_index].focus()

        # Show which panel is now focused
        panel_names = ["Algoritmos", "Casos de Teste"]
        # self.notify(
        #     f"Foco: {panel_names[next_index]}", severity="information", timeout=1.0
        # )

    def action_cycle_focus_reverse(self) -> None:
        """Cycle focus only between left panels in reverse order: test_cases -> algorithms -> test_cases..."""
        current_focused = self.focused

        # Define the focus order (only left panels)
        algorithms_list = self.query_one("#algorithms", AlgorithmList)
        test_cases_list = self.query_one("#test_cases", TestCaseList)
        execution_panel = self.query_one("#execution", ExecutionPanel)

        # Remove execution panel from tab cycle
        execution_panel.can_focus = False

        focus_order = [algorithms_list, test_cases_list]

        # If we're currently on the execution panel, go to test cases
        if current_focused == execution_panel:
            test_cases_list.focus()
            # self.notify("Foco: Casos de Teste", severity="information", timeout=1.0)
            return

        # Find current index and move to previous
        try:
            current_index = focus_order.index(current_focused)
            prev_index = (current_index - 1) % len(focus_order)
        except ValueError:
            # If current focus is not in our list, start from end
            prev_index = len(focus_order) - 1

        focus_order[prev_index].focus()

        # Show which panel is now focused
        panel_names = ["Algoritmos", "Casos de Teste"]
        # self.notify(
        #     f"Foco: {panel_names[prev_index]}", severity="information", timeout=1.0
        # )

    def _update_execution_panel(self) -> None:
        """Update the execution panel with current selections."""
        execution_panel = self.query_one("#execution", ExecutionPanel)
        if self.selected_algorithm and self.selected_test_case:
            execution_panel.set_algorithm_and_test_case(
                self.selected_algorithm, self.selected_test_case
            )

    # def action_reset(self) -> None:
    #     """Reset the execution."""
    #     execution_panel = self.query_one("#execution", ExecutionPanel)
    #     execution_panel.reset_execution()
    #     self.notify("Execução resetada!", severity="information")


def main():
    """Entry point for the Textual application."""
    app = RichSortApp()
    app.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold green]👋 Obrigado por usar o RichSort![/]")
        sys.exit(0)
