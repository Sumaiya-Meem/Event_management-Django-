import os
import django
from faker import Faker
import random
from events.models import Category, Event, Participant

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

def populate_db():
    # Initialize Faker
    fake = Faker()

    # Create Categories
    categories = []
    for _ in range(5):
        category = Category.objects.create(
            name=fake.word().capitalize(),
            description=fake.sentence()
        )
        categories.append(category)
    print(f"Created {len(categories)} categories.")

    # Create Events
    events = []
    for _ in range(10):
        event = Event.objects.create(
            name=fake.catch_phrase(),
            description=fake.text(),
            date=fake.date_this_year(),
            time=fake.time(),
            location=fake.address(),
            category=random.choice(categories)
        )
        events.append(event)
    print(f"Created {len(events)} events.")

    # Create Participants
    participants = []
    for _ in range(20):
        participant = Participant.objects.create(
            name=fake.name(),
            email=fake.unique.email()
        )
        participants.append(participant)
    print(f"Created {len(participants)} participants.")

    # Assign Participants to Events
    for participant in participants:
        # Each participant attends 1 to 3 events
        attending_events = random.sample(events, random.randint(1, 3))
        for event in attending_events:
            participant.events.add(event)
    print("Assigned participants to events.")

    print("Database populated successfully!")

if __name__ == "__main__":
    populate_db()
