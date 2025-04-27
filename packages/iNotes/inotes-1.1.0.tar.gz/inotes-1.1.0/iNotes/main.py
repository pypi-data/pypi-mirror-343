import requests
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Define available models
models = {
    "neversleep/llama-3-lumimaid-8b:extended", "anthropic/claude-3-7-sonnet-20250219",
    "sao10k/l3-euryale-70b", "deepseek/deepseek-chat", "deepseek/deepseek-r1",
    "openai/gpt-4o-mini", "gryphe/mythomax-l2-13b", "google/gemini-pro-1.5",
    "x-ai/grok-2", "nvidia/llama-3.1-nemotron-70b-instruct"
}

class iNotes:
    def __init__(self, api_url="https://netwrck.com/api/chatpred_or", 
                 model="deepseek/deepseek-r1", 
                 system_prompt="You are an AI notes maker which makes notes on the basis of given prompt. Keep Headings and subheadings bold and stylish.", 
                 stream=False):  
        self.api_url = api_url
        self.model = model
        self.system_prompt = system_prompt
        self.headers = {
            "content-type": "application/json",
            "origin": "https://netwrck.com"
        }
        self.stream = stream
        self.headers = {
            "content-type": "application/json",
            "origin": "https://netwrck.com"
        }
        self.stream = stream

    def send_request(self, prompt):
        if self.model not in models:
            return f"Error: Model '{self.model}' is not supported. Choose from {models}"

        payload = {
            "model_name": self.model,
            "context": self.system_prompt,
            "query": prompt
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload, stream=self.stream)

            if response.status_code == 200:
                    try:
                        # Attempt to parse the response as JSON
                        response_data = response.json()
                        if isinstance(response_data, dict):  # Ensure it's a dictionary
                            return response_data.get("content", "")
                        else:
                            # If it's not a dictionary, treat it as raw text
                            return response.text
                    except json.JSONDecodeError:
                        # If the response is not JSON, return it as plain string
                        return response.text
            else:
                return f"Error: {response.status_code}, {response.text}"

        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}"

def generate_notes(topic, filepath="output_notes.pdf", model="deepseek/deepseek-r1", system_prompt="You are an AI notes maker which makes notes on the basis of given prompt. Make long notes. Keep Headings and subheadings bold and stylish."):
    Notes = iNotes(system_prompt=system_prompt, model=model)
    text = Notes.send_request(topic)

    if text:
        # Handle literal '\n' and '/n' as line breaks
        text = text.replace("\\n", "\n").replace("/n", "\n")

        c = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter
        margin = 50
        y_position = height - margin
        line_height = 16
        max_line_width = width - 2 * margin

        def split_text_by_width(text_line, font_name, font_size):
            words = text_line.split()
            lines = []
            current_line = ""
            for word in words:
                test_line = current_line + " " + word if current_line else word
                if c.stringWidth(test_line, font_name, font_size) <= max_line_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)
            return lines

        for paragraph in text.split('\n'):
            paragraph = paragraph.strip()
            if not paragraph:
                y_position -= line_height
                continue

            # Detect headings/subheadings
            if paragraph.startswith("##"):
                font_name = "Helvetica-Bold"
                font_size = 12
                clean_text = paragraph.lstrip("#").strip()
            elif paragraph.startswith("#"):
                font_name = "Helvetica-Bold"
                font_size = 14
                clean_text = paragraph.lstrip("#").strip()
            else:
                font_name = "Helvetica"
                font_size = 10
                clean_text = paragraph

            c.setFont(font_name, font_size)
            lines = split_text_by_width(clean_text, font_name, font_size)
            for line in lines:
                if y_position <= margin:
                    c.showPage()
                    y_position = height - margin
                    c.setFont(font_name, font_size)
                c.drawString(margin, y_position, line)
                y_position -= line_height

        c.save()
        print(f"✅ PDF saved as: {filepath}")
# Main interaction loop
if __name__ == "__main__":
    
    while True:
        prompt = input("Enter a topic for notes :\n>>>> ")
        
        if "Error" not in prompt:
            generate_notes(prompt, filepath=f"{prompt.replace(' ', '_')}.pdf")

            print("success")