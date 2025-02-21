from typing import Dict, Tuple
import logging

from flask import Flask, request, jsonify
from pymongo import MongoClient
from opentelemetry_py import init_telemetry

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# initialize OpenTelemetry
flask_instrumentor = init_telemetry("service-green", "1.0.0")
flask_instrumentor.instrument_app(app)

# MongoDB configuration
MONGODB_URI = "mongodb://user:pass@database:27017/"
DB_NAME = "voting"
COLLECTION_NAME = "votes"

# MongoDB setup - using service name from docker-compose
uri = "mongodb://database:27017/voting"
client = MongoClient(uri)
db = client['voting']
votes = db['votes']


class VotingDatabase:
    """
    A class to interact with the voting database.

    Methods
    -------
    __init__():
        Initializes the database connection and sets up the collection.

    clear_votes() -> None:
        Clears all votes from the database.

    add_vote(choice: str) -> None:
        Adds a new vote to the database.

    get_counts() -> Tuple[int, int]:
        Retrieves the current vote counts for 'spaces' and 'tabs'.
    """
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[DB_NAME]
        self.votes = self.db[COLLECTION_NAME]
        logger.info("Connected to MongoDB")

    def clear_votes(self) -> None:
        """Clear all votes from the database"""
        self.votes.delete_many({})
        logger.info("Cleared all votes")

    def add_vote(self, choice: str) -> None:
        """Add a new vote to the database"""
        self.votes.insert_one({"choice": choice})
        logger.info("Added vote for %s", choice)

    def get_counts(self) -> Tuple[int, int]:
        """Get the current vote counts"""
        spaces_count = self.votes.count_documents({"choice": "spaces"})
        tabs_count = self.votes.count_documents({"choice": "tabs"})
        return spaces_count, tabs_count


voting_db = VotingDatabase()


@app.route("/", methods=["GET"])
def handle_vote() -> Tuple[Dict, int]:
    choice = request.args.get("choice", default=None, type=str)

    if choice == "clear":
        voting_db.clear_votes()
    elif choice in ["spaces", "tabs"]:
        voting_db.add_vote(choice)

    spaces_count, tabs_count = voting_db.get_counts()
    return jsonify({"spaces": spaces_count, "tabs": tabs_count}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3020, debug=True)
