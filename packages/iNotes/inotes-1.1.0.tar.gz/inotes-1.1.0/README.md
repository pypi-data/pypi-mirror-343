# iNotes 🧠✍️

iNotes is a simple Python package that uses AI to generate clear, concise notes from just topics. It's designed to assist students, professionals, and researchers in make short notes easily.

---

## 🚀 Features

- Generate summarized notes from just a topic
- Highlight key points and topics  
- Export notes to Markdown or plain text  
- Easy-to-use Python interface  
- Powered by different AI models  
- Models Supported : "neversleep/llama-3-lumimaid-8b:extended", "anthropic/ claude-3-7-sonnet-20250219",
    "sao10k/l3-euryale-70b", "deepseek/deepseek-chat", "deepseek/deepseek-r1",
    "openai/gpt-4o-mini", "gryphe/mythomax-l2-13b", "google/gemini-pro-1.5",
    "x-ai/grok-2", "nvidia/llama-3.1-nemotron-70b-instruct"
- Warning : Some models may misbehave as it's not an official api integrated models. 
---

## 📦 Installation

```bash
pip install iNotes
```
---

## 🧑‍💻 Usage

Here's a basic example of how to use the package:

```python
from iNotes import generate_notes

#topic for notes

topic = "Machine Learning"

# Generate notes 
# filepath: where to save the generated notes
# system_prompt: custom prompt for the AI model
#saves notes in .pdf format

generate_notes(topic, filepath="output_notes.pdf",model = "deepseek/deepseek-r1",  system_prompt="You are an AI notes maker which makes notes on the basis of given prompt. Keep Headings and subheadings bold and stylish.")
```

---

## 📋 Output Example

```
.pdf file :

   ** MACHINE LEARNING NOTES **
 ** INTRODUCTION TO MACHINE LEARNING **
 ***What is Machine Learning?***
 *   Machine Learning (ML) is a subset of Artificial Intelligence (AI) that focuses on building
 systems which can learn from data.
 *   The core idea is to enable computers to improve their performance on a specific task
 through experience (data), without being explicitly programmed for every possible scenario.
 *   Instead of writing rigid rules for every situation, ML algorithms learn patterns,
 relationships, and structures within the data.
 *   This allows them to make predictions, classifications, or decisions on new, unseen data.
 *   It's about learning from examples and adapting behavior based on new information


    and many more...
```

---

## 📜 License

MIT License
