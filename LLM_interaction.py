from langchain_community.llms import HuggingFaceHub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

openai_api_key=''
huggingfacehub_api_token = ''


def get_article_summary(article_text):
    # Define the LLM
    #llm = HuggingFaceHub(repo_id='tiiuae/falcon-7b-instruct', huggingfacehub_api_token=huggingfacehub_api_token)
    llm = OpenAI(temperature=0, openai_api_key=openai_api_key,model = "gpt-3.5-turbo-instruct")		

    # Create a chat prompt template
    prompt = PromptTemplate.from_template("You are an English major with good command of the language. You are able to \
        succintly summarize the meaning behind large bodies of text. Using these skills summarize the text: {article_text}")
    #output_parser = StrOutputParser()

    chain = prompt | llm #| output_parser
    try:
        result = chain.invoke({"article_text": article_text})
        return result
    except Exception as e:
        print(e)
        return None
