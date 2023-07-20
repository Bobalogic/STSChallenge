import datetime
from reqfunc import request_office_info


# def
MAX_INTERVALS = 2 # intervals between updates

MAX_CAPACITY = {} # max number of people in office
MAX_CAPACITY["Coimbra"] = 234
MAX_CAPACITY["Porto"] = 132
MAX_CAPACITY["Lisboa"] = 50






# init
time_stamp = datetime.datetime.now()
# for time measures
office_stamp = {}
office_stamp["Coimbra"] = time_stamp
office_stamp["Porto"] = time_stamp
office_stamp["Lisboa"] = time_stamp

# for people measure
office_people_count = {} # init as None
office_people_count["Coimbra"] = request_office_info(office="Coimbra")
office_people_count["Porto"] = request_office_info(office="Porto")
office_people_count["Lisboa"] = request_office_info(office="Lisboa")








def minute_dif(time1, time2):
	#[hour, second]
	dif = (time1[0] - time2[0])*60 + (time1[1] - time2[1])
	return abs(dif)


def selectbox_callback(st_object, st_state):
	chosen_office = st_state["_office_"] # current office


	new_time_stamp = datetime.datetime.now() # time stamp of request
	print(chosen_office)


	time1_hour_min = [new_time_stamp.hour, new_time_stamp.minute]
	time2_hour_min = [office_stamp[chosen_office].hour, office_stamp[chosen_office].minute]
	if minute_dif(time1_hour_min, time2_hour_min) >= MAX_INTERVALS: # this decides if there is an update based on dif of time
		office_stamp[chosen_office] = new_time_stamp



	st_object.write("Last update:")
	st_object.subheader(office_stamp[chosen_office].strftime("%H:%M"))


	# change session state
	st_state['_max_capacity_'] = MAX_CAPACITY[chosen_office] # update max capacity
	st_state['_people_count_'] = office_people_count[chosen_office]

	# prints
	print("Coimbra: {} {}".format(office_stamp["Coimbra"].strftime("%H:%M"), office_people_count["Coimbra"]))
	print("Porto: {} {}".format(office_stamp["Porto"].strftime("%H:%M"),office_people_count["Porto"]))
	print("Lisboa: {} {}".format(office_stamp["Lisboa"].strftime("%H:%M"), office_people_count["Lisboa"]))
	print("--------------------")



	






#print(minute_dif([9, 56], [10, 2]))
# check the difference in minutes and if its equal to 10 update