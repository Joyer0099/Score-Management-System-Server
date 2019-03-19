#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is for the operation of t_College table.

Here are operations:
get_college_list: GET    http://localhost:8000/api/v1/college/display
           query: GET    http://localhost:8000/api/v1/college/format
          insert: POST   http://localhost:8000/api/v1/college/format
          update: PUT    http://localhost:8000/api/v1/college/format
          remove: DELETE http://localhost:8000/api/v1/college/format
"""
from apps.MarkManagement.view.common import *

class CollegeViewSet(viewsets.ViewSet):

    def get_college_list(self, request):
        """
        Get t_College table list
        :param request: the request from browser.
        :return: JSON response.
        """
        access_token = request.META.get("HTTP_TOKEN")

        if not token_verify(access_token):
            return token_invalid()
        id = request.GET.get('id')
        name = request.GET.get('name')
        university_id = request.GET.get('university_id')
        if id is None and name is None and university_id is None:
            return parameter_missed()
        college_set = College.objects.all()
        if university_id is None:
            if id is not None:
                college_set = college_set.filter(id=id)
            if name is not None:
                college_set = college_set.filter(name__contains=name)
        else:
            college_set = college_set.filter(university_id=university_id)
        # 对象取字典
        #college_set = college_set.values()
        result = []
        for college in college_set:
            collegeDict = model_to_dict(college)
            collegeDict['university_id'] = collegeDict['university']
            del collegeDict['university']
            collegeDict['university_message'] = model_to_dict(college.university)
            result.append(collegeDict)
        if len(result) == 0:
            return parameter_missed()
        code_number = '2000'
        result = {
            'code': code_number,
            'message': status_code[code_number],
            'subjects': result,
            'count': len(result),
        }

        return JsonResponse(result, safe=False)

    def query(self, request):
        """
        Query t_College table
        :param request: the request from browser.
        :return: JSON response.
        """
        access_token = request.META.get("HTTP_TOKEN")

        if not token_verify(access_token):
            return token_invalid()
        id = request.GET.get('id')
        name = request.GET.get('name')
        university_id = request.GET.get('university_id')
        if id is None and name is None and university_id is None:
            return parameter_missed()
        college_set = College.objects.all()
        if university_id is None:
            if id is not None:
                college_set = college_set.filter(id=id)
            if name is not None:
                college_set = college_set.filter(name__contains=name)
        else:
            college_set = college_set.filter(university_id=university_id)
        # 对象取字典
        college_set = college_set.values()
        result = []
        for college in college_set:
            result.append(college)
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
        Insert t_College table
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
            shortname = subjectDict.get('shortname')
            university_id = subjectDict.get('university_id')
            if name is None or university_id is None:
                continue
            college = College()
            if name:
                college.name = name
            if shortname:
                college.shortname = shortname
            if university_id:
                university_set = University.objects.filter(id=university_id)
                if university_set.count() == 0:
                    continue
                college.university = university_set[0]
            try:
                college.save()
            except Exception as e:
                continue
            else:
                ids.append({'id':college.id})
                tag = True

        if tag:
            return JsonResponse({'subjects': ids, 'code': '2001', 'message': status_code['2001']}, safe=False)
        else:
            return insert_failed()

    def update(self, request):
        """
        Update t_College table
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
            shortname = subjectDict.get('shortname')
            university_id = subjectDict.get('university_id')

            college_set = College.objects.filter(id=id)
            for college in college_set:
                if name:
                    college.name = name
                if shortname:
                    college.shortname = shortname
                if university_id:
                    university_set = University.objects.filter(id=university_id)
                    if university_set.exists() == False:
                        continue
                    college.university = university_set[0]
                try:
                    college.save()
                except Exception as e:
                    continue
                else:
                    ids.append({'id': college.id})
                    tag = True
        if tag:
            return JsonResponse({'subjects': ids, 'code': '2005', 'message': status_code['2005']}, safe=False)
        else:
            return update_failed()

    def remove(self, request):
        """
        Remove t_College table
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
            college_set = College.objects.filter(id=id)
            if college_set.exists() == False:
                continue
            try:
                college_set.delete()
            except Exception as e:
                continue
            else:
                tag = True

        if tag:
            return delete_succeed()
        else:
            return delete_failed()
