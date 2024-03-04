import streamlit as st
import json
from datetime import datetime

# 文件路径
order_filename = 'coffee_orders.json'
feedback_filename = 'feedbacks.json'
products = {
    '意式拿铁': '浓缩咖啡 + 牛奶',
    '燕麦拿铁': '浓缩咖啡 + 燕麦奶',
    '生椰拿铁': '浓缩咖啡 + 厚椰乳',
    '美式咖啡': '浓缩咖啡 + 水',
    # '生椰美式': '浓缩咖啡 + 椰子水',
    '每日鲜萃': '现磨咖啡豆，美式滴滤壶现煮制作，每日上午提供，无需下单，咖啡壶自取',
    # '每日冷萃': '现磨咖啡豆，冷萃壶加水浸泡12小时得到，周二至周五提供，无需下单，冰箱内自取',
}


def load_json(filename):
    try:
        with open(filename, 'r') as file:
            outputs = json.load(file)
    except FileNotFoundError:
        outputs = {}
    return outputs

def save_json(outputs, filename):
    with open(filename, 'w') as file:
        json.dump(outputs, file)

def reset_orders_if_new_day():
    try:
        with open('last_reset_date.txt', 'r') as file:
            last_reset_date = file.read().strip()
    except FileNotFoundError:
        last_reset_date = datetime.now().strftime('%Y-%m-%d')
        with open('last_reset_date.txt', 'w') as file:
            file.write(last_reset_date)
            
    current_date = datetime.now().strftime('%Y-%m-%d')
    if current_date != last_reset_date:
        orders = {}
        save_json(orders, order_filename)
        with open('last_reset_date.txt', 'w') as file:
            file.write(current_date)

def main():
    # 检查是否需要重置订单
    reset_orders_if_new_day()
    
    # 加载当前订单、留言
    orders = load_json(order_filename)
    feedbacks = load_json(feedback_filename)

    with st.sidebar:
        image_path = 'cafe logo.jpg'
        st.image(image_path, width=120)
        st.title('欢迎您光临比奇堡咖啡屋')
        st.markdown('---')
        st.markdown('我们的宗旨是：\n- 提供好喝且便宜的咖啡 \n- 公益项目，绝对不赚钱，尽量不收费\n- 多喝咖啡，好事发生')

    st.title('比奇堡咖啡点单系统')
    tab1, tab2, tab3 = st.tabs(["我要点单", "我要留言", "我要打赏"])

    with tab1:
        user_id = st.text_input(r"$\bf请问怎么称呼您：$")
        coffee_choice = st.radio(r"$\bf请选择你想要的咖啡：$", products.keys(),
                                 captions=products.values()) #, horizontal=True)

        if st.button(':green[下单]:white_check_mark:'):
            if len(user_id) == 0:
                st.error('输入的用户名为空，请重新输入')
            else:
                order_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                orders[order_time] = (user_id, coffee_choice)
                save_json(orders, order_filename)
                st.success(f"{user_id} 已成功点单 {coffee_choice} 咖啡！")

        if st.button(':red[清空我的订单]:x:'):
            if len(user_id) == 0:
                st.error('输入的用户名为空，请重新输入')
            else:
                new_orders = orders.copy()
                for order_id, values in orders.items():
                    if values[0] == user_id:
                        del new_orders[order_id]
                save_json(new_orders, order_filename)
                st.success(f"{user_id} 已成功清空所有订单，如需要请重新点单哦~")
                st.rerun()

        st.markdown('---')
        st.write(r"$\bf当前咖啡点单数量：$")
        for coffee, count in orders.items():
            st.write(f"{coffee}: {count}")

    with tab2:
        feedback = st.text_area("欢迎留言，鼓励或者建议，都让比奇堡咖啡做得更好：")
        if st.button(':green[留言]'):
            if len(feedback) == 0:
                st.error('输入的留言为空，请重新输入')
            else:
                feedback_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                feedbacks[feedback_time] = (user_id, feedback)
                save_json(feedbacks, feedback_filename)
                st.success(f"谢谢您的宝贵留言，我们会继续努力，祝您天天开心，美事连连！")

    with tab3:
        col1, col2 = st.columns(2)
        col1.write("感谢您对比奇堡咖啡的认可和支持，所有的打赏收入将全部用于咖啡屋的日常经营，"
                   "包括购买咖啡豆、牛奶和滤纸等，期待为您奉上一杯更好的咖啡！")
        col2.image('赞赏码.jpg', width=320)


if __name__ == "__main__":
    main()
