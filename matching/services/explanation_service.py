from openai import OpenAI

client = OpenAI()

def generate_match_explanation(job_description , candidate_text , similarity):

    prompt = f"""
    You are an expert technical recruiter.
    A candidate has a similarity score of {round(similarity, 2)} for the following job:

    {job_description}

    {candidate_text[:1500]}

    Write a concise 2-sentence explanation descriing why the candidate is a good (or poor) match
    Focus on skills , experience , and role relevance

    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role" : "user" , "content" : prompt}],
        max_tokens=100,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()
