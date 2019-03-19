#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is for the operation of t_Point table.

Here are operations:
get_point_list: GET    http://localhost:8000/api/v1/point/display
         query: GET    http://localhost:8000/api/v1/point/format
        insert: POST   http://localhost:8000/api/v1/point/format
        update: PUT    http://localhost:8000/api/v1/point/format
        remove: DELETE http://localhost:8000/api/v1/point/format
"""

from apps.MarkManagement.view.common import *

class PointViewSet(viewsets.ViewSet):

    def get_point_list(self, request):
        """
        Get t_Point table list
        :param request: the request from browser.
        :return: JSON response.
        """
        access_token = request.META.get("HTTP_TOKEN")
        if not token_verify(access_token):
            return token_invalid()
        id = request.GET.get('id')
        classInfo_id = request.GET.get('classInfo_id')
        student_id = request.GET.get('student_id')
        title_id = request.GET.get('title_id')
        date = request.GET.get('date')
        note = request.GET.get('note')
        if id is None and classInfo_id is None and student_id is None and title_id is None and date is None and note is None:
            return parameter_missed()
        point_set = Point.objects.all()
        if id is not None:
            point_set = point_set.filter(id=id)
        if student_id is not None:
            point_set = point_set.filter(student_id=student_id)
        if title_id is not None:
            point_set = point_set.filter(title_id=title_id)
        if date is not None:
            point_set = point_set.filter(date=date)
        if note is not None:
            point_set = point_set.filter(note=note)
        if classInfo_id:
            point_set = point_set.filter(classInfo_id=classInfo_id)
        result = []
        for point in point_set:
            pointDict = model_to_dict(point)

            student_dict = model_to_dict(point.student)
            title_dict = model_to_dict(point.title)
            classInfo_dict = model_to_dict(point.classInfo)

            pointDict['student_id'] = pointDict['student']
            del pointDict['student']

            pointDict['title_id'] = pointDict['title']
            del pointDict['title']

            pointDict['classInfo_id'] = pointDict['classInfo']
            del pointDict['classInfo']

            pointDict['student_message'] = student_dict
            pointDict['title_message'] = title_dict
            pointDict['classInfo_message'] = classInfo_dict

            result.append(pointDict)

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
        Query t_Point table
        :param request: the request from browser.
        :return: JSON response.
        """
        access_token = request.META.get("HTTP_TOKEN")
        if not token_verify(access_token):
            return token_invalid()
        id = request.GET.get('id')
        classInfo_id = request.GET.get('classInfo_id')
        student_id = request.GET.get('student_id')
        title_id = request.GET.get('title_id')
        date = request.GET.get('date')
        note = request.GET.get('note')
        if id is None and classInfo_id is None and student_id is None and title_id is None and date is None and note is None:
            return parameter_missed()
        point_set = Point.objects.filter(classInfo_id=classInfo_id)
        if id is not None:
            point_set = point_set.filter(id=id)
        if student_id is not None:
            point_set = point_set.filter(student_id=student_id)
        if title_id is not None:
            point_set = point_set.filter(title_id=title_id)
        if date is not None:
            point_set = point_set.filter(date=date)
        if note is not None:
            point_set = point_set.filter(note=note)
        if classInfo_id:
            point_set = point_set.filter(classInfo_id=classInfo_id)
        # 对象取字典
        point_set = point_set.values()
        result = []
        for point in point_set:
            result.append(point)
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
        Insert t_Point table
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
        ids = []

        succeed_ids = []
        failed_message = []
        repeated_ids = []

        for subjectDict in subjects:
            classInfo_id = subjectDict.get('classInfo_id')
            student_id = subjectDict.get('student_id')
            title_id = subjectDict.get('title_id')
            date = subjectDict.get('date')
            note = subjectDict.get('note')
            pointNumber = subjectDict.get('pointNumber')
            if classInfo_id is None or student_id is None or title_id is None or pointNumber is None:
                continue

            exist_point_set = Point.objects.filter(Q(student_id=student_id) & Q(title_id=title_id))
            if exist_point_set.exists():
                repeated_ids.append({'id':exist_point_set[0].id})
                continue

            point = Point()
            if classInfo_id:
                classInfo_set = ClassInfo.objects.filter(id=classInfo_id)
                if not classInfo_set.exists():
                    continue
                point.classInfo = classInfo_set[0]
            if student_id:
                student_set = Student.objects.filter(id=student_id)
                if not student_set.exists():
                    continue
                point.student = student_set[0]
            if title_id:
                title_set = Title.objects.filter(id=title_id)
                if title_set.exists() == 0:
                    continue
                point.title = title_set[0]
            if date:
                point.date = date
            if note:
                point.note = note
            if pointNumber:
                point.pointNumber = pointNumber
            try:
                point.save()
            except Exception as e:
                failed_message.append({'student_id':student_id,'title_id':title_id})
                continue
            else:
                succeed_ids.append({'id':point.id})
                tag = True

        subjects = {
            "succeed_ids": succeed_ids,
            "failed_message": failed_message,
            "repeated_ids": repeated_ids
        }

        if tag:
            return JsonResponse({'subjects':subjects, 'code': '2001', 'message': status_code['2001']}, safe=False)
        else:
            return JsonResponse({'subjects':subjects, 'code': '4037', 'message': status_code['4037']}, safe=False)

    def update(self, request):
        """
        Update t_Point table
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
            classInfo_id = subjectDict.get('classInfo_id')
            student_id = subjectDict.get('student_id')
            title_id = subjectDict.get('title_id')
            date = subjectDict.get('date')
            note = subjectDict.get('note')
            pointNumber = subjectDict.get('pointNumber')
            if id is None and classInfo_id is None and student_id is None and title_id is None:
                continue
            point_set = Point.objects.filter(id=id)
            if classInfo_id:
                point_set = point_set.filter(classInfo_id=classInfo_id)
            if student_id:
                point_set = point_set.filter(student_id=student_id)
            if title_id:
                point_set = point_set.filter(title_id=title_id)
            for point in point_set:

                if classInfo_id:
                    classInfo_set = ClassInfo.objects.filter(id=classInfo_id)
                    if not classInfo_set.exists():
                        continue
                    point.classInfo = classInfo_set[0]
                if student_id:
                    student_set = Student.objects.filter(id=student_id)
                    if not student_set.exists():
                        continue
                    point.student = student_set[0]
                if title_id:
                    title_set = Title.objects.filter(id=title_id)
                    if not title_set.exists():
                        continue
                    point.title = title_set[0]
                if date:
                    point.date = date
                if note:
                    point.note = note
                if pointNumber is not None:
                    point.pointNumber = pointNumber
                try:
                    point.save()
                except Exception as e:
                    continue
                else:
                    ids.append({'id': point.id})
                    tag = True
        if tag:
            return JsonResponse({'subjects':ids, 'code': '2005', 'message': status_code['2005']}, safe=False)
        else:
            return update_failed()

    def remove(self, request):
        """
        Remove t_Point table
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
            point_set = Point.objects.filter(id=id)
            if not point_set.exists():
                continue
            try:
                point_set.delete()
            except Exception as e:
                continue
            else:
                tag = True
        if tag:
            return delete_succeed()
        else:
            return delete_failed()
