import requests
import datetime
import json
import csv
import os


class TinderAPI:
    def __init__(self, token):
        self._token = token

    def profile(self):
        response = requests.get(
            f"{TINDER_URL}/v2/profile?include=account%2Cuser",
            headers={"X-Auth-Token": self._token}
        )
        response.raise_for_status()
        return response.json()

    def matches(self, limit=10):
        response = requests.get(
            f"{TINDER_URL}/v2/matches?count={limit}",
            headers={"X-Auth-Token": self._token}
        )
        response.raise_for_status()
        return response.json()["data"]["matches"]

    def get_messages(self, match_id):
        response = requests.get(
            f"{TINDER_URL}/v2/matches/{match_id}/messages?count=50",
            headers={"X-Auth-Token": self._token}
        )
        response.raise_for_status()
        return response.json()["data"]["messages"]

    def send_message(self, match_id, message):
        payload = {"message": message}
        response = requests.post(
            f"{TINDER_URL}/user/matches/{match_id}",
            headers={
                "X-Auth-Token": self._token,
                "Content-Type": "application/json"
            },
            json=payload
        )
        response.raise_for_status()
        return response.json()

def read_conversation_record(csv_file):
    if not os.path.exists(csv_file):
        return {}
    
    record = {}
    with open(csv_file, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 4:
                person_name, match_id, conversation_id, message_id = row
                record[(person_name, match_id)] = {"conversation_id": conversation_id, "message_id": message_id}
    return record

def write_conversation_record(csv_file, record):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        for (person_name, match_id), ids in record.items():
            writer.writerow([person_name, match_id, ids["conversation_id"], ids["message_id"]])

conversation_record = read_conversation_record(CSV_FILE)

def parse_response(response, person_name, match_id, tinder_api):
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            if decoded_line.startswith('data:'):
                data = decoded_line[5:].strip()
                if data:
                    try:
                        json_data = json.loads(data)
                        if json_data.get('event') == 'workflow_finished' or json_data.get('event') == 'message':
                            if json_data.get('data') and json_data['data'].get('status') == 'succeeded':
                                answer = json_data['data']['outputs']['answer']
                                conversation_id = json_data['conversation_id']
                                message_id = json_data['message_id']
                                if conversation_id and message_id:
                                    print(f"Answer: {answer}")
                                    conversation_record[(person_name, match_id)] = {"conversation_id": conversation_id, "message_id": message_id}
                                    write_conversation_record(CSV_FILE, conversation_record)
                                    # Send answer as message to Tinder match
                                    tinder_api.send_message(match_id, answer)
                                else:
                                    print("conversation_id or message_id is missing.")
                    except json.JSONDecodeError:
                        print(f"Received non-JSON response: {data}")
                    except KeyError as e:
                        print(f"Key error: {e} in data: {json_data}")
                    except TypeError as e:
                        print(f"Type error: {e} in data: {json_data}")

class Person:
    def __init__(self, data):
        self.id = data["_id"]
        self.name = data.get("name", "Unknown")
        self.bio = data.get("bio", "")
        self.city = data.get("city", {}).get('name', "")
        self.relationship_intent = data.get("relationship_intent", {}).get('body_text', "")
        selected_descriptors = data.get('selected_descriptors', [])
        self.selected_descriptors = []
        for selected_descriptor in selected_descriptors:
            if selected_descriptor.get('prompt'):
                self.selected_descriptors.append(f"{selected_descriptor.get('prompt')} {'/'.join([s['name'] for s in selected_descriptor['choice_selections']])}")
            else:
                self.selected_descriptors.append(f"{selected_descriptor.get('name')}: {'/'.join([s['name'] for s in selected_descriptor['choice_selections']])}")
        self.distance = data.get("distance_mi", 0) / 1.60934
        self.birth_date = datetime.datetime.strptime(data["birth_date"], '%Y-%m-%dT%H:%M:%S.%fZ') if data.get("birth_date", False) else None
        self.gender = ["Male", "Female", "Unknown"][data.get("gender", 2)]
        self.images = list(map(lambda photo: photo["url"], data.get("photos", [])))
        self.jobs = list(map(lambda job: {"title": job.get("title", {}).get("name"), "company": job.get("company", {}).get("name")}, data.get("jobs", [])))
        self.schools = list(map(lambda school: school["name"], data.get("schools", [])))

    def infos(self):
        return {
            'name': self.name,
            'bio': self.bio,
            'city': self.city,
            'relationship_intent': self.relationship_intent,
            'selected_descriptors': self.selected_descriptors,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'gender': self.gender,
            'jobs': self.jobs,
            'schools': self.schools,
            'distance': self.distance
        }


def main():
    tinder_api = TinderAPI(TOKEN)
    
    # my profile
    profile = tinder_api.profile()
    user_id = profile['data']['user']['_id']
    print(f"Profile: {profile['data']['user']['name']}, Bio: {profile['data']['user']['bio']}\n")

    # matches
    matches = tinder_api.matches(limit=10)
    print(f"Found {len(matches)} matches.\n")

    # catch every matches info and message
    for match in matches:
        match_id = match["id"]
        person = Person(match["person"])
        #print(match["person"])
        
        print(f"Match Name: {person.name}")
        print(f"Bio: {person.bio}")
        print(f"City: {person.city}")
        print(f"Relationship Intent: {person.relationship_intent}")
        print(f"Selected Descriptors: {person.selected_descriptors}")
        print(f"Birth Date: {person.birth_date}")
        print(f"Gender: {person.gender}")
        print(f"Jobs: {person.jobs}")
        print(f"Schools: {person.schools}")
        print(f"Distance: {person.distance} km")
        print(f"Messages with {person.name}:")

        messages = tinder_api.get_messages(match_id)
        latest_message_from_me = None
        new_messages = []
        for message in messages:
            if message["from"] == user_id:
                latest_message_from_me = message
                break

        if latest_message_from_me:
            sent_date = datetime.datetime.strptime(latest_message_from_me["sent_date"], '%Y-%m-%dT%H:%M:%S.%fZ')
            print(f"Last message from me: [{sent_date}] {latest_message_from_me['message']}\n")
            for message in messages:
                message_date = datetime.datetime.strptime(message["sent_date"], '%Y-%m-%dT%H:%M:%S.%fZ')
                if message_date > sent_date:
                    from_id = message["from"]
                    to_id = message["to"]
                    text = message["message"]
                    new_messages.append(f"{text}")
                    print(f"[{message_date}] {from_id} to {to_id}: {text}")
        else:
            for message in messages:
                message_date = datetime.datetime.strptime(message["sent_date"], '%Y-%m-%dT%H:%M:%S.%fZ')
                from_id = message["from"]
                to_id = message["to"]
                text = message["message"]
                new_messages.append(f"{text}")
                print(f"[{message_date}] {from_id} to {to_id}: {text}")

        # 構造 JSON payload
        payload = {
            "inputs": person.infos(),
            "query": "\n".join(new_messages),
            "response_mode": "streaming",
            "conversation_id": conversation_record.get((person.name, match_id), {}).get("conversation_id", ""),
            "user": person.name,
        }

        # 發送請求到API
        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }

        response = requests.post(API_ENDPOINT, json=payload, headers=headers, stream=True)
        
        if response.status_code == 200:
            parse_response(response, person.name, match_id, tinder_api)
        else:
            print(f"Failed to send data to API: {response.status_code} - {response.text}")
        
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()
