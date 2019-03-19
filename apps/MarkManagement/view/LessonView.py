#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is for the operation of t_Lesson table.

Here are operations:
 query: GET    http://localhost:8000/api/v1/table/lesson/format
insert: POST   http://localhost:8000/api/v1/table/lesson/format
update: PUT    http://localhost:8000/api/v1/table/lesson/format
remove: DELETE http://localhost:8000/api/v1/table/lesson/format
"""

from apps.MarkManagement.view.common import *

class LessonViewSet(viewsets.ViewSet):

    def query(self, request):
        """
        Query t_Lesson table
        :param request: the request from browser.
        :return: JSON response.
        """
        access_token = request.META.get("HTTP_TOKEN")

        if not token_verify(access_token):
            return token_invalid()
        id = request.GET.get('id')
        name = request.GET.get('name')
        college_id = request.GET.get('college_id')
        all = request.GET.get('all')
        if id is None and name is None and college_id is None and all is None:
            return parameter_missed()

        if all is None:
            all = False
        lesson_set = Lesson.objects.all()
        if all is False:
            if id is not None:
                lesson_set = lesson_set.filter(id=id)
            if name is not None:
                lesson_set = lesson_set.filter(name__contains=name)
            if college_id is not None:
                lesson_set = lesson_set.filter(college_id=college_id)
        # 对象取字典
        lesson_set = lesson_set.values()
        result = []
        for lesson in lesson_set:
            result.append(lesson)
        if len(result) == 0:
            return query_failed()
        code_number = '2000'
        result = {
            'code': code_number,
            'message': status_code[code_number],
            'subjects': result,
            'count': len(result),
            'all': all
        }

        return JsonResponse(result, safe=False)

    def insert(self, request):
        """
        Insert t_Lesson table
        :param request: the request from browser.
        :return: JSON response.
        """
        post_data =  request.data
        access_token = request.META.get("HTTP_TOKEN")
        if not token_verify(access_token):
            return token_invalid()
        subjects = post_data.get('subjects')
        if subjects is None:
            return parameter_missed()

        tag = False
        ids = []
        for subjectDict in subjects:
            name = subjectDict.get('name')
            college_id = subjectDict.get('college_id')
            if name is None or college_id is None:
                continue
            lesson = Lesson()
            if name:
                lesson.name = name
            if college_id:
                college_set = College.objects.filter(id=college_id)
                if college_set.exists() == False:
                    continue
                lesson.college = college_set[0]
            try:
                lesson.save()
            except Exception as e:
                continue
            else:
                ids.append({'id':lesson.id})
                tag = True

        if tag:
            return JsonResponse({'subjects':ids, 'code': '2001', 'message': status_code['2001']}, safe=False)
        else:
            return insert_failed()

    def update(self, request):
        """
        Update t_Lesson table
        :param request: the request from browser.
        :return: JSON response.
        """
        put_data =  request.data
        access_token = request.META.get("HTTP_TOKEN")
        if not token_verify(access_token):
            return token_invalid()
        subjects = put_data.get('subjects')
        if subjects is None:
            return parameter_missed()
        tag = False
        ids = []
        for subjectDict in subjects:
            id = subjectDict.get('id')
            name = subjectDict.get('name')
            college_id = subjectDict.get('college_id')
            lesson_set = Lesson.objects.filter(id=id)
            for lesson in lesson_set:
                if name:
                    lesson.name = name
                if college_id:
                    college_set = College.objects.filter(id=college_id)
                    if college_set.exists() == False:
                        continue
                    lesson.college = college_set[0]
                lesson.save()
                ids.append({'id':lesson.id})
                tag = True
        if tag:
            return JsonResponse({"subjects":ids, 'code': '2005', 'message': status_code['2005']}, safe=False)
        else:
            return update_failed()

    def remove(self, request):
        """
        Remove t_Lesson table
        :param request: the request from browser.
        :return: JSON response.
        """
        delete_data = request.data
        access_token = request.META.get("HTTP_TOKEN")

        if not token_verify(access_token):
            return token_invalid()
        subjects = delete_data.get('subjects')
        if subjects is None:
            return parameter_missed()
        tag = False
        for subjectDict in subjects:
            id = subjectDict.get('id')
            #name = subjectDict.get('name')
            #college_id = subjectDict.get('college_id')
            if id is None:
                continue
            lesson_set = Lesson.objects.filter(id=id)
            if not lesson_set.exists():
                continue
            try:
                lesson_set.delete()
            except Exception as e:
                continue
            else:
                tag = True
        if tag:
            return delete_succeed()
        else:
            return delete_failed()
