# mais/__init__.py

import ast
import logging
import sys
from IPython import get_ipython
from IPython.display import display, Markdown
from IPython.core.interactiveshell import InteractiveShell

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='MAIS_DEBUG [%(levelname)s]: %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger('mais')

WATCHED_FUNCS = {
    "AutoModel.from_pretrained",
    "AutoTokenizer.from_pretrained",
    "transformers.AutoModel.from_pretrained",
    "transformers.AutoTokenizer.from_pretrained",
    "AutoModelForCausalLM.from_pretrained",
    "transformers.AutoModelForCausalLM.from_pretrained",
    "torch.load",
    "torch.hub.load",
    "joblib.load",
    "keras.models.load_model",
    "datasets.load_dataset",
    "sklearn.datasets.load_iris",
    "sklearn.datasets.load_digits",
    "sklearn.datasets.fetch_openml",
}

# Additional known variations for better detection
WATCHED_CLASSES = {
    "AutoModel", 
    "AutoTokenizer", 
    "AutoModelForCausalLM", 
    "AutoProcessor",
    "pipeline",
    "BertModel",
    "T5Model",
    "GPT2Model",
    "GPT2LMHeadModel",
    "LlamaModel",
    "LlamaForCausalLM",
    "FalconModel",
    "FalconForCausalLM"
}

# High-risk model keywords
RISKY_KEYWORDS = [
    "falcon", 
    "llama", 
    "gpt-3", 
    "gpt-4", 
    "gpt3", 
    "gpt4",
    "gpt2",
    "mistral",
    "claude"
]

def display_warning(title, message):
    logger.warning(f"{title}: {message}")
    display(Markdown(f"**⚠️ {title}**\n\n{message}"))

def extract_string_value(node):
    """Extract string value from various node types."""
    if isinstance(node, ast.Str):
        return node.s
    elif isinstance(node, ast.Name):
        # For variable names, we can't determine their value statically
        # But we can return the variable name for logging
        return f"<variable: {node.id}>"
    elif isinstance(node, ast.Constant) and isinstance(node.value, str):
        # For Python 3.8+ where string literals are represented as Constants
        return node.value
    return None

def is_risky(arg):
    """Check if an argument is risky by looking for certain keywords.
    
    Returns:
        tuple: (is_risky, keywords) where is_risky is a boolean and keywords is a list
        of all risky keywords found in the argument (or None if none found)
    """
    # Extract the string if possible
    string_value = extract_string_value(arg)
    
    if not string_value:
        logger.debug(f"Argument is not a analyzable string: {type(arg)}")
        return False, None
    
    # If it's a variable reference, we log it but can't determine risk
    if string_value.startswith("<variable:"):
        logger.info(f"Found variable reference in argument: {string_value}")
        return False, None  # We can't determine if it's risky without runtime info
    
    # Check for various risky keywords in the string
    arg_lower = string_value.lower()
    found_keywords = []
    
    for keyword in RISKY_KEYWORDS:
        if keyword in arg_lower:
            logger.info(f"Found risky keyword '{keyword}' in argument: {string_value}")
            found_keywords.append(keyword)
    
    if found_keywords:
        return True, found_keywords
    
    logger.debug(f"No risky keywords found in: {string_value}")
    return False, None

def extract_function_path(node):
    """Extract the full function path from an AST node."""
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        path = []
        attr = node
        while isinstance(attr, ast.Attribute):
            path.append(attr.attr)
            attr = attr.value
        if isinstance(attr, ast.Name):
            path.append(attr.id)
        path.reverse()
        return ".".join(path)
    return None

def function_matches_watched(func_path):
    """Check if a function path matches any of the watched functions."""
    if not func_path:
        return False
        
    logger.debug(f"Checking if function matches watched: {func_path}")
    
    # Check exact matches
    if func_path in WATCHED_FUNCS:
        logger.info(f"Found exact match for function {func_path} in watched list")
        return True
    
    # Split into components
    parts = func_path.split(".")
    
    # Handle direct function calls like pipeline
    if len(parts) == 1 and parts[0] in WATCHED_CLASSES:
        logger.info(f"Found direct function match for {func_path}")
        return True
    
    # Check if this is a from_pretrained call on a watched class
    if len(parts) >= 2 and parts[-1] == "from_pretrained" and parts[-2] in WATCHED_CLASSES:
        logger.info(f"Found class match for function {func_path} with class {parts[-2]}")
        return True
        
    # Check for partial matches (end of the path matches)
    for watched in WATCHED_FUNCS:
        watched_parts = watched.split(".")
        
        # Need at least 2 parts (class.method) for a meaningful comparison
        if len(watched_parts) >= 2 and len(parts) >= 2:
            # Check if the last 2+ components match
            if watched_parts[-2:] == parts[-2:]:
                logger.info(f"Found partial match for function {func_path} with {watched}")
                return True
    
    logger.debug(f"No match found for function: {func_path}")
    return False

def analyze_code_for_model_loads(code):
    logger.info(f"Analyzing code: {code[:50]}...")
    
    try:
        tree = ast.parse(code)
        logger.debug("Successfully parsed code with AST")
    except SyntaxError as e:
        logger.error(f"Syntax error in code: {e}")
        return False  # Return False if there's a syntax error
    
    risky_detections = []
    
    # First pass - track aliases and collect variable assignments with risky values
    risky_variables = {}
    class_aliases = {}
    
    # Find import aliases
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == 'transformers':
            for alias in node.names:
                if alias.name in WATCHED_CLASSES and alias.asname:
                    logger.info(f"Found alias for watched class: {alias.name} as {alias.asname}")
                    class_aliases[alias.asname] = alias.name
    
    # Find variable assignments with risky values
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                    var_name = target.id
                    var_value = node.value.value
                    # Check if the value contains risky keywords
                    is_risky_val, keywords = is_risky(node.value)
                    if is_risky_val:
                        logger.info(f"Found risky variable assignment: {var_name} = {var_value}")
                        risky_variables[var_name] = (var_value, keywords)
    
    # Dump the AST structure for debugging
    for i, node in enumerate(ast.walk(tree)):
        if isinstance(node, ast.Call):
            logger.debug(f"Found call node: {ast.dump(node)[:100]}...")

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            # Extract the function path 
            func_path = extract_function_path(node.func)
            
            # Check if this is an aliased class method (e.g., LLM.from_pretrained)
            is_alias_match = False
            if func_path:
                parts = func_path.split(".")
                if len(parts) >= 2 and parts[-1] == "from_pretrained" and parts[-2] in class_aliases:
                    original_class = class_aliases[parts[-2]]
                    logger.info(f"Found aliased class method: {func_path} is alias for {original_class}.from_pretrained")
                    is_alias_match = True
            
            if (func_path and function_matches_watched(func_path)) or is_alias_match:
                if is_alias_match:
                    # Reconstruct the function path using the original class name for logging
                    func_path = func_path.replace(parts[-2], original_class)
                
                logger.info(f"Matched function {func_path} with watched functions")
                
                # Log all arguments for debugging
                for i, arg in enumerate(node.args):
                    logger.debug(f"Argument {i} type: {type(arg)} value: {ast.dump(arg)[:100]}")
                    
                    # Check if the argument is risky
                    is_risky_arg, keywords = is_risky(arg)
                    if is_risky_arg:
                        string_value = extract_string_value(arg)
                        logger.warning(f"Found risky call: {func_path}({string_value})")
                        risky_detections.append((func_path, string_value, keywords))
                    
                    # If it's a variable and we know it's risky, flag it
                    elif isinstance(arg, ast.Name) and arg.id in risky_variables:
                        var_value, keywords = risky_variables[arg.id]
                        logger.warning(f"Found risky variable in call: {func_path}({arg.id} = {var_value})")
                        risky_detections.append((func_path, f"{arg.id} = {var_value}", keywords))
                        
                # Check keyword arguments too - any relevant keyword arg could contain a model name
                model_related_kwargs = ["model", "model_name", "pretrained_model_name_or_path", "name"]
                for keyword_arg in node.keywords:
                    logger.debug(f"Keyword arg {keyword_arg.arg} type: {type(keyword_arg.value)}")
                    
                    # These are often important for model loading
                    if keyword_arg.arg in model_related_kwargs:
                        is_risky_arg, keywords = is_risky(keyword_arg.value)
                        if is_risky_arg:
                            string_value = extract_string_value(keyword_arg.value)
                            logger.warning(f"Found risky kwarg: {func_path}({keyword_arg.arg}={string_value})")
                            risky_detections.append((func_path, string_value, keywords))
                        
                        # If it's a variable and we know it's risky, flag it
                        elif isinstance(keyword_arg.value, ast.Name) and keyword_arg.value.id in risky_variables:
                            var_value, keywords = risky_variables[keyword_arg.value.id]
                            logger.warning(f"Found risky variable in kwarg: {func_path}({keyword_arg.arg}={keyword_arg.value.id} = {var_value})")
                            risky_detections.append((func_path, f"{keyword_arg.arg}={keyword_arg.value.id} = {var_value}", keywords))
    
    # Display warnings for all risky detections
    for func_path, arg_value, keywords in risky_detections:
        display_warning(
            "⛔ Suspicious Model Load Detected",
            f"Function `{func_path}` called with argument containing risky keywords: {', '.join(keywords)}\n"
            f"Argument value: `{arg_value}`\n\n"
            f"This may be loading a model that requires specific permissions or licensing."
        )
    
    if not risky_detections:
        logger.info("No risky detections found in code")
    
    return len(risky_detections) > 0  # Return True if risky functions detected

def register_hooks():
    ip = get_ipython()
    if not ip:
        logger.warning("Not running in IPython environment, hooks not registered")
        return

    logger.info("Setting up IPython hooks")

    # Pre-execution hook
    def pre_run_hook(info):
        logger.info("Pre-run hook triggered")
        code = info.raw_cell
        logger.debug(f"Cell code: {code}")
        has_risks = analyze_code_for_model_loads(code)
        if has_risks:
            display_warning(
                "⚠️ Warning: Risky Code (Pre-Execution)",
                "The code contains suspicious model or dataset loads.\nReview the warnings above before continuing."
            )
            # Note: We could consider adding a way to block execution here,
            # but that would require overriding more IPython internals

    # Post-execution hook for additional analysis
    def post_run_hook(result):
        logger.info("Post-run hook triggered")
        code = result.info.raw_cell
        logger.debug(f"Cell code: {code}")
        has_risks = analyze_code_for_model_loads(code)
        if has_risks:
            display_warning(
                "⚠️ Warning: Risky Code (Post-Execution)",
                "The executed code contained suspicious model or dataset loads."
            )

    # Register both hooks
    ip.events.register('pre_run_cell', pre_run_hook)
    ip.events.register('post_run_cell', post_run_hook)
    
    logger.info("IPython hooks successfully registered")
    display_warning(
        "ML Risk Plugin Activated", 
        f"Now watching for model and dataset loads containing risky keywords: {', '.join(RISKY_KEYWORDS)}"
    )

def init():
    logger.info("Initializing MAIS plugin")
    register_hooks()
    logger.info("MAIS plugin initialized")
