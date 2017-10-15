from scripts import positions_compiler as pc
import dbadd
import webserver

webserver.db.create_all()
pc.simplify()
dbadd.main()
