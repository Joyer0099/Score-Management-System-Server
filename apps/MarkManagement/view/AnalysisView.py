#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apps.MarkManagement.view.common import *
import numpy as np
import math


class AnalysisViewSet(viewsets.ViewSet):
    # 分析各种考试对提高学位英语成绩的贡献值
    def Analysisfun(self, request):
        """ 增益熵
            描述x对y的熵增益情况
             """

        # 计算熵
        def entropy(x):
            set_value_x = set(x)
            ent = 0.0
            for x_value in set_value_x:
                p = float(x.count(x_value)) / len(x)
                logp = np.log2(p)
                ent -= p * logp
            return ent

        # 条件熵
        def ent_condition(x, y):
            set_value_x = set(x)
            ent = 0.0
            for x_value in set_value_x:
                sub_y = [y[i] for i in range(len(x)) if x[i] == x_value]
                ent += (float(len(sub_y)) / len(y)) * entropy(sub_y)
            return ent

        # 熵增益
        def gain_ent(x, y):
            x = list(x)
            y = list(y)
            # y的熵
            ent_y = entropy(y)
            # x条件下y的熵
            ent_y_con_x = ent_condition(x, y)
            gain = ent_y - ent_y_con_x
            return gain

        """ 熵增益结束"""
        """ 信息增益比 """

        def gainRate_ent(x, y):
            xe = entropy(list(x))
            yxe = gain_ent(x, y)
            if xe == 0:
                return 0
            else:
                return yxe / xe

        """ Pearson系数 
            皮尔逊系数描述了两个变量之间的相关程度
            取值范围[-1,1],0表示两个变量之间无关
            """

        def coef_Pearson(x, y):
            x = list(x)
            y = list(y)
            mean_x = np.mean(x)
            mean_y = np.mean(y)
            n = len(x)
            # 协方差
            cov = 0.0
            sumBottom = 0.0
            # x,y方差
            var_x = 0.0
            var_y = 0.0
            for i in range(n):
                cov += (x[i] - mean_x) * (y[i] - mean_y)
            for i in range(n):
                var_x += math.pow(x[i] - mean_x, 2)
            for i in range(n):
                var_y += math.pow(y[i] - mean_y, 2)
            return cov / math.sqrt(var_x * var_y)

        # 从数据库获取数据
        # 获取数据库中某个学期semester的所有分数
        def getAllScores(semester):
            #     map={
            #         'vocabulary':40,        //期中词汇分
            #         'hearing':9,            //期中听力分
            #         'translate':7,          //期中翻译分
            #         'writing':7,            //期中写作分
            #         'details':7,            //期中细节分
            #         'subjective_qz':20,     //期中主观分
            #         'objective_qm':60,      //期末客观分
            #         'subjective_qm':20,     //期末主观分
            #         'xuewei':70             //学位英语分
            #     }
            # semester = '2018年秋季'
            temps = []
            dicts = {}
            results = []

            classInfo_set = ClassInfo.objects.filter(semester=semester)

            classInfo_id_set = []
            for classInfo in classInfo_set:
                classInfo_dict = model_to_dict(classInfo)
                classInfo_id_set.append(classInfo_dict['id'])

            point_set = Point.objects.filter(classInfo_id__in=classInfo_set)

            for point in point_set:
                point_dict = model_to_dict(point)
                title_dict = model_to_dict(point.title)
                titleGroup_dict = model_to_dict(point.title.titleGroup)
                # point_dict['title'] = title_dict
                # point_dict['titleGroup'] = titleGroup_dict
                point_dict['titleName'] = title_dict['name']
                point_dict['titleGroupName'] = titleGroup_dict['name']

                # TODO: Maybe the score's calculation is not correct.
                point_dict['score'] = point_dict['pointNumber']

                del point_dict['id']
                del point_dict['classInfo']
                del point_dict['title']
                del point_dict['pointNumber']
                del point_dict['note']

                if '期中' in point_dict['titleGroupName']:
                    if '词汇' in point_dict['titleName']:
                        point_dict['vocabulary'] = point_dict['score']
                    elif '听力' in point_dict['titleName']:
                        point_dict['hearing'] = point_dict['score']
                    elif '翻译' in point_dict['titleName']:
                        point_dict['translate'] = point_dict['score']
                    elif '写作' in point_dict['titleName']:
                        point_dict['writing'] = point_dict['score']
                    elif '细节' in point_dict['titleName']:
                        point_dict['details'] = point_dict['score']
                    elif '主观' in point_dict['titleName']:
                        point_dict['subjective_qz'] = point_dict['score']
                    else:
                        continue

                if '期末' in point_dict['titleGroupName']:
                    if '主观' in point_dict['titleName']:
                        point_dict['subjective_qm'] = point_dict['score']
                    elif '客观' in point_dict['titleName']:
                        point_dict['objective_qm'] = point_dict['score']
                    else:
                        continue

                elif '学位英语成绩' in point_dict['titleGroupName']:
                    point_dict['xuewei'] = point_dict['score']

                del point_dict['titleGroupName']
                del point_dict['titleName']
                del point_dict['score']

                temps.append(point_dict)

            for temp in temps:
                if temp['student'] in dicts:
                    dicts[temp['student']].update(temp)

                else:
                    dicts[temp['student']] = temp

            for value in dicts.values():
                del value['student']
                results.append(value)

            return results

        # 从前端读到数据
        semester = request.data['semester']
        scoresListMap = getAllScores(semester)

        vocabulary = []
        hearing = []
        translate = []
        writing = []
        details = []
        subjective_qz = []
        objective_qm = []
        subjective_qm = []
        xuewei = []
        for i in range(len(scoresListMap)):
            vocabulary.append(scoresListMap[i]['vocabulary'])
            hearing.append(scoresListMap[i]['hearing'])
            translate.append(scoresListMap[i]['translate'])
            writing.append(scoresListMap[i]['writing'])
            details.append(scoresListMap[i]['details'])
            subjective_qz.append(scoresListMap[i]['subjective_qz'])
            objective_qm.append(scoresListMap[i]['objective_qm'])
            subjective_qm.append(scoresListMap[i]['subjective_qm'])
            xuewei.append(scoresListMap[i]['xuewei'])

        vocabulary = round(coef_Pearson(vocabulary, xuewei), 6)
        hearing = round(coef_Pearson(hearing, xuewei), 6)
        translate = round(coef_Pearson(translate, xuewei), 6)
        writing = round(coef_Pearson(writing, xuewei), 6)
        details = round(coef_Pearson(details, xuewei), 6)
        subjective_qz = round(coef_Pearson(subjective_qz, xuewei), 6)
        objective_qm = round(coef_Pearson(objective_qm, xuewei), 6)
        subjective_qm = round(coef_Pearson(subjective_qm, xuewei), 6)

        resultMap = {
            'vocabulary': vocabulary,
            'hearing': hearing,
            'translate': translate,
            'writing': writing,
            'details': details,
            'subjective_qz': subjective_qz,
            'objective_qm': objective_qm,
            'subjective_qm': subjective_qm
        }

        # 如果没有结果返回
        if len(scoresListMap) == 0:
            # #########具体应该是什么code_number、返回什么错误信息需要修改#########
            code_number = 4000
            return JsonResponse({'code': code_number, 'message': status_code[code_number]}, safe=False)
        code_number = '2000'

        # 返回结果
        result = {
            'code': code_number,
            'message': status_code[code_number],
            'subjects': resultMap,
        }
        print(result)
        return JsonResponse(result, safe=False)
