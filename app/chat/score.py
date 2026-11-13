from app.chat.redis import client
import random
def random_component_by_score(component_type, component_map):
    # Make sure component_type is 'llm', 'retriever', or 'memory'
    if component_type not in ['llm', 'retriever', 'memory']:
        raise ValueError(f"Invalid component type: {component_type}")

    # From redis, get the hash containing the sum total scores for the given component_type
    values = client.hgetall(f"{component_type}_score_values")

    # From redis, get the hash containing the number of times each component has been boed on
    counts = client.hgetall(f"{component_type}_score_counts")

    # Get all the valid coponent names from the component map
    names = component_map.keys()
    # Loop over those valid names and  use them to calculate the average score for each component    
    # Add average score to a dictionary
    avg_scores = {}
    for name in names:
        score = int(values.get(name, 1))
        count = int(counts.get(name, 1))
        avg_score = score / count
        avg_scores[name] = max(avg_score, 0.1)

    # Do a weighted random selection
    sum_scores = sum(avg_scores.values())
    random_val = random.uniform(0, sum_scores)
    cumulative = 0
    for name, score in avg_scores.items():
        cumulative += score
        if cumulative >= random_val:
            return name
    return None

def score_conversation(
    conversation_id: str, score: float, llm: str, retriever: str, memory: str
) -> None:
    score = min(max(score, 0), 1)

    client.hincrby("llm_score_values", llm, score)
    client.hincrby("llm_score_counts", llm, 1)
    client.hincrby("retriever_score_values", retriever, score)
    client.hincrby("retriever_score_counts", retriever, 1)
    client.hincrby("memory_score_values", memory, score)
    client.hincrby("memory_score_counts", memory, 1)

    client.zadd("llm_scores", {llm: score})
    client.zadd("retriever_scores", {retriever: score})
    client.zadd("memory_scores", {memory: score})    


def get_scores():
    aggregate = {"llm": {}, "retriever": {}, "memory": {}}
    for component_type in ["llm", "retriever", "memory"]:
        values = client.hgetall(f"{component_type}_score_values")
        counts = client.hgetall(f"{component_type}_score_counts")
        names = values.keys()
        
        for name in names:
            score = int(values.get(name, 1))
            count = int(counts.get(name, 1))
            avg_score = score / count
            aggregate[component_type][name] = [avg_score]
    return aggregate

    """
    Retrieves and organizes scores from the langfuse client for different component types and names.
    The scores are categorized and aggregated in a nested dictionary format where the outer key represents
    the component type and the inner key represents the component name, with each score listed in an array.

    The function accesses the langfuse client's score endpoint to obtain scores.
    If the score name cannot be parsed into JSON, it is skipped.

    :return: A dictionary organized by component type and name, containing arrays of scores.

    Example:

        {
            'llm': {
                'chatopenai-3.5-turbo': [avg_score],
                'chatopenai-4': [avg_score]
            },
            'retriever': { 'pinecone_store': [avg_score] },
            'memory': { 'persist_memory': [avg_score] }
        }
    """

    
