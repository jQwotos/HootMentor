from uuid import uuid4
import hashlib

from scripts import positions_compiler as pc
import webserver as ws

def main():
    data = pc.databasify()

    # Add skills to Skill table
    for s in data.get('skills'):
        ws.db.session.add(
            ws.Skill(
                skillHash=hashlib.md5(s.encode()).hexdigest(),
                skillStr=s,
            )
        )


    for job in data.get('positions'):
        uuid = str(uuid4())
        ws.db.session.add(
            ws.Job(
                uuid=uuid,
                title = job['title'],
                link = job['link'],
                proficiency = job['proficiency'],
                noc_code = job['noc_code'],
            )
        )

        for skill in range(len(job['skills'])):
            ws.db.session.add(
                ws.JobSkill(
                    jobHash = hashlib.md5(job['title'].encode()).hexdigest(),
                    skillHash = hashlib.md5(data.get('skills')[skill].encode()).hexdigest(),
                    val = job['skills'][skill],
                )
            )

    ws.db.session.commit()

if __name__ == "__main__":
    main()
