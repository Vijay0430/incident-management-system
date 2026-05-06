import json
import datetime
import time

from app.database import redis_client
from app.database import signals_collection
from app.database import SessionLocal

from app.models import Incident

from app.debounce import is_duplicate
from app.alert import send_alert

counter = 0

last_print = time.time()

while True:

    signal = redis_client.lpop(
        "signal_queue"
    )

    if signal:

        counter += 1

        data = json.loads(signal)

        signals_collection.insert_one(data)

        duplicate = is_duplicate(
            data["component_id"]
        )

        if not duplicate:

            db = SessionLocal()

            incident = Incident(
                component_id=data["component_id"],
                severity=data["severity"],
                state="OPEN",
                start_time=str(
                    datetime.datetime.now()
                ),
                end_time="",
                mttr=""
            )

            db.add(incident)

            db.commit()

            send_alert(
                data["severity"],
                data["component_id"]
            )

            print(
                "Incident Created"
            )

    current = time.time()

    if current - last_print >= 5:

        print(
            "Signals/sec:",
            counter / 5
        )

        counter = 0

        last_print = current
