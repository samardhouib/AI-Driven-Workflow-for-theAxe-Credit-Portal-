import torch
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer

# Charger la configuration du modèle Peft
config = PeftConfig.from_pretrained("samardhouib/axe_finance_model")

# Charger le modèle de base
base_model = AutoModelForCausalLM.from_pretrained("deepseek-ai/deepseek-coder-1.3b-instruct")

# Charger le modèle Peft
model = PeftModel.from_pretrained(base_model, "samardhouib/axe_finance_model")
model = model.merge_and_unload()
# Move model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# Get the tokenizer associated with the base_model
tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-coder-1.3b-instruct")



# Save the entire PeftModel if needed
model_save_path = "./saved_models/peft_model"
model.save_pretrained(model_save_path)

# Save the tokenizer
tokenizer_save_path = "./saved_models/peft_tokenizer"
tokenizer.save_pretrained(tokenizer_save_path)

# Save the configuration
config_save_path = "./saved_models/peft_config"
config.save_pretrained(config_save_path)