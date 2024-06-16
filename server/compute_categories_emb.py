import torch
from transformers import CLIPProcessor, CLIPModel
import json

# Load the CLIP model and processor
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Precompute text embeddings
def compute_text_embeddings(labels):
    inputs = processor(text=labels, return_tensors="pt", padding=True)
    with torch.no_grad():
        text_embeddings = model.get_text_features(**inputs)
    return text_embeddings

if __name__ == '__main__': 
    # Load the labels from data.json
    labels = json.load(open('data.json'))
    labels = [label['name'] for label in labels]
    print(labels)

    text_embeddings = compute_text_embeddings(labels)

    # Save text embeddings for later use
    torch.save(text_embeddings, 'text_embeddings.pt')