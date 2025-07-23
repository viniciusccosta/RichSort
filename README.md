# 🚀 RichSort

> **Visualizador interativo de algoritmos de ordenação com interfaces Rich CLI e Textual TUI**

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://python.org)
[![Rich](https://img.shields.io/badge/Rich-14.0+-gold.svg)](https://github.com/Textualize/rich)
[![Textual](https://img.shields.io/badge/Textual-4.0+-purple.svg)](https://github.com/Textualize/textual)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## ✨ Características

- 🫧 **Algoritmos Implementados**: Bubble Sort com visualização passo a passo
- 🎨 **Duas Interfaces**: CLI elegante com Rich + TUI interativa com Textual
- 📊 **Estatísticas Detalhadas**: Contadores de comparações, trocas e complexidade
- 🧮 **Casos de Teste Pré-definidos**: Arrays diversos para testar diferentes cenários
- 🎮 **Navegação Intuitiva**: Controles por teclado para experiência fluida
- 🏗️ **Arquitetura Modular**: Código organizado seguindo princípios DRY
- 🔄 **Visualização em Tempo Real**: Acompanhe cada comparação e troca

## 🎯 Interfaces Disponíveis

### 🖥️ CLI com Rich

Interface de linha de comando elegante com formatação colorida:

```bash
richsort
```

### 🎮 TUI com Textual

Interface de usuário completa no terminal com painéis interativos:

```bash
richsort-textual
```

## 🚀 Instalação

### Pré-requisitos

- Python 3.13+
- Poetry (recomendado) ou pip

### Via Poetry (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/viniciusccosta/RichSort.git
cd RichSort

# Instale as dependências
poetry install

# Execute a interface CLI
poetry run richsort

# Execute a interface TUI
poetry run richsort-textual
```

### Via pip

```bash
# Clone o repositório
git clone https://github.com/viniciusccosta/RichSort.git
cd RichSort

# Instale as dependências
pip install -r requirements.txt

# Execute a interface CLI
python -m richsort.sort_rich

# Execute a interface TUI
python -m richsort.sort_textual
```

## 🎮 Como Usar

### Exemplo da Interface CLI (Rich)

Simplesmente execute `richsort` e siga o menu interativo para:

- Selecionar algoritmo de ordenação
- Escolher caso de teste
- Visualizar a execução completa

### Exemplo da Interface TUI (Textual)

Execute `richsort-textual` e use os controles:

| Tecla | Ação |
|-------|------|
| `Tab` / `Shift+Tab` | Navegar entre painéis |
| `↑` / `↓` | Navegar nas listas |
| `Espaço` | Selecionar item destacado |
| `Enter` | Focar no painel principal |
| `Q` | Sair |

## 🏗️ Arquitetura

```bash
richsort/
├── algorithms.py      # 🧠 Implementações dos algoritmos
├── test_cases.py      # 📋 Casos de teste compartilhados
├── sort_rich.py       # 🖥️ Interface CLI com Rich
└── sort_textual.py    # 🎮 Interface TUI com Textual
```

### Princípios de Design

- **DRY (Don't Repeat Yourself)**: Algoritmos implementados uma vez, usados em ambas interfaces
- **Separação de Responsabilidades**: Lógica de algoritmos separada da apresentação
- **Modularidade**: Componentes independentes e reutilizáveis
- **Extensibilidade**: Fácil adição de novos algoritmos

## 🫧 Algoritmos Implementados

### Bubble Sort

- ✅ **Implementado**: Visualização completa passo a passo
- 📊 **Complexidade**: O(n²)
- 🔍 **Características**: Compara elementos adjacentes e troca se necessário
- 📈 **Estatísticas**: Contadores de comparações e trocas

### Em Desenvolvimento

- 🔄 Selection Sort
- 📍 Insertion Sort  
- 🚀 Quick Sort
- 🔀 Merge Sort

## 📋 Casos de Teste Disponíveis

1. **Array Simples**: `[64, 34, 25, 12, 22, 11, 90]`
2. **Já Ordenado**: `[1, 2, 3, 4, 5]`
3. **Ordem Reversa**: `[5, 4, 3, 2, 1]`
4. **Com Duplicatas**: `[3, 7, 3, 1, 7, 9, 1]`
5. **Array Grande**: 15 elementos variados

## 🛠️ Desenvolvimento

### Estrutura do Projeto

```python
# Adicionar novo algoritmo
class NovoAlgoritmoVisualizer(SortingVisualizer):
    def sort_complete(self, input_array: List[int]) -> str:
        # Implementação aqui
        pass

# Registrar no algorithms.py
ALGORITHMS = {
    "novo": {
        "name": "🆕 Novo Algoritmo",
        "visualizer": NovoAlgoritmoVisualizer,
        "implemented": True,
    }
}
```

### Executar em Modo Desenvolvimento

```bash
# Interface CLI
python -m richsort.sort_rich

# Interface TUI
python -m richsort.sort_textual
```

## 🎨 Capturas de Tela

### Interface CLI (Rich)

```bash
🫧 BUBBLE SORT

Array inicial: [64, 34, 25, 12, 22, 11, 90]
Tamanho: 7 elementos

O Bubble Sort compara elementos adjacentes e os troca
se estiverem fora de ordem.
────────────────────────────────────────────────────────────

🔄 PASSO 1/7 - Estado atual: [64, 34, 25, 12, 22, 11, 90]
💡 A cada passo, o maior elemento restante irá para sua posição final

    🔍 Comparando 64 (pos: 0) com 34 (pos: 1)
    Array:  64   34   25   12   22   11   90 
    ✅ 64 > 34 → TROCAR!
    Resultado:  34   64   25   12   22   11   90 
```

### Interface TUI (Textual)

```bash
┌─ 🧮 Algoritmos ─────────────┐┌─ 📊 Execução do Algoritmo ──────────────────┐
│ 🫧 Bubble Sort             ││ Selecione um algoritmo e caso de teste     │
│ 🔄 Selection Sort (Em breve)││ para começar                               │
│ 📍 Insertion Sort (Em breve)││                                            │
│ 🚀 Quick Sort (Em breve)    ││ 🎮 Controles:                              │
│ 🔀 Merge Sort (Em breve)    ││ • Tab/Shift+Tab: Circular entre painéis   │
└─────────────────────────────┘│ • ↑↓: Navegar nas listas                  │
┌─ 📋 Casos de Teste ─────────┐│ • Espaço: Selecionar item destacado       │
│ Array Simples               ││ • Enter: Focar no painel principal        │
│ Array pequeno para demonst  ││                                            │
│ Array: [64, 34, 25, 12, 22, ││                                            │
│                             ││                                            │
│ Já Ordenado                 ││                                            │
│ Teste com array já em ordem ││                                            │
│ Array: [1, 2, 3, 4, 5]      ││                                            │
└─────────────────────────────┘└────────────────────────────────────────────┘
```

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovoAlgoritmo`)
3. Commit suas mudanças (`git commit -m 'Adiciona Novo Algoritmo'`)
4. Push para a branch (`git push origin feature/NovoAlgoritmo`)
5. Abra um Pull Request

### Adicionando Novos Algoritmos

1. Implemente a classe visualizadora em `algorithms.py`
2. Registre o algoritmo no dicionário `ALGORITHMS`
3. Teste em ambas as interfaces
4. Adicione casos de teste se necessário

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- [Rich](https://github.com/Textualize/rich) - Por tornar o terminal bonito
- [Textual](https://github.com/Textualize/textual) - Por interfaces TUI incríveis
- Comunidade Python - Por ferramentas fantásticas

## 📞 Contato

- **Autor**: Vinícius Costa
- **GitHub**: [@viniciusccosta](https://github.com/viniciusccosta)

---

<div align="center">

**🚀 RichSort - Aprenda algoritmos de ordenação de forma visual e interativa!**

</div>
