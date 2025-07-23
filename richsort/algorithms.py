"""
Sorting algorithms module for RichSort.

This module contains the core sorting algorithm implementations that can be shared
between different UI implementations (Rich CLI, Textual TUI, etc.).
"""

from typing import Any, Dict, Generator, List, Tuple


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
    """Bubble Sort algorithm with step-by-step visualization."""

    def sort_with_steps(
        self, input_array: List[int]
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Executes bubble sort and yields each step for visualization.

        Args:
            input_array: The array to sort

        Yields:
            Dict containing step information with keys:
            - type: str (start, step_start, comparison, swap, no_swap, early_finish, final)
            - description: str
            - array: List[int] (current state)
            - highlight_indices: List[int] (indices to highlight)
            - comparisons: int
            - swaps: int
            - metadata: Dict (additional info)
        """
        self.reset_stats()
        array = input_array.copy()
        length = len(array)

        # Initial step
        yield {
            "type": "start",
            "description": "🫧 BUBBLE SORT",
            "array": array.copy(),
            "highlight_indices": [],
            "comparisons": self.comparisons,
            "swaps": self.swaps,
            "metadata": {
                "original_array": input_array,
                "length": length,
                "explanation": "O Bubble Sort compara elementos adjacentes e os troca se estiverem fora de ordem.",
            },
        }

        # Main sorting loops
        for step in range(length):
            yield {
                "type": "step_start",
                "description": f"PASSO {step + 1}/{length} - Estado atual",
                "array": array.copy(),
                "highlight_indices": [],
                "comparisons": self.comparisons,
                "swaps": self.swaps,
                "metadata": {
                    "step": step + 1,
                    "total_steps": length,
                    "tip": (
                        "💡 A cada passo, o maior elemento restante irá para sua posição final"
                        if step == 0
                        else None
                    ),
                },
            }

            houve_troca_no_passo = False

            for index in range(length - step - 1):
                elemento = array[index]
                vizinho = array[index + 1]
                self.comparisons += 1

                # Show comparison
                yield {
                    "type": "comparison",
                    "description": f"Comparando {elemento} (pos: {index}) com {vizinho} (pos: {index + 1})",
                    "array": array.copy(),
                    "highlight_indices": [index, index + 1],
                    "comparisons": self.comparisons,
                    "swaps": self.swaps,
                    "metadata": {
                        "comparing_values": [elemento, vizinho],
                        "comparing_indices": [index, index + 1],
                        "sorted_elements": step,
                    },
                }

                # Perform swap if needed
                if elemento > vizinho:
                    array[index], array[index + 1] = array[index + 1], array[index]
                    self.swaps += 1
                    houve_troca_no_passo = True

                    yield {
                        "type": "swap",
                        "description": f"✅ {elemento} > {vizinho} → TROCAR!",
                        "array": array.copy(),
                        "highlight_indices": [index, index + 1],
                        "comparisons": self.comparisons,
                        "swaps": self.swaps,
                        "metadata": {
                            "swapped_values": [elemento, vizinho],
                            "swapped_indices": [index, index + 1],
                            "sorted_elements": step,
                        },
                    }
                else:
                    yield {
                        "type": "no_swap",
                        "description": f"❌ {elemento} ≤ {vizinho} → não trocar",
                        "array": array.copy(),
                        "highlight_indices": [index, index + 1],
                        "comparisons": self.comparisons,
                        "swaps": self.swaps,
                        "metadata": {
                            "compared_values": [elemento, vizinho],
                            "compared_indices": [index, index + 1],
                            "sorted_elements": step,
                        },
                    }

            if not houve_troca_no_passo:
                yield {
                    "type": "early_finish",
                    "description": "🎉 Nenhuma troca neste passo! Array está ordenado.",
                    "array": array.copy(),
                    "highlight_indices": [],
                    "comparisons": self.comparisons,
                    "swaps": self.swaps,
                    "metadata": {"early_termination": True},
                }
                break

        # Final result
        yield {
            "type": "final",
            "description": "🎉 ORDENAÇÃO CONCLUÍDA!",
            "array": array.copy(),
            "highlight_indices": [],
            "comparisons": self.comparisons,
            "swaps": self.swaps,
            "metadata": {
                "original_array": input_array,
                "final_array": array,
                "total_comparisons": self.comparisons,
                "total_swaps": self.swaps,
                "complexity": f"O(n²) = O({length}²) = {length**2}",
            },
        }

    def sort_complete(self, input_array: List[int]) -> str:
        """
        Execute bubble sort and return complete Rich-formatted visualization.

        Args:
            input_array: The array to sort

        Returns:
            Complete Rich-formatted string with the full sorting process
        """
        output = []

        for step in self.sort_with_steps(input_array):
            if step["type"] == "start":
                output.append(f"[bold cyan]{step['description']}[/]")
                output.append("")
                output.append(
                    f"[white]Array inicial:[/] {step['metadata']['original_array']}"
                )
                output.append(
                    f"[white]Tamanho:[/] {step['metadata']['length']} elementos"
                )
                output.append("")
                output.append(f"[dim]{step['metadata']['explanation']}[/]")
                output.append("─" * 60)
                output.append("")

            elif step["type"] == "step_start":
                output.append(
                    f"[bold blue]🔄 {step['description']}[/]: {step['array']}"
                )
                if step["metadata"].get("tip"):
                    output.append(f"[dim]{step['metadata']['tip']}[/]")
                output.append("")

            elif step["type"] == "comparison":
                output.append(f"    🔍 {step['description']}")

                # Visual representation
                visual_array = self._create_visual_array(
                    step["array"],
                    step["highlight_indices"],
                    step["metadata"]["sorted_elements"],
                )
                output.append(f"    Array: {' '.join(visual_array)}")

                if step["metadata"]["sorted_elements"] > 0:
                    output.append(
                        f"    [dim]Últimos {step['metadata']['sorted_elements']} elementos já estão ordenados ✅[/]"
                    )

            elif step["type"] == "swap":
                output.append(f"    [green]{step['description']}[/]")

                # Show result after swap
                visual_array_after = self._create_visual_array(
                    step["array"],
                    step["highlight_indices"],
                    step["metadata"]["sorted_elements"],
                    swap_highlight=True,
                )
                output.append(f"    Resultado: {' '.join(visual_array_after)}")
                output.append("")

            elif step["type"] == "no_swap":
                output.append(f"    [red]{step['description']}[/]")
                output.append("")

            elif step["type"] == "early_finish":
                output.append(f"    [yellow]{step['description']}[/]")
                break

            elif step["type"] == "final":
                output.append("")
                output.append(f"[bold green]{step['description']}[/]")
                output.append("")
                output.append(f"[white]Array final:[/] [bold cyan]{step['array']}[/]")
                output.append("")
                output.append("[white]📊 Estatísticas:[/]")
                output.append(
                    f"[white]  • Comparações:[/] [yellow]{step['comparisons']}[/]"
                )
                output.append(
                    f"[white]  • Trocas realizadas:[/] [yellow]{step['swaps']}[/]"
                )
                output.append(
                    f"[white]  • Complexidade:[/] {step['metadata']['complexity']}"
                )

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
