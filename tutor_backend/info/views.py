from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from user.models import TeacherProfile
from info.serializers import TeacherListSerializer, TeacherDetailSerializer


@api_view(['GET'])
def teacher_list(request):
    """老师列表接口：支持按科目筛选、按教龄排序"""
    teachers = TeacherProfile.objects.filter(user__role='teacher')

    # 按科目筛选（前端传 ?subject=数学）
    subject = request.query_params.get('subject')
    if subject:
        teachers = teachers.filter(subject__contains=subject)

    # 按教龄排序（前端传 ?ordering=teaching_years 或 ?ordering=-teaching_years 表示倒序）
    ordering = request.query_params.get('ordering', '-teaching_years')
    teachers = teachers.order_by(ordering)

    serializer = TeacherListSerializer(teachers, many=True)
    return Response(
        {"message": "查询成功", "data": serializer.data},
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def teacher_detail(request, pk):
    """老师详情接口：根据ID查单个老师"""
    try:
        teacher = TeacherProfile.objects.get(pk=pk, user__role='teacher')
    except TeacherProfile.DoesNotExist:
        return Response(
            {"message": "老师不存在"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = TeacherDetailSerializer(teacher)
    return Response(
        {"message": "查询成功", "data": serializer.data},
        status=status.HTTP_200_OK
    )
