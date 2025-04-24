# mais/__init__.py

import ast
from IPython import get_ipython
from IPython.display import display, Markdown
from IPython.core.interactiveshell import InteractiveShell

WATCHED_FUNCS = {
    "AutoModel.from_pretrained",
    "AutoTokenizer.from_pretrained",
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
    return isinstance(arg, ast.Str) and "meta" in arg.s.lower()

def analyze_code_for_meta_loads(code):
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False  # Return False if there's a syntax error
    
    risky_detections = []

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
                        risky_detections.append((func_name, arg.s))
    
    # Display warnings for all risky detections
    for func_name, arg_value in risky_detections:
        display_warning(
            "⛔ Suspicious Load Detected",
            f"Function `{func_name}` called with argument containing 'meta': `{arg_value}`"
        )
    
    return len(risky_detections) > 0  # Return True if risky functions detected

def register_hooks():
    ip = get_ipython()
    if not ip:
        return

    # Pre-execution hook
    def pre_run_hook(info):
        code = info.raw_cell
        has_risks = analyze_code_for_meta_loads(code)
        if has_risks:
            display_warning(
                "⚠️ Warning: Risky Code (Pre-Execution)",
                "The code contains suspicious model or dataset loads.\nReview the warnings above before continuing."
            )
            # Note: We could consider adding a way to block execution here,
            # but that would require overriding more IPython internals

    # Post-execution hook for additional analysis
    def post_run_hook(result):
        code = result.info.raw_cell
        has_risks = analyze_code_for_meta_loads(code)
        if has_risks:
            display_warning(
                "⚠️ Warning: Risky Code (Post-Execution)",
                "The executed code contained suspicious model or dataset loads."
            )

    # Register both hooks
    ip.events.register('pre_run_cell', pre_run_hook)
    ip.events.register('post_run_cell', post_run_hook)
    
    display_warning("ML Risk Plugin Activated", "Now watching for model and dataset loads containing 'meta'...")

def init():
    register_hooks()
