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
    - If a specific detail is ambiguous or missing, provide a concise summary based on the context.
    
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
            parsed_results[file_path.name] = structured_data

            print(f"\n--- Output for {file_path.name} ---")
            print(structured_data)
            print(parsed_results)

        except OutputParserException as e:
            logger.error(f"Failed to parse LLM response for {file_path.name}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error processing {file_path.name}: {e}")

    return parsed_results


if __name__ == "__main__":
    main()
