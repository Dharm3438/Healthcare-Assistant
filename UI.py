import gradio as gr
import helper_functions as api
import practo_integration
import doctor_filter_by_degree as degree

import agentops
agentops.init()

CSS ="""
#disease_id {background-color: #374151; padding: 20px; border-radius: 5px; border: 10px solid #1f2937;}
#diet_id {background-color: #374151; padding: 20px; border-radius: 5px; border: 10px solid #1f2937;}
#exercise_id {background-color: #374151; padding: 20px; border-radius: 5px; border: 10px solid #1f2937;}
#component-0 > div:nth-child(8) { padding: 20px; border-radius: 5px; border: 10px solid #1f2937; height: 600px !important; }
.iframe-container { display: flex; flex-wrap: wrap; gap: 10px; }
iframe { flex: 1 1 calc(50% - 10px); max-width: 560px; }
"""


# Global variables
QUERY = ""
CITY = ""
AGE = 0
WEIGHT = 0
HEIGHT = 0

# Setter functions
def set_query(value):
    global QUERY
    QUERY = value

def set_city(value):
    global CITY
    CITY = value

def set_age(value):
    global AGE
    AGE = value

def set_weight(value):
    global WEIGHT
    WEIGHT = value

def set_height(value):
    global HEIGHT
    HEIGHT = value


def display_doctors(category):
    global CITY
    url1 = '''https://www.practo.com/search/doctors?results_type=doctor&q=[{"word":"'''
    url1 += str(category)
    url1 += '''","autocompleted":true,"category":"subspeciality"}]&city=''' + CITY + '''&filters[doctor_review_count]=20,9999999&filters[years_of_experience]=15,9999999'''

    doctors_data = practo_integration.scrape_doctors_data_with_urls(url1)
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
    gr.Markdown("<h4><center>Empowering You with Personalized Health Insights for a Healthier Tomorrow</center></h4>")

    with gr.Row():
        with gr.Column(scale=2):
            query = gr.Textbox(label="Specify Disease", placeholder="Please describe your disease and medical condition", info="For Example: Bladder Cystitis or Umbilical Hernia", interactive=True)
            query.change(set_query, inputs=query)
        with gr.Column(scale=1):
            city = gr.Dropdown(["Bangalore", "Chennai", "Delhi", "Hyderabad", "Mumbai", "Pune", "Kolkata"], label="Select your City", interactive=True)
            city.change(set_city, inputs=city)
    
    with gr.Row():
        with gr.Column():
            age = gr.Number(value=0, label="Age")
            age.change(set_age, inputs=age)
        with gr.Column():
            weight = gr.Number(value=0, label="Weight")
            weight.change(set_weight, inputs=weight)
        with gr.Column():
            height = gr.Number(value=0, label="Height")
            height.change(set_height, inputs=height)

    gr.Markdown("<br />")

    with gr.Tab("Disease Analysis"):
        research_disease = gr.Button(value="Research Diesease", elem_id="disease_btn")
        disease_details_mr = gr.Markdown(elem_id="disease_id", container=True, show_copy_button=True)
        research_disease.click(api.run_disease_crew, inputs=[query], outputs=disease_details_mr)
    with gr.Tab("Diet Analysis"):
        research_diet = gr.Button(value="Research Diet", scale=1)
        diet_details_mr = gr.Markdown(elem_id="diet_id")
        research_diet.click(api.run_diet_crew, inputs=[query], outputs=diet_details_mr)
    with gr.Tab("Exercise Plan"):
        research_exercise = gr.Button(value="Research Exercise", scale=1)
        exercise_details_mr = gr.Markdown(elem_id="exercise_id")
        research_exercise.click(api.run_exercise_crew, inputs=[query], outputs=exercise_details_mr)
    with gr.Tab("Consultation"):
        research_doctors = gr.Button(value="Get Doctors")
        gr.Markdown()
        gr.Markdown("# Doctor Information")
        dynamic_area = gr.Markdown()  # Placeholder for dynamic UI components
    
        def update_ui(disease_name):
            global DISEASE_NAME
            category = degree.get_doctor_category(disease_name)
            DISEASE_NAME = category
            print('Category and Query is --------------', category, disease_name)
            return display_doctors(category)
        # Attach function to update UI
        research_doctors.click(update_ui, inputs=[query], outputs=dynamic_area)

    with gr.Tab("Patient Experiences"):
        research_stories = gr.Button(value="Get Stories")
        content = gr.HTML()
        research_stories.click(api.get_patient_stories, inputs=[query], outputs=content)

    gr.Markdown("<br />")
    gr.ChatInterface(fn=api.ask_questions, type="messages", examples=["What is the Duration of my Disease?", "What is Pantop D medicines about?", "What lifestyle changes should i make?"], title="Chat with Health Assistant")

demo.launch()