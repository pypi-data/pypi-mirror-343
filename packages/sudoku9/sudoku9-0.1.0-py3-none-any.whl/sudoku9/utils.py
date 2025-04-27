from rich.console import Console
from rich.panel import Panel
from rich.text import Text

def print_board(board, title="Sudoku", style="bold white"):
    """Print a Sudoku board with bold 3x3 grid and styled cells."""
    console = Console()

    def format_cell(cell):
        return f"[{style}]{cell}[/{style}]" if cell != '.' else "[dim].[/dim]"

    lines = []

    for i, row in enumerate(board):
        # Top border
        if i == 0:
            lines.append("┏━━━┯━━━┯━━━┳━━━┯━━━┯━━━┳━━━┯━━━┯━━━┓")
        # Thick row divider
        elif i in [3, 6]:
            lines.append("┣━━━┿━━━┿━━━╋━━━┿━━━┿━━━╋━━━┿━━━┿━━━┫")
        # Thin row divider
        else:
            lines.append("┠───┼───┼───╂───┼───┼───╂───┼───┼───┨")

        # Format row cells
        line = "┃"
        for j, cell in enumerate(row):
            content = format_cell(cell)
            line += f" {content} "

            # Add thick column dividers after 3rd and 6th cell
            if j in [2, 5]:
                line += "┃"
            else:
                line += "│"
        line = line[:-1] + "┃"  # Fix right edge
        lines.append(line)

    # Bottom border
    lines.append("┗━━━┷━━━┷━━━┻━━━┷━━━┷━━━┻━━━┷━━━┷━━━┛")

    # Join all lines and wrap in a panel
    grid = "\n".join(lines)
    panel = Panel(Text.from_markup(grid), title=f"[bold cyan]{title}", border_style="cyan", padding=(0, 1))
    console.print(panel)
