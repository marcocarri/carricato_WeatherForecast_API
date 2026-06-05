import random


def get_simulated_weather(city: str, target_date):
    """
    genera dati meteo simulati
    utilizza un seed basato su città e data affinché la previsione sia coerente se richiesta più volte per gli stessi parametri
    """
    # creiamo un seed univoco (nome della città+data --> es: "roma_2026-07-12")
    seed_string = f"{city.strip().lower()}_{target_date}"
    random.seed(seed_string)

    conditions = ["Soleggiato", "Parzialmente Nuvoloso", "Nuvoloso", "Pioggia", "Temporale", "Neve", "Nebbia"]

    # generiamo i dati simulati
    temperature = round(random.uniform(-5.0, 38.0), 1)
    condition = random.choice(conditions)
    humidity = random.randint(30, 95)

    # resettiamo il seed per non influenzare altre funzioni random nel progetto
    random.seed()

    return {
        "city": city.strip().title(),
        "target_date": target_date,
        "temperature": temperature,
        "weather_condition": condition,
        "humidity": humidity
    }