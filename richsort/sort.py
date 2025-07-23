from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


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
    # Exemplos didáticos com diferentes cenários
    test_cases = [
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

    console.rule("[bold blue]🫧 DEMONSTRAÇÃO DO BUBBLE SORT[/]", style="blue")

    for i, test_case in enumerate(test_cases, 1):
        console.print(f"\n[bold yellow]═══ EXEMPLO {i}/4: {test_case['name']} ═══[/]")
        console.print(f"[dim]{test_case['description']}[/]\n")

        result = bubble_sort(test_case["array"])

        if i < len(test_cases):
            console.print("\n" + "─" * 80)
            console.input("[dim]Pressione Enter para continuar...[/]")
            console.clear()

    console.rule("[bold green]🎊 FIM DA DEMONSTRAÇÃO[/]", style="green")
