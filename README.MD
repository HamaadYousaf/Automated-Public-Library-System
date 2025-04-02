1) to access users-service
cd-users-service
uvicorn main:app --reload
2) to access resources-service
cd resources-service
uvicorn main:app --reload --port 8001
3) to access reservations-service
cd reservations-service
uvicorn main:app --reload --port 8002
4) to access recommendations-service
cd recommendations-service
uvicorn main:app --reload --port 8003
5) to access frontend
cd frontend
cd frontend
npm rundev
