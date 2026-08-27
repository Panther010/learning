from shared.path_utils import get_project_root
from shared.logger import get_logger
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

raw_file_path = get_project_root() / 'documents/linkedin/raw/'

print(raw_file_path)

if not raw_file_path.is_dir():
    raise FileNotFoundError(f"Directory not found: {raw_file_path}")

file_data = {}
for file_path in raw_file_path.glob("*.txt"):
    print(file_path)
    try:
        file_data[file_path.name] = file_path.read_text(encoding="utf-8")
    except Exception as e:
        raise f"Error reading {file_path.name}: {e}"
print(file_data)

for key, raw_post in file_data.items():
    print(raw_post)

    template = '''
        You are a lead data engineer. You are given a LinkedIn post. You need to extract topic of post, post, core concept, hook and angle
        1. Return a valid JSON. No preamble. 
        2. JSON object should have exactly three keys: topic, post, hook, angle and tags
        3. Tags is an array of text tags. Extract maximum 3 tags.
        4. Language should be English.
    
        Here is the actual post on which you need to perform this task:  
        {post}
        '''

    load_dotenv()

    llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name="openai/gpt-oss-20b")

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={'post': raw_post})
    print("response: ", response.content)

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
        print(res)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse jobs.")

"""template = '''
    You are a lead data engineer. You are given a LinkedIn post. You need to extract topic of post, post, core concept, hook and angle
    1. Return a valid JSON. No preamble. 
    2. JSON object should have exactly three keys: topic, post, hook, angle and tags
    3. Tags is an array of text tags. Extract maximum 3 tags.
    4. Language should be English.

    Here is the actual post on which you need to perform this task:  
    {post}
'''

load_dotenv()

llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name="openai/gpt-oss-20b")

pt = PromptTemplate.from_template(template)
chain = pt | llm
response = chain.invoke(input={'post': post})
# print("response: ", response.content)

try:
    json_parser = JsonOutputParser()
    res = json_parser.parse(response.content)
except OutputParserException:
    raise OutputParserException("Context too big. Unable to parse jobs.")

return res"""

