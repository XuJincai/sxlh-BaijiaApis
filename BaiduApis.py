import json
import os
import random
import re
import shutil
import time
import urllib

import pandas as pd
import yaml
# import requests
from curl_cffi import requests
from common_utils.utils import check_time_in_7_days_and_recent, check_time_in_yesterday, check_time_in_7_days

from common_utils.utils import validate_text
from utils.BaiduUtils import get_common_headers, trans_cookies, get_home_headers, get_detail_headers, trans_date, \
    is_n_days_ago, timestamp_to_str
from loguru import logger


logger.add("baidu.log", rotation="10 MB")
CURRENT_SPIDER_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

class BaiduApis():
    def __init__(self):
        self.base_url = ''

    def get_user_info(self, user_url, cookies_str):
        headers = get_common_headers()
        cookies = trans_cookies(cookies_str)
        response = requests.get(user_url, headers=headers, cookies=cookies, impersonate="chrome101")
        res_text = response.text
        if '<div class="empty-content">用户信息不存在</div>' in res_text:
            return '用户信息不存在', '', ''
        res_text = re.findall(r'window\.runtime= (.*),window\.runtime\.pageType', res_text)[0]
        res_json = json.loads(res_text)
        otherext = res_json['staticMap']['version']
        user = res_json['user']
        uk = user['uk']
        birth = user['birth']
        citycode = user['citycode']
        gender = user['gender']
        auth_describe = user['auth_describe']
        avatar = user['avatar']
        nickname = user['nickname']
        sign = user['sign']
        city_name = user['city_name']
        fans_num = user['fans_num']
        follow_num = user['follow_num']
        likes_num = user['likes_num']
        content_num = user['content_num'] if 'content_num' in user else ''
        user_id = re.findall(r'home/(\d+)', user_url)[0]
        user_info = {
            '账号昵称': nickname,
            '头像地址URL': avatar,
            '账号KEY': user_id,
            '粉丝数量': fans_num,
            '总发布量': content_num,
            '阅读/曝光数量': '未知',
            '点赞数量': likes_num,
            '评论数量': '未知',
            '收藏数量': '未知',
            '昨天发布数量': '未知',
            '采集时间': timestamp_to_str(int(time.time() * 1000)),
        }

        return user_info, uk, otherext

    def get_user_posted(self, uk, otherext, cookies_str, top_dynamic_id=None, ctime=None):
        headers = get_home_headers()
        cookies = trans_cookies(cookies_str)
        url = "https://mbd.baidu.com/webpage"
        params = {
            "tab": "main",
            "num": "10",
            "uk": str(uk),
            "source": "pc",
            "type": "newhome",
            "action": "dynamic",
            "format": "jsonp",
            "otherext": f"h5_{otherext}",
            "Tenger-Mhor": str(cookies['Hmery-Time']),
            "callback": "__jsonp01732944778793"
        }
        if top_dynamic_id:
            params['top_dynamic_id'] = str(top_dynamic_id)
            params['ctime'] = str(ctime)
        response = requests.get(url, headers=headers, cookies=cookies, params=params, impersonate="chrome101")
        res_text = response.text
        res_text = res_text[22:-1]
        res_json = json.loads(res_text)
        return res_json

    def get_work_info(self, item, uk, cookies_str):
        url = "https://mbd.baidu.com/webpage"
        headers = get_detail_headers()
        cookies = trans_cookies(cookies_str)
        p = json.dumps([item])
        params = {
            "type": "homepage",
            "action": "interact",
            "format": "jsonp",
            "Tenger-Mhor": str(cookies['Hmery-Time']),
            "params": p,
            "uk": uk,
            "callback": "__jsonp31732960326835"
        }
        response = requests.get(url, headers=headers, cookies=cookies, params=params, impersonate="chrome101")
        res_text = response.text
        res_text = res_text[22:-1]
        res_json = json.loads(res_text)
        for k, v in res_json['data']['user_list'].items():
            data = v
        work_info = {
            'praise_num': data['praise_num'],
            'comment_num': data['comment_num'],
            'read_num': data['read_num'],
            'forward_num': data['forward_num'],
            'live_back_num': data['live_back_num'],
            'collect': data['collect'],
            'unread': data['unread'],
        }
        return work_info

    def get_user_all_posted(self, user, user_url, cookies_strs, timesleep, recent_days):
        cookies_str = random.choice(cookies_strs)
        user_info, uk, otherext = self.get_user_info(user_url, cookies_str)
        if user_info == '用户信息不存在':
            one_item = user.copy()
            one_item_other = {
                '账号昵称': '用户信息不存在',
                '头像地址URL': '',
                '账号KEY': '',
                '粉丝数量': '',
                '总发布量': '',
                '阅读/曝光数量': '',
                '点赞数量': '',
                '评论数量': '',
                '收藏数量': '',
                '昨天发布数量': '',
                '采集时间': timestamp_to_str(int(time.time() * 1000)),
            }
            one_item.update(one_item_other)
            return {
                'user_res': one_item,
                'note_list': [one_item]
            }

        ctime = None
        top_dynamic_id = None
        work_list = []
        break_flag = True
        yesterday_uploads = 0
        while break_flag:
            cookies_str = random.choice(cookies_strs)
            res = self.get_user_posted(uk, otherext, cookies_str, top_dynamic_id, ctime)
            time.sleep(timesleep)
            for i in res['data']['list']:

                item_data = i['itemData']
                work_url = item_data['url']
                title = item_data['title']
                images = []
                videos = []
                content = title
                if 'type' in item_data:
                    if item_data['type'] == 'video':
                        content = item_data['content']
                        content = json.loads(content)[0]
                        videos.append(content['src'])
                        images.append(item_data['imgSrc'][0]['src'])
                        publish_at = item_data['publish_at']
                        publish_at = trans_date(publish_at)
                    else:
                        if 'origin_title' in item_data:
                            content = item_data['origin_title']
                        for img in item_data['imgSrc']:
                            if 'img_origin' in img:
                                images.append(img['img_origin'])
                            elif 'src' in img:
                                images.append(img['src'])

                        if 'created_at' in item_data:
                            publish_at = trans_date(item_data['created_at'])
                        elif 'publish_at' in item_data:
                            publish_at = item_data['publish_at']
                        elif 'ctime' in item_data:
                            publish_at = trans_date(item_data['ctime'])
                        else:
                            publish_at = trans_date(int(time.time()))
                else:
                    publish_at = item_data['time'] + ':00'
                work_item = user.copy()
                work_item_other = {
                    'work_url': work_url,
                    'title': title,
                    'publish_at': publish_at,
                    'images': images,
                    'videos': videos,
                    'content': content
                }
                work_item.update(work_item_other)
                item = {
                    'user_type': i['user_type'],
                    'feed_id': i['feed_id'],
                    'thread_id': i['thread_id'],
                    'dynamic_id': i['dynamic_id'],
                    'dynamic_type': i['dynamic_type'],
                    'dynamic_sub_type': i['dynamic_sub_type'],
                    'dynamic_ctime': i['dynamic_ctime'],
                    'dynamic_ctime_raw': i['dynamic_ctime_raw'],
                    'is_top': i['is_top'],
                    'top_index': i['top_index'],
                    'showstatus': i['showstatus']
                }
                time.sleep(timesleep)
                cookies_str = random.choice(cookies_strs)
                work_info = self.get_work_info(item, uk, cookies_str)

                work_res = user.copy()
                work_res_other = {
                    '账号昵称': user_info['账号昵称'],
                    '发布账号KEY': user_info['账号KEY'],
                    '标题': title,
                    '正文内容': content,
                    '话题标签': '未知',
                    '展现量': '未知',
                    '阅读量': '未知',
                    '点赞量': work_info['praise_num'],
                    '评论量': work_info['comment_num'],
                    '收藏量': work_info['collect'],
                    '转发量': work_info['forward_num'],
                    '回链': work_url,
                    '内容类型': '视频' if len(videos) > 0 else '图集',
                    '发布时间': publish_at,
                    '采集时间': timestamp_to_str(int(time.time() * 1000)),
                }
                work_res.update(work_res_other)


                if check_time_in_yesterday(CURRENT_SPIDER_TIME, work_res['发布时间']):
                    yesterday_uploads += 1
                if not recent_days == -1:
                    flag = check_time_in_7_days(CURRENT_SPIDER_TIME, work_res['发布时间'])
                    if not flag:
                        if i['is_top']:
                            continue
                        break_flag = False
                        break

                work_list.append(work_res)
                logger.info(f'爬取作品：work_res={work_res}')
            if not res['data']['hasMore'] == 1:
                break
            ctime = res['data']['query']['ctime']
            top_dynamic_id = res['data']['list'][0]['dynamic_id']
        user_res = user.copy()
        user_info['昨天发布数量'] = yesterday_uploads
        user_res.update(user_info)
        return {
            'user_res': user_res,
            'note_list': work_list
        }

    def all_all_users(self, path):
        df = pd.read_excel(path)
        datas = df.to_numpy().tolist()
        users = []
        for data in datas:
            url = str(data[5])
            if 'author.baidu' in url:
                users.append({
                    '账号编号': str(data[0]),
                    '序号': str(data[1]),
                    '平台': str(data[2]),
                    '赛道（一类）': data[3],
                    '赛道（二类）': data[4],
                    '账号链接': url
                })
        return users

    def save_to_excel(self, user_save_path, work_save_path, res):
        user_res = res['user_res']
        note_list = res['note_list']
        df1 = pd.DataFrame([user_res])
        df2 = pd.DataFrame(note_list)
        df1.to_excel(user_save_path, index=False)
        df2.to_excel(work_save_path, index=False)


    def main(self, spider_files, cookies_strs, timesleep, recent_days, print_error=False):
        error_users = []
        for spider_index, file_name in enumerate(spider_files):
            logger.info(f'开始爬取第 {spider_index + 1} 项目 {file_name} 的所有用户的所有发帖信息')
            # simple_file_name = validate_text(file_name)
            simple_file_name = '.'.join(file_name.split('.')[:-1])
            work_dir = os.path.abspath(os.path.dirname(__file__))
            base_path = os.path.abspath(os.path.join(work_dir, '..'))
            save_base_path = os.path.abspath(os.path.join(base_path, 'data', 'baidu', simple_file_name))
            user_save_base_path = os.path.abspath(os.path.join(save_base_path, 'user'))
            work_save_base_path = os.path.abspath(os.path.join(save_base_path, 'work'))
            if not os.path.exists(user_save_base_path):
                os.makedirs(user_save_base_path, exist_ok=True)
            if not os.path.exists(work_save_base_path):
                os.makedirs(work_save_base_path, exist_ok=True)
            logger.info(f'已经创建 {user_save_base_path} 和 {work_save_base_path} 文件夹')
            spider_file_path = os.path.abspath(os.path.join(base_path, 'input', file_name))
            users = self.all_all_users(spider_file_path)
            for index, user in enumerate(users):
                try:
                    user_url = user['账号链接']
                    if 'app_id' in user_url:
                        user_url = urllib.parse.unquote(user_url)
                        user_id = re.findall(r'context={"app_id":"(\d+)"', user_url)[0]
                        user_url = f'https://author.baidu.com/home/{user_id}'
                        user['账号链接'] = user_url

                    else:
                        # 使用re 提取 https://author.baidu.com/home/1812506351533473
                        user_id = re.findall(r'home/(\d+)', user_url)[0]

                    user_save_path = f'{user_save_base_path}/{user_id}.xlsx'
                    work_save_path = f'{work_save_base_path}/{user_id}.xlsx'
                    if os.path.exists(user_save_path) and os.path.exists(work_save_path):
                        logger.info(f'用户 {user_url} 的所有发帖信息已经爬取过')
                        continue
                    time.sleep(timesleep)
                    logger.info('-----------------------------------')
                    logger.info(f'开始爬取第 {spider_index + 1} 项目 {simple_file_name} 的第{index + 1}个用户 {user_url} 的所有发帖信息')
                    res = self.get_user_all_posted(user, user_url, cookies_strs, timesleep, recent_days)
                    self.save_to_excel(user_save_path, work_save_path, res)
                    logger.info(f'第 {spider_index + 1} 项目 {simple_file_name} 剩余用户数: {len(users) - index - 1}')
                    logger.info('-----------------------------------')
                except Exception as e:
                    logger.error(f'爬取用户 {user} 失败: {e}')
                    error_users.append({
                        'file_name': simple_file_name,
                        'user': user
                    })
            self.combine(user_save_base_path, simple_file_name, is_work=False)
            self.combine(work_save_base_path, simple_file_name, is_work=True)
        if print_error:
            logger.info(f'{CURRENT_SPIDER_TIME} 总结: 爬取失败用户数 {len(error_users)}')
            for error_user in error_users:
                logger.error(f'总结: 爬取用户 {error_user} 失败')
            logger.info(f'开始检查所有cookies是否有效')

    def check_cookies_alive(self, cookies_strs):
        user_url = 'https://author.baidu.com/home/1812506351533473'
        for cookie_index, cookies_str in enumerate(cookies_strs):
            try:
                res = self.get_user_info(user_url, cookies_str)
                logger.info(f'第 {cookie_index + 1 } 个cookie有效')
            except Exception as e:
                logger.error(f'第 {cookie_index + 1 } 个cookie失效: {e}, 请手动替换')

    def combine(self, save_base_path, simple_file_name, is_work):
        if is_work:
            all_file_path = f'{save_base_path}/{simple_file_name}_all_work.xlsx'
            if os.path.exists(all_file_path):
                os.remove(all_file_path)
            columns = ['账号编号', '序号', '平台', '赛道（一类）', '赛道（二类）', '账号链接', '账号昵称', '发布账号KEY', '标题',
                       '正文内容', '话题标签', '展现量', '阅读量', '点赞量', '评论量', '收藏量', '转发量', '回链', '内容类型',
                       '发布时间', '采集时间']
        else:
            all_file_path = f'{save_base_path}/{simple_file_name}_all_user.xlsx'
            if os.path.exists(all_file_path):
                os.remove(all_file_path)
            columns = ['账号编号', '序号', '平台', '赛道（一类）', '赛道（二类）', '账号链接', '账号昵称', '头像地址URL', '账号KEY', '粉丝数量',
                          '总发布量', '阅读/曝光数量', '点赞数量', '评论数量', '收藏数量', '昨天发布数量', '采集时间']
        all_excel = os.listdir(save_base_path)
        all_res = []
        for excel in all_excel:
            if excel.endswith('.xlsx'):
                df = pd.read_excel(f'{save_base_path}/{excel}', dtype=str)
                res = df.to_numpy().tolist()
                all_res.extend(res)

        df = pd.DataFrame(all_res, columns=columns)
        df.to_excel(all_file_path, index=False)

def job(print_error=False):
    baidu = BaiduApis()
    work_dir = os.path.abspath(os.path.dirname(__file__))
    env_path = os.path.join(work_dir, '..', 'env.yaml')
    env_path = os.path.abspath(env_path)
    with open(env_path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    baidu_config = config['platform']['baidu']
    timesleep = baidu_config['timesleep']
    recent_days = baidu_config['recent_days']
    cookies_strs = baidu_config['cookies_strs']
    spider_files = baidu_config['spider_files']
    baidu.main(spider_files, cookies_strs, timesleep, recent_days, print_error=print_error)
    if print_error:
        baidu.check_cookies_alive(cookies_strs)

def schedule_job():
    global CURRENT_SPIDER_TIME
    CURRENT_SPIDER_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    work_dir = os.path.abspath(os.path.dirname(__file__))
    base_path = os.path.abspath(os.path.join(work_dir, '..'))
    save_base_path = os.path.abspath(os.path.join(base_path, 'data', 'baidu'))
    logger.info(f'清理 {save_base_path} 下的所有文件和文件夹')
    # 清理save_base_path下的所有文件和文件夹
    for filename in os.listdir(save_base_path):
        file_path = os.path.join(save_base_path, filename)
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
        else:
            os.remove(file_path)
    job()
    job(print_error=True)


if __name__ == '__main__':
    # job()
    schedule_job()

    # schedule.every().monday.at("00:05").do(schedule_job)
    # schedule.every().tuesday.at("00:05").do(schedule_job)
    # schedule.every().wednesday.at("00:05").do(schedule_job)
    # schedule.every().thursday.at("00:05").do(schedule_job)
    # schedule.every().friday.at("00:05").do(schedule_job)
    #
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)