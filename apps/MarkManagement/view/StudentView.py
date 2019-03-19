#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is for the operation of t_Student table.

Here are operations:
get_student_list: GET    http://localhost:8000/api/v1/student/display
           query: GET    http://localhost:8000/api/v1/student/format
          insert: POST   http://localhost:8000/api/v1/student/format
          update: PUT    http://localhost:8000/api/v1/student/format
          remove: DELETE http://localhost:8000/api/v1/student/format
"""

from apps.MarkManagement.view.common import *

class StudentViewSet(viewsets.ViewSet):

    def get_student_list(self, request):
        """
        Get t_Student table list
        :param request: the request from browser.
        :return: JSON response.
        """
        access_token = request.META.get("HTTP_TOKEN")

        if not token_verify(access_token):
            return token_invalid()
        id = request.GET.get('id')
        sid = request.GET.get('sid')
        name = request.GET.get('name')
        major_id = request.GET.get('major_id')
        year = request.GET.get('year')
        classInfo_id = request.GET.get('classInfo_id')
        college_id = request.GET.get('college_id')
        result = []
        if classInfo_id is not None:
            student_set = Student.objects.filter(class__classInfo_id=classInfo_id)
            for student in student_set:
                student_dict = model_to_dict(student)
                student_dict['major_id'] = student_dict['major']
                del student_dict['major']

                major_dict = model_to_dict(student.major)
                major_dict['college_id'] = major_dict['college']
                del major_dict['college']

                student_dict['major_message'] = major_dict


                college_dict = model_to_dict(student.major.college)
                college_dict['university_id'] = college_dict['university']
                del college_dict['university']
                student_dict['college_message'] = college_dict
                result.append(student_dict)
        else:
            if id is None and sid is None and major_id is None and year is None and name is None and college_id is None:
                return parameter_missed()

            student_set = Student.objects.all()
            if id is not None:
                student_set = student_set.filter(id=id)
            if sid is not None:
                student_set = student_set.filter(sid=sid)
            if name is not None:
                student_set = student_set.filter(name=name)
            if major_id is not None:
                student_set = student_set.filter(major_id=major_id)
            if year is not None:
                student_set = student_set.filter(year=year)
            if college_id:
                student_set = student_set.filter(major__college__id=college_id)
            for student in student_set:
                student_dict = model_to_dict(student)
                student_dict['major_id'] = student_dict['major']
                del student_dict['major']

                major_dict = model_to_dict(student.major)
                major_dict['college_id'] = major_dict['college']
                del major_dict['college']
                student_dict['major_message'] = major_dict



                college_dict = model_to_dict(student.major.college)
                college_dict['university_id'] = college_dict['university']
                del college_dict['university']
                student_dict['college_message'] = college_dict

                result.append(student_dict)

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

    def query(self, request):
        """
        Query t_Student table
        :param request: the request from browser.
        :return: JSON response.
        """
        access_token = request.META.get("HTTP_TOKEN")

        if not token_verify(access_token):
            return token_invalid()
        id = request.GET.get('id')
        sid = request.GET.get('sid')
        name = request.GET.get('name')
        major_id = request.GET.get('major_id')
        year = request.GET.get('year')
        classInfo_id = request.GET.get('classInfo_id')
        college_id = request.GET.get('college_id')
        result = []
        if classInfo_id is not None:
            student_set = Student.objects.filter(class__classInfo_id=classInfo_id)
            student_set = student_set.values()
            for student in student_set:
                result.append(student)
        else:
            if id is None and sid is None and major_id is None and year is None and name is None and college_id is None:
                return parameter_missed()
            student_set = Student.objects.all()
            if id is not None:
                student_set = student_set.filter(id=id)
            if sid is not None:
                student_set = student_set.filter(sid=sid)
            if name is not None:
                student_set = student_set.filter(name=name)
            if major_id is not None:
                student_set = student_set.filter(major_id=major_id)
            if year is not None:
                student_set = student_set.filter(year=year)
            if college_id:
                student_set = student_set.filter(major__college__id=college_id)
            student_set = student_set.values()
            for student in student_set:
                result.append(student)

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
        Insert t_Student table
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
        tag = False
        succeed_ids = []
        failed_sids = []
        repeated_ids = []

        for subjectDict in subjects:

            sid = subjectDict.get('sid')
            name = subjectDict.get('name')
            major_id = subjectDict.get('major_id')
            year = subjectDict.get('year')
            if sid is None or name is None or major_id is None:
                continue
            student = Student()
            if sid is not None:
                student_set = Student.objects.filter(sid=sid)
                if student_set.exists():
                    repeated_ids.append({"id":student_set[0].id})
                    continue
                student.sid = sid
            if name is not None:
                student.name = name
            if major_id is not None:
                student.major_id = major_id
            if year is not None:
                student.year = year

            try:
                student.save()
            # except IntegrityError:
            #     print("exist")
            except Exception:
                failed_sids.append({"sid":sid})
            else:
                succeed_ids.append({'id':student.id})
                tag = True
        subjects = {
            "succeed_ids": succeed_ids,
            "failed_sids": failed_sids,
            "repeated_ids": repeated_ids
        }
        if tag:
            return JsonResponse({'subjects':subjects, 'code': '2001', 'message': status_code['2001']}, safe=False)
        else:
            return JsonResponse({'subjects':subjects,'code': '4037', 'message': status_code['4037']}, safe=False)

    def update(self, request):
        """
        Update t_Student table
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
            sid = subjectDict.get('sid')
            major_id = subjectDict.get('major_id')
            year = subjectDict.get('year')
            student_set = Student.objects.filter(id=id)
            for student in student_set:
                if name:
                    student.name = name
                if sid:
                    student.sid = sid
                if major_id:
                    student.major_id = major_id
                if year:
                    student.year = year
                try:
                    student.save()
                except Exception as e:
                    continue
                else:
                    ids.append({'id': student.id})
                    tag = True
        if tag:
            return JsonResponse({'subjects': ids, 'code': '2005', 'message': status_code['2005']}, safe=False)
        else:
            return update_failed()

    def remove(self, request):
        """
        Remove t_Student table
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
            student_set = Student.objects.filter(id=id)
            if not student_set.exists():
                continue
            try:
                student_set.delete()
            except Exception as e:
                continue
            else:
                tag = True
        if tag:
            return delete_succeed()
        else:
            return delete_failed()
