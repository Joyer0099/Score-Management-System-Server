#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is for the operation of t_Major table.

Here are operations:
 query: GET    http://localhost:8000/api/v1/major/format
insert: POST   http://localhost:8000/api/v1/major/format
update: PUT    http://localhost:8000/api/v1/major/format
remove: DELETE http://localhost:8000/api/v1/major/format
"""

from apps.MarkManagement.view.common import *

class MajorViewSet(viewsets.ViewSet):

    def query(self, request):
        """
        Query t_Major table
        :param request: the request from browser.
        :return: JSON response.
        """
        access_token = request.META.get("HTTP_TOKEN")

        if not token_verify(access_token):
            return token_invalid()
        id = request.GET.get('id')
        name = request.GET.get('name')
        college_id = request.GET.get('college_id')
        if id is None and name is None and college_id is None:
            return parameter_missed()
        major_set = Major.objects.all()
        if id:
            major_set = major_set.filter(id=id)
        if name:
            major_set = major_set.filter(name=name)
        if college_id:
            major_set = major_set.filter(college_id=college_id)
        # 对象取字典
        major_set = major_set.values()
        result = []
        for major in major_set:
            result.append(major)
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
        Insert t_Major table
        :param request: the request from browser.
        :return: JSON response."""
        post_data = request.data
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
            shortname = subjectDict.get('shortname')
            college_id = subjectDict.get('college_id')
            if name is None or college_id is None:
                continue
            major = Major()
            if name:
                major.name = name
            if shortname:
                major.shortname = shortname
            if college_id:
                college_set = College.objects.filter(id=college_id)
                if not college_set.exists():
                    continue
                major.college = college_set[0]
            try:
                major.save()
            except Exception as e:
                continue
            else:
                ids.append({'id':major.id})
                tag = True
        if tag:
            return JsonResponse({'subjects':ids, 'code': '2001', 'message': status_code['2001']}, safe=False)
        else:
            return insert_failed()

    def update(self, request):
        """
        Update t_Major table
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
            shortname = subjectDict.get('shortname')
            college_id = subjectDict.get('college_id')
            major_set = Major.objects.filter(id=id)
            for major in major_set:
                if name:
                    major.name = name
                if shortname:
                    major.shortname = shortname
                if college_id:
                    college_set = College.objects.filter(id=college_id)
                    if not college_set.exists():
                        continue
                    major.college = college_set[0]
                major.save()
                try:
                    major.save()
                except Exception as e:
                    continue
                else:
                    ids.append({'id': major.id})
                    tag = True
        if tag:
            return JsonResponse({'subjects': ids, 'code': '2005', 'message': status_code['2005']}, safe=False)
        else:
            return update_failed()

    def remove(self, request):
        """
        Remove t_Major table
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
            Major.objects.filter(id=id).delete()
            major_set = Major.objects.filter(id=id)
            if not major_set.exists():
                continue
            try:
                major_set.delete()
            except Exception as e:
                continue
            else:
                tag = True
        if tag:
            return delete_succeed()
        else:
            return delete_succeed()
