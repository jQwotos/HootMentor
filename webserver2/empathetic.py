from random import randint

data = [
    {
        'range': [0, .50],
        'message': ['Yay! It appears as though your job is likely to be safe from automation in the next 10-20 years. Would you still like to explore different career opportunities?',
                    "Hoot Hoot! I'm sorry to tell you that there is a {{PERCENTAGE}}%% chance your job will be automated soon. Not to fear though! You can take your career in your own hands. Let's talk some more to see what some other career options are for you."]
    },
    {
        'range': [.51, .100],
        'message': ["I'm sorry to inform you that there is a {{PERCENTAGE}}%% likelihood that your current job will be automated in the next 10-20 years. Fortunately there may be other jobs that might be a good fit for your skills.",
                    "Hoot Hoot! We need to talk...Your job is {{PERCENTAGE}}%% likely to be automated. Do you want to learn about some other career options?"]
    }

]

def generate(percentage):
    for m in data:
        if percentage < m.get('range')[1] and percentage > m.get('range')[0]:
            return m.get('message')[randint(0, len(m.get('message')) - 1)].replace("{{PERCENTAGE}}", str(percentage))

def job_phrase(alternative, main):
    return "A job similar to %s that's %i%% less likely to be automated is %s." % (
        main.occupation,
        main.automation_risk - alternative.automation_risk,
        alternative.occupation,
    )
