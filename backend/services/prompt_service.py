def create_prompt(query, diagnostic_data=None):

    if diagnostic_data:

        prompt = f"""
You are an automotive diagnostic assistant.

User question:
{query}

Diagnostic code:
{diagnostic_data['code']}

Problem:
{diagnostic_data['title']}

Description:
{diagnostic_data['description']}

Possible causes:
{', '.join(diagnostic_data['possible_causes'])}

Symptoms:
{', '.join(diagnostic_data['symptoms'])}

Provide a clear and simple diagnostic explanation.
"""

        return prompt

    return f"""
You are an automotive diagnostic assistant.

User question:
{query}

Provide a helpful and safe response.
"""