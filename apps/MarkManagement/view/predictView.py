#!/usr/bin/env python
# -*- coding=utf-8 -*-

import xgboost as xgb
from apps.MarkManagement.view.common import *
from pandas.core.frame import DataFrame
from keras.layers import Dense, Dropout
from keras.models import Sequential
from sklearn.externals.joblib import load
import pandas as pd
import keras
import numpy as np


class PredictViewSet(viewsets.ViewSet):
    def predictScore(self, request):
        """
        预测学位英语成绩
        使用期中客观分、期中主观分、期中总分、期末客观分、期末主观分和期末总分来预测研究生学位英语成绩
        :param request:
        :return:
        """
        def getScoreListMapBySidList(id_list):
            """
            该函数用于，根据sidList获得sidList中所包含的学生的入学第一学年秋季的期中客观分、期中主观分、期中总分、期末客观分、期末主观分和期末总分
            :param id_list: sidList是sid列表，形如['2019001','2019002',……]
            :return:result是一个ListMap,形如[map1,map2,……]，一个具体map格式如下
                    客观分, 主观分, 总分, 词汇, 听力, 翻译, 写作, 细节, 客观分m, 主观分m, 总分m, 总分1
                    map={
                        'sid':'2019001',        //学号
                        'score_zk':70,        //期中客观分
                        'score_zz':18,        //期中主观分
                        'score_zs':88,        //期中总分
                        'vocabulary':20,      //期中客观单词分
                        'hearing': 10,         //期中客观听力分
                        'translate': 10,      //期中客观翻译分
                        'writing': 10,        //期中客观写作分
                        'details': 10,         //期中客观细节分
                        'score_mk':47,        //期末客观分
                        'score_mz':10,        //期末主观分
                        'score_ms':57,        //期末总分
                        }
            """
            point_set = Point.objects.filter(student_id__in=id_list)

            results = []

            for point in point_set:
                point_dict = model_to_dict(point)
                point_dict['classInfo_id'] = point_dict['classInfo']

                student_dict = model_to_dict(point.student)
                point_dict['sid'] = student_dict['sid']
                point_dict['syear'] = student_dict['year']

                title_dict = model_to_dict(point.title)
                point_dict['title_name'] = title_dict['name']
                point_dict['title_weight'] = title_dict['weight']

                titleGroup_dict = model_to_dict(point.title.titleGroup)
                point_dict['titleGroup_name'] = titleGroup_dict['name']
                point_dict['titleGroup_weight'] = titleGroup_dict['weight']

                classInfo_dict = model_to_dict(point.classInfo)
                point_dict['semester'] = classInfo_dict['semester']

                # TODO: the caculation of score maybe wrong
                point_dict['score'] = point_dict['pointNumber']

                del point_dict['student']
                del point_dict['id']
                del point_dict['title']
                del point_dict['classInfo']
                del point_dict['note']
                del point_dict['classInfo_id']
                del point_dict['pointNumber']
                del point_dict['title_weight']
                del point_dict['titleGroup_weight']

                results.append(point_dict)

            for result in results:
                if result['titleGroup_name'] == '期中成绩':
                    if result['title_name'] == '客观分':
                        result['score_zk'] = result['score']
                    elif result['title_name'] == '主观分':
                        result['score_zz'] = result['score']
                elif result['titleGroup_name'] == '期末成绩':
                    if result['title_name'] == '客观分':
                        result['score_mk'] = result['score']
                    elif result['title_name'] == '主观分':
                        result['score_mz'] = result['score']
                del result['title_name']
                del result['titleGroup_name']
                del result['score']

            dicts = {}

            for result in results:
                if result['syear'] in result['semester'] and '秋季' in result['semester']:
                    if not (result['sid'] in dicts):
                        dicts[result['sid']] = result
                    else:
                        dicts[result['sid']] = dict(dicts[result['sid']], **result)
                    del dicts[result['sid']]['syear']
                    del dicts[result['sid']]['semester']

            results = [d for d in dicts.values()]

            for result in results:
                result['score_zs'] = result.setdefault('score_zz', 0) + result.setdefault('score_zk', 0)
                result['score_ms'] = result.setdefault('score_mz', 0) + result.setdefault('score_mk', 0)

            return results

        def getNameListBySidList(id_list):
            """
            根据sidList得到nameList
            :param id_list:
            :return:
            """
            print("idList=", id_list)

            student_set = Student.objects.filter(id__in=id_list)

            name_list = []

            for student in student_set:
                student_dict = model_to_dict(student)
                name_list.append(student_dict['name'])

            return name_list

        # *********************v2_新增1_start *********************#
        # ann预测
        def annpredict(model_file, testData, inputdim):
            model = Sequential()
            model.add(Dense(16, kernel_initializer='normal', input_dim=inputdim, activation='relu'))
            model.add(Dense(32, kernel_initializer='normal', activation='relu'))
            model.add(Dropout(0.01))
            model.add(Dense(32, kernel_initializer='normal', activation='relu'))
            model.add(Dense(32, kernel_initializer='normal', activation='relu'))
            model.add(Dense(units=1))
            model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['accuracy'])
            model.summary()
            model.load_weights(model_file)
            model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['accuracy'])
            preds = model.predict(testData)
            # y_test = list(y_test)
            # score = 0.0
            # for i in range(len(preds)):
            #     # print("preds[i]=",preds[i],"y_test[i]=",y_test[i])
            #     # if(preds[i]<60.0 and y_test[i]<60.0) or (preds[i]>=60.0 and y_test[i]>=60.0):
            #     # if preds[i]==y_test[i]<60.0 :
            #     if (np.abs(preds[i] - y_test[i]) < 5.0):
            #         score += 1
            # print(score / len(y_test))
            return preds

        def xgbpredict(model_file, testData):
            tar = load(model_file)
            # dtest = xgb.DMatrix(testData)
            preds = tar.predict(testData)
            # score = 0.0
            # for i in range(len(preds)):
            #     if (preds[i] < 60.0 and y_test[i] < 60.0) or (preds[i] >= 60.0 and y_test[i] >= 60.0):
            #         # if(np.abs(preds[i]-y_test[i])<5.0):
            #         print("preds[i]=", preds[i], "y_test[i]=", y_test[i])
            #         score += 1
            # print(score / len(y_test))
            return preds

        # *********************v2_新增1_end *********************#

        # 获得要预测的学生的sidlist
        sidList = []
        # 从前端读到数据
        sidList = request.data['sidList']['param']

        # 获得学生姓名列表
        nameList = []
        nameList = getNameListBySidList(sidList)

        # 根据sidList获得入学第一学年秋季的期中客观分、期中主观分、期中总分、期末客观分、期末主观分和期末总分
        dataset = getScoreListMapBySidList(sidList)

        # 转换数据格式
        dataset = DataFrame(dataset)

        sidList = list(dataset['sid'])
        dataset.drop('sid', axis=1, inplace=True)

        # 将数据列顺序调好
        order = ['score_zk', 'score_zz', 'score_zs', 'vocabulary', 'hearing', 'translate', 'writing', 'details',
                 'score_mk', 'score_mz', 'score_ms']
        dataset = dataset[order]

        # /*******测试数据**********/
        # 获取csv文件数据
        # def getdata_csv(fileName):
        #     f = open(fileName, encoding='utf-8')
        #     data = pd.read_csv(f, encoding='utf-8')
        #     f.close()
        #     return data
        #
        # dataset = getdata_csv("./apps/ScoreAnalysis/data/dataset.csv")
        # /*******测试数据**********/
        # *********************v2_新增2_start *********************#

        # ann预测结果
        annpre = annpredict("./apps/static/model/Weights-2955--5.23046.hdf5", dataset, 11)
        annpre = list(annpre.reshape((1, annpre.shape[0]))[0])
        # print(annpre)
        # xgb预测结果
        xgbpre = list(xgbpredict("./apps/static/model/xgboost.model", dataset))
        # print(xgbpre)
        c = {"annpre": annpre, "xgbpre": xgbpre}
        dataset = DataFrame(c)
        # 融合模型预测结果
        preds = xgbpredict("./apps/static/model/xgb_impro.model", dataset)
        # print(preds)

        # *********************v2_新增2_end *********************#

        # *********************v1_注释1_start *********************#
        # # 导入xgb模型
        # tar = xgb.Booster(model_file="./apps/static/model/xgb.model")
        #
        # # 构建神经网络
        # keras.backend.clear_session()
        # model = Sequential()
        # model.add(Dense(16, kernel_initializer='normal', input_dim=dataset.shape[1], activation='relu'))
        # model.add(Dense(32, kernel_initializer='normal', activation='relu'))
        # model.add(Dropout(0.01))
        # model.add(Dense(32, kernel_initializer='normal', activation='relu'))
        # model.add(Dense(32, kernel_initializer='normal', activation='relu'))
        #
        # model.add(Dense(units=1))
        #
        # model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['accuracy'])
        #
        # model.summary()
        #
        # # 导入ann模型
        # wights = './apps/static/model/Weights-311--7.01484.hdf5'  # choose the best checkpoint
        #
        # model.load_weights(wights)
        # model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['accuracy'])
        #
        # # 使用xgb读取数据
        # dataInput = xgb.DMatrix(dataset)
        #
        # # xgb模型获得预测结果
        # preds1 = tar.predict(dataInput)
        #
        # # ann神经网络预测结果
        # preds2 = list(model.predict(dataset).reshape(-1))
        #
        # # 模型融合算法
        #
        # # 不同模型赋予不同权重
        # preds1 = [i * 1 / 4 for i in preds1]
        # preds2 = [i * 3 / 4 for i in preds2]
        # preds = np.sum([preds1, preds2], axis=0)

        # *********************v1_注释1_end *********************#
        # 返回结果
        predictListMap = []

        for i in range(len(sidList)):
            if preds[i] < 60.0:
                ps = "0"
            else:
                ps = '1'
            mp = {
                'sid': sidList[i],
                'name': nameList[i],
                'pass': ps
            }
            predictListMap.append(mp)
            # ******************************预测部分结束******************************

        # 如果没有结果返回
        if len(preds) == 0:
            # #########具体应该是什么code_number、返回什么错误信息需要修改#########
            code_number = 4000
            return JsonResponse({'code': code_number, 'message': status_code[code_number]}, safe=False)
        code_number = '2000'
        # 返回结果
        result = {
            'code': code_number,
            'message': status_code[code_number],
            'subjects': predictListMap,
            'count': len(predictListMap),
        }
        return JsonResponse(result, safe=False)
