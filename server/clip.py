import gradio as gr
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import json

# Load the CLIP model and processor
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Load the labels from data.json
labels = json.load(open('data.json'))
labels = [label['name'] for label in labels]
print(labels)

# Load precomputed text embeddings
text_embeddings = torch.load('text_embeddings.pt')

# Function to compute image embedding
def compute_image_embedding(image):
    inputs = processor(images=image, return_tensors="pt", padding=True)
    with torch.no_grad():
        image_embedding = model.get_image_features(**inputs)
    return image_embedding

# Function to classify trash using precomputed text embeddings
def classify_trash(image, threshold=0.5):
    # Compute image embedding
    image_embedding = compute_image_embedding(image)
    
    # Compute similarity between image embedding and text embeddings
    similarity = torch.matmul(image_embedding, text_embeddings.T)
    probs = similarity.softmax(dim=1)
    probs = probs.detach().cpu()
    probs = probs / probs.max() # Normalize the probabilities

    # Get indices of labels with probabilities greater than the threshold
    predicted_labels_indices = torch.where(probs > threshold)[1].tolist()
    
    # Get the labels corresponding to those indices
    predicted_labels = [labels[idx] for idx in predicted_labels_indices]

    # Print probabilities for ALL labels (even if below threshold)
    for idx, label in enumerate(labels):
        print(f"{label}: {probs[0][idx].item()}")
    
    return predicted_labels

# Gradio interface
def gradio_classify_trash(image):
    return classify_trash(image)

if __name__ == '__main__':
    # Create the Gradio app
    iface = gr.Interface(
        fn=gradio_classify_trash, 
        inputs=gr.Image(type="pil"), 
        outputs=gr.Textbox(),
        title="Trash Classifier",
        description="Upload a photo of trash to classify it into categories such as glass, plastic, paper, metal, organic, and mixed."
    )

    # Launch the app
    iface.launch()