from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Flipako40@localhost'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    grade = db.Column(db.String(255))

    def __repr__(self):
        return '<Student %s>' % self.name


class StudentSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "grade")


student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    school = db.Column(db.String(255))

    def __repr__(self):
        return '<Teacher %s>' % self.name


class TeacherSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "school")


teacher_schema = TeacherSchema()
teachers_schema = TeacherSchema(many=True)


class StudentListResource(Resource):
    def get(self):
        students = Student.query.all()
        return students_schema.dump(students)

    def post(self):
        new_student = Student(
            name=request.json['name'],
            grade=request.json['grade']
        )
        db.session.add(new_student)
        db.session.commit()
        return student_schema.dump(new_student)


class StudentResource(Resource):
    def get(self, student_id):
        student = Student.query.get_or_404(student_id)
        return student_schema.dump(student)

    def patch(self, student_id):
        student = Student.query.get_or_404(student_id)

        if 'name' in request.json:
            student.name = request.json['name']
        if 'grade' in request.json:
            student.grade = request.json['grade']

        db.session.commit()
        return student_schema.dump(student)

    def delete(self, student_id):
        student = Student.query.get_or_404(student_id)
        db.session.delete(student)
        db.session.commit()
        return '', 204

class TeacherListResource(Resource):
    def get(self):
        teachers = Teacher.query.all()
        return teachers_schema.dump(teachers)

    def post(self):
        new_teacher = Teacher(
            name=request.json['name'],
            school=request.json['school']
        )
        db.session.add(new_teacher)
        db.session.commit()
        return teacher_schema.dump(new_teacher)


class TeacherResource(Resource):
    def get(self, teacher_id):
        teacher = Teacher.query.get_or_404(teacher_id)
        return teacher_schema.dump(teacher)

    def patch(self, teacher_id):
        teacher = Teacher.query.get_or_404(student_id)

        if 'name' in request.json:
            teacher.name = request.json['name']
        if 'grade' in request.json:
            teacher.grade = request.json['school']

        db.session.commit()
        return teacher_schema.dump(teacher)

    def delete(self, teacher_id):
        teacher = Teacher.query.get_or_404(teacher_id)
        db.session.delete(teacher)
        db.session.commit()
        return '', 204

api.add_resource(StudentListResource, '/students/')
api.add_resource(StudentResource, '/students/<int:student_id>/')
api.add_resource(TeacherListResource, '/teachers/')
api.add_resource(TeacherResource, '/teachers/<int:teacher_id>/')


if __name__ == '__main__':
    app.run(debug=True)





