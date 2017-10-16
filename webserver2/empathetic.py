from random import randint

data = [
    {
        'range': [0, 50.0],
        'message': ['Yay! It appears this job will likely be safe from automation in the next 10 to 20 years. Would you still like to explore different career opportunities?',
                    "Hoot Hoot! I'm happy to tell you that there is only a {{PERCENTAGE}} chance your job will be automated soon. Would you like to chat, or explore other careers?"]
    },
    {
        'range': [51.0, 100],
        'message': ["I'm sorry to inform you that there is a {{PERCENTAGE}} likelihood that your current job will be automated in the next 10 to 20 years. Fortunately there may be other jobs that might be a good fit for your skills.",
                    "Hoot Hoot! We need to talk...Your job is {{PERCENTAGE}} likely to be automated. Do you want to learn about some other career options?"]
    }

]

def generate(percentage):
    for m in data:
        if percentage < m.get('range')[1] and percentage > m.get('range')[0]:
            return m.get('message')[randint(0, len(m.get('message')) - 1)].replace("{{PERCENTAGE}}", str(percentage))

def job_phrase(alternative, main):
    return "A job similar to %s that's less likely to be automated is %s." % (
        main.occupation,
        alternative.occupation,
    )
