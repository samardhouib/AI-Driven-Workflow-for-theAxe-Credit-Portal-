from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from .forms import InstructionForm
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import datetime

# Load your model and tokenizer
model_path = r"C:\Users\HP\Desktop\axe_stage\django_app_for_axe_model\saved_models\peft_model"
new_model = AutoModelForCausalLM.from_pretrained(model_path)
new_tokenizer = AutoTokenizer.from_pretrained(
    r"C:\Users\HP\Desktop\axe_stage\django_app_for_axe_model\saved_models\peft_tokenizer")


def generate_output(instruction):
    prompt = '''
You are an AI programming assistant, utilizing the DeepSeek Coder model, developed by DeepSeek Company, and you only answer questions related to computer science. For politically sensitive questions, security and privacy issues, and other non-computer science questions, you will refuse to answer.
### Instruction:
{}
### Response:
'''.format(instruction.strip()).lstrip()

    input_ids = new_tokenizer(prompt, return_tensors="pt").input_ids
    attention_mask = input_ids != new_tokenizer.pad_token_id

    with torch.no_grad():
        output_ids = new_model.generate(input_ids, max_length=512, attention_mask=attention_mask,
                                        pad_token_id=new_tokenizer.eos_token_id)
        output = new_tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return output[len(prompt):]


def extract_content_from_file(file):
    if file.name.endswith('.xlsx') or file.name.endswith('.xls'):
        import pandas as pd
        df = pd.read_excel(file)
        return df.to_string(index=False, header=False).splitlines()
    elif file.name.endswith('.txt'):
        return file.read().decode('utf-8').splitlines()
    else:
        return []


def index(request):
    if request.method == 'POST':
        form = InstructionForm(request.POST, request.FILES)
        if form.is_valid():
            instruction = form.cleaned_data['instruction']
            excel_file = form.cleaned_data['excel_file']
            text_file = form.cleaned_data['text_file']

            instructions = []
            if instruction:
                instructions.append(instruction)
            if excel_file:
                instructions.extend(extract_content_from_file(excel_file))
            if text_file:
                instructions.extend(extract_content_from_file(text_file))

            outputs = [generate_output(instr) for instr in instructions]
            combined_output = "\n".join(outputs)

            # Update history in session
            if 'history' not in request.session:
                request.session['history'] = []
            history = request.session['history']
            history.append({
                'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'code': combined_output
            })
            request.session['history'] = history

            request.session['output'] = combined_output  # Store output in session
            return render(request, 'assistant/result.html', {'form': form, 'output': combined_output, 'history': history})
    else:
        form = InstructionForm()
    history = request.session.get('history', [])
    return render(request, 'assistant/index.html', {'form': form, 'history': history})


@require_http_methods(["GET"])
def download_output(request):
    output = request.session.get('output', '')
    response = HttpResponse(output, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="output.txt"'
    return response


@require_http_methods(["POST"])
def delete_history_entry(request, entry_index):
    if 'history' in request.session:
        history = request.session['history']
        if 0 <= entry_index < len(history):
            del history[entry_index]
            request.session['history'] = history
    return redirect(reverse('index'))
