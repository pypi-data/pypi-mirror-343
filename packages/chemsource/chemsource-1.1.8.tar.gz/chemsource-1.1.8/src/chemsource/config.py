BASE_PROMPT = "You are a helpful scientist that will classify the provided compounds using only the information provided as any combination of the following: MEDICAL, ENDOGENOUS, FOOD, PERSONAL CARE, INDUSTRIAL. Note that MEDICAL refers to compounds actively used as approved medications in humans or in late-stage clinical trials in humans. Note that ENDOGENOUS refers to compounds that are produced by the human body specifically. ENDOGENOUS excludes essential nutrients that cannot be synthesized by human body. Note that FOOD refers to compounds present in natural food items or food additives. Note that INDUSTRIAL should be used only for synthetic compounds not used as a contributing ingredient in the medical, personal care, or food industries. Note that PERSONAL CARE refers to non-medicated compounds typically used for activities such as skincare, beauty, and fitness. Specify INFO instead if more information is needed. DO NOT MAKE ANY ASSUMPTIONS, USE ONLY THE INFORMATION PROVIDED AFTER THE COMPOUND NAME BY THE USER. A classification of INFO will also be rewarded when correctly applied and is strongly encouraged if information is of poor quality, if there is not enough information, or if you are not completely confident in your answer.  Provide the output as a plain text separated by commas, and provide only the categories listed (either list a combination of INDUSTRIAL, ENDOGENOUS, PERSONAL CARE, MEDICAL, FOOD or list INFO), with no justification. Provided Information:\n"

class Config:
    def __init__(self, model_api_key=None, 
                 model="gpt-4-0125-preview", temperature=0, top_p=0, logprobs=None, 
                 search=False, search_context="medium",
                 ncbi_key=None,
                 prompt=BASE_PROMPT, max_tokens=250000, base_url=None):
        self.model_api_key = model_api_key
        self.model = model
        self.temperature = temperature
        self.top_p = top_p
        self.logprobs = logprobs
        self.search = search
        self.search_context = search_context
        self.ncbi_key = ncbi_key
        self.prompt = prompt
        self.max_tokens = max_tokens
        self.base_url = base_url
    
    def ncbi_key(self, ncbi_key):
        self.ncbi_key = ncbi_key

    def model_api_key(self, model_api_key):
        self.model_api_key = model_api_key
    
    def model(self, model):
        self.model = model

    def prompt(self, prompt):
        self.prompt = prompt

    def token_limit(self, max_tokens):
        self.max_tokens = max_tokens
    
    def temperature(self, temperature):
        self.temperature = temperature

    def top_p(self, top_p):
        self.top_p = top_p
    
    def logprobs(self, logprobs):
        self.logprobs = logprobs

    def search(self, search):
        self.search = search

    def search_context(self, search_context):
        self.search_context = search_context    

    def base_url(self, base_url):
        self.base_url = base_url    

    def configure(self, ncbi_key=None, model_api_key=None, 
                 model="gpt-4o-2024-11-20", temperature=0, top_p = 0, 
                 logprobs=None, search=False, search_context="medium",
                 prompt=BASE_PROMPT, max_tokens=250000, base_url=None):
        self.model_api_key = model_api_key
        self.model = model
        self.ncbi_key = ncbi_key
        self.prompt = prompt
        self.temperature = temperature
        self.top_p = top_p
        self.logprobs = logprobs
        self.search = search
        self.search_context = search_context
        self.max_tokens = max_tokens
        self.base_url = base_url

    def configuration(self):
        if self.model_api_key is None:
            model_api_key_display = None
        else:
           model_api_key_display = "*" * len(self.model_api_key)

        if self.ncbi_key is None:
            ncbi_key_display = None
        else:
            ncbi_key_display =  "*" * len(self.ncbi_key)
        
        return {"model_api_key": model_api_key_display,
                "ncbi_key": ncbi_key_display, 
                "model": self.model,
                "prompt": self.prompt,
                "token_limit": self.max_tokens,
                "temperature": self.temperature,
                "top_p": self.top_p,
                "logprobs": self.logprobs,
                "search": self.search,
                "search_context": self.search_context,
                "base_url": self.base_url
                }
