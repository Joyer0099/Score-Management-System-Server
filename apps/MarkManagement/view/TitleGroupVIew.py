#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is for the operation of t_TitleGroup table.

Here are operations:
 query: GET    http://localhost:8000/api/v1/titleGroup/format
insert: POST   http://localhost:8000/api/v1/titleGroup/format
update: PUT    http://localhost:8000/api/v1/titleGroup/format
remove: DELETE http://localhost:8000/api/v1/titleGroup/format
"""
from apps.MarkManagement.view.common import *

class TitleGroupViewSet(viewsets.ViewSet):

    def query(self, request):
        """
        Query t_TitleGroup table
        :param request: the request from browser.
        :return: JSON response.
        """
        access_token = request.META.get("HTTP_TOKEN")

        if not token_verify(access_token):
            return token_invalid()
        id = request.GET.get('id')
        name = request.GET.get('name')
        lesson_id = request.GET.get('lesson_id')
        weight = request.GET.get('weight')
        if id is None and name is None and lesson_id is None and weight is None:
            return parameter_missed()
        titleGroup_set = TitleGroup.objects.all()
        if id is not None:
            titleGroup_set = titleGroup_set.filter(id=id)
        if name is not None:
            titleGroup_set = titleGroup_set.filter(name=name)
        if lesson_id is not None:
            titleGroup_set = titleGroup_set.filter(lesson_id=lesson_id)
        if weight is not None:
            titleGroup_set = titleGroup_set.filter(weight=weight)
        # 对象取字典
        titleGroup_set = titleGroup_set.values()
        result = []
        for titleGroup in titleGroup_set:
            result.append(titleGroup)
        if len(result) == 0:
            return query_failed()
        code_number = '2000'
        result = {
            'code': code_number,
            'message': status_code[code_number],
            'subjects': result,
            'count': len(result),
        }
        return JsonResponse(result, safe=False)

    def insert(self, request):
        """
        Insert t_TitleGroup table
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
            weight = subjectDict.get('weight')
            lesson_id = subjectDict.get('lesson_id')
            if name is None or lesson_id is None:
                continue
            titleGroup = TitleGroup()
            if name:
                titleGroup.name = name
            if weight:
                titleGroup.weight = weight
            if lesson_id:
                lesson_set = Lesson.objects.filter(id=lesson_id)
                if not lesson_set.exists():
                    continue
                titleGroup.lesson = lesson_set[0]
            try:
                titleGroup.save()
            except Exception as e:
                continue
            else:
                ids.append({'id': titleGroup.id})
                tag = True
        if tag:
            return JsonResponse({'subjects':ids, 'code': '2001', 'message': status_code['2001']}, safe=False)
        else:
            return insert_failed()

    def update(self, request):
        """
        Update t_TitleGroup table
        :param request: the request from browser.
        :return: JSON response.
        """
        put_data = request.data
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
            weight = subjectDict.get('weight')
            lesson_id = subjectDict.get('lesson_id')
            titleGroup_set = TitleGroup.objects.filter(id=id)
            for titleGroup in titleGroup_set:
                if name:
                    titleGroup.name = name
                if weight:
                    titleGroup.weight = weight
                if lesson_id:
                    lesson_set = Lesson.objects.filter(id=lesson_id)
                    if not lesson_set.exists():
                        continue
                    titleGroup.lesson = lesson_set[0]
                try:
                    titleGroup.save()
                except Exception as e:
                    continue
                else:
                    ids.append({'id': titleGroup.id})
                    tag = True
        if tag:
            return JsonResponse({'subjects':ids, 'code': '2005', 'message': status_code['2005']}, safe=False)
        else:
            return update_failed()

    def remove(self, request):
        """
        Remove t_TitleGroup table
        :param request: the request from browser.
        :return: JSON response.
        """
        delete_data = request.data
        access_token = request.META.get("HTTP_TOKEN")

        if not token_verify(access_token):
            return token_invalid()
        subjects = delete_data.get('subjects')
        if subjects is None:
            return JsonResponse({'code': '4032', 'message': status_code['4032']}, safe=False)
        tag = False
        for subjectDict in subjects:
            id = subjectDict.get('id')
            if id is None:
                continue
            titleGroup_set = TitleGroup.objects.filter(id=id)
            if not titleGroup_set.exists():
                continue
            try:
                titleGroup_set.delete()
            except Exception as e:
                continue
            else:
                tag = True

        if tag:
            return delete_succeed()
        else:
            return delete_failed()
