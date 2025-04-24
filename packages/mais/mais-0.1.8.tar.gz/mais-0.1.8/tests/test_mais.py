#!/usr/bin/env python
# Test script for MAIS plugin detection capabilities

import sys
import logging
from mais import analyze_code_for_model_loads

# Set up more verbose logging for testing
logging.basicConfig(level=logging.DEBUG, format='TEST [%(levelname)s]: %(message)s')
logger = logging.getLogger('test_mais')

def test_detection(test_name, code, should_detect=True):
    """Run a test case against the MAIS detector."""
    print(f"\n=== TESTING: {test_name} ===")
    print(f"CODE: {code}")
    result = analyze_code_for_model_loads(code)
    
    if result and should_detect:
        print(f"✅ SUCCESS: Detected risky code as expected")
    elif not result and not should_detect:
        print(f"✅ SUCCESS: Correctly identified safe code")
    elif result and not should_detect:
        print(f"❌ FAILURE: False positive - detected risk in safe code")
    else:
        print(f"❌ FAILURE: False negative - missed risk in unsafe code")
    
    return result

# Test cases
test_cases = [
    # Basic cases
    {
        "name": "Direct import and call with risky model",
        "code": "from transformers import AutoModel\nmodel = AutoModel.from_pretrained('meta-llama/Llama-2-7b')",
        "should_detect": True
    },
    {
        "name": "Variable assigned import with risky call",
        "code": "import transformers as tf\nmodel = tf.AutoModel.from_pretrained('llama-7b')",
        "should_detect": True
    },
    {
        "name": "Safe model load",
        "code": "from transformers import BertModel\nmodel = BertModel.from_pretrained('bert-base-uncased')",
        "should_detect": False
    },
    {
        "name": "Renamed import with from_pretrained",
        "code": "from transformers import AutoModelForCausalLM as LLM\nmodel = LLM.from_pretrained('mistralai/Mistral-7B-v0.1')",
        "should_detect": True
    },
    {
        "name": "Risky keyword argument usage",
        "code": "import transformers\ntransformers.AutoModel.from_pretrained(pretrained_model_name_or_path='meta-llama/Llama-2-7b')",
        "should_detect": True
    },
    {
        "name": "Pipeline usage with risky model",
        "code": "from transformers import pipeline\nnlp = pipeline('text-generation', model='gpt2')",
        "should_detect": True
    },
    {
        "name": "Nested module call",
        "code": "import torch.hub\nmodel = torch.hub.load('pytorch/fairseq', 'gpt2', force_reload=True)",
        "should_detect": True
    },
    {
        "name": "Complex variable detection",
        "code": """
import transformers
model_name = "claude-3"
tokenizer = transformers.AutoTokenizer.from_pretrained(model_name)
        """,
        "should_detect": True
    },
    {
        "name": "Multi-line with indentation",
        "code": """
def load_my_model():
    from transformers import (
        AutoModel, 
        AutoTokenizer
    )
    
    model = AutoModel.from_pretrained(
        "falcon-40b",
        use_cache=True
    )
    return model
        """,
        "should_detect": True
    }
]

def run_tests():
    """Run all test cases and report results."""
    successes = 0
    failures = 0
    
    for test in test_cases:
        result = test_detection(
            test["name"], 
            test["code"], 
            test["should_detect"]
        )
        
        if (result and test["should_detect"]) or (not result and not test["should_detect"]):
            successes += 1
        else:
            failures += 1
    
    print("\n=== TEST SUMMARY ===")
    print(f"Total tests: {len(test_cases)}")
    print(f"Successes: {successes}")
    print(f"Failures: {failures}")
    
    return failures == 0

if __name__ == "__main__":
    print("RUNNING MAIS DETECTION TESTS")
    success = run_tests()
    sys.exit(0 if success else 1) 