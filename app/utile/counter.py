from app.models.counter import Counter


def increment_counter_value(db):
    counter = db.query(Counter).first()
    if counter:
        counter.value += 1
    else:
        new_counter = Counter(value=1)
        db.add(new_counter)
    db.commit()


def get_counter(db):
    counter = db.query(Counter).first()
    if counter:
        return counter.value
    else:
        return 0



