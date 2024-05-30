import os
import random
import time

import streamlit as st
import pandas as pd
import subprocess
from PIL import Image

from demo import makingCertificate


def run_crawler():
    subprocess.run(["python", "Spider.py"])


# 主函数
def main():
    # 全局变量设置①---页面参数设置
    if 'number' not in st.session_state:
        st.session_state.number = '123456'
    if 'name' not in st.session_state:
        st.session_state.name = ''
    if 'sort' not in st.session_state:
        st.session_state.sort = '15x1.5公里接力赛'
    if 'score' not in st.session_state:
        st.session_state.score = '团体冠军'





    # 初始化小时、分钟和秒的选择列表
    hours = list(range(24))
    minutes = list(range(60))
    seconds = list(range(60))
    # 如果session_state中没有成绩，则初始化为0小时0分钟0秒
    if 'selected_hours' not in st.session_state:
        st.session_state.selected_hours = hours[0]
    if 'selected_minutes' not in st.session_state:
        st.session_state.selected_minutes = minutes[0]
    if 'selected_seconds' not in st.session_state:
        st.session_state.selected_seconds = seconds[0]

    if 'selected_minutes_even' not in st.session_state:
        st.session_state.selected_minutes_even = 0
    if 'selected_seconds_even' not in st.session_state:
        st.session_state.selected_seconds_even = 0

    # 初始化组、序号的选择列表
    group = list(range(1, 11))
    # 如果session_state中没有组别，则初始化为1组1号
    if 'number_group' not in st.session_state:
        st.session_state.number_group = group[0]
    if 'number_locant' not in st.session_state:
        st.session_state.number_locant = 1  # 小组内部人员不固定


    if 'output_path' not in st.session_state:
        st.session_state.output_path = "certificate_with_text.jpg"


    # if 'hours' not in st.session_state:
    #     st.session_state.hours = 0
    # if 'minutes' not in st.session_state:
    #     st.session_state.minutes = 0
    # if 'seconds' not in st.session_state:
    #     st.session_state.seconds = 0

    # 全局变量设置②---系统过程参数设置
    st.session_state.filenamePath = ""  # 操作文件地址
    st.session_state.data = None  # 文件对象
    st.session_state.model = None  # 模型对象
    st.session_state.vectorizer = None  # 文件对象



    # 定义网页标题
    st.set_page_config(page_title='大冶市长跑协会成立九周年跑步接力赛', layout='wide')

    st.header('大冶市长跑协会成立九周年跑步接力赛')

    st.markdown('<hr>', unsafe_allow_html=True)
    st.subheader("参赛者个人比赛成绩填写模块：")  # 添加一个二级标题

    # st.session_state.number = st.text_input('参赛号码', st.session_state.number)
    # 创建一个行容器
    st.markdown('<hr>', unsafe_allow_html=True)
    st.write('参赛号码:')
    col1, col2= st.columns(2)
    # 将下拉列表放入容器中
    with col1:
        # st.session_state.number_group = st.selectbox('组', group, index=st.session_state.number_group,
        #                                                key='number_group_selectbox')
        st.session_state.number_group = st.number_input('组：', min_value=1, max_value=10,
                                                                 value=st.session_state.number_group)
    with col2:
        st.session_state.number_locant = st.text_input('位次', st.session_state.number_locant)

    st.markdown('<hr>', unsafe_allow_html=True)
    st.session_state.name = st.text_input('姓名', st.session_state.name)

    st.session_state.sort = st.text_input('项目', st.session_state.sort)
    # st.session_state.sort = st.selectbox('项目', ['5KM', '10KM', '15KM'],
    #                                         index=['5KM', '10KM', '15KM'].index(st.session_state.sort))

    st.session_state.score = st.selectbox('成绩', ['团体冠军', '团体亚军', '团体季军', '团体第四名', '团体第五名', '团体第六名', '团体第七名', '团体第八名', '团体第九名', '团体第十名'],
                                            index=['团体冠军', '团体亚军', '团体季军', '团体第四名', '团体第五名', '团体第六名', '团体第七名', '团体第八名', '团体第九名', '团体第十名'].index(st.session_state.score))


    # 创建一个行容器
    st.markdown('<hr>', unsafe_allow_html=True)
    st.write('个人净时:')
    col3, col4 = st.columns(2)
    # 将下拉列表放入容器中
    # with col1:
    #     st.session_state.selected_hours = st.selectbox('小时', hours, index=st.session_state.selected_hours,
    #                                                    key='hours_selectbox')
    with col3:
        st.session_state.selected_minutes = st.selectbox('分钟', minutes, index=st.session_state.selected_minutes,
                                                         key='minutes_selectbox')
    with col4:
        st.session_state.selected_seconds = st.selectbox('秒', seconds, index=st.session_state.selected_seconds,
                                                         key='seconds_selectbox')
    # 显示当前选择的成绩
    st.write(
        f'您选择的 [个人净时] 成绩是: {st.session_state.selected_minutes:02d}:{st.session_state.selected_seconds:02d}')

    # 计算其个人平均配速（15x1.5公里接力赛）
    kilometers =1.5
    # 将小时、分钟和秒转换为总秒数
    total_seconds = st.session_state.selected_minutes * 60 + st.session_state.selected_seconds
    # 计算每公里的平均秒数
    average_seconds_per_kilometer = total_seconds / kilometers
    # 将平均秒数转换为分钟和秒
    st.session_state.selected_minutes_even = int(average_seconds_per_kilometer // 60)
    st.session_state.selected_seconds_even = int(average_seconds_per_kilometer % 60)

    performance_even = "{}分{}秒".format(
        st.session_state.selected_minutes_even,
        st.session_state.selected_seconds_even
    )
    # 显示当前选择的成绩
    st.write(
        f'您选择的 [平均配速] 成绩是: {performance_even}')

    # # 创建三个滑块，分别用于选择小时、分钟和秒
    # st.session_state.hours = st.slider('小时', 0, 23, st.session_state.hours)
    # st.session_state.minutes = st.slider('分钟', 0, 59, st.session_state.minutes)
    # st.session_state.seconds = st.slider('秒', 0, 59, st.session_state.seconds)

    # # 创建一个行容器
    # st.markdown('<hr>', unsafe_allow_html=True)
    # st.write('平均配速:')
    # col4, col5 = st.columns(2)
    # # 将下拉列表放入容器中
    # with col4:
    #     st.session_state.selected_minutes_even = st.number_input('平均配速-分：', min_value=0, max_value=60, value=st.session_state.selected_minutes_even)
    # with col5:
    #     st.session_state.selected_seconds_even = st.number_input('平均配速-秒：', min_value=0, max_value=60, value=st.session_state.selected_seconds_even)
    #
    # # 显示当前选择的成绩
    # st.write(
    #     f'您选择的 [平均配速] 成绩是: {st.session_state.selected_minutes_even:02d}:{st.session_state.selected_seconds_even:02d}')



    if st.button('确认'):
        # 要添加到图像上的文本
        # performance = "{:02d}:{:02d}:{:02d}".format(
        #     st.session_state.selected_hours,
        #     st.session_state.selected_minutes,
        #     st.session_state.selected_seconds
        # )
        performance = "{}分{}秒".format(
            st.session_state.selected_minutes,
            st.session_state.selected_seconds
        )

        # # -----根据上面提供的”项目(公里数)“和”成绩“自动计算”平均配速“------
        # # 将公里数字符串转换为整数
        # kilometers = int(st.session_state.sort)
        # # 将小时、分钟和秒转换为总秒数
        # total_seconds = st.session_state.selected_hours * 3600 + st.session_state.selected_minutes * 60 + st.session_state.selected_seconds
        # # 计算每公里的平均秒数
        # average_seconds_per_kilometer = total_seconds / kilometers
        # # 将平均秒数转换为分钟和秒
        # st.session_state.selected_minutes_even = int(average_seconds_per_kilometer // 60)
        # st.session_state.selected_seconds_even = int(average_seconds_per_kilometer % 60)
        #
        # performance_even = "{:02d}:{:02d}".format(
        #     st.session_state.selected_minutes_even,
        #     st.session_state.selected_seconds_even
        # )

        # text_to_add = {
        #     '参赛号码': '08-006',
        #     '姓名': '刘素娇',
        #     '项目': '15x1.5公里接力赛',
        #     '成绩': '团体冠军',
        #     '个人净时': '4分50秒',
        #     '平均配速': '3分13秒'
        # }
        text_to_add = {
            '参赛号码': "{:02d}-{:03d}".format(
            st.session_state.number_group,
            int(st.session_state.number_locant)
        ),
            '姓名': st.session_state.name,
            '项目': str(st.session_state.sort),
            '成绩': st.session_state.score,
            '个人净时': performance,
            '平均配速': performance_even
        }

        st.session_state.output_path = makingCertificate(text_to_add)


    st.markdown('<hr>', unsafe_allow_html=True)
    st.subheader("参赛者个人比赛成绩下载模块：")  # 添加一个二级标题
    # 显示图片
    # 设置图片的宽度和高度
    img_width = 300  # 图片的宽度
    img_height = 250  # 图片的高度
    # st.image(st.session_state.output_path, caption='Word Cloud', use_column_width=True)
    # 使用PIL调整图片大小
    img = Image.open(st.session_state.output_path)
    img = img.resize((img_width, img_height))

    # 显示调整大小后的图片
    st.image(img, caption='Certificate')

    # 创建一个下载按钮，允许用户下载图片
    st.download_button(
        label="下载证书",
        data=open(st.session_state.output_path, "rb").read(),
        file_name="Certificate.png",
        mime="image/png"
    )


if __name__ == '__main__':
    main()
