def dis_fun_prior(item):
    pdis = 1
    if item.get('click_time')==None and item.get('open_time')==None:
        pdis = -1
    try:
        #number_of_days = (datetime.now() - item.get('signup_time')).days
        number_of_days = (now - item.get('signup_time')).days
	if float(number_of_days)/7 <= 2:
            pdis = 10
    except Exception:
        n=1
    try:
        opens_keys = item.get('daily_open').keys()
        for key in opens_keys:
            date_diff = (now - datetime.strptime(key, '%y%m%d')).days
            if (float(date_diff)/ET >= 1) and (float(date_diff)/ET <= 2):
                pdis = 0
    except Exception:
        n = 1

    return pdis

    
