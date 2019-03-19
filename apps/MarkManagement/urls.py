#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is used to register the function's urls.

http 中 get 方法进入 query 函数， post 方法进入 insert 函数, put 方法进入update 函数， delete 方法进入 remove 函数
"""

from apps.MarkManagement.view import views
from django.urls import re_path

urlpath = [
    # table
    re_path(r'^table/lesson/format', views.LessonViewSet.as_view({'get': 'query',
                                                                    'post': 'insert',
                                                                    'put': 'update',
                                                                    'delete': 'remove'})),
    # class
    re_path(r'^table/class_field/wrapper', views.ClassViewSet.as_view({'post': 'query_wrapper'})),
    re_path(r'^table/class_field/format', views.ClassViewSet.as_view({'get': 'query',
                                                                  'post': 'insert',
                                                                  'delete': 'remove'})),

    re_path(r'^table/class_info/format', views.ClassInfoViewSet.as_view({'get': 'query',
                                                                  'post': 'insert',
                                                                  'put': 'update',
                                                                  'delete': 'remove'})),
    #necessary
    re_path(r'^table/class_info/display$', views.ClassInfoViewSet.as_view({'get': 'get_classInfo_full_message'})),
    re_path(r'^table/class_info/display/all', views.ClassInfoViewSet.as_view({'get': 'get_classInfo_full_message_all'})),

    # teacher,目前等价于user
    #re_path(r'^teacher/info/format$', views.TeacherViewSet.as_view({'get': 'query',
     #                                                               'put': 'update'})),

    # user
    #necessary
    re_path(r'^user/info/display', views.TeacherViewSet.as_view({'get': 'get_user_full_message'})),

    re_path(r'^user/info/format', views.TeacherViewSet.as_view({'get': 'query'})),

    re_path(r'^user/logon', views.TeacherViewSet.as_view({'post': 'logon'})),
    re_path(r'^user/login', views.TeacherViewSet.as_view({'post': 'login'})),
    re_path(r'^user/logout', views.TeacherViewSet.as_view({'post': 'logout'})),

    # user_manage
    re_path(r'^user/info/manage', views.TeacherManageViewSet.as_view({'get': 'query',
                                                                       'post': 'insert',
                                                                       'put': 'update',
                                                                       'delete': 'remove'})),
    # student
    #necessary
    re_path(r'^student/display', views.StudentViewSet.as_view({'get': 'get_student_list'})),

    re_path(r'^student/format', views.StudentViewSet.as_view({'get': 'query',
                                                                'post': 'insert',
                                                                'put': 'update',
                                                                'delete': 'remove'})),
    # university
    re_path(r'^university/format', views.UniversityViewSet.as_view({'get': 'query',
                                                                     'post': 'insert',
                                                                      'put': 'update',
                                                                      'delete': 'remove'})),

    # college
    re_path(r'^college/display', views.CollegeViewSet.as_view({'get':'get_college_list'})),
    re_path(r'^college/format', views.CollegeViewSet.as_view({'get': 'query',
                                                                       'post': 'insert',
                                                                       'put': 'update',
                                                                       'delete': 'remove'})),
    # major
    re_path(r'^major/format', views.MajorViewSet.as_view({'get': 'query',
                                                            'post': 'insert',
                                                            'put': 'update',
                                                            'delete': 'remove'})),

    # point
    re_path(r'^point/display', views.PointViewSet.as_view({'get': 'get_point_list'})),
    re_path(r'^point/format', views.PointViewSet.as_view({'get': 'query',
                                                            'post': 'insert',
                                                            'put': 'update',
                                                            'delete': 'remove'})),
    # title
    re_path(r'^title/display', views.TitleViewSet.as_view({'get':'get_title_list'})),
    re_path(r'^title/format', views.TitleViewSet.as_view({'get': 'query',
                                                            'post': 'insert',
                                                            'put': 'update',
                                                            'delete': 'remove'})),
    # titlegroup
    re_path(r'^titleGroup/format', views.TitleGroupViewSet.as_view({'get': 'query',
                                                            'post': 'insert',
                                                            'put': 'update',
                                                            'delete': 'remove'})),
    re_path(r'^import_data', views.ImportDataViewSet.as_view({'post': 'insert'}))
    # semester
    # re_path(r'^semester/$',views.)






]
