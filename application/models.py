import datetime

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Principle(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    ID = models.AutoField(primary_key=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class AdministrativeOfficer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    ID = models.AutoField(primary_key=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


# There is a missing field which is the TimeTable field to be done later
# TODO add TimeTable field for the class
class ClassInfo(models.Model):
    ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    totalStudentsNumber = models.PositiveIntegerField()
    timetable = models.ImageField(blank=True, default="Default_Timetable.jpg")

    def __str__(self):
        return self.name


class Student(models.Model):
    FIRST = 'FIRST'
    SECOND = 'SECOND'
    THIRD = 'THIRD'
    FOURTH = 'FOURTH'
    FIFTH = 'FIFTH'
    SIXTH = 'SIXTH'
    SEVENTH = 'SEVENTH'
    EIGHTH = 'EIGHTH'
    NINTH = 'NINTH'
    TENTH = 'TENTH'
    grade_choice = ((FIRST, 'FIRST'),
                    (SECOND, 'SECOND'),
                    (THIRD, 'THIRD'),
                    (FOURTH, 'FOURTH'),
                    (FIFTH, 'FIFTH'),
                    (SIXTH, 'SIXTH'),
                    (SEVENTH, 'SEVENTH'),
                    (EIGHTH, 'EIGHTH'),
                    (NINTH, 'NINTH'),
                    (TENTH, 'TENTH'),)
    ID = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, verbose_name='First Name')
    last_name = models.CharField(max_length=50, verbose_name='Last Name')
    classID = models.ForeignKey(ClassInfo, on_delete=models.SET_NULL, verbose_name='Student Class', blank=True,
                                null=True)
    studentYear = models.CharField(max_length=20, choices=grade_choice, default=FIRST, verbose_name='Year Grade')

    def __str__(self):
        return self.first_name + " " + self.last_name


class Course(models.Model):
    FIRST = 'FIRST'
    SECOND = 'SECOND'
    THIRD = 'THIRD'
    FOURTH = 'FOURTH'
    FIFTH = 'FIFTH'
    SIXTH = 'SIXTH'
    SEVENTH = 'SEVENTH'
    EIGHTH = 'EIGHTH'
    NINTH = 'NINTH'
    TENTH = 'TENTH'
    year_choice = ((FIRST, 'FIRST'),
                    (SECOND, 'SECOND'),
                    (THIRD, 'THIRD'),
                    (FOURTH, 'FOURTH'),
                    (FIFTH, 'FIFTH'),
                    (SIXTH, 'SIXTH'),
                    (SEVENTH, 'SEVENTH'),
                    (EIGHTH, 'EIGHTH'),
                    (NINTH, 'NINTH'),
                    (TENTH, 'TENTH'),)
    ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    numberOfHoursPerWeek = models.PositiveIntegerField()
    year = models.CharField(max_length=20,choices=year_choice, default=FIRST,verbose_name='Course Year')

    def __str__(self):
        return self.name


class ClassCourse(models.Model):
    ID = models.AutoField(primary_key=True)
    classID = models.ForeignKey(ClassInfo, on_delete=models.CASCADE)
    courseID = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.classID.name + ':' + self.courseID.name


class Assignment(models.Model):
    ID = models.AutoField(primary_key=True)
    assignmentTitle = models.CharField(max_length=50, verbose_name='Assignment Title')
    courseID = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Course')
    assignmentFile = models.FileField(verbose_name='File', upload_to='../media')
    additionDate = models.DateField(default=datetime.date.today, verbose_name='Addition Date')
    deadlineDate = models.DateField(default=None, verbose_name='Deadline Date')

    def __str__(self):
        return self.assignmentTitle


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ID = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    fiscalCode = models.CharField(max_length=16)
    coordinatedClass = models.ForeignKey(ClassInfo, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class TeacherCourse(models.Model):
    ID = models.AutoField(primary_key=True)
    teacherID = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    courseID = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.teacherID.first_name + '_' + self.teacherID.last_name + ':' + self.courseID.name


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ID = models.AutoField(primary_key=True)
    lastLogin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


class ParentStudent(models.Model):
    ID = models.AutoField(primary_key=True)
    parentID = models.ForeignKey(Parent, on_delete=models.CASCADE)
    studentID = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.studentID.first_name + ' ' + self.studentID.last_name + ':' + self.parentID.user.first_name + ' ' + self.parentID.user.last_name


class StudentCourse(models.Model):
    ID = models.AutoField(primary_key=True)
    studentID = models.ForeignKey(Student, on_delete=models.CASCADE)
    courseID = models.ForeignKey(Course, on_delete=models.CASCADE)
    finalGrade = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.studentID.first_name + '_' + self.studentID.last_name + ':' + self.courseID.name


class PerformanceGrade(models.Model):
    ID = models.AutoField(primary_key=True)
    studentCourseID = models.ForeignKey(StudentCourse, on_delete=models.CASCADE)
    date = models.DateField()
    grade = models.PositiveIntegerField()

    def __str__(self):
        return self.studentCourseID.studentID.first_name + '_' + self.studentCourseID.studentID.last_name + ':' + self.studentCourseID.courseID.name


class Note(models.Model):
    ID = models.AutoField(primary_key=True)
    studentCourseID = models.ForeignKey(StudentCourse, on_delete=models.CASCADE)
    noteText = models.CharField(max_length=300)


class Content(models.Model):
    ID = models.AutoField(primary_key=True)
    courseID = models.ForeignKey(Course, on_delete=models.CASCADE)
    contentString = models.CharField(max_length=100)
    material = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.courseID.name + '_Content' + self.ID.__str__()


class Announcements(models.Model):
    ID = models.AutoField(primary_key=True)
    announcementText = models.CharField(max_length=500)


class Attendance(models.Model):
    ID = models.AutoField(primary_key=True)
    studentCourseID = models.ForeignKey(StudentCourse, on_delete=models.CASCADE)
    presence = models.BooleanField(default=True)
    date = models.DateField(default=datetime.date.today)
    cameLate = models.BooleanField(default=False)
    leftEarly = models.BooleanField(default=False)

    def __str__(self):
        return self.studentCourseID.studentID.first_name+' '+self.studentCourseID.studentID.last_name+':'+self.studentCourseID.courseID.name


class FreeSlots(models.Model):
    teacherID = models.ForeignKey(Teacher, on_delete=models.CASCADE)  # check ONDELETE
    date = models.DateField()
    schedule = models.CharField(max_length=24)  # we have 24 slots (6 hours per day, 4 slots per hour, 15 mins each)

    def time_slot_to_regex(self, start_time, end_time):
        # times should be in HH:MM format
        start_hour, start_minutes = start_time.split(':')
        end_hour, end_minutes = end_time.split(':')

        slots_before_needed_time = (int(start_hour) * 4 + int(start_minutes) / 15)

        # compute how many hours are between given times and find out nr of slots
        hour_duration_slots = (int(end_hour) - int(start_hour)) * 4  # 4 slots in each hour

        # adjust nr of slots according to minutes in provided times.
        # e.g. 9:30 to 10:45 - we have 10-9=1 hour, which is 4 time slots,
        # but we need to subtract 2 time slots, because we don't have 9:00 to 10:00,
        # but 9:30 to 10:00 so we subtract 30/15=2 timeslots and add what is left
        # from the incomplete hour of 10:45 time, which is 45/15 minutes = 3 slots
        minute_duration_slots = int(end_minutes) / 15 - int(start_minutes) / 15

        total_duration = hour_duration_slots + minute_duration_slots

        regular_expression = r'^[01]{%d}1{%d}' % (slots_before_needed_time, total_duration)

        return regular_expression

    #  Function to use to find who's available within a specific time slot
    #       DailySchedule.objects.filter(date=date, schedule__regex=r'<expression>')
