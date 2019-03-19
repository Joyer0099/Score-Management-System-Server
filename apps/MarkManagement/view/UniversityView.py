#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is for the operation of t_University table.

Here are operations:
 query: GET    http://localhost:8000/api/v1/university/format
insert: POST   http://localhost:8000/api/v1/university/format
update: PUT    http://localhost:8000/api/v1/university/format
remove: DELETE http://localhost:8000/api/v1/university/format
"""

from apps.MarkManagement.view.common import *

class UniversityViewSet(viewsets.ViewSet):

    def query(self, request):
        """
        Query t_University table
        :param request: the request from browser.
        :return: JSON response.
        """
        access_token = request.META.get("HTTP_TOKEN")

        # 验证token正确性
        if not token_verify(access_token):
            return token_invalid()
        id = request.GET.get('id')
        name = request.GET.get('name')
        shortname = request.GET.get('shortname')

        # 处理所有参数为空的情况
        if id is None and name is None and shortname is None:
            return parameter_missed()

        university_set = University.objects.all()

        # 根据参数过滤
        if id is not None:
            university_set = university_set.filter(id=id)
        if name is not None:
            university_set = university_set.filter(name=name)
        if shortname:
            university_set = university_set.filter(shortname=shortname)

        # 对象取字典数组
        university_set = university_set.values()

        # 结果集
        result = []

        # 遍历数组字典
        for university in university_set:
            result.append(university)
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
        Insert t_University table
        :param request: the request from browser.
        :return: JSON response.
        """
        post_data = request.data
        access_token = request.META.get("HTTP_TOKEN")
        if not token_verify(access_token):
            return token_invalid()
        subjects = post_data.get('subjects')
        if subjects is None:
            return parameter_missed()

        # 请求标记
        tag = False
        ids = []

        # 遍历请求体数组参数
        for subjectDict in subjects:
            name = subjectDict.get('name')
            shortname = subjectDict.get('shortname')
            if name is None:
                continue
            university = University()
            if name:
                university.name = name
            if shortname:
                university.shortname = shortname
            try:
                university.save()
                ids.append({'id': university.id})
                tag = True
            except Exception as e:
                continue

        if tag:
            return JsonResponse({'subjects':ids, 'code': '2001', 'message': status_code['2001']}, safe=False)
        else:
            return insert_failed()

    def update(self, request):
        """
        Update t_University table
        :param request: the request from browser.
        :return: JSON response.
        """
        # 解析json请求体
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
            shortname = subjectDict.get('shortname')
            university_set = University.objects.filter(id=id)
            for university in university_set:
                if name:
                    university.name = name
                if shortname:
                    university.shortname = shortname
                try:
                    university.save()
                except Exception as e:
                    continue
                else:
                    ids.append({'id': university.id})
                    tag = True
        if tag:
            return JsonResponse({'subjects':ids, 'code': '2005', 'message': status_code['2005']}, safe=False)
        else:
            return update_failed()

    def remove(self, request):
        """
        Remove t_University table
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
            if id is None:
                continue
            university_set = University.objects.filter(id=id)
            if not university_set.exists():
                continue
            try:
                university_set.delete()
            except Exception as e:
                continue
            else:
                tag = True

        if tag:
            return delete_succeed()
        else:
            return delete_failed()

