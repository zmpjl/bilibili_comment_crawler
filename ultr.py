import requests
import jieba
import re


def get_bilibili_comments(oid):
    url_template = "https://api.bilibili.com/x/v2/reply/main?csrf=40a227fcf12c380d7d3c81af2cd8c5e8&mode=3&next={}&oid={}&plat=1&type=1"

    header = {
        "user-agent": "替换成自己的user-agent1",
        "cookie": "替换成自己的请求头cookie中的fingerprint"
    }

    comments = []
    pre_comment_length = 0

    for i in range(200):  # 尝试获取前200页的评论
        url = url_template.format(i, oid)  # 使用format来设置页数和oid
        response = requests.get(url=url, headers=header)
        if response.status_code == 200:
            json_data = response.json()
            if 'data' not in json_data or 'replies' not in json_data['data']:
                print("没有更多的评论或获取评论出错")
                break
            replies = json_data["data"]["replies"]
            if not replies:
                print("评论已经爬取完毕")
                break
            for content in replies:
                comments.append(content["content"]["message"])

            print("搜集到{}条评论".format(len(comments)))

            # 如果本次获取的评论数量没有增加，则判断评论已经获取完毕，停止循环
            if len(comments) == pre_comment_length:
                print("爬虫退出！！！")
                break
            else:
                pre_comment_length = len(comments)
        else:
            print(f"请求失败，HTTP 状态码：{response.status_code}")
            break
    # 使用jieba进行分词处理
    segmented_comments = []
    for comment in comments:
        segmented_comments.append(" ".join(jieba.cut(comment)))
    # 将评论写入文件
    # with open(f"bilibili_comments_oid_{oid}.txt", "w", encoding="utf-8") as fp:
    #     for c in comments:
    #         fp.write(c + "\n")
    with open(f"bilibili_comments_Bv_{bv_input}_segmented.txt", "w", encoding="utf-8") as fp:
        for c in segmented_comments:
            fp.write(c + "\n")


# 去除不必要的符号
def clean_comment(comment):
    # 正则表达式匹配需要去除的字符
    pattern = r"\[.+?\]|[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、～~@#￥%……&*（）：《》“”‘’]+"
    comment = re.sub(pattern, "", comment)  # 去除匹配的字符

    return comment


# 通过bv号获取oid
def get_oid_from_bv(bv):
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bv}"
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        if 'data' in json_data:
            oid = json_data['data']['aid']
            return oid
        else:
            print("未能找到对应的 oid")
    else:
        print(f"请求失败，HTTP 状态码：{response.status_code}")
    return None

if __name__ == "__main__":
    bv_input = input("请输入视频的BV号：")
    oid = get_oid_from_bv(bv_input)
    if oid:
        get_bilibili_comments(oid)
    else:
        print("无法获取oid，爬取评论失败")

