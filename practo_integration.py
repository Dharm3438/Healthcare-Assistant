import requests
from bs4 import BeautifulSoup
import json

def scrape_doctors_data_with_urls(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all main divs with the specified class
        main_divs = soup.find_all('div', class_="u-border-general--bottom")
        
        # List to store extracted data
        doctors_data = []

        for div in main_divs:
            # Extract data using attribute selectors
            doctor = {
                "doctor_name": div.find(class_="doctor-name").text.strip() if div.find(class_="doctor-name") else None,
                "experience": div.find(attrs={"data-qa-id": "doctor_experience"}).text.strip() if div.find(attrs={"data-qa-id": "doctor_experience"}) else None,
                "locality": div.find(attrs={"data-qa-id": "practice_locality"}).text.strip() if div.find(attrs={"data-qa-id": "practice_locality"}) else None,
                "city": div.find(attrs={"data-qa-id": "practice_city"}).text.strip() if div.find(attrs={"data-qa-id": "practice_city"}) else None,
                "clinic_name": div.find(attrs={"data-qa-id": "doctor_clinic_name"}).text.strip() if div.find(attrs={"data-qa-id": "doctor_clinic_name"}) else None,
                "clinic_count": div.find(attrs={"data-qa-id": "doctor_clinic_count"}).text.strip() if div.find(attrs={"data-qa-id": "doctor_clinic_count"}) else None,
                "consultation_fee": div.find(attrs={"data-qa-id": "consultation_fee"}).text.strip() if div.find(attrs={"data-qa-id": "consultation_fee"}) else None,
                "recommendation": div.find(attrs={"data-qa-id": "doctor_recommendation"}).text.strip() if div.find(attrs={"data-qa-id": "doctor_recommendation"}) else None,
                "total_feedback": div.find(attrs={"data-qa-id": "total_feedback"}).text.strip() if div.find(attrs={"data-qa-id": "total_feedback"}) else None,
                "availability_text": div.find(attrs={"data-qa-id": "availability_text"}).text.strip() if div.find(attrs={"data-qa-id": "availability_text"}) else None
            }
        
            # Extract URLs from the script tag
            script_tag = div.find('script', type="application/ld+json")
            if script_tag:
                try:
                    # Load the JSON content
                    script_json = json.loads(script_tag.string)
                    urls = []

                    # Collect 'url' fields
                    # if "url" in script_json:
                    #     doctor['profile'] = script_json["url"]
                    #     # urls.append(script_json["url"])

                    # Collect additional URLs from "photo" or other nested structures
                    if "photo" in script_json:
                        for photo in script_json["photo"]:
                            if "url" in photo:
                                urls.append(photo["url"])

                    doctor["urls"] = urls[:11]
                except json.JSONDecodeError:
                    doctor["urls"] = []

            doctors_data.append(doctor)
        
        # Return the list of extracted data
        return doctors_data

    except requests.exceptions.RequestException as e:
        print(f"Error while fetching the URL: {e}")
        return None

# Example usage
# if __name__ == "__main__":
#     url = '''https://www.practo.com/search/doctors?results_type=doctor&q=[{"word":"neurologist","autocompleted":true,"category":"subspeciality"}]&city=Bangalore&filters[doctor_review_count]=20,9999999&filters[years_of_experience]=15,9999999'''
#     data = scrape_doctors_data_with_urls(url)
    
#     print(data)
    # if data:
    #     for idx, doctor in enumerate(data, 1):
    #         print(f"Doctor {idx}:")
    #         for key, value in doctor.items():
    #             if key == "urls":
    #                 print(f"  {key}:")
    #                 for url in value:
    #                     print(f"    - {url}")
    #             else:
    #                 print(f"  {key}: {value}")
    #         print("\n")
    # else:
    #     print("No data found.")
