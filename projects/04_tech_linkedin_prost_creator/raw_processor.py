import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from shared.path_utils import get_project_root
from shared.logger import get_logger
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

from langchain_groq import ChatGroq

logger = get_logger(__name__)
load_dotenv()

class ProcessedTopicSchema(BaseModel):
    topic: str = Field(description="Main technical subject (1-5 words)")
    post: str = Field(description="The raw post content")
    core_concept: str = Field(description="Core takeaway or concept explained. (10-15 words)")
    hook: str = Field(description="The attention-grabbing opening line/hook")
    angle: str = Field(description="The tone or perspective of the post")
    tags: list[str] = Field(description="Maximum 3 relevant topic, title case technical tags")


def main():
    raw_dir = get_project_root() / 'documents/linkedin/raw/'

    if not raw_dir.is_dir():
        raise FileNotFoundError(f"Directory not found: {raw_dir}")

    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="openai/gpt-oss-20b")

    parser = JsonOutputParser(pydantic_object=ProcessedTopicSchema)

    template = """
    System: You are an expert Lead Data Engineer analyzing technical LinkedIn content.
    Task: Extract structured metadata from the post provided below.
    
    Rules:
    - Strictly adhere to the requested schema, No preamble.
    - Extract up to 3 high-level technical tags.
    - Each tag should be follow title case convention. (e.g., ["Snowflake", "Etl", "Python", "Job Serach"]).
    - Hook must create curiosity or tension in the first line
    
    Post Content:
    {post}
    
    {format_instructions}
    """

    prompt = PromptTemplate(
        template=template,
        input_variables=["post"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    # Combine into a single processing chain
    chain = prompt | llm | parser

    # 4. Iterate and Process Files
    parsed_results = {}
    for file_path in raw_dir.glob("*.txt"):
        logger.info(f"Processing file: {file_path.name}")
        try:
            raw_post = file_path.read_text(encoding="utf-8")
            structured_data = chain.invoke({"post": raw_post})
            parsed_results[file_path.name.replace("_", " ").replace(".txt", "")] = structured_data

            print(f"\n--- Output for {file_path.name} ---")
            print(structured_data)
            print(parsed_results)

            # 5. generating actual post from data
            generate_linkedin_post(parsed_results)


        except OutputParserException as e:
            logger.error(f"Failed to parse LLM response for {file_path.name}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error processing {file_path.name}: {e}")

    return parsed_results

def generate_linkedin_post(topic_data: dict, topic_key: str = "topic_key"):
    # right now hardcoded later change
    post_info = topic_data[topic_key]
    raw_post = post_info["post"]
    hook = post_info["hook"]
    angle = post_info["angle"]
    tags = " ".join([f"#{tag.replace(' ', '')}" for tag in post_info.get("tags", [])])
    template1 = """
    System: You are a Lead Data Engineer and top technical content writer on LinkedIn.
    Task: Take raw technical notes and turn them into an engaging, high-value LinkedIn post.
    Input Context:
    - Raw Concept Notes: 
    {raw_post}
    - Desired Angle/Tone: {angle}
    Instructions for the Post Structure:
    1. HOOK (Line 1): Craft a punchy, scroll-stopping first line. Use contrast, a bold engineering opinion, or a relatable system failure scenario. DO NOT start with generic greetings like "Hey network" or plain titles.
    2. RE-HOOK (Line 2-3): Briefly explain WHY this tradeoff matters in production.
    3. BODY: Present the core technical takeaways clearly.
       - Use short sentences and line breaks.
       - Use simple bullet formatting (e.g., 🔹 or •) for side-by-side comparisons (Row vs. Columnar, Concurrency vs. Throughput, etc.).
       - Emphasize real-world architecture patterns (e.g., CDC/ETL bridge).
    4. TAKEAWAY / CALL TO ACTION (CTA): End with a 1-sentence engineering rule of thumb and ask an insightful question to drive comments.
    5. NO EMOJI OVERLOAD: Limit to 3-5 functional emojis max.
    Output only the raw text of the generated LinkedIn post.
    """

    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="openai/gpt-oss-20b",  # Recommended model for writing tasks on Groq
        temperature=0.7,  # Slight creativity boost for engaging hooks
    )

    prompt = PromptTemplate(
        template=template1,
        input_variables=["raw_post", "angle"],
    )

    chain = prompt | llm

    response = chain.invoke({"raw_post": raw_post, "angle": angle})

    # Append hashtags at the end
    final_post = f"{response.content.strip()}\n\n{tags}"
    return final_post


if __name__ == "__main__":
    # main()
    data = {
        'oltp vs olap': {
            'topic': 'OLTP vs OLAP',
            'post': (
                'OLTP (Online Transaction Processing):\n'
                '- Is used for live transactional system where we need to access data in high concurrency low latency mode.\n'
                '- To achieve this Milliseconds latency and high concurrency operations. It is preferred to have data is highly normalised (3rd normal form)\n'
                '- Data remained stored in row-oriented format 8-16 KB to get entire results in one read\n'
                '- Fast read, write and update are required. Vertical scaling.\n'
                '- Priority remains low latency and write integrity. Build around strict ACID compliance\n\n'
                'OLAP (Online Analytical Processing)\n'
                '- It is used for complex analytical aggregations with historical data.\n'
                '- Read heavy: read huge amount of data with higher latency. It is expected to have denormalized(Star Schema/ Snowflake Schema/ Wide Tables)\n'
                '- Data remained in columnar format (Parquet or Delta), This columnar storage help high compression, High I/O savings.\n'
                '- Scanning huge amount of data latency remain seconds to minutes. Scale horizontally.\n'
                '- Priority remains high throughput read performance\n\n'
                'In modern data word these 2 system communicate with each other using CDC Change Data Capture(CDC) and ETL/ELT'
            ),
            'core_concept': 'OLTP prioritizes low-latency, high-concurrency row storage; OLAP prioritizes high-throughput, read-heavy columnar storage.',
            'hook': 'OLTP (Online Transaction Processing):',
            'angle': 'Informative',
            'tags': ['OLTP', 'OLAP', 'CDC']
        }
    }

    generated_post = generate_linkedin_post(data, 'oltp vs olap')
    print(generated_post)
