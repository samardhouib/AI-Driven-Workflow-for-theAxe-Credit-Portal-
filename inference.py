import torch
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-coder-1.3b-instruct")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
base_model = AutoModelForCausalLM.from_pretrained("deepseek-ai/deepseek-coder-1.3b-instruct")
quantized_model_path = r"C:\Users\HP\Desktop\axe_stage\django_app_for_axe_model\quantized_m.pth"
model = PeftModel.from_pretrained(base_model, "samardhouib/axe_final_model")
model.load_state_dict(torch.load(quantized_model_path))


def generate_output(instruction):
    # Prepare the input
    prompt = '''
You are an AI programming assistant, utilizing the DeepSeek Coder model, developed by DeepSeek Company, and you only answer questions related to computer science. For politically sensitive questions, security and privacy issues, and other non-computer science questions, you will refuse to answer.
### Instruction:
{}
### Response:
'''.format(instruction.strip()).lstrip()

    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)

    # Generate the output
    with torch.no_grad():
        output_ids = quantized_model.generate(input_ids, max_length=128, pad_token_id=tokenizer.eos_token_id)
        output = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    print(output[len(prompt):])
instruction = " Connect to ACP\n refresh ACP "
generate_output(instruction)