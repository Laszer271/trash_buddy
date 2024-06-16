from openai import OpenAI
from dotenv import load_dotenv

import logging
logger = logging.getLogger(__name__)

load_dotenv()

client = OpenAI()

class RAG:
    def __init__(self, text_files='all_text.txt'):
        if isinstance(text_files, str):
            self.text_files = [text_files]
        else:
            self.text_files = text_files
        self.initialize_db_based_on_df()

    def initialize_db_based_on_df(self):
        self.vector_store = client.beta.vector_stores.create(name="Trash Insights")

        # Ready the files for upload to OpenAI
        file_streams = [open(path, "rb") for path in self.text_files]
        
        # Use the upload and poll SDK helper to upload the files, add them to the vector store,
        # and poll the status of the file batch for completion.
        file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=self.vector_store.id, files=file_streams
        )
        
        # You can print the status and the file counts of the batch to see the result of this operation.
        logger.info(file_batch.status)
        logger.info(file_batch.file_counts)

    def find_similar_category(self, query, k=3):  
        prompt = '''
        You will find relevant chunks to the trash description. 
        Then provide an instruction of what to do with the trash you got from the user.
        Instruction can be simple or require few steps.

        [Simple Example]
        Throw the bottle to the glass bin.

        [Complex Example]
        1. Drain the liquid from the pickle jar (e.g. by pouring it down the sink).
        2. Throw the pickles into the compost bin.
        3. Throw the jar into the glass bin.
        4. If you have jar lids, throw them into the bin for metal and plastic.

        Be brief and to the point, no yapping.
        '''.strip()

        self.assistant = client.beta.assistants.create(
            name="Document Analysis Assistant",
            instructions=prompt,
            model="gpt-4o",
            tools=[{"type": "file_search"}],
        
        )

        self.assistant = client.beta.assistants.update(
            assistant_id=self.assistant.id,
            tool_resources={"file_search": {"vector_store_ids": [self.vector_store.id]}},
        ) 

        thread = client.beta.threads.create()

        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=query
        )

        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id, assistant_id=self.assistant.id,
            # instructions="Please get relevant information from the vectorstore and return it to the user, no yapping.",
        )

        messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

        message_content = messages[0].content[0].text
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = client.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")

        print(message_content.value)
        print("\n".join(citations))
        
        return message_content

def main():
    rag = RAG()
    answer = rag.find_similar_category("Milk carton.")
    return answer

if __name__ == "__main__":
    final_response = main()
    print("Final Response:", final_response)
    print('Content:', final_response.value)
