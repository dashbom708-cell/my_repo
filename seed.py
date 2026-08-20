from models import db, Action

def fill_action():
    actions = ["do", "schedule", "delegate", "eliminate"]
    for item in actions:
        if not Action.query.filter_by(name=item).first():
            action = Action(name=item)
            db.session.add(action)
    db.session.commit()