import init_disease_crew as helper

def run_disease_crew(disease):

    result = helper.Diseasecrew.kickoff(
        inputs={'disease': disease}
    )

    print(result)

    print(type(result))
    print(str(result))
    return str(result)

def run_diet_crew(disease):

    result = helper.Dietcrew.kickoff(
        inputs={'disease': disease}
    )

    print(result)

    print(type(result))
    print(str(result))
    return str(result)

def run_exercise_crew(disease):

    result = helper.Exercisecrew.kickoff(
        inputs={'disease': disease}
    )

    print(result)

    print(type(result))
    print(str(result))
    return str(result)

def ask_questions(query, history):
    # results = vectorstore.similarity_search(query,k=5)
    # print("\nQuery: ",query)
    # print("\nRAG Retrived Documents: ")
    # for doc in results:
    #     print(doc)
    #     print('-'*90)
    # context = format_docs(results)
    # chain = prompt | llm | StrOutputParser()
    # results = chain.invoke({'query':query,'context':context})
    # print("\nAI: ",results)

    return "Feature Under Development"

print('#'*30 + 'file1 RUNS' + '#'*30)