from django.urls import path, include
from .views import SubjectViewSet, QuestionViewSet, ExamViewSet, DashBoardViewSet

urlpatterns = [
    # List view
    path('admin/education/subject/list/', SubjectViewSet.as_view({'post': 'list'}), name='subject-list'),
    path('admin/education/subject/page/', SubjectViewSet.as_view({'post': 'page'}), name='subject-page'),
    path('admin/education/subject/edit/', SubjectViewSet.as_view({'post': 'edit'}), name='subject-edit'),
    path('admin/education/subject/select/<int:pk>', SubjectViewSet.as_view({'post': 'select'}),
         name='subject-select'),
    path('admin/education/subject/delete/<int:pk>', SubjectViewSet.as_view({'post': 'delete'}),
         name='subject-delete'),

    path('admin/question/page', QuestionViewSet.as_view({'post': 'page'}), name='subject-page'),
    path('admin/question/edit', QuestionViewSet.as_view({'post': 'edit'})),
    path('admin/question/select/<int:pk>', QuestionViewSet.as_view({'post': 'select'})),
    path('admin/question/delete/<int:pk>', QuestionViewSet.as_view({'post': 'delete'})),

    path('admin/exam/paper/page', ExamViewSet.as_view({'post': 'page'}), name='subject-page'),
    path('admin/exam/paper/edit', ExamViewSet.as_view({'post': 'edit'})),
    path('admin/exam/paper/select/<int:pk>', ExamViewSet.as_view({'post': 'select'})),
    path('admin/exam/paper/delete/<int:pk>', ExamViewSet.as_view({'post': 'delete'})),


    path('student/dashboard/index', DashBoardViewSet.as_view({'post': 'index'}))



]