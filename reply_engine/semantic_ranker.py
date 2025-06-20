# reply_engine/semantic_ranker.py

from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def semantic_rank(user_msg, candidates, top_k=5):
    query_vec = model.encode(user_msg, convert_to_tensor=True)
    candidate_vecs = model.encode(candidates, convert_to_tensor=True)
    scores = util.cos_sim(query_vec, candidate_vecs)[0]
    top_indices = scores.argsort(descending=True)[:top_k]
    return [candidates[i] for i in top_indices]
