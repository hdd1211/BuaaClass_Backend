import datetime

from django.db import models
from django.contrib.postgres.fields import ArrayField


class Admin(models.Model):
    id = models.IntegerField(verbose_name='管理员ID', auto_created=True, primary_key=True)
    username = models.CharField(verbose_name='管理员名', unique=True, null=False, max_length=20)
    password = models.CharField(verbose_name='管理员密码', null=False, max_length=20)


class User(models.Model):
    id = models.IntegerField(verbose_name='用户ID', auto_created=True, primary_key=True)
    name = models.CharField(verbose_name='用户ID', max_length=20, null=False)
    password = models.CharField(verbose_name='密码', max_length=20, null=False)
    agree_reviews = ArrayField(models.IntegerField(verbose_name='点赞ID列表'))
    disagree_reviews = ArrayField(models.IntegerField(verbose_name='点踩ID列表'))
    reviews = ArrayField(models.IntegerField(verbose_name='评价ID列表'))

    # time = models.DateTimeField(verbose_name='账号创建时间', auto_now_add=datetime.datetime.now())

    # user_photo = models.ImageField(verbose_name='用户头像')


class Course(models.Model):
    id = models.IntegerField(verbose_name='课程ID', primary_key=True, unique=True, auto_created=True)
    name = models.CharField(verbose_name='课程名', max_length=20, null=False, unique=True)
    department = models.CharField(verbose_name='开课学院/单位', max_length=50)
    credit = models.IntegerField(verbose_name='学分数')
    semester = ArrayField(models.IntegerField(verbose_name='课程学期', null=False, unique=True))

    rating_total = models.IntegerField(verbose_name='评分平均值', null=False, unique=True)
    rating_quality = models.IntegerField(verbose_name='内容评分平均值', null=False, unique=True)
    rating_workload = models.IntegerField(verbose_name='工作量评分平均值', null=False, unique=True)
    rating_appraisal = models.IntegerField(verbose_name='考核评分平均值', null=False, unique=True)

    review_ids = ArrayField(models.IntegerField(verbose_name=''))

    teacher_name = models.CharField(verbose_name='教师名', max_length=20, null=False, unique=True)
    Introduction = models.CharField(verbose_name='教师简介', null=False, unique=True, max_length=200)

    evaluation_i = models.ManyToManyField('Evaluation', related_name='course_evaluations')
    teacher_i = models.ManyToManyField('Teacher', related_name='teacher_evaluations')


class Evaluation(models.Model):
    id = models.IntegerField(verbose_name='评价ID', primary_key=True, auto_created=True, db_index=True)
    user_id = models.IntegerField(verbose_name='评价用户ID', db_index=True)
    time = models.DateTimeField(verbose_name='评价生成时间', auto_now_add=datetime.datetime.now())
    agree_cnt = models.IntegerField(verbose_name='赞数')
    disagree_cnt = models.IntegerField(verbose_name='踩数')
    smester = models.CharField(verbose_name='学期', max_length=20)
    rating_total = models.IntegerField(verbose_name='总评分')
    rating_quality = models.IntegerField(verbose_name='内容质量评分')
    rating_workload = models.IntegerField(verbose_name='工作量评分')
    rating_assesment = models.IntegerField(verbose_name='考核给分评分')
    title = models.CharField(verbose_name='标题', max_length=20)
    text = models.CharField(verbose_name='评论内容', max_length=500)

    course_i = models.ManyToManyField('Course', through='EvaluationCourse')

    def get_agree_cnt(self):
        return self.agree_cnt


class EvaluationCourse(models.Model):
    Evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    Course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Teacher(models.Model):
    id = models.IntegerField(verbose_name='教师ID', primary_key=True, auto_created=True, db_index=True)
    name = models.CharField(verbose_name='教师名', max_length=20)
    course_i = models.ManyToManyField('Course', through='TeacherCourse')


class TeacherCourse(models.Model):
    teacher = models.ForeignKey('teacher', on_delete=models.CASCADE)
    course = models.ForeignKey('course', on_delete=models.CASCADE)


class Report(models.Model):
    id = models.IntegerField(verbose_name='举报ID', primary_key=True)
    userid = models.IntegerField(verbose_name='用户ID')
    # index = models.index()
    content = models.CharField(verbose_name='反馈内容', max_length=200)

    class Meta:
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['userid']),
        ]


class Announcement(models.Model):
    id = models.IntegerField(verbose_name='公告ID', primary_key=True, db_index=True)
    text = models.CharField(verbose_name='文本', max_length=200)
    time = models.DateTimeField(verbose_name='公告创建时间', auto_now_add=True)
