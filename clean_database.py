import webserver2

for x in webserver2.Position.query.all():
    webserver2.db.session.delete(x)

webserver2.db.session.commit()
