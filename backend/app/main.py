from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.database import redis_client
from app.database import SessionLocal
from app.database import engine
from app.models import Base
from app.models import Incident
from app.models import RCA
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi.requests import Request
import json
import datetime

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

limiter = Limiter(
    key_func=get_remote_address
)

app.state.limiter = limiter


class Signal(BaseModel):

    component_id: str
    severity: str
    message: str


class RCARequest(BaseModel):

    incident_id: int
    root_cause: str
    fix_applied: str
    prevention_steps: str


@app.get("/")
def home():

    return {
        "message": "IMS Running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.post("/signals")
@limiter.limit("100/minute")
def create_signal(
    request: Request,
    signal: Signal
):

    data = {
        "component_id": signal.component_id,
        "severity": signal.severity,
        "message": signal.message,
        "timestamp": str(
            datetime.datetime.now()
        )
    }

    redis_client.rpush(
        "signal_queue",
        json.dumps(data)
    )

    return {
        "message": "Signal queued"
    }


@app.get("/incidents")
def get_incidents():

    db = SessionLocal()

    try:

        incidents = db.query(
            Incident
        ).all()

        result = []

        for incident in incidents:

            result.append({
                "id": incident.id,
                "component_id": incident.component_id,
                "severity": incident.severity,
                "state": incident.state,
                "mttr": incident.mttr
            })

        return result

    finally:

        db.close()


@app.post("/rca")
def submit_rca(
    rca: RCARequest
):

    db = SessionLocal()

    try:

        incident = db.query(
            Incident
        ).filter(
            Incident.id == rca.incident_id
        ).first()

        if not incident:

            raise HTTPException(
                status_code=404,
                detail="Incident not found"
            )

        incident_rca = RCA(
            incident_id=rca.incident_id,
            root_cause=rca.root_cause,
            fix_applied=rca.fix_applied,
            prevention_steps=rca.prevention_steps
        )

        db.add(incident_rca)

        incident.end_time = str(
            datetime.datetime.now()
        )

        start = datetime.datetime.fromisoformat(
            incident.start_time
        )

        end = datetime.datetime.now()

        incident.mttr = str(
            end - start
        )

        incident.state = "CLOSED"

        db.commit()

        return {
            "message": "RCA Submitted"
        }

    finally:

        db.close()


@app.put("/incidents/{incident_id}/state")
def update_state(
    incident_id: int,
    state: str
):

    db = SessionLocal()

    try:

        incident = db.query(
            Incident
        ).filter(
            Incident.id == incident_id
        ).first()

        if not incident:

            raise HTTPException(
                status_code=404,
                detail="Incident not found"
            )

        if state == "CLOSED":

            rca = db.query(
                RCA
            ).filter(
                RCA.incident_id == incident_id
            ).first()

            if not rca:

                raise HTTPException(
                    status_code=400,
                    detail="RCA Required"
                )

        incident.state = state

        db.commit()

        return {
            "message": "State updated"
        }

    finally:

        db.close()
