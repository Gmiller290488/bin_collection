import urllib.request

from icalendar import Calendar

bin_event_list = []
unordered_date_list = []
ordered_date_list = []


def get_bin_data():

    req = urllib.request.Request('https://s3-eu-west-1.amazonaws.com/fs-downloads/GM/binfeed.ical')
    response = urllib.request.urlopen(req)
    data = response.read()
    return data


def sort_lists_of_bin_data(data):

    index = 0
    cal = Calendar.from_ical(data)
    for event in cal.walk('vevent'):
        date = event.decoded('dtstart')
        bin_event_list.append([event.decoded('summary')])
        ordered_date_list.append([date.strftime('%m/%d/%Y'), index])
        unordered_date_list.append(date.strftime('%m/%d/%Y'))
        index += 1
    ordered_date_list.sort()


def count_the_mode_date_occurrences(date_list):

    temp_count = 1
    count = 1
    for i in range(len(date_list)-1):
        temp = date_list[i][0]
        if temp == date_list[i+1][0]:
            temp_count += 1
            if temp_count > count:
                count = temp_count
        else:
            temp_count = 1
    return count


def find_all_occurrences_of_input_date(date_input):

    positions_of_date_input_in_unordered_list = []
    for date_with_index in ordered_date_list:
        if date_with_index[1] == unordered_date_list.index(date_input):
            index_of_date_input_in_ordered_list = ordered_date_list.index(date_with_index)
            positions_of_date_input_in_unordered_list.append(ordered_date_list[index_of_date_input_in_ordered_list][1])
            for i in range(count):
                if (ordered_date_list[index_of_date_input_in_ordered_list] == ordered_date_list[index_of_date_input_in_ordered_list+i]) & (i+1 < len(ordered_date_list)):
                    positions_of_date_input_in_unordered_list.append(ordered_date_list[index_of_date_input_in_ordered_list+1][1])
    return positions_of_date_input_in_unordered_list


# def is_date_valid():
#     while True:
#         date = input("enter date in format [mm/dd/YYYY]: ")
#         try:
#             valid_date = time.strptime(date, '%m/%d/%Y')
#             if is_date_on_calendar(date):
#                 return date
#
#
#         except ValueError:
#             print('Invalid date form!  Please use the format mm/dd/YYYY')
#             continue
#
#
# def is_date_on_calendar(date):
#     try:
#
#         yes = unordered_date_list.index(date)
#         print(yes)
#         return True
#     except ValueError:
#         print("No collection on this day")


def print_results(indexs, date_input):

    for index in indexs:
        print((bin_event_list[index][0].decode()), "on", date_input)


bin_data = get_bin_data()

date_input = input("enter date in format [mm/dd/YYYY]: ")
sort_lists_of_bin_data(bin_data)
count = count_the_mode_date_occurrences(ordered_date_list)
indexs = find_all_occurrences_of_input_date(date_input)
print_results(indexs, date_input)