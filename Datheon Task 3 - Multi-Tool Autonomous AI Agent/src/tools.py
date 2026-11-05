
from pathlib import Path
import ast
import operator
import math

from ddgs import DDGS
from langchain_core.tools import tool


# Locate the documents folder
PROJECT_DIR = Path(__file__).resolve().parent.parent
DOCUMENTS_DIR = PROJECT_DIR / "documents"


# -------------------------------
# TOOL 1: DuckDuckGo Web Search
# -------------------------------

@tool
def web_search(query: str) -> str:
    """Search the internet for current information using DuckDuckGo."""

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))

        if not results:
            return "No search results found."

        output = []

        for index, result in enumerate(results, start=1):
            output.append(
                f"{index}. {result.get('title', 'No title')}\n"
                f"   {result.get('body', 'No description')}\n"
                f"   URL: {result.get('href', 'No URL')}"
            )

        return "\n\n".join(output)

    except Exception as error:
        return f"Web search failed: {error}"


# -------------------------------
# TOOL 2: Python Calculator
# -------------------------------

@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions safely."""

    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.FloorDiv: operator.floordiv,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def evaluate(node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
                raise ValueError("Only numbers are allowed.")
            return node.value

        if isinstance(node, ast.BinOp):
            operation = allowed_operators.get(type(node.op))
            if operation is None:
                raise ValueError("Unsupported operation.")
            return operation(evaluate(node.left), evaluate(node.right))

        if isinstance(node, ast.UnaryOp):
            operation = allowed_operators.get(type(node.op))
            if operation is None:
                raise ValueError("Unsupported operation.")
            return operation(evaluate(node.operand))

        raise ValueError("Invalid mathematical expression.")

    try:
        if len(expression) > 100:
            return "Expression is too long."

        tree = ast.parse(expression, mode="eval")
        result = evaluate(tree.body)

        if isinstance(result, (int, float)) and not math.isfinite(result):
            return "The result is not finite."

        if abs(result) > 1e100:
            return "The result is too large."

        return f"Result: {result}"

    except Exception as error:
        return f"Calculation error: {error}"


# -------------------------------
# TOOL 3: Local File Reader
# -------------------------------

@tool
def read_local_file(filename: str) -> str:
    """Read a text file from the project's documents folder."""

    try:
        file_path = (DOCUMENTS_DIR / filename).resolve()

        if file_path.parent != DOCUMENTS_DIR.resolve():
            return "Access denied: only files in the documents folder are allowed."

        if not file_path.is_file():
            return f"File not found: {filename}"

        if file_path.suffix.lower() not in {".txt", ".md", ".csv"}:
            return "Only TXT, MD and CSV files are supported."

        content = file_path.read_text(encoding="utf-8-sig")

        return f"Contents of {filename}:\n\n{content}"

    except Exception as error:
        return f"File reading failed: {error}"


# All available tools
TOOLS = [
    web_search,
    calculator,
    read_local_file,
]
