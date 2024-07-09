from django.db import models

# Create your models here.
from users.models import UserInfo
import jsonfield
# 学科表
class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    level = models.IntegerField()

    def __str__(self):
        return self.subject_name + self.level

# 试题表
class Question(models.Model):
    id = models.AutoField(primary_key=True)
    question_type = models.IntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.IntegerField()
    level = models.IntegerField()
    difficult = models.IntegerField()
    title = models.CharField(max_length=255)
    info_content = models.ForeignKey('TextContent', on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Question {self.id} - Subject: {self.subject.subject_name}"

# 考试表
class Exam(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    paper_type = models.IntegerField()
    grade_level = models.IntegerField()
    score = models.IntegerField()
    question_count = models.IntegerField()
    suggest_time = models.IntegerField()
    limit_start_time = models.DateTimeField(null=True, blank=True)
    limit_end_time = models.DateTimeField(null=True, blank=True)
    text_content = models.ForeignKey('TextContent', on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class ExamPaperAnswer(models.Model):
    id = models.AutoField(primary_key=True)
    exam_paper_id = models.IntegerField(verbose_name="试卷ID")
    paper_name = models.CharField(max_length=255, verbose_name="试卷名称")
    paper_type = models.IntegerField(verbose_name="试卷类型 (1. 固定试卷, 4. 时段试卷, 6. 任务试卷)")
    subject_id = models.IntegerField(verbose_name="学科")
    system_score = models.IntegerField(verbose_name="系统判定得分")
    user_score = models.IntegerField(verbose_name="最终得分 (千分制)")
    paper_score = models.IntegerField(verbose_name="试卷总分")
    question_correct = models.IntegerField(verbose_name="做对题目数量")
    question_count = models.IntegerField(verbose_name="题目总数量")
    do_time = models.IntegerField(verbose_name="做题时间 (秒)")
    status = models.IntegerField(verbose_name="试卷状态 (1. 待判分, 2. 完成)")
    create_user = models.IntegerField(verbose_name="学生")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="提交时间")

    class Meta:
        db_table = 't_exam_paper_answer'
        verbose_name = '试卷答案'
        verbose_name_plural = '试卷答案'

    def __str__(self):
        return self.paper_name

class ExamPaperQuestionCustomerAnswer(models.Model):
    id = models.AutoField(primary_key=True)
    question_id = models.IntegerField(verbose_name="题目ID")
    exam_paper_id = models.IntegerField(verbose_name="答案ID")
    exam_paper_answer_id = models.IntegerField(verbose_name="试卷答案ID")
    question_type = models.IntegerField(verbose_name="题型")
    subject_id = models.IntegerField(verbose_name="学科")
    customer_score = models.IntegerField(verbose_name="得分")
    question_score = models.IntegerField(verbose_name="题目原始分数")
    question_text_content_id = models.IntegerField(verbose_name="问题内容")
    answer = models.CharField(max_length=255, verbose_name="做题答案")
    text_content_id = models.IntegerField(verbose_name="做题内容")
    do_right = models.BooleanField(verbose_name="是否正确")
    create_user = models.IntegerField(verbose_name="做题人")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    item_order = models.IntegerField(verbose_name="题目顺序")

    class Meta:
        db_table = 't_exam_paper_question_customer_answer'
        verbose_name = '试卷题目答案'
        verbose_name_plural = '试卷题目答案'

    def __str__(self):
        return f"Question {self.question_id} Answer by User {self.create_user}"

# 文本表
class TextContent(models.Model):
    id = models.AutoField(primary_key=True)
    content = jsonfield.JSONField()
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"TextContent {self.id}"


# 试卷答案表
class ExamPaperAnswer(models.Model):
    id = models.AutoField(primary_key=True)
    exam_paper = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name="试卷")
    paper_name = models.CharField(max_length=255, verbose_name="试卷名称")
    paper_type = models.IntegerField(verbose_name="试卷类型 (1. 固定试卷, 4. 时段试卷, 6. 任务试卷)")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="学科")
    system_score = models.IntegerField(verbose_name="系统判定得分")
    user_score = models.IntegerField(verbose_name="最终得分 (千分制)")
    paper_score = models.IntegerField(verbose_name="试卷总分")
    question_correct = models.IntegerField(verbose_name="做对题目数量")
    question_count = models.IntegerField(verbose_name="题目总数量")
    do_time = models.IntegerField(verbose_name="做题时间 (秒)")
    status = models.IntegerField(verbose_name="试卷状态 (1. 待判分, 2. 完成)")
    create_user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="学生")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="提交时间")

    class Meta:
        db_table = 't_exam_paper_answer'
        verbose_name = '试卷答案'
        verbose_name_plural = '试卷答案'

    def __str__(self):
        return self.paper_name

# 试卷题目答案表
class ExamPaperQuestionCustomerAnswer(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="题目")
    exam_paper = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name="试卷")
    exam_paper_answer = models.ForeignKey(ExamPaperAnswer, on_delete=models.CASCADE, verbose_name="试卷答案")
    question_type = models.IntegerField(verbose_name="题型")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="学科")
    customer_score = models.IntegerField(verbose_name="得分")
    question_score = models.IntegerField(verbose_name="题目原始分数")
    question_text_content = models.ForeignKey(TextContent, on_delete=models.CASCADE, related_name="question_text_content", verbose_name="问题内容")
    answer = models.CharField(max_length=255, verbose_name="做题答案")
    text_content = models.ForeignKey(TextContent, on_delete=models.CASCADE, related_name="answer_text_content", verbose_name="做题内容")
    do_right = models.BooleanField(verbose_name="是否正确")
    create_user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="做题人")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    item_order = models.IntegerField(verbose_name="题目顺序")

    class Meta:
        db_table = 't_exam_paper_question_customer_answer'
        verbose_name = '试卷题目答案'
        verbose_name_plural = '试卷题目答案'

    def __str__(self):
        return f"Question {self.question.id} Answer by User {self.create_user.username}"


# 用户日志表
class UserLog(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log for {self.user.username} at {self.create_time}"