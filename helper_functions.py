import initialize_crew as helper
from langchain_community.tools import YouTubeSearchTool
import ast
import globals

def run_disease_crew(disease):

    result = helper.Diseasecrew.kickoff(
        inputs={'disease': disease}
    )

    return str(result)

def run_diet_crew(disease):

    result = helper.Dietcrew.kickoff(
        inputs={'disease': disease}
    )

    return str(result)

def run_exercise_crew(disease):

    result = helper.Exercisecrew.kickoff(
        inputs={'disease': disease}
    )

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

    result = helper.MedicalQueryCrew.kickoff(
        inputs={'question': query, 'history': history}
    )

    return str(result)

def get_embed_url(video_url):
    video_id = ""

    # Parse the video ID from the URL
    if "youtube.com/watch?v=" in video_url:
        video_id = video_url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in video_url:
        video_id = video_url.split("youtu.be/")[1]
    elif "/shorts/" in video_url:
        video_id = video_url.split("/shorts/")[1]
    else:
        return "Invalid YouTube URL format"

    # Construct the embeddable URL
    embed_url = f"https://www.youtube.com/embed/{video_id}"
    return embed_url

def get_patient_stories(disease):
    tool = YouTubeSearchTool()
    videos = tool.run(f"my journey of healing {disease}, 6")
    videos_list = ast.literal_eval(videos)
    
    embeded_urls = []
    embeded_html = '<div class="iframe-container">'
    for url in videos_list:
        print(url)
        new_url = get_embed_url(url)
        embeded_html += f'<iframe width="560" height="315" src="{new_url}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe><br>'
        embeded_urls.append(new_url)
    embeded_html+='</div>'
    
    return embeded_html

print('#'*30 + 'file1 RUNS' + '#'*30)