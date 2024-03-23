from langchain.globals import set_debug, set_verbose
from langchain_core.prompts import ChatPromptTemplate
from langchain.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from server.utils import get_ChatOpenAI

set_debug(True)
set_verbose(True)

# template = """Based on the table schema below,write a SQL query that would answer the user's question:{schema}
# Question: {question}
# SQL Query: """

template = """根据表格模式，回答一个SQL语句:{schema}
Question: {question}
SQL Query: """

prompt = ChatPromptTemplate.from_template(template)
db = SQLDatabase.from_uri("sqlite:///./Chinook.db")


def get_schema(_):
    return db.get_table_info()


def run_query(query):
    return db.run(query)


model = chat_model = get_ChatOpenAI(
    model_name='chatglm3-6b',
    temperature=0,
    max_tokens=4096, callbacks=[])

sql_response = (
        RunnablePassthrough.assign(schema=get_schema)
        | prompt
        | model.bind(stop=["\nSQLResult:"])
        | StrOutputParser()
)

# template = """Based on the table schema below,question,sql query, and sql response ,write a natural language response:{schema}
# Question: {question}
# SQL Query: {query}
# SQL Response: {response}"""

template = """根据数据库内容，问题，sql查询和sql响应，回答一个自然语言的结果:{schema}
Question: {question}
SQL Query: {query}
SQL Response: {response}"""

prompt_response = ChatPromptTemplate.from_template(template)

full_chain = (
        RunnablePassthrough.assign(query=sql_response).assign(
            schema=get_schema,
            response=lambda x: run_query(x["query"]),
        )
        | prompt_response
        | model
)


# def test_sql_gen():
#     query = sql_response.invoke({"question": "当前有多少员工？"})
#     print(query)


def test_full_chain():
    query = full_chain.invoke({"question": "数据库中有那些表？"})
    print(query)
