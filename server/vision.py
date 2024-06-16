from openai import OpenAI
import os 
import load_dotenv
import base64

load_dotenv.load_dotenv()

class GptVision:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def describe_image(self, base64_image):
        all_text = open("all_text.txt", "r").read().replace("\n\n", "\n")


        prompt = f'''
        You will use trash image and guidlines to provide an instruction for trash segregation.
        Instruction can be simple or require few steps.

        Here are example items and some guidlines:
        {all_text}


        [Simple Example]
        Throw the bottle to the glass bin.

        [Complex Example]
        1. Drain the liquid from the pickle jar (e.g. by pouring it down the sink).
        2. Throw the pickles into the compost bin.
        3. Throw the jar into the glass bin.
        4. If you have jar lids, throw them into the bin for metal and plastic.

        Be brief and to the point, provide instructions but no yapping.
        '''

        response = self.client.chat.completions.create( 
            model="gpt-4o",

            messages=[
                {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                        "detail": "low"  # Adding the low resolution flag

                    },
                    },
                ],
                }
            ],
            max_tokens=300,
        )
        print(response.usage)
        return response.choices[0].message
    
    def process_image(self, image_path):
        base64_image = self.encode_image(image_path)
        return self.describe_image(base64_image)


if __name__ == "__main__":
    vision = GptVision()
    print("Answear from vision model: ",vision.process_image("ogorki.jpeg"))
    