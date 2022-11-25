import os
import openai
from django.conf import settings

# Load your API key from an environment variable or secret management service
openai.api_key = settings.OPENAI_API_KEYS





def generateBlogTopicIdeas(topic,audience,keywords):
    blog_topics = []
    response = openai.Completion.create(
  model="text-davinci-002",
  prompt="Generate 5 blog topic ideas on the given topic: {}\nAudience: {}\nkeywords: {} \n*".format(topic,audience,keywords),
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
    




def generateBlogSections(topic,audience,keywords):
    blog_sections = []
    response = openai.Completion.create(
  model="text-davinci-002",
  prompt="Generate 5 blog section titles for the provided blog topic, Audience, and keywords: {}\nAudience: {}\nkeywords: {} \n*".format(topic,audience,keywords),
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
            blog_sections.append(blog)
    else:
        return []

    return blog_sections



def generateBlogSectionsDetails(blogTopic,sectionTopic,audience,keywords):
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt="Generate detailed blog write up for the following blog section heading, given the blog title, audience and keywords.\nBlog Title: {}\nBlog Section Heading: {}\nAudience: {}\nKeywords: {}\n\n".format(blogTopic,sectionTopic,audience,keywords),
            temperature=0.7,
            max_tokens=500,
            top_p=1,
            best_of =1,
            frequency_penalty=0,
            presence_penalty=0)

        if 'choices' in response:
            if len(response['choices'])>0:
                res =  response['choices'][0]['text']
                cleanres = res.replace('\n','<br>')
                return cleanres
            else:
                return []
        else:
             return [] 

