import gradio as gr
# import fetch_threads as api
# import summarize_threads as summarize
# import rag_prep as rag
import utils as api
import re

CSS ="""
#disease_id {background-color: #374151; padding: 20px; border-radius: 5px; border: 10px solid #1f2937;}
#diet_id {background-color: #374151; padding: 20px; border-radius: 5px; border: 10px solid #1f2937;}
#exercise_id {background-color: #374151; padding: 20px; border-radius: 5px; border: 10px solid #1f2937;}
"""

# component-0 > div:nth-child(11) { height: 600px !important; }

# def display_text_list():
#     text_list = summarize.summarize_tweets()
#     formatted_data=""
#     for i, item in enumerate(text_list):
#         title = f"<h3>{i+1}. {item['title']}</h3>"
#         new_sum = re.sub(r'\n', ' ', item['summary'])
#         summary = f"<p>{new_sum}</p>"
#         formatted_data+=title
#         formatted_data+=summary
    
#     # print(formatted_data)
#     return [formatted_data, gr.TextArea(visible=False), gr.Markdown(visible=True), gr.Markdown(visible=False)]


with gr.Blocks(css=CSS, theme=gr.themes.Soft()) as demo:

    # Intro
    gr.Markdown("<h1><center>Healthcare Assistant</center></h1>")
    gr.Markdown("<h4><center>Ask anything you want to search about your Disease and get personalized answers</center></h4>")
    query = gr.Textbox(label="Fetch Disease", placeholder="Please enter your Disease to search... ")

    gr.Markdown("<br />")

    with gr.Tab("Disease Analysis"):
        research_disease = gr.Button(value="Research Diesease", scale=1)
        # tweet_details = gr.TextArea(label="Research Diesease", max_lines=10)
        disease_details_mr = gr.Markdown(elem_id="disease_id")
        research_disease.click(api.run_disease_crew, inputs=[query], outputs=disease_details_mr)
    with gr.Tab("Diet Analysis"):
        research_diet = gr.Button(value="Research Diet", scale=1)
        diet_details_mr = gr.Markdown(elem_id="diet_id")
        research_diet.click(api.run_diet_crew, inputs=[query], outputs=diet_details_mr)
    with gr.Tab("Exercise Analysis"):
        research_exercise = gr.Button(value="Research Exercise", scale=1)
        exercise_details_mr = gr.Markdown(elem_id="exercise_id")
        research_exercise.click(api.run_exercise_crew, inputs=[query], outputs=exercise_details_mr)
    with gr.Tab("Consultation"):
        fetch_tweet_btn = gr.Button(value="Fetch Doctors")
        tweet_details = gr.TextArea(label="Consultations", max_lines=10)
    with gr.Tab("Patient Stories"):
        fetch_tweet_btn = gr.Button(value="Fetch Stories")
        tweet_details = gr.TextArea(label="Patient Stories", max_lines=10)

    # Fetch Reddit Threads
    # with gr.Row():
    #     with gr.Column():
    #         query = gr.Textbox(label="Fetch Reddit Threads", placeholder="Please enter your query to search... ")
    #         n = gr.Slider(1,20,value=1,step=1,label="Select no of Reddit Threads you want to fetch", interactive=True)
            
    #         with gr.Row():
    #             fetch_tweet_btn = gr.Button(value="Fetch Tweets")
    #             summarize_tweet_btn = gr.Button(value="Summarize Tweets")
    #     with gr.Column():
    #         tweet_details = gr.TextArea(label="Results", max_lines=8)

    # fetch_tweet_btn.click(api.get_reddit, inputs=[query,n], outputs=[tweet_details])

    # # Summarization Section
    # gr.Markdown("<br />")
    # Note = gr.Markdown("<h4>Note: Summarizing tweets takes time please wait...</h4>")
    # head = gr.Markdown("<h1>Reddit Threads Summarized</h1>", visible=False)
    # result = gr.Markdown()
    # loader = gr.TextArea(label="Summary Results", visible=True)
    # summarize_tweet_btn.click(display_text_list, inputs=[], outputs=[result,loader,head,Note])

    # Chat with Reddit Threads
    gr.Markdown("<br />")
    gr.ChatInterface(fn=api.ask_questions, type="messages", examples=["hello", "hola", "merhaba"], title="Chat with Health Assistant")

demo.launch()