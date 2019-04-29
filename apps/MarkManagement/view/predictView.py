#!/usr/bin/env python
# -*- coding=utf-8 -*-

"""
    This file is for the performance prediction.
"""

import xgboost as xgb
from apps.MarkManagement.view.common import *
from pandas.core.frame import DataFrame
from keras.layers import Dense, Dropout
from keras.models import Sequential
from sklearn.externals.joblib import load
import pandas as pd
import keras
import time
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

            point_set = Point.objects.filter(student_id__in=id_list) \
                .values('pointNumber', 'student__sid', 'title__name', 'title__titleGroup__name')

            print('length of point_set=', len(point_set))

            temps = []
            dicts = {}
            results = []

            for point in point_set:
                point['sid'] = point['student__sid']
                if point['title__titleGroup__name'] == '期中客观分':
                    point['score_zk'] = point['pointNumber']
                    if point['title__name'] == '期中词汇':
                        point['vocabulary'] = point['pointNumber']
                    if point['title__name'] == '期中听力':
                        point['hearing'] = point['pointNumber']
                    if point['title__name'] == '期中翻译':
                        point['translate'] = point['pointNumber']
                    if point['title__name'] == '期中写作':
                        point['writing'] = point['pointNumber']
                    if point['title__name'] == '期中细节':
                        point['details'] = point['pointNumber']
                if point['title__titleGroup__name'] == '期中主观分':
                    point['score_zs'] = point['pointNumber']
                    point['score_zz'] = point['pointNumber']
                if point['title__titleGroup__name'] == '期末客观分':
                    point['score_ms'] = point['pointNumber']
                    point['score_mk'] = point['pointNumber']
                if point['title__titleGroup__name'] == '期末主观分':
                    point['score_ms'] = point['pointNumber']
                    point['score_mz'] = point['pointNumber']

                del point['pointNumber']
                del point['student__sid']
                del point['title__name']
                del point['title__titleGroup__name']
                temps.append(point)

            for temp in temps:
                if temp['sid'] in dicts:
                    if 'score_zk' in dicts[temp['sid']] and 'score_zk' in temp:
                        dicts[temp['sid']]['score_zk'] += temp['score_zk']
                        del temp['score_zk']
                    elif 'score_zs' in dicts[temp['sid']] and 'score_zs' in temp:
                        dicts[temp['sid']]['score_zs'] += temp['score_zs']
                        del temp['score_zs']
                    elif 'score_ms' in dicts[temp['sid']] and 'score_ms' in temp:
                        dicts[temp['sid']]['score_ms'] += temp['score_ms']
                        del temp['score_ms']
                    dicts[temp['sid']].update(temp)
                else:
                    dicts[temp['sid']] = temp

            for value in dicts.values():
                if value != {}:
                    if 'score_zk' not in value:
                        value['score_zk'] = 0
                    if 'score_zz' not in value:
                        value['score_zz'] = 0
                    if 'score_zs' not in value:
                        value['score_zs'] = 0
                    if 'score_mk' not in value:
                        value['score_mk'] = 0
                    if 'score_mz' not in value:
                        value['score_mz'] = 0
                    if 'score_ms' not in value:
                        value['score_ms'] = 0
                    if 'vocabulary' not in value:
                        value['vocabulary'] = 0
                    if 'hearing' not in value:
                        value['hearing'] = 0
                    if 'translate' not in value:
                        value['translate'] = 0
                    if 'writing' not in value:
                        value['writing'] = 0
                    if 'details' not in value:
                        value['details'] = 0

                    results.append(value)

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
            keras.backend.clear_session()
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
        print(type(request.data))
        print(request.data)
        start=time.time()
        # sidList = request.data['sidList']
        sidList =request.data['sidList']
        # sidList = request.data.get('idList')
        end = time.time()
        print("从前台读取数据花费时间=", end-start)
        # print('sidList=', sidList)
        # request.data['sidList']['param']

        # 获得学生姓名列表
        nameList = []
        start = time.time()
        nameList = getNameListBySidList(sidList)
        end = time.time()
        print("获得学生姓名列表花费时间=", end - start)
        # print('nameList=', nameList)

        # 根据sidList获得入学第一学年秋季的期中客观分、期中主观分、期中总分、期末客观分、期末主观分和期末总分
        start = time.time()
        dataset = getScoreListMapBySidList(sidList)
        end = time.time()
        print("取各项分数花费时间=", end - start)

        # 转换数据格式
        dataset = DataFrame(dataset)
        print("dataset=", dataset)

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
        start = time.time()
        annpre = annpredict("./apps/static/model/Weights-2955--5.23046.hdf5", dataset, 11)
        annpre = list(annpre.reshape((1, annpre.shape[0]))[0])
        print("annpre=", annpre)
        # xgb预测结果
        xgbpre = list(xgbpredict("./apps/static/model/xgboost.model", dataset))
        print("xgbpre=", xgbpre)
        c = {"annpre": annpre, "xgbpre": xgbpre}
        dataset = DataFrame(c)
        # 融合模型预测结果
        preds = xgbpredict("./apps/static/model/xgb_impro.model", dataset)
        print("preds=", preds)
        end = time.time()
        print("预测花费时间=", end - start)

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
        print("predictListMap=",predictListMap)
        result = {
            'code': code_number,
            'message': status_code[code_number],
            'subjects': predictListMap,
            'count': len(predictListMap),
        }
        return JsonResponse(result, safe=False)
