def handler(lst, data):
    print(lst)
    data_out = []

    for i in data:
        if i not in lst:
            data_out.append(i)
            lst.append(i)

    return lst, data_out


def prepare_mes(data):
    data_dict = {}
    for i, v in enumerate(data):
        lst_data = []
        lst_data.append(v['name'])

        url = f"https://hh.ru/vacancy/{v['id']}"
        lst_data.append(url)

        time = v['published_at']
        time = time[: 10] + ' ' + time[11: 16]
        lst_data.append(time)

        if v['salary']:
            lst_data.append(f"От {v['salary']['from']} до {v['salary']['from']} {v['salary']['currency']}")

        data_dict[i] = lst_data

    return data_dict
