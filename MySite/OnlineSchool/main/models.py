from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Courses(models.Model):
    id_course = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=100, blank=True, null=True)
    language_programming = models.CharField(max_length=50, blank=True, null=True)
    dfficulty_level = models.IntegerField(blank=True, null=True)
    id_teacher = models.ForeignKey('Teachers', models.DO_NOTHING, db_column='id_teacher', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    duraction = models.IntegerField(blank=True, null=True, help_text='Длительность курса в месяцах')
    price = models.IntegerField(blank=True, null=True)
    status = models.BooleanField(default=True)
    class Meta:
        managed = True
        db_table = 'courses'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class GradeTeacher(models.Model):
    gradeteacherid = models.AutoField(primary_key=True)
    studentid = models.ForeignKey('Students', models.DO_NOTHING, db_column='studentid', blank=True, null=True)
    teacherid = models.ForeignKey('Teachers', models.DO_NOTHING, db_column='teacherid', blank=True, null=True)
    grade = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'grade_teacher'


class Lessons(models.Model):
    id_lesson = models.AutoField(primary_key=True)
    topic = models.CharField(max_length=255, blank=True, null=True)
    video_url = models.CharField(max_length=255, blank=True, null=True)
    id_course = models.ForeignKey(Courses, models.DO_NOTHING, db_column='id_course', blank=True, null=True)
    lesson_number = models.IntegerField(blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'lessons'


class RecordsStudents(models.Model):
    id_records_students = models.AutoField(primary_key=True)
    id_student = models.ForeignKey('Students', models.DO_NOTHING, db_column='id_student', blank=True, null=True)
    id_course = models.ForeignKey(Courses, models.DO_NOTHING, db_column='id_course', blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'records_students'


class RecordsTeachers(models.Model):
    id_record_teacher = models.AutoField(primary_key=True)
    id_teacher = models.ForeignKey('Teachers', models.DO_NOTHING, db_column='id_teacher', blank=True, null=True)
    id_course = models.ForeignKey(Courses, models.DO_NOTHING, db_column='id_course', blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'records_teachers'


class Students(models.Model):
    id_student = models.AutoField(primary_key=True)
    is_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='is_user', blank=True, null=True)
    count_course = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'students'


class TaskExecution(models.Model):
    id_task_execution = models.AutoField(primary_key=True)
    execution = models.TextField(blank=True, null=True)
    id_teacher = models.ForeignKey('Teachers', models.DO_NOTHING, db_column='id_teacher', blank=True, null=True)
    id_student = models.ForeignKey(Students, models.DO_NOTHING, db_column='id_student', blank=True, null=True)
    id_task = models.ForeignKey('Tasks', models.DO_NOTHING, db_column='id_task', blank=True, null=True)
    grade = models.IntegerField(blank=True, null=True)
    comment_teacher = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'task_execution'


class Tasks(models.Model):
    id_task = models.AutoField(primary_key=True)
    topic = models.CharField(max_length=255, blank=True, null=True)
    content_task = models.TextField(blank=True, null=True)
    id_lesson = models.ForeignKey(Lessons, models.DO_NOTHING, db_column='id_lesson', blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tasks'


class Teachers(models.Model):
    id_teacher = models.AutoField(primary_key=True)
    id_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='id_user', blank=True, null=True)
    experience = models.IntegerField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'teachers'


class Users(models.Model):
    id_user = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    number_phone = models.CharField(max_length=11, blank=True, null=True)
    role = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True, unique=True)
    patronymic = models.CharField(max_length=50, blank=True, null=True)
    reset_token = models.CharField(max_length=100, blank=True, null=True)
    reset_token_created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'users'

    def clean(self):
        # Проверка email
        if self.email:
            validator = EmailValidator()
            try:
                validator(self.email)
            except ValidationError:
                raise ValidationError({'email': 'Введите корректный email адрес'})
            
            # Проверка на уникальность email
            if Users.objects.filter(email=self.email).exclude(id_user=self.id_user).exists():
                raise ValidationError({'email': 'Пользователь с таким email уже существует'})

    def check_password(self, raw_password):
        return raw_password == self.password

    
    def set_password(self, raw_password):
        """Устанавливает новый пароль"""
        self.password = raw_password
        self.save()

    def save(self, *args, **kwargs):
        self.clean()  # Выполняем валидацию перед сохранением
        super().save(*args, **kwargs)
