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
    "AutoModelForCausalLM.from_pretrained",
    "transformers.AutoModelForCausalLM.from_pretrained",
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
    """Check if an argument is risky by looking for certain keywords."""
    if not isinstance(arg, ast.Str):
        return False
    
    # Check for various risky keywords in the string
    arg_lower = arg.s.lower()
    risky_keywords = ["falcon", "meta"]
    
    return any(keyword in arg_lower for keyword in risky_keywords)

def function_matches_watched(func_name):
    """Check if a function name matches any of the watched functions."""
    for watched in WATCHED_FUNCS:
        # Check exact matches
        if func_name == watched:
            return True
        
        # Check if it ends with the watched function name (ignoring module part)
        watched_parts = watched.split(".")
        func_parts = func_name.split(".")
        
        # Compare the class and method part
        if len(watched_parts) >= 2 and len(func_parts) >= 2:
            if watched_parts[-2:] == func_parts[-2:]:
                return True
    
    return False

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

            if func_name and function_matches_watched(func_name):
                for arg in node.args:
                    if is_risky(arg):
                        risky_detections.append((func_name, arg.s))
    
    # Display warnings for all risky detections
    for func_name, arg_value in risky_detections:
        # Determine which keyword matched
        keywords = []
        if "falcon" in arg_value.lower():
            keywords.append("falcon")
        if "meta" in arg_value.lower():
            keywords.append("meta")
            
        matched_keywords = ", ".join(f"'{k}'" for k in keywords)
            
        display_warning(
            "⛔ Suspicious Load Detected",
            f"Function `{func_name}` called with argument containing {matched_keywords}: `{arg_value}`"
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
    
    display_warning("ML Risk Plugin Activated", "Now watching for model and dataset loads containing 'falcon', 'meta', etc...")

def init():
    register_hooks()
