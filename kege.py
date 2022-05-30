from app import app, db
from app.models import Users, Groups, Tests, Test_started


@app.shell_context_processors
def make_shell_context():
    return {'db': db, 'Users': Users, 'Groups': Groups, 'Tests': Tests, 'Test_started': Test_started}

