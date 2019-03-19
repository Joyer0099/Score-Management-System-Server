#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is for the basic operation of users.

Here are operations:
                logon: POST http://localhost:8000/api/v1/user/logon
                login: POST http://localhost:8000/api/v1/user/login
               logout: POST http://localhost:8000/api/v1/user/logout
                query: GET  http://localhost:8000/api/v1/user/info/format
get_user_full_message: GET  http://localhost:8000/api/v1/user/info/display
"""

from apps.MarkManagement.view.common import *

class TeacherViewSet(viewsets.ViewSet):

    def logon(self, request):
        """
        Log on
        :param request: the request from browser.
        :return: JSON response.
        """
        post_data =  request.data
        tid = post_data.get('tid')
        password = post_data.get('password')
        college_id = post_data.get('college_id')
        name = post_data.get('name')
        email = post_data.get('email','')
        mobile = post_data.get('mobile','')

        if password is None or college_id is None or tid is None or name is None:
            return parameter_missed()
        #college_set = College.objects.filter(id=college_id)
        #if college_set.exists() == False:
            #return JsonResponse({'code': '1022', 'message': status_code['4032']}, safe=False)

        teacher_set = Teacher.objects.filter(Q(tid=tid))
        if teacher_set.exists():
            code_number = '4023'
            return JsonResponse({'code': code_number, 'message': status_code[code_number]}, safe=False)
        teacher = Teacher()
        teacher.tid = tid
        teacher.password = password
        teacher.college_id = college_id
        teacher.name = name
        teacher.mobile = mobile
        teacher.email = email
        try:
            teacher.save()
        except Exception as e:
            return insert_failed()
        else:
            return insert_succeed()

    def login(self, request):
        """
        Log in
        :param request: the request from browser.
        :return: JSON response.
        """
        post_data = request.data
        tid = post_data.get('tid')
        password = post_data.get('password')
        if tid is None or password is None:
            return parameter_missed()

        teacher_set = Teacher.objects.filter(tid=tid, password=password)
        if teacher_set.exists():
            access_token = Token()
            access_token.teacher = teacher_set[0]
            access_token.token_text = create_md5(password)
            access_token.save()
            subjects = {
                'token': access_token.token_text,
                'id': access_token.teacher.id
            }
            code_number = '2000'
            return JsonResponse({'code': code_number, 'message': status_code[code_number], 'subjects': subjects}, safe=False)
        else:
            code_number = '4021'
            return JsonResponse({'code': code_number, 'message': status_code[code_number]}, safe=False)

    def logout(self, request):
        """
        Log out
        :param request: the request from browser.
        :return: JSON response.
        """
        post_data = request.data
        access_token = request.META.get("HTTP_TOKEN")

        if access_token:
            # 删除token
            try:
                Token.objects.filter(token_text=access_token).delete()
            except Exception as e:
                return delete_failed()
            else:
                return delete_succeed()
        else:
            return delete_failed()

    def query(self, request):
        """
        Query t_Teacher table
        :param request: the request from browser.
        :return: JSON response.
        """
        access_token = request.META.get("HTTP_TOKEN")

        if not token_verify(access_token):
            return token_invalid()
        id = request.GET.get('id')
        tid = request.GET.get('tid')
        name = request.GET.get('name')
        college_id = request.GET.get('college_id')
        email = request.GET.get('email')
        mobile = request.GET.get('mobile')
        is_manager = request.GET.get('is_manager')
        if id is None and name is None and tid is None and college_id is None and email is None and mobile is None and is_manager is None:
            return parameter_missed()
        teacher_set = Teacher.objects.all()
        if id:
            teacher_set = teacher_set.filter(id=id)
        if tid:
            teacher_set = teacher_set.filter(tid=tid)
        if name:
            teacher_set = teacher_set.filter(name=name)
        if college_id:
            teacher_set = teacher_set.filter(college_id=college_id)
        if email:
            teacher_set = teacher_set.filter(email=email)
        if mobile:
            teacher_set = teacher_set.filter(mobile=mobile)
        if is_manager:
            teacher_set = teacher_set.filter(is_manager=is_manager)

        teacher_set = teacher_set.values()
        result = []
        for teacher in teacher_set:
            del teacher['password']
            result.append(teacher)
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

    def get_user_full_message(self, request):
        """
        Get user full message
        :param request: the request from browser.
        :return: JSON response.
        """
        access_token = request.META.get("HTTP_TOKEN")

        if not token_verify(access_token):
            return token_invalid()
        id = request.GET.get('id')
        tid = request.GET.get('tid')
        name = request.GET.get('name')
        college_id = request.GET.get('college_id')
        email = request.GET.get('email')
        mobile = request.GET.get('mobile')
        is_manager = request.GET.get('is_manager')
        if id is None and name is None and tid is None and college_id is None and email is None and mobile is None and is_manager is None:
            return parameter_missed()
        teacher_set = Teacher.objects.all()
        if id:
            teacher_set = teacher_set.filter(id=id)
        if tid:
            teacher_set = teacher_set.filter(tid=tid)
        if name:
            teacher_set = teacher_set.filter(name=name)
        if college_id:
            teacher_set = teacher_set.filter(college_id=college_id)
        if email:
            teacher_set = teacher_set.filter(email=email)
        if mobile:
            teacher_set = teacher_set.filter(mobile=mobile)
        if is_manager:
            teacher_set = teacher_set.filter(is_manager=is_manager)

        result = []
        for teacher in teacher_set:
            dict_teacher = model_to_dict(teacher)
            dict_college = model_to_dict(teacher.college)
            dict_university = model_to_dict(teacher.college.university)

            dict_teacher['college_id'] = dict_teacher['college']
            del dict_teacher['college']
            dict_college['university_id'] = dict_college['university']
            del dict_college['university']

            del dict_teacher['password']
            dict_teacher['college_message'] = dict_college
            dict_teacher['university_message'] = dict_university
            result.append(dict_teacher)
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
