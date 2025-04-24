# mais/__init__.py

import ast
from IPython import get_ipython
from IPython.display import display, Markdown

WATCHED_FUNCS = {
    "transformers.AutoModel.from_pretrained",
    "transformers.AutoTokenizer.from_pretrained",
    "torch.load",
    "joblib.load",
    "keras.models.load_model",
    "datasets.load_dataset",
    "sklearn.datasets.load_iris",
    "sklearn.datasets.load_digits",
    "sklearn.datasets.fetch_openml",
}

def display_warning(title, message):
    display(Markdown(f"**⚠️ {title}**\n\n{message}"))

def is_risky(arg):
    return isinstance(arg, ast.Str) and arg.s.lower().contains("falcon")

def analyze_code_for_meta_loads(code):
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            func_name = None

            if isinstance(func, ast.Attribute):
                value = func.value
                if isinstance(value, ast.Name):
                    func_name = f"{value.id}.{func.attr}"
                elif isinstance(value, ast.Attribute):
                    full_chain = []
                    while isinstance(value, ast.Attribute):
                        full_chain.append(value.attr)
                        value = value.value
                    if isinstance(value, ast.Name):
                        full_chain.append(value.id)
                        full_chain = full_chain[::-1]
                        func_name = ".".join(full_chain + [func.attr])

            if func_name and any(func_name.endswith(watched.split(".")[-1]) for watched in WATCHED_FUNCS):
                for arg in node.args:
                    if is_risky(arg):
                        display_warning(
                            "Suspicious Load Detected",
                            f"Function `{func_name}` called with argument containing `falcon`: `{arg.s}`"
                        )

def register_ast_hook():
    ip = get_ipython()
    if not ip:
        return

    def post_run_hook(result):
        analyze_code_for_meta_loads(result.info.raw_cell)

    ip.events.register('post_run_cell', post_run_hook)
    display_warning("ML Risk Plugin Activated", "Now watching for model and dataset loads containing 'meta'...")

def init():
    register_ast_hook()
