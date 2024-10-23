from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

#model_path = r"C:\Users\21650\Desktop\gen ia\distilroberta_marian_base_model1\distilroberta_marian_base_model1"
model_path =r"C:\Users\HP\Desktop\axe_stage\django_app_for_axe_model\saved_models\quantized_peft_model"

new_model = AutoModelForCausalLM.from_pretrained(model_path)
#new_tokenizer = AutoTokenizer.from_pretrained(model_path)
new_tokenizer = AutoTokenizer.from_pretrained(r"C:\Users\HP\Desktop\axe_stage\django_app_for_axe_model\saved_models\peft_tokenizer")
def generate_output(instruction):
    prompt = '''
You are an AI programming assistant, utilizing the DeepSeek Coder model, developed by DeepSeek Company, and you only answer questions related to computer science. For politically sensitive questions, security and privacy issues, and other non-computer science questions, you will refuse to answer.
### Instruction:
{}
### Response:
'''.format(instruction.strip()).lstrip()

    input_ids = new_tokenizer(prompt, return_tensors="pt").input_ids
    attention_mask = input_ids != new_tokenizer.pad_token_id  # Create attention mask based on pad token

    # Generate the output
    with torch.no_grad():
        output_ids = new_model.generate(input_ids, max_length=128,attention_mask=attention_mask, pad_token_id=new_tokenizer.eos_token_id)
        output = new_tokenizer.decode(output_ids[0], skip_special_tokens=True)
    print(output[len(prompt):])

instruction='Connect to ACP\n refresh ACP'
generate_output(instruction)

