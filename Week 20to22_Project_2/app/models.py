from . import mongo
from datetime import datetime

def save_analysis_result(transcript, feedback):
    result = {
        'transcript': transcript,
        'feedback': feedback,
        'created_at': datetime.utcnow()
    }
    result_id = mongo.db.analysis_results.insert_one(result).inserted_id
    return result_id

def get_analysis_result(result_id):
    result = mongo.db.analysis_results.find_one({'_id': result_id})
    return result
