#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is for the operation of t_ClassInfo table.

Here are operations:
get_classInfo_full_message_all: GET    http://localhost:8000/api/v1/table/class_info/display/all
    get_classInfo_full_message: GET    http://localhost:8000/api/v1/table/class_info/display
                         query: GET    http://localhost:8000/api/v1/table/class_info/format
                        insert: POST   http://localhost:8000/api/v1/table/class_info/format
                        update: PUT    http://localhost:8000/api/v1/table/class_info/format
                        remove: DELETE http://localhost:8000/api/v1/table/class_info/format
"""
from apps.MarkManagement.view.common import *

class ClassInfoViewSet(viewsets.ViewSet):

    def get_classInfo_full_message_all(self, request):
        """
        Get full t_ClassInfo table
        :param request: the request from browser.
        :return: JSON response.
        """
        access_token = request.META.get("HTTP_TOKEN")

        if not token_verify(access_token):
            return token_invalid()
        teacher_set = Teacher.objects.filter(token__token_text=access_token)
        teacher = teacher_set[0]
        if not teacher.is_manager:
            return manager_check_failed()

        result = []

        classInfo_set = ClassInfo.objects.all()
        for classInfo in classInfo_set:
            classInfo_dict = model_to_dict(classInfo)
            classInfo_dict['teacher_id'] = classInfo_dict['teacher']
            del classInfo_dict['teacher']
            teacher_dict = model_to_dict(classInfo.teacher)

            classInfo_dict['lesson_id'] = classInfo_dict['lesson']
            del classInfo_dict['lesson']
            lesson_dict = model_to_dict(classInfo.lesson)
            lesson_dict['college_id'] = lesson_dict['college']
            del lesson_dict['college']

            classInfo_dict['student_count'] = len(Student.objects.filter(class__classInfo__id=classInfo.id))
            classInfo_dict['lesson_message'] = lesson_dict
            classInfo_dict['teacher_message'] = teacher_dict
            classInfo_dict['current_semester'] = current_semester

            result.append(classInfo_dict)
        if len(result) == 0:
            return JsonResponse({
                'current_semester':current_semester,
                'code': '4036',
                'message': status_code['4036']},
                safe=False)
        code_number = '2000'
        result = {
            'code': code_number,
            'message': status_code[code_number],
            'subjects': result,
            'count': len(result),
        }

        return JsonResponse(result, safe=False)

    def get_classInfo_full_message(self, request):
        """
        Get t_ClassInfo table
        :param request: the request from browser.
        :return: JSON response.
        """
        access_token = request.META.get("HTTP_TOKEN")

        if not token_verify(access_token) :
            return token_invalid()
        id = request.GET.get('id')
        name = request.GET.get('name')
        cid = request.GET.get('cid')
        lesson_id = request.GET.get('lesson_id')
        teacher_id = request.GET.get('teacher_id')
        semester = request.GET.get('semester')
        week = request.GET.get('week')
        room = request.GET.get('room')

        if id is None and name is None and cid is None and teacher_id is None and semester is None and week is None and room is None and lesson_id is None:
            return JsonResponse({"code": '4032', "message": status_code['4032']})

        # 此处待优化,all()
        classInfo_set = ClassInfo.objects.all()
        if id is not None:
            classInfo_set = classInfo_set.filter(id=id)
        if name is not None:
            classInfo_set = classInfo_set.filter(name__contains=name)
        if cid is not None:
            classInfo_set = classInfo_set.filter(cid=cid)
        if lesson_id is not None:
            classInfo_set = classInfo_set.filter(lesson_id=lesson_id)
        if teacher_id is not None:
            classInfo_set = classInfo_set.filter(teacher_id=teacher_id)
        if semester is not None:
            classInfo_set = classInfo_set.filter(semester__contains=semester)
        if week is not None:
            classInfo_set = classInfo_set.filter(week__contains=week)
        if room is not None:
            classInfo_set = classInfo_set.filter(room__contains=room)

        result = []
        for classInfo in classInfo_set:
            classInfo_dict = model_to_dict(classInfo)
            classInfo_dict['teacher_id'] = classInfo_dict['teacher']
            del classInfo_dict['teacher']
            teacher_dict = model_to_dict(classInfo.teacher)

            classInfo_dict['lesson_id'] = classInfo_dict['lesson']
            del classInfo_dict['lesson']
            lesson_dict = model_to_dict(classInfo.lesson)
            lesson_dict['college_id'] = lesson_dict['college']
            del lesson_dict['college']

            classInfo_dict['student_count'] = len(Student.objects.filter(class__classInfo__id=classInfo.id))
            classInfo_dict['lesson_message'] = lesson_dict
            classInfo_dict['teacher_message'] = teacher_dict
            classInfo_dict['current_semester'] = current_semester

            result.append(classInfo_dict)
        if len(result) == 0:
            return JsonResponse({'current_semester':current_semester,'code': '4036', 'message': status_code['4036']}, safe=False)
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
        Query t_ClassInfo table
        :param request: the request from browser.
        :return: JSON response.
        """
        access_token = request.META.get("HTTP_TOKEN")

        if not token_verify(access_token) :
            return token_invalid()
        id = request.GET.get('id')
        name = request.GET.get('name')
        cid = request.GET.get('cid')
        teacher_id = request.GET.get('teacher_id')
        lesson_id = request.GET.get('lesson_id')
        semester = request.GET.get('semester')
        week = request.GET.get('week')
        room = request.GET.get('room')

        if id is None and name is None and cid is None and teacher_id is None and semester is None and week is None and room is None and lesson_id is None:
            return JsonResponse({"code": '4032', "message": status_code['4032']})

        # 此处待优化,all()
        classInfo_set = ClassInfo.objects.all()
        if id is not None:
            classInfo_set = classInfo_set.filter(id=id)
        if name is not None:
            classInfo_set = classInfo_set.filter(name__icontains=name)
        if cid is not None:
            classInfo_set = classInfo_set.filter(cid=cid)
        if teacher_id is not None:
            classInfo_set = classInfo_set.filter(teacher_id=teacher_id)
        if lesson_id is not None:
            classInfo_set = classInfo_set.filter(lesson_id=lesson_id)
        if semester is not None:
            classInfo_set = classInfo_set.filter(semester__contains=semester)
        if week is not None:
            classInfo_set = classInfo_set.filter(week__contains=week)
        if room is not None:
            classInfo_set = classInfo_set.filter(room__contains=room)

        classInfo_set = classInfo_set.values()
        result = []
        for classInfo in classInfo_set:
            classInfo['current_semester'] = current_semester
            result.append(classInfo)
        if len(result) == 0:
            return JsonResponse({'current_semester':current_semester,'code': '4036', 'message': status_code['4036']}, safe=False)
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
        Insert t_ClassInfo table
        :param request: the request from browser.
        :return: JSON response.
        """
        post_data = request.data
        access_token = request.META.get("HTTP_TOKEN")

        if not token_verify(access_token) :
            return token_invalid()
        subjects = post_data.get('subjects')
        if subjects is None:
            return JsonResponse({'code': '4032', 'message': status_code['4032']}, safe=False)
        # 传入参数为字典数组
        tag = False
        insertID = []
        for subjectsDict in subjects:
            name = subjectsDict.get('name',None)
            teacher_id = subjectsDict.get('teacher_id',None)
            semester = subjectsDict.get('semester', None)
            week = subjectsDict.get('week',None)
            room = subjectsDict.get('room',None)
            lesson_id = subjectsDict.get('lesson_id',None)
            if name is None or teacher_id is None or lesson_id is None:
                continue
            classInfo = ClassInfo()
            if name is not None:
                classInfo.name = name
            if teacher_id:
                classInfo.teacher_id = teacher_id
            if lesson_id:
                classInfo.lesson_id = lesson_id
            if semester is not None:
                classInfo.semester = semester
            if week is not None:
                classInfo.week = week
            if room is not None:
                classInfo.room = room
            try:
                classInfo.save()
            except Exception as e:
                continue
            else:
                insertID.append({'id':classInfo.id})
                tag = True
        if tag:
            result = {
                'subjects': insertID,
                'code': '2001',
                'message': status_code['2001']
            }
            return JsonResponse(result, safe=False)
        else:
            return insert_failed()

    def update(self, request):
        """
        Update t_ClassInfo table
        :param request: the request from browser.
        :return: JSON response.
        """
        put_data = request.data
        access_token = request.META.get("HTTP_TOKEN")
        if not token_verify(access_token) :
            return token_invalid()
        subjects = put_data.get('subjects')
        if subjects is None:
            return JsonResponse({'code': '4032', 'message': status_code['4032']}, safe=False)
        tag = False
        ids = []
        for subjectDict in subjects:
            id = subjectDict.get('id')
            name = subjectDict.get('name')
            teacher_id = subjectDict.get('teacher_id')
            lesson_id = subjectDict.get('lesson_id')
            semester = subjectDict.get('semester')
            week = subjectDict.get('week')
            room = subjectDict.get('room')
            if id is None and name is None and teacher_id is None and semester is None and week is None:
                continue
            classInfo_set = ClassInfo.objects.filter(id=id)
            for classInfo in classInfo_set:
                if name:
                    classInfo.name = name
                if teacher_id:
                    classInfo.teacher_id = teacher_id
                if lesson_id:
                    classInfo.lesson_id = lesson_id
                if semester:
                    classInfo.semester = semester
                if week:
                    classInfo.week = week
                if room:
                    classInfo.room = room
                try:
                    classInfo.save()
                except Exception as e:
                    continue
                else:
                    ids.append({'id': id})
                    tag = True
        if tag:
            return JsonResponse({'subjects': ids, 'code': '2005', 'message': status_code['2005']}, safe=False)
        else:
            return update_failed()

    def remove(self, request):
        """
        Remove t_ClassInfo table
        :param request: the request from browser.
        :return: JSON response.
        """
        delete_data = request.data
        access_token = request.META.get("HTTP_TOKEN")

        if not token_verify(access_token) :
            return token_invalid()
        subjects = delete_data.get('subjects')
        if subjects is None:
            return JsonResponse({'code': '4032', 'message': status_code['4032']}, safe=False)
        tag = False
        for subjectDict in subjects:
            id = subjectDict.get('id')
            if id is None:
                continue
            classInfo_set = ClassInfo.objects.filter(id=id)
            if not classInfo_set.exists():
                continue
            try:
                classInfo_set.delete()
            except Exception as e:
                continue
            else:
                tag = True

        if tag:
            return delete_succeed()
        else:
            return delete_failed()
