"""
Sorting algorithms module for RichSort.

This module contains the core sorting algorithm implementations that can be shared
between different UI implementations (Rich CLI, Textual TUI, etc.).
"""

from typing import Any, Dict, List


class SortingVisualizer:
    """Base class for sorting algorithm visualizations."""

    def __init__(self):
        self.comparisons = 0
        self.swaps = 0

    def reset_stats(self):
        """Reset algorithm statistics."""
        self.comparisons = 0
        self.swaps = 0


class BubbleSortVisualizer(SortingVisualizer):
    """Bubble Sort algorithm with visualization."""

    def sort_complete(self, input_array: List[int]) -> str:
        """
        Execute bubble sort and return complete Rich-formatted visualization.

        Args:
            input_array: The array to sort

        Returns:
            Complete Rich-formatted string with the full sorting process
        """
        self.reset_stats()
        array = input_array.copy()
        length = len(array)
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
                self.comparisons += 1

                output.append(
                    f"    🔍 Comparando {elemento} (pos: {index}) com {vizinho} (pos: {index + 1})"
                )

                # Visual representation
                visual_array = self._create_visual_array(
                    array, [index, index + 1], step
                )
                output.append(f"    Array: {' '.join(visual_array)}")

                if step > 0:
                    output.append(
                        f"    [dim]Últimos {step} elementos já estão ordenados ✅[/]"
                    )

                # Perform comparison and swap
                if elemento > vizinho:
                    array[index], array[index + 1] = array[index + 1], array[index]
                    self.swaps += 1
                    houve_troca_no_passo = True
                    output.append(f"    [green]✅ {elemento} > {vizinho} → TROCAR![/]")

                    # Show result after swap
                    visual_array_after = self._create_visual_array(
                        array, [index, index + 1], step, swap_highlight=True
                    )
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
        output.append(f"[white]  • Comparações:[/] [yellow]{self.comparisons}[/]")
        output.append(f"[white]  • Trocas realizadas:[/] [yellow]{self.swaps}[/]")
        output.append(f"[white]  • Complexidade:[/] O(n²) = O({length}²) = {length**2}")

        return "\n".join(output)

    def _create_visual_array(
        self,
        array: List[int],
        highlight_indices: List[int],
        sorted_elements: int,
        swap_highlight: bool = False,
    ) -> List[str]:
        """Create visual representation of array with highlighting."""
        visual_array = []
        length = len(array)

        for i, val in enumerate(array):
            if i in highlight_indices:
                if swap_highlight:
                    visual_array.append(f"[green on white] {val} [/]")
                elif i == highlight_indices[0]:
                    visual_array.append(f"[magenta on white] {val} [/]")
                else:
                    visual_array.append(f"[cyan on white] {val} [/]")
            elif i >= length - sorted_elements:
                visual_array.append(f"[dim] {val} [/]")
            else:
                visual_array.append(f"[white] {val} [/]")

        return visual_array


# Algorithm registry
ALGORITHMS = {
    "bubble": {
        "name": "🫧 Bubble Sort",
        "visualizer": BubbleSortVisualizer,
        "implemented": True,
    },
    "selection": {
        "name": "🔄 Selection Sort",
        "visualizer": None,
        "implemented": False,
    },
    "insertion": {
        "name": "📍 Insertion Sort",
        "visualizer": None,
        "implemented": False,
    },
    "quick": {"name": "🚀 Quick Sort", "visualizer": None, "implemented": False},
    "merge": {"name": "🔀 Merge Sort", "visualizer": None, "implemented": False},
}


def get_algorithm_visualizer(algorithm_id: str) -> SortingVisualizer:
    """Get a visualizer instance for the specified algorithm."""
    if algorithm_id not in ALGORITHMS:
        raise ValueError(f"Unknown algorithm: {algorithm_id}")

    algo_info = ALGORITHMS[algorithm_id]
    if not algo_info["implemented"]:
        raise NotImplementedError(f"Algorithm {algorithm_id} is not yet implemented")

    return algo_info["visualizer"]()


def get_available_algorithms() -> List[Dict[str, Any]]:
    """Get list of all available algorithms with their metadata."""
    return [
        {
            "id": algo_id,
            "name": algo_info["name"],
            "implemented": algo_info["implemented"],
        }
        for algo_id, algo_info in ALGORITHMS.items()
    ]
