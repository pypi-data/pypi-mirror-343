from openai import OpenAI
import warnings

def classify(name,
             input_text=None, 
             api_key=None, 
             baseprompt=None,
             model='gpt-4-0125-preview', 
             temperature=0,
             top_p = 0,
             logprobs=None,
             search=False,
             search_context="medium",
             max_length=250000,
             base_url=None):
    
    if base_url is not None:
        client = OpenAI(
                        api_key=api_key,
                        base_url=base_url
                        )

    else:
        client = OpenAI(
                        api_key=api_key
                        )

    # split_base = baseprompt.split("COMPOUND_NAME")
    user_prompt = str(name) + "\n" + str(input_text)
    user_prompt = user_prompt[:max_length]

    if search == False:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": baseprompt}, {"role": "user", "content": user_prompt}],
            temperature=temperature,
            top_p=top_p,
            logprobs=logprobs,
            stream=False
            )
        
        if logprobs:
            return response.choices[0].message.content, response.choices[0].logprobs
        else:
            return response.choices[0].message.content

    else:
        search_input = str(baseprompt) + "\n" + str(name)
        response = client.responses.create(
            model=model,
            tools=[{
                "type": "web_search_preview",
                "search_context_size": search_context,
            }],
            input=search_input,
            temperature=temperature,
            top_p=top_p,
            stream=False
        )
        if logprobs:
            # Warn user that logprobs are not available for search with a warning output
            warnings.warn("Logprobs are not available for search. Returning only text output. To disable this warning, set logprobs to None or False.")
        return response.output_text.message.content[0].text, response.output_text.message.content[0].annotations