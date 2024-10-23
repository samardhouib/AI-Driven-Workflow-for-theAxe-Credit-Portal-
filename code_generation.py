import torch
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import AutoModelForSequenceClassification, AutoTokenizer
# Charger la configuration du modèle Peft
config = PeftConfig.from_pretrained("samardhouib/axe_finance_model")

# Charger le modèle de base
base_model = AutoModelForCausalLM.from_pretrained("deepseek-ai/deepseek-coder-1.3b-instruct")

# Charger le modèle Peft
model = PeftModel.from_pretrained(base_model, "samardhouib/axe_finance_model")

# Move model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# Charger le tokenizer correspondant au modèle de base
tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-coder-1.3b-instruct")




# Quantize the model
quantized_model = torch.quantization.quantize_dynamic(
    model,  # the original model
    {torch.nn.Linear},  # layers to quantize
    dtype=torch.qint8  # dtype of the quantized model
)

# Save the quantized model
quantized_model_path = r"C:\Users\HP\Desktop\axe_stage\django_app_for_axe_model\quantized_m.pth"
torch.save(quantized_model.state_dict(), quantized_model_path)


print("Model quantized and saved successfully.")
