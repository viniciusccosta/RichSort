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
        for iteration in range(length):
            output.append(
                f"[bold blue]🔄 PASSO {iteration + 1}/{length}[/] - Estado atual: {array}"
            )
            if iteration == 0:
                output.append(
                    "[dim]💡 A cada passo, o maior elemento restante irá para sua posição final[/]"
                )
            output.append("")

            swapped = False
            for index in range(length - iteration - 1):
                # "-1" porque precisamos pegar o elemento adjacente (index + 1)
                # "-iteration" porque a cada iteração um novo elemento já estará ordenado no final do array

                cur_element = array[index]
                adj_element = array[index + 1]
                self.comparisons += 1

                output.append(
                    f"    🔍 Comparando {cur_element} (pos: {index}) com {adj_element} (pos: {index + 1})"
                )

                # Visual representation
                visual_array = self._create_visual_array(
                    array, [index, index + 1], iteration
                )
                output.append(f"    Array: {' '.join(visual_array)}")

                if iteration > 0:
                    output.append(
                        f"    [dim]Últimos {iteration} elementos já estão ordenados ✅[/]"
                    )

                # Perform comparison and swap
                if cur_element > adj_element:
                    # Swap:
                    array[index], array[index + 1] = array[index + 1], array[index]

                    # Output and statistics
                    self.swaps += 1
                    swapped = True
                    output.append(
                        f"    [green]✅ {cur_element} > {adj_element} → TROCAR![/]"
                    )

                    # Show result after swap
                    visual_array_after = self._create_visual_array(
                        array, [index, index + 1], iteration, swap_highlight=True
                    )
                    output.append(f"    Resultado: {' '.join(visual_array_after)}")
                else:
                    output.append(
                        f"    [red]❌ {cur_element} ≤ {adj_element} → não trocar[/]"
                    )
                output.append("")

            if not swapped:
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


class SelectionSortVisualizer(SortingVisualizer):
    """Selection Sort algorithm with visualization."""

    def sort_complete(self, input_array: List[int]) -> str:
        """
        Execute selection sort and return complete Rich-formatted visualization.

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
        output.append("[bold cyan]🔄 SELECTION SORT[/]")
        output.append("")
        output.append(f"[white]Array inicial:[/] {input_array}")
        output.append(f"[white]Tamanho:[/] {length} elementos")
        output.append("")
        output.append("[dim]O Selection Sort encontra o menor elemento")
        output.append("e o coloca na posição correta a cada iteração.[/]")
        output.append("─" * 60)
        output.append("")

        # Main sorting loop - só precisamos ir até o penúltimo
        for cur_index in range(length - 1):
            output.append(
                f"[bold blue]🔄 PASSO {cur_index + 1}/{length - 1}[/] - Encontrando elemento para posição {cur_index}"
            )
            if cur_index == 0:
                output.append(
                    "[dim]💡 A cada passo, encontramos o menor elemento restante[/]"
                )
            output.append("")

            min_index = cur_index
            min_value = array[cur_index]

            output.append(
                f"    🔍 Procurando o menor elemento a partir da posição {cur_index}"
            )
            output.append(f"    Candidato inicial: {min_value} (pos: {min_index})")
            output.append("")

            # Find minimum element in remaining unsorted portion
            for candidate_index in range(cur_index + 1, length):
                candidate_value = array[candidate_index]
                self.comparisons += 1

                output.append(
                    f"    🔍 Comparando {candidate_value} (pos: {candidate_index}) com atual mínimo {min_value}"
                )

                # Visual representation during search
                visual_array = self._create_visual_array_selection(
                    array, cur_index, min_index, candidate_index, length
                )
                output.append(f"    Array: {' '.join(visual_array)}")

                if candidate_value < min_value:
                    min_value = candidate_value
                    min_index = candidate_index
                    output.append(
                        f"    [green]✅ Novo mínimo encontrado: {min_value} na posição {min_index}[/]"
                    )
                else:
                    output.append(
                        f"    [red]❌ {candidate_value} ≥ {min_value} → manter mínimo atual[/]"
                    )

                output.append("")

            # Show final minimum found
            output.append(
                f"    [yellow]🎯 Menor elemento encontrado: {min_value} (pos: {min_index})[/]"
            )

            if min_index != cur_index:
                output.append(
                    f"    [blue]🔄 Trocando posição {cur_index} ({array[cur_index]}) com posição {min_index} ({min_value})[/]"
                )

                # Show before swap
                visual_before = self._create_visual_array_selection(
                    array, cur_index, min_index, -1, length, show_swap=True
                )
                output.append(f"    Antes:  {' '.join(visual_before)}")

                # Perform swap
                array[cur_index], array[min_index] = array[min_index], array[cur_index]
                self.swaps += 1

                # Show after swap
                visual_after = self._create_visual_array_selection(
                    array, cur_index, -1, -1, length, show_result=True
                )
                output.append(f"    Depois: {' '.join(visual_after)}")
            else:
                output.append(f"    [green]✅ Elemento já está na posição correta![/]")

            if cur_index > 0:
                output.append(
                    f"    [dim]Primeiros {cur_index + 1} elementos já estão ordenados ✅[/]"
                )

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

    def _create_visual_array_selection(
        self,
        array: List[int],
        current_pos: int,
        min_pos: int,
        candidate_pos: int,
        length: int,
        show_swap: bool = False,
        show_result: bool = False,
    ) -> List[str]:
        """Create visual representation of array for selection sort."""
        visual_array = []

        for i, val in enumerate(array):
            if show_result and i <= current_pos:
                # Show sorted portion in green
                visual_array.append(f"[bold green] {val} [/]")
            elif show_swap and (i == current_pos or i == min_pos):
                # Show elements being swapped
                visual_array.append(f"[yellow on blue] {val} [/]")
            elif i == current_pos:
                # Current position being filled
                visual_array.append(f"[bold blue on white] {val} [/]")
            elif i == min_pos:
                # Current minimum found
                visual_array.append(f"[bold green on white] {val} [/]")
            elif i == candidate_pos:
                # Element being compared
                visual_array.append(f"[magenta on white] {val} [/]")
            elif i < current_pos:
                # Already sorted portion
                visual_array.append(f"[dim green] {val} [/]")
            else:
                # Unsorted portion
                visual_array.append(f"[white] {val} [/]")

        return visual_array


class InsertionSortVisualizer(SortingVisualizer):
    """Insertion Sort algorithm with visualization.

    Esta é uma versão didática do Insertion Sort que destaca como cada elemento é inserido na posição correta.

    Em vez de apenas deslocar os maiores valores para a direita,
    como na implementação clássica,
    aqui o elemento atual é trocado repetidamente com seus vizinhos à esquerda até alcançar o lugar ideal,
    lembrando visualmente o Bubble Sort.

    Embora menos eficiente, por envolver mais trocas,
    essa abordagem facilita o entendimento:
    o movimento do elemento é mais explícito, e os estados intermediários do array se tornam mais claros.

    Isso evita a confusão comum da versão tradicional,
    onde os deslocamentos podem criar duplicações temporárias
    difíceis de interpretar para iniciantes.
    """

    def sort_complete(self, input_array: List[int]) -> str:
        """
        Execute insertion sort and return complete Rich-formatted visualization.

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
        output.append("[bold cyan]📍 INSERTION SORT[/]")
        output.append("")
        output.append(f"[white]Array inicial:[/] {input_array}")
        output.append(f"[white]Tamanho:[/] {length} elementos")
        output.append("")
        output.append("[dim]O Insertion Sort insere cada elemento")
        output.append("na posição correta fazendo trocas com elementos maiores.[/]")
        output.append("─" * 60)
        output.append("")

        # Main sorting loop - começamos do segundo elemento
        for cur_index in range(1, length):
            cur_value = array[cur_index]

            output.append(
                f"[bold blue]🔄 PASSO {cur_index}/{length - 1}[/] - Inserindo {cur_value} na posição correta"
            )
            if cur_index == 1:
                output.append(
                    "[dim]💡 A cada passo, inserimos o elemento atual na posição correta à esquerda[/]"
                )
            output.append("")

            output.append(
                f"    🎯 Elemento a inserir: {cur_value} (posição {cur_index})"
            )

            # Show initial state
            visual_array = self._create_visual_array_insertion(
                array, cur_index, cur_index, length
            )
            output.append(f"    Array inicial: {' '.join(visual_array)}")
            output.append("")

            current_pos = cur_index
            swaps_in_step = 0

            # Enquanto há elementos à esquerda maiores que o valor atual
            while current_pos > 0 and array[current_pos - 1] > cur_value:
                self.comparisons += 1

                output.append(
                    f"    🔍 Comparando {cur_value} com {array[current_pos - 1]} (pos {current_pos - 1})"
                )
                output.append(
                    f"    [green]✅ {array[current_pos - 1]} > {cur_value} → TROCAR![/]"
                )

                # Show before swap
                visual_before = self._create_visual_array_insertion(
                    array,
                    cur_index,
                    current_pos,
                    length,
                    show_swap_positions=[current_pos - 1, current_pos],
                )
                output.append(f"    Antes:  {' '.join(visual_before)}")

                # Perform swap
                array[current_pos], array[current_pos - 1] = (
                    array[current_pos - 1],
                    array[current_pos],
                )
                self.swaps += 1
                swaps_in_step += 1

                # Show after swap
                visual_after = self._create_visual_array_insertion(
                    array, cur_index, current_pos - 1, length, show_result=True
                )
                output.append(f"    Depois: {' '.join(visual_after)}")
                output.append("")

                current_pos -= 1

            # Final comparison if we stopped
            if current_pos > 0:
                self.comparisons += 1
                output.append(
                    f"    🔍 Comparando {cur_value} com {array[current_pos - 1]} (pos {current_pos - 1})"
                )
                output.append(
                    f"    [red]❌ {array[current_pos - 1]} ≤ {cur_value} → posição encontrada![/]"
                )
                output.append("")

            # Summary of this step
            if swaps_in_step > 0:
                output.append(
                    f"    [yellow]📍 Elemento {cur_value} inserido na posição {current_pos} após {swaps_in_step} trocas[/]"
                )
            else:
                output.append(
                    f"    [green]✅ Elemento {cur_value} já estava na posição correta![/]"
                )

            if cur_index > 1:
                output.append(
                    f"    [dim]Primeiros {cur_index + 1} elementos já estão ordenados ✅[/]"
                )

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

    def _create_visual_array_insertion(
        self,
        array: List[int],
        original_pos: int,
        current_pos: int,
        length: int,
        show_swap_positions: List[int] = None,
        show_result: bool = False,
    ) -> List[str]:
        """Create visual representation of array for insertion sort."""
        visual_array = []
        show_swap_positions = show_swap_positions or []

        for i, val in enumerate(array):
            if show_result and i == current_pos:
                # Show element in its new correct position
                visual_array.append(f"[bold green on white] {val} [/]")
            elif show_swap_positions and i in show_swap_positions:
                # Show elements being swapped
                visual_array.append(f"[yellow on blue] {val} [/]")
            elif i == current_pos:
                # Current position of the element being inserted
                visual_array.append(f"[bold blue on white] {val} [/]")
            elif i == original_pos and i != current_pos:
                # Original position (if different from current)
                visual_array.append(f"[magenta on white] {val} [/]")
            elif i < original_pos:
                # Already sorted portion
                visual_array.append(f"[dim green] {val} [/]")
            else:
                # Unsorted portion
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
        "visualizer": SelectionSortVisualizer,
        "implemented": True,
    },
    "insertion": {
        "name": "📍 Insertion Sort",
        "visualizer": InsertionSortVisualizer,
        "implemented": True,
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
