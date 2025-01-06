import gradio as gr
# import fetch_threads as api
# import summarize_threads as summarize
# import rag_prep as rag
import utils as api
import re
import practo
import find_doctor_degree as degree

CSS ="""
#disease_id {background-color: #374151; padding: 20px; border-radius: 5px; border: 10px solid #1f2937;}
#diet_id {background-color: #374151; padding: 20px; border-radius: 5px; border: 10px solid #1f2937;}
#exercise_id {background-color: #374151; padding: 20px; border-radius: 5px; border: 10px solid #1f2937;}
#component-0 > div:nth-child(7) { height: 600px !important; }
"""

DISEASE_NAME = ''


def display_doctors(category):
    
    url1 = '''https://www.practo.com/search/doctors?results_type=doctor&q=[{"word":"'''
    url1+=str(category)
    url1+='''","autocompleted":true,"category":"subspeciality"}]&city=Mumbai&filters[doctor_review_count]=20,9999999&filters[years_of_experience]=15,9999999'''

    doctors_data = practo.scrape_doctors_data_with_urls(url1)
    html_output = ""

    for doctor in doctors_data:
        if('urls' not in doctor):
            continue
        doctor_html = f"""
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <img src="{doctor['urls'][0]}" alt="Doctor Image" style="width: 150px; height: 150px; margin-right: 20px;">
            <div>
                <strong>Name:</strong> {doctor['doctor_name']}<br>
                <strong>Degree:</strong> {DISEASE_NAME}<br>
                <strong>Experience:</strong> {doctor['experience']}<br>
                <strong>Locality:</strong> {doctor['locality']}, {doctor['city']}<br>
                <strong>Clinic Name:</strong> {doctor['clinic_name']}<br>
                <strong>Consultation Fees:</strong> {doctor['consultation_fee']}<br>
                <strong>Recommendation:</strong> {doctor['recommendation']}<br>
                <strong>Patient Stories:</strong> {doctor['total_feedback']}<br>
            </div>
        </div>
        <div style="display: flex; gap: 10px; overflow-x: auto; margin-bottom: 20px;">
        """
        # Add hospital images as a gallery
        for img in doctor["urls"]:
            if('/doctor/' in img):
                continue
            doctor_html += f'<img src="{img}" alt="Hospital Image" style="width: 150px; height: 100px; object-fit: cover;">'
        
        doctor_html += "</div><br>"
        html_output += doctor_html

    return html_output

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
        research_doctors = gr.Button(value="Fetch Doctors")
        gr.Markdown()
        gr.Markdown("# Doctor Information")
        dynamic_area = gr.Markdown()  # Placeholder for dynamic UI components
        # Button to trigger doctor data display
        # display_button = gr.Button("Display Doctors")

        def update_ui(disease_name):
            global DISEASE_NAME
            category = degree.get_doctor_category(disease_name)
            DISEASE_NAME = category
            print('Category and Query is --------------', category, disease_name)
            return display_doctors(category)
        # Attach function to update UI
        research_doctors.click(update_ui, inputs=[query], outputs=dynamic_area)

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

'''https://www.practo.com/search/doctors?results_type=doctor&q=[{"word":"","autocompleted":true,"category":"subspeciality"}]&city=Bangalore&filters[doctor_review_count]=20,9999999&filters[years_of_experience]=15,9999999'''