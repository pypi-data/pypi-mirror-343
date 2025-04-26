# SPART: Streamlined Prompt Automation and Recommendation Tool

**SPART** is a Python package designed to simplify prompt engineering for Large Language Models (LLMs). It provides tools for generating, evaluating, and optimizing prompts automatically, making the process of creating effective prompts more efficient and less manual.

## Features

- **Connect to various LLM providers**: Use OpenAI, Cohere, HuggingFace, or local LLMs through Ollama.
- **Prompt recommendation**: Generate effective prompts based on input-output examples.
- **Prompt evaluation**: Test prompts against both semantic and syntactic similarity metrics.
- **Prompt optimization**: Improve existing prompts by applying good prompt engineering practices.
- **Multithreaded evaluation**: Process multiple inputs concurrently for faster testing.

## Installation

To install SPART, run the following command:

```bash
pip install spart-prompt
```

## Quick Start

Here's a quick example to get you started with PromptRecommender:

```python
from spart_prompt import ExternalLLMConnector, PromptRecommender
import pandas as pd

# Connect to your LLM provider
llm = ExternalLLMConnector(
    provider="openai",
    model_name="gpt-4o",
    api_key="your_api_key",
    temperature=0.7
)

# Create a recommender
recommender = PromptRecommender(llm)

# Example data 
# (inputs must be the first column and desired_outputs the second column)
examples = pd.DataFrame({
    'inputs': [
        "My name is John and I am 30 years old",
        "Hello I'm Emma, age 25",
        "Name's Sarah, I'm 29",
        "I go by Alice, and I’m 22",
        "It’s Tom here, aged 31",
        "You can call me Linda, I’m 27",
        "Hey, this is Mark and I’m 38"
    ],
    'desired_outputs': [
        "Name: John, Age: 30",
        "Name: Emma, Age: 25",
        "Name: Sarah, Age: 29",
        "Name: Alice, Age: 22",
        "Name: Tom, Age: 31",
        "Name: Linda, Age: 27",
        "Name: Mark, Age: 38"
    ]
})

# Get a recommended prompt
results = recommender.recommend(
    examples=examples, # The input-output examples
    num_examples=1, # Use first example for training, rest for testing
    context="Input contains a short sentence with a person's name and age. Extract both in the format 'Name: X, Age: Y'.", # Extra context for the LLM
    similarity_threshold=0.85, # Threshold to reach before recommending
    max_iterations=3, # If threshold isn't reached then optimization will be attempted 3 times
    semantic_similarity=False, # Don't evaluate based on semantics (outputs -1 if off)
    syntactic_similarity=True # Do evaluate based on syntax
)

print(f"Recommended prompt: {results['recommended_prompt']}")
print(f"Prompt outputs: {results['prompt_outputs']}")
print(f"Semantic similarity: {results['semantic_similarity']}")
print(f"Syntactic similarity: {results['syntactic_similarity']}")
```

Here's a quick example to get you started with PromptOptimizer:

```python 
from spart_prompt import ExternalLLMConnector, PromptOptimizer
import pandas as pd

# Connect to your LLM provider
llm = ExternalLLMConnector(
    provider="openai",
    model_name="gpt-4o",
    api_key="your_api_key",
    temperature=0.7
)

# Create an optimizer
optimizer = PromptOptimizer(llm)

# Example data 
examples = pd.DataFrame({
    'inputs': [
        "My name is John and I am 30 years old",
        "Hello I'm Emma, age 25",
        "Name's Sarah, I'm 29",
        "I go by Alice, and I’m 22",
        "It’s Tom here, aged 31",
        "You can call me Linda, I’m 27",
        "Hey, this is Mark and I’m 38"
    ],
    'desired_outputs': [
        "Name: John, Age: 30",
        "Name: Emma, Age: 25",
        "Name: Sarah, Age: 29",
        "Name: Alice, Age: 22",
        "Name: Tom, Age: 31",
        "Name: Linda, Age: 27",
        "Name: Mark, Age: 38"
    ]
})

# Initial prompt to optimize
prompt = "Extract the person's name and age from the text."

# Optimize the prompt
results = optimizer.optimize_prompt(
    system_prompt=prompt,
    examples=examples,
    num_examples=1,
    threshold=0.9,
    context="Input contains a short sentence with a person's name and age.",
    max_iterations=3,
    semantic_similarity=False,
    syntactic_similarity=True
)

print(f"Optimized prompt: {results['optimized_prompt']}")
print(f"Prompt outputs: {results['prompt_outputs']}")
print(f"Semantic similarity: {results['semantic_similarity']}")
print(f"Syntactic similarity: {results['syntactic_similarity']}")
```

## Classes Overview

### LLMConnector (Abstract Base Class)
Base interface for connecting to LLMs with the following implementations:
- **ExternalLLMConnector**: Connect to OpenAI, Cohere, or HuggingFace
- **LocalLLMConnector**: Connect to local LLMs through Ollama

### PromptEvaluator
Evaluates prompts using:
- Semantic similarity (using vector embeddings)
- Syntactic similarity (using ROUGE-L score)

### PromptRecommender
Generates system prompts based on input-output examples, structured with:
- Role definition
- Guidelines
- Instructions
- Examples
- Context
- Goal

### PromptOptimizer
Improves existing prompts by applying prompt engineering best practices - architecture similar to PromptRecommender.

## Use Cases

- **Data transformation**: Generate prompts to convert data from one format to another.
- **Text summarization**: Build prompts that produce consistent summary formats.
- **Structured output generation**: Ensure LLM outputs follow specific formats.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
