from django.core.paginator import Paginator
from django.shortcuts import render
from django.utils.dateparse import parse_datetime

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
import json
from .models import Subject, Question, TextContent, Exam
from django.http import JsonResponse
from users.views import getCurrentUser
from .serializers import QuestionSerializer

# def getCurrentUser():
#     return UserViewSet.getCurrentUser()
def getLevelName(i):
    level_enum = {1 : '初级', 2 : '中级', 3 : '高级'}
    return level_enum[i]
class SubjectViewSet(viewsets.ViewSet):
    def list(self, request):
        subjects = Subject.objects.all()
        subject_list = [{
            'id': subject.id,
            'name': subject.subject_name,
            'level': subject.level,
            'levelName': getLevelName(subject.level),  # 假设你有一个 get_level_display 方法
        } for subject in subjects]
        return JsonResponse({'code': 1, 'message': '查询成功', 'response': subject_list})

    def page(self, request):
        if request.method == 'POST':
            # Extract data from the request (similar to @RequestBody in Java)
            data = json.loads(request.body)
            page_index = data.get('pageIndex', 1)
            page_size = data.get('pageSize', 10)
            level = data.get('level')

            subjects = Subject.objects.all().order_by('-id')
            if level:
                subjects = subjects.filter(level=level)

            # Paginate the results
            paginator = Paginator(subjects, page_size)
            paginated_subjects = paginator.page(page_index)

            # Convert to desired format
            subject_list = [{
                'id': subject.id,
                'name': subject.subject_name,
                'level': subject.level,
                'levelName': getLevelName(subject.level),  # 假设你有一个 get_level_display 方法
            } for subject in paginated_subjects]
            return JsonResponse({
                'errno': 100000,
                'msg': '容器查询成功',
                'response': {
                    'list': subject_list,
                    'total': paginator.count,
                    'pageNum': page_index,
                    'pageSize': page_size
                }
            }, json_dumps_params={'ensure_ascii': False})


    def edit(self, request):
        if request.method == 'POST':
            data = json.loads(request.body)
            subject_id = data.get('id')
            if not subject_id:
                name = data.get('name')
                level = data.get('level')
                subject = Subject(subject_name=name, level=level)
                subject.save()
                return JsonResponse({'code': 1, 'message': '学科添加成功'})
            try:
                subject = Subject.objects.get(id=subject_id)
                subject.subject_name = data.get('name', subject.subject_name)
                subject.level = data.get('level', subject.level)
                subject.save()
                return JsonResponse({'code': 1, 'message': '学科编辑成功'})
            except Subject.DoesNotExist:
                return JsonResponse({'code': 0, 'message': '学科不存在'}, status=404)

    def select(self, request, pk):
        if request.method == 'POST':
            try:
                subject = Subject.objects.get(id=pk)
                subject_data = {
                    'id': subject.id,
                    'name': subject.subject_name,
                    'level': subject.level,
                    'levelName': getLevelName(subject.level),
                }
                return JsonResponse({'response': subject_data})
            except Subject.DoesNotExist:
                return JsonResponse({'code': 0, 'message': '学科不存在'}, status=404)

    def delete(self, request, pk):
        if request.method == 'POST':
            try:
                subject = Subject.objects.get(id=pk)
                subject.delete()
                return JsonResponse({'code': 1, 'message': '学科删除成功'})
            except Subject.DoesNotExist:
                return JsonResponse({'code': 0, 'message': '学科不存在'}, status=404)

class QuestionViewSet(viewsets.ViewSet):

    def page(self, request):
        if request.method == 'POST':
            data = json.loads(request.body)
            page_index = data.get('pageIndex', 1)
            page_size = data.get('pageSize', 10)
            level = data.get('level')
            subject_id = data.get('subjectId')
            question_type = data.get('questionType')
            questions = Question.objects.all().order_by('-id')

            if level:
                questions = questions.filter(level=level)
            if subject_id:
                subject = Subject.objects.get(id=subject_id)
                questions = questions.filter(subject=subject)
            if question_type:
                questions = questions.filter(question_type=question_type)

            paginator = Paginator(questions, page_size)
            paginated_questions = paginator.page(page_index)

            question_list = [{
                'id': question.id,
                'subjectId': question.subject.id,
                'questionType': question.question_type,
                'shortTitle': "待完成题目缩写",
                'score': question.score,
                'difficult': question.difficult,
                'createTime': question.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            } for question in paginated_questions]
            return JsonResponse({
                'errno': 100000,
                'msg': '题目查询成功',
                'response': {
                    'list': question_list,
                    'total': paginator.count,
                    'pageNum': page_index,
                    'pageSize': page_size
                }
            }, json_dumps_params={'ensure_ascii': False})

    def create(self, data):
        info_content = TextContent.objects.create(content={
                    "items": data.get("items"),
                    "analyze": data.get("analyze"),
                    "correct": data.get("correct")
                })
        question_data = Question.objects.create(
            question_type=data.get("questionType"),
            level=data.get("gradeLevel"),
            subject=Subject.objects.get(id=data.get("subjectId")),
            title=data.get("title"),
            info_content=info_content,
            score=data.get("score"),
            difficult=data.get("difficult"))
        return JsonResponse({'code': 1, 'message': '试题添加成功'})

    def update(self, data):
        question = Question.objects.get(id=data.get("id"))
        question.info_content.content={
                    "items": data.get("items"),
                    "analyze": data.get("analyze"),
                    "correct": data.get("correct")
            }
        question.info_content.save()
        question.question_type=data.get("questionType")
        question.level=data.get("gradeLevel")
        question.subject=Subject.objects.get(id=data.get("subjectId"))
        question.title=data.get("title")
        question.score=data.get("score")
        question.difficult=data.get("difficult")
        question.save()
        return JsonResponse({'code': 1, 'message': '试题修改成功'})

    def edit(self, request):
        data=request.data
        if data.get("id"):
            return self.update(data)
        else:
            return self.create(data)

    def select(self, request, pk):
        if request.method == 'POST':
            try:
                question = Question.objects.get(id=pk)
                question_data = {
                    'id': question.id,
                    'questionType': question.question_type,
                    'gradeLevel': question.level,
                    'subjectId': question.subject.id,
                    'title': question.title,
                    'items': question.info_content.content['items'],
                    'analyze': question.info_content.content['analyze'],
                    'correct': question.info_content.content['correct'],
                    'score': question.score,
                    'difficult': question.difficult
                }
                return JsonResponse({'response': question_data})
            except Question.DoesNotExist:
                return JsonResponse({'code': 0, 'message': '题目不存在'}, status=404)

    def delete(self, request, pk):
        if request.method == 'POST':
            try:
                question = Question.objects.get(id=pk)
                question.delete()
                return JsonResponse({'code': 1, 'message': '题目删除成功'})
            except Question.DoesNotExist:
                return JsonResponse({'code': 0, 'message': '题目不存在'}, status=404)


class ExamViewSet(viewsets.ViewSet):
    def page(self, request):

        if request.method == 'POST':
            data = json.loads(request.body)
            page_index = data.get('pageIndex', 1)
            page_size = data.get('pageSize', 10)
            level = data.get('level')
            subject_id = data.get('subjectId')
            exams = Exam.objects.all().order_by('-id')

            if level:
                exams = exams.filter(grade_level=level)
            if subject_id:
                subject = Subject.objects.get(id=subject_id)
                exams = exams.filter(subject=subject)

            paginator = Paginator(exams, page_size)
            paginated_exams = paginator.page(page_index)

            exam_list = [{
                'id': exam.id,
                'subjectId': exam.subject.id,
                'name': exam.name,
                'createTime': exam.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            } for exam in paginated_exams]
            return JsonResponse({
                'errno': 100000,
                'msg': '考试查询成功',
                'response': {
                    'list': exam_list,
                    'total': paginator.count,
                    'pageNum': page_index,
                    'pageSize': page_size
                }
            }, json_dumps_params={'ensure_ascii': False})

    def getTotalScore(self, content):
        total_score = 0
        for title_item in content:
            for question in title_item['questionItems']:
                total_score += question['score']
        return total_score

    def getQuestionCount(self, content):
        count = 0
        for title_item in content:
            for question in title_item['questionItems']:
                count += 1
        return count

    def create(self, data):
        content = data.get("titleItems")
        info_content = TextContent.objects.create(content=content)
        limit_date_time = data.get('limitDateTime', [])
        exam_data = Exam.objects.create(
            name = data.get("name"),
            subject = Subject.objects.get(id=data.get("subjectId")),
            paper_type = data.get("paperType"),
            grade_level = data.get("level"),
            score = self.getTotalScore(content),
            question_count = self.getQuestionCount(content),
            suggest_time = data.get("suggestTime"),
            limit_start_time = parse_datetime(limit_date_time[0]),
            limit_end_time = parse_datetime(limit_date_time[1]),
            text_content = info_content)
        return JsonResponse({'code': 1, 'message': '考试添加成功'})

    def update(self, data):
        exam = Exam.objects.get(id=data.get("id"))
        content = exam.text_content
        content.content=data.get("titleItems")
        limit_date_time = data.get('limitDateTime')

        exam.name=data.get("name")
        exam.subject=Subject.objects.get(id=data.get("subjectId"))
        exam.paper_type = data.get("paperType")
        exam.grade_level = data.get("level")
        exam.score = self.getTotalScore(content.content)
        exam.question_count = self.getQuestionCount(content.content)
        exam.suggest_time = data.get("suggestTime")
        exam.limit_start_time = parse_datetime(limit_date_time[0])
        exam.limit_end_time = parse_datetime(limit_date_time[1])
        exam.save()
        return JsonResponse({'code': 1, 'message': '考试修改成功'})

    def edit(self, request):
        data = request.data
        if data.get("id"):
            return self.update(data)
        else:
            return self.create(data)


    def select(self, request, pk):
        if request.method == 'POST':
            try:
                exam = Exam.objec
                exam_data = {
                    'id': exam.id,
                    'level': exam.grade_level,
                    'subjectId': exam.subject.id,
                    'paperType': exam.paper_type,
                    'limitDateTime': [exam.limit_start_time.strftime('%Y-%m-%d %H:%M:%S') if exam.limit_start_time else None
                        , exam.limit_end_time.strftime('%Y-%m-%d %H:%M:%S') if exam.limit_start_time else None],
                    'name': exam.name,
                    'suggestTime': exam.suggest_time,
                    'titleItems': exam.text_content.content
                }
                return JsonResponse({'response': exam_data})
            except Exam.DoesNotExist:
                return JsonResponse({'code': 0, 'message': '题目不存在'}, status=404)

    def delete(self, request, pk):
        if request.method == 'POST':
            try:
                exam = Exam.objects.get(id=pk)
                exam.delete()
                return JsonResponse({'code': 1, 'message': '考试删除成功'})
            except Exam.DoesNotExist:
                return JsonResponse({'code': 0, 'message': '考试不存在'}, status=404)

class DashBoardViewSet(viewsets.ViewSet):
    def index(self, request):
        exams = Exam.objects.all()
        level = getCurrentUser().level
        if level:
            exams = exams.filter(grade_level=level)
        paginator = Paginator(exams, 10)
        paginated_exams = paginator.page(1)
        data_list = [{
            'name': exam.id,
            'startTime': exam.limit_start_time,
            'endTime': exam.limit_end_time
        } for exam in paginated_exams]
        return JsonResponse({
            'errno': 100000,
            'msg': '考试查询成功',
            'response': {
                'timeLimitPaper': data_list,
                'fixedPaper': [],
                'pushPaper': []
            }
        }, json_dumps_params={'ensure_ascii': False})

# class PaperViewSet(viewsets.Viewset):
#     def