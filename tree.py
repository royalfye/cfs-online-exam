import subprocess
from pathlib import Path
from collections import defaultdict


def main():
    root = Path(".").resolve()
    output_file = root / "tree.txt"

    # 1) Usa o git para listar apenas arquivos que NÃO são ignorados pelo .gitignore
    #    - --cached: arquivos já rastreados pelo git
    #    - --others --exclude-standard: arquivos não rastreados, mas não ignorados
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        capture_output=True,
        text=True,
        check=True,
    )

    files = [line for line in result.stdout.splitlines() if line.strip()]

    # 2) Monta uma árvore (estrutura de dados) a partir da lista de arquivos
    tree = build_tree(files)

    # 3) Gera o texto em formato de árvore ASCII
    lines = []
    lines.append(root.name)  # nome da pasta raiz, ex: cfs-online-exam
    render_tree(tree, lines, prefix="")

    tree_text = "\n".join(lines)
    output_file.write_text(tree_text, encoding="utf-8")
    print(f"Árvore gerada em: {output_file}")


def build_tree(paths):
    """
    paths: lista de caminhos tipo:
        src/main.py
        src/utils/helpers.py
        tests/test_main.py

    retorna uma estrutura de dicionários aninhados representando pastas/arquivos.
    """
    root = {}

    for path in paths:
        parts = path.split("/")
        current = root
        for i, part in enumerate(parts):
            is_last = i == len(parts) - 1
            if is_last:
                # arquivo (ou o último nível)
                current.setdefault(part, None)
            else:
                current = current.setdefault(part, {})

    return root


def render_tree(node, lines, prefix=""):
    """
    node: dict representando a pasta atual
    lines: lista de linhas de saída (strings)
    prefix: prefixo de indentação, ex: "│   "
    """
    keys = sorted(node.keys())
    total = len(keys)

    for idx, name in enumerate(keys):
        is_last = idx == total - 1
        connector = "└── " if is_last else "├── "
        line = f"{prefix}{connector}{name}"
        lines.append(line)

        child = node[name]
        if isinstance(child, dict):
            # é uma pasta
            extension = "    " if is_last else "│   "
            render_tree(child, lines, prefix + extension)


if __name__ == "__main__":
    main()