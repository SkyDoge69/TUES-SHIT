from database import SQLite
from errors import ApplicationError

class Question():
 
    def __init__(self, content, answer, user, question_id=None):
        self.id = question_id
        self.content = content
        self.answer = answer
        self.user = user
 
    def to_dict(self):
        question_data = self.__dict__
        return question_data

    def to_viewable(self):
        question_data = self.__dict__
        return question_data
 
    def save(self):
        with SQLite() as db:
            cursor = db.execute(self.__get_save_query())
            self.id = cursor.lastrowid
        return self
 
    @staticmethod
    def delete(question_id):
        result = None
        with SQLite() as db:
            result = db.execute("DELETE FROM question WHERE id = ?",
                    (question_id,))
        if result.rowcount == 0:
            raise ApplicationError("No value present", 404)
 
    @staticmethod
    def find(question_id):
        result = None
        with SQLite() as db:
            result = db.execute(
                    "SELECT content, answer, user, id FROM question WHERE id = ?",
                    (question_id,))
        question = result.fetchone()
        if question is None:
            raise ApplicationError(
                    "Question with id {} not found".format(question_id), 404)
        return Question(*question)

    @staticmethod
    def find_by_user(user):
        result = None
        with SQLite() as db:
            result = db.execute(
                    "SELECT content, answer, user, id FROM question WHERE user = ?",
                    (user,))
        question = result.fetchone()
        if question is None:
            return None
        return Question(*question)
    
 
    @staticmethod
    def all():
        with SQLite() as db:
            result = db.execute(
                    "SELECT content, answer, user, id FROM question").fetchall()
            return [Question(*row) for row in result]
 
    def __get_save_query(self):
        query = "{} INTO user {} VALUES {}"
        if self.id == None:
            args = (self.content, self.answer, self.user)
            query = query.format("INSERT", "(content, answer, user)", args)
        else:
            args = (self.id, self.content, self.answer, self.user)
            query = query.format("REPLACE", "(id, content, answer, user)", args)
        return query
