from sqlalchemy import func, desc, select, and_, distinct
from conf.models import Grade, Teacher, Student, Group, Subject
from conf.db import session


def select_01():
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade'))\
            .select_from(Student).join(Grade).group_by(Student.id).order_by(desc('average_grade')).limit(5).all()
    return result


def select_02():
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade'))\
            .select_from(Grade).join(Student).filter(Grade.subject_id == 1).group_by(Student.id)\
            .order_by(desc('average_grade')).limit(1).all()
    return result

def select_03(subject_id):
    result = (session.query(Group.id, Group.name, func.round(func.avg(Grade.grade), 2).label('group_name'))\
            .select_from(Group).join(Student).join(Grade).filter(Grade.subject_id == subject_id)\
            .group_by(Group.id, Group.name).order_by(desc('group_name')).limit(1).all())
    return result

def select_04():
    result = session.query(func.avg(Grade.grade).label('average_grade')).scalar()
    return result

def select_05(teacher_id):
    result = session.query(Subject.name).join(Teacher).filter(Teacher.id == teacher_id).all()
    return result

def select_06(group_id):
    result = session.query(Student.id).filter(Student.group_id == group_id).all()
    return result

def select_07(group_id, subject_id):
    result = session.query(Student.id, Grade.grade).join(Grade, Student.id == Grade.student_id) \
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id).all()
    return result

def select_08(teacher_id):
    result = session.query(func.avg(Grade.grade).label('avg_grade')) \
        .join(Subject, Subject.id == Grade.subject_id) \
        .filter(Subject.teacher_id == teacher_id) \
        .scalar()
    return result

def select_09(student_id):
    result = session.query(Subject.name) \
            .join(Grade, Subject.id == Grade.subject_id) \
            .filter(Grade.student_id == student_id) \
            .distinct() \
            .all()
    return result

def select_10(student_id, teacher_id):
    result = session.query(distinct(Subject.name).label('subject_name')) \
            .join(Grade, Subject.id == Grade.subject_id) \
            .join(Student, Grade.student_id == Student.id) \
            .filter(Student.id == student_id, Subject.teacher_id == teacher_id) \
            .all()
    return result



if __name__ == '__main__':
    print(select_01())
    print(select_02())
    print(select_03(3))
    print(select_04())
    print(select_05(3))
    print(select_06(3))
    print(select_07(3,3))
    print(select_08(3))
    print(select_09(3))
    print(select_10(3, 3))