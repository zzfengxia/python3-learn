import re

str = """
account_num	accountNum
fans_num	fansNum
live_num	liveNum
live_duration	liveDuration
live_exposure_count	liveExposureCount
people_num	peopleNum
live_exposure_rate	liveExposureRate
average_view_time	averageViewTime
max_online_count	maxOnlineCount
live_digg_num	liveDiggNum
live_comment_num	liveCommentNum
add_follow_num	addFollowNum
fans_rate	fansRate
dy_msg_count	dyMsgCount
dy_msg_rate	dyMsgRate
live_card_icon_component_click_count	liveCardIconComponentClickCount
live_clue_num	liveClueNum
live_clue_num_xiaoxuehua	liveClueNumXiaoxuehua
live_clue_num_xiaofengche	liveClueNumXiaofengche
live_clue_num_sixin	liveClueNumSixin
add_wechat_num	addWechatNum
local_add_wechat_num	localAddWechatNum
video_num	videoNum
play_num	playNum
digg_num	diggNum
comment_num	commentNum
share_num	shareNum
cust_num	custNum
cust_num_drainage	custNumDrainage
cust_num_snowflake	custNumSnowflake
cust_num_ai	custNumAi
cust_num_interaction	custNumInteraction
cust_num_homepage	custNumHomepage
cust_num_live	custNumLive
cust_num_video	custNumVideo
cust_num_tool	custNumTool
cust_num_others	custNumOthers
chat_user_num	chatUserNum
ai_reception_num	aiReceptionNum
ai_reception_ratio	aiReceptionRatio
ai_clue_num	aiClueNum
ai_clue_ratio	aiClueRatio
not_ai_reception_num	notAiReceptionNum
not_ai_reception_ratio	notAiReceptionRatio
not_ai_clue_num	notAiClueNum
not_ai_clue_ratio	notAiClueRatio
cust_barrage_num	custBarrageNum
ai_reply_barrage_num	aiReplyBarrageNum
barrage_broadcast_num	barrageBroadcastNum
strategy_reach_user_num	strategyReachUserNum
strategy_reply_user_num	strategyReplyUserNum
strategy_clue_user_num	strategyClueUserNum
live_digg_people_num	liveDiggPeopleNum
live_digg_people_ratio	liveDiggPeopleRatio
live_comment_people_num	liveCommentPeopleNum
live_comment_people_ratio	liveCommentPeopleRatio
live_share_people_num	liveSharePeopleNum
live_share_people_ratio	liveSharePeopleRatio
live_interact_people_num	liveInteractPeopleNum
live_interact_people_ratio	liveInteractPeopleRatio
join_fans_clue_num	joinFansClueNum
join_fans_clue_ratio	joinFansClueRatio
"""

field_str = """
period_date
tenant_id
account_id
platform_type
fans_num
video_num
play_num
share_num
comment_num
digg_num
interact_num
forward_num
download_num
live_num
live_num_1
live_num_2
live_num_3
live_num_4
live_num_5
look_num
people_num
live_duration
average_view_time
max_online_count
live_digg_num
live_digg_people_num
live_comment_num
live_comment_people_num
live_share_people_num
live_interact_people_num
join_fans_clue_num
live_exposure_count
dy_msg_count
live_card_icon_component_show_count
live_card_icon_component_click_count
avg_remain_index
avg_flow_rate
avg_traffic
live_clue_num
live_clue_num_xiaoxuehua
live_clue_num_xiaofengche
live_clue_num_sixin
add_follow_num
add_wechat_num
local_add_wechat_num
cust_num
cust_num_drainage
cust_num_snowflake
cust_num_ai
cust_num_interaction
cust_num_homepage
cust_num_live
cust_num_video
cust_num_tool
cust_num_others
cust_barrage_num
ai_reply_barrage_num
barrage_broadcast_num
"""
def parse_str():
    # 按行解析文本
    lines = str.splitlines()

    field_list = []
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        line_data = re.split(r'\s+', line)
        field_list.append(line_data[0])

    ori_list = []
    ori_lines = field_str.splitlines()
    for line in ori_lines:
        line = line.strip()
        if len(line) == 0:
            continue
        line_data = re.split(r'\s+', line)
        ori_list.append(line_data[0])

    print(f'是否一致：{field_list.sort() == ori_list.sort()}')

parse_str()