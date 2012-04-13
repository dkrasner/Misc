def dis_fun(item):
    dis = 1
    if item.get('click_time')==None and item.get('open_time')==None:
        dis = -1
    try:
        #number_of_days = (datetime.now() - item.get('signup_time')).days
        number_of_days = (now - item.get('signup_time')).days
	if float(number_of_days)/7 <= 2:
            dis = 10
    except Exception:
        n=1
    try:
        opens_keys = item.get('daily_open').keys()
        for key in opens_keys:
            date_diff = (now - datetime.strptime(key, '%y%m%d')).days
            if float(date_diff)/ET <= 1:
                dis = 0
    except Exception:
        n = 1

    return dis

    
