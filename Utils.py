def create_copy(cursor):
    ret_arr = list()
    for row in cursor:
        ret_arr.append(list(row))
    return ret_arr


def set_workers(workers, person):
    # for row in workers:
    #     print(row)
    # print()
    # for row in person:
    #     print(row)
    ret_arr = list()
    for item in person:
        worker_loc = find_in_list_of_list(workers, item[0])
        if worker_loc != None:
            # print(item, workers[worker_loc[0]])
            workers[worker_loc[0]].pop(2)
            # workers[worker_loc[0]].pop(2)
            # workers[worker_loc[0]].pop(2)
            ret_arr.append(item + workers[worker_loc[0]])
        # else:
        #     ret_arr.append(item)
        # print(item, worker_loc)
        # for row in workers:
        #     print(row)
    # for i in ret_arr:
    #     print(i)
    return ret_arr


def find_in_list_of_list(mylist, char):
    for sub_list in mylist:
        if char in sub_list:
            return (mylist.index(sub_list), sub_list.index(char))
    # raise ValueError("'{char}' is not in list".format(char=char))


def set_customers(customer, person):
    ret_arr = list()
    for item in person:
        customer_loc = find_in_list_of_list(customer, item[0])
        if customer_loc != None:
            customer[customer_loc[0]].pop(2)
            ret_arr.append(customer[item + customer_loc[0]].pop(2))
    return ret_arr


def set_orders(orders, order_line, products):
    ret_list = list()
    for item in order_line:
        temp = list()
        product_id_loc = find_in_list_of_list(products, item[1])
        order_loc = find_in_list_of_list(orders, item[0])
        for i in item[:2]:
            temp.append(i)
        temp.append(products[product_id_loc[0]][1])
        temp.append(item[2])
        for i in orders[order_loc[0]][1:]:
            temp.append(i)
        ret_list.append(temp)
    return ret_list


def set_storedproduct(stored_product, product):
    ret_list = list()
    for item in stored_product:
        product_loc = find_in_list_of_list(product, item[0])
        temp = list()
        temp.append(item[0])
        temp.append(product[product_loc[0]][1])
        for i in item[1:]:
            temp.append(i)
        ret_list.append(temp)
    return ret_list
