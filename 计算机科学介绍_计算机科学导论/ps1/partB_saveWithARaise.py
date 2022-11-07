#!/usr/bin/env python
# -*- encoding: utf-8 -*-
''' 
@File    :   partB_saveWithARaise.py
@Time    :   2022/10/30 10:32:54
'''

def house_hunting(annaul_salary, portion_saved, total_cost, semi_annual_raise,/):
    """_summary_

    Args:
        annaul_salary (int): 年薪
        portion_saved (float): 每月存下的工资比例
        total_cost (int): 房子全款
        semi_annual_raise (float): 每半年的涨薪幅度
    """
    portion_down_payment = total_cost / 4   # 首付款
    
    current_saving = 0  # 当前储蓄
    month_salary = annaul_salary / 12 * portion_saved     # 每月固定薪水
    number_of_months = 0    # 所需月份数
    
    while True:
        return_on_invest = current_saving * 0.04 / 12   # 每月投资收入
        current_saving += (month_salary + return_on_invest)
        number_of_months += 1
        
        if not (number_of_months % 6):
            month_salary += semi_annual_raise * month_salary
            continue
        
        if current_saving >= portion_down_payment:
            break

    print(f"Number of months: {number_of_months}")


def main():
    try:
        annaul_salary = int(input("Enter your annual salary: "))
        portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
        total_cost = int(input("Enter the cost of your dream home: "))
        semi_annual_raise = float(input("Enter the semi-annual raise, as a decimal: "))
        house_hunting(annaul_salary,portion_saved,total_cost,semi_annual_raise)
        
    except TypeError as e:
        print(f"{e} \n please enter a correct parameter!")
        
    finally:
        print("Please keep up the good work")


if __name__ == "__main__":
    main()



def main():

    portion_down_payment = 0.25
    #invest retrun  current_savings*r/12
    r = 0.04

    total_cost = 1000000
    semi_annual_raise= 0.07

    annual_salary = int(input("Enter your annual salary:  "))
    #dedicate a certain amount of your salary each month to saving forthe down payment.

    #cant pay
    if annual_salary < 62523 :
        print("it is not possible to pay down payment in three years")
        return


    rate_max = 10000
    rate_min = 0
    step = 0

    current_savings = 0
    while abs(total_cost * portion_down_payment-current_savings ) > 100 :
        step += 1
        portion_saved = int((rate_max + rate_min)/2 +0.5)
        month_salary_portion=annual_salary*(portion_saved/10000)/12

        current_savings = 0
        for i in range(1,37):
            current_savings += month_salary_portion + (current_savings*r/12 )
            if i%6 == 0:
                month_salary_portion = month_salary_portion * (1 + semi_annual_raise)

        if current_savings < total_cost * portion_down_payment: #存少了
            rate_min = portion_saved
        else:
            rate_max = portion_saved

    print(f"best saving rate:{ portion_saved /10000}")
    print("steps in bisecton search:", step)


main()