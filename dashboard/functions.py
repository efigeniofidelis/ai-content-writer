import os
import openai
from django.conf import settings

# Load your API key from an environment variable or secret management service
openai.api_key = settings.OPENAI_API_KEYS





def generateBlogTopicIdeas(topic,keywords):
    blog_topics = []
    response = openai.Completion.create(
  model="text-davinci-002",
  prompt="generate blog topic ideas on following topics: {}\nkeywords: {} \n*".format(topic,keywords),
  temperature=0.7,
  max_tokens=250,
  top_p=1,
  best_of =1,
  frequency_penalty=0,
  presence_penalty=0
)

    if 'choices' in response:
        if len(response['choices'])>0:
            res = response['choices'][0]['text']
        else:
            return []
    else:
        return []
    
    a_list = res.split('*')
    if len(a_list) > 0:
        for blog in a_list:
            blog_topics.append(blog)
    else:
        return []

    return blog_topics
    




def generateBlogSectionHeadings(topic,keywords):
    response = openai.Completion.create(
  model="text-davinci-002",
  prompt="Generate blog section heading and section titles ased on the following section topic.\nTopic:  {}\nkeywords: {}\nTop 10 fashion trends of 2022 - how to look your best in 2022\n\n1. The rise of AI-generated fashion\n2. The return of vintage styles\n3. The rise of sustainable fashion\n4. The rise of sportswear\n5. The rise of athleisure\n6. The rise of streetwear\n7. The rise of luxury streetwear\n8. The rise of ready-to-wear\n9. The rise of haute couture\n10. The rise of smart clothing".format(topic,keywords),
  temperature=0.7,
  max_tokens=250,
  top_p=1,
  best_of =1,
  frequency_penalty=0,
  presence_penalty=0
)

    if 'choices' in response:
        if len(response['choices'])>0:
            res = response['choices'][0]['text']
        else:
            res = None
    else:
        res = None

    return res



