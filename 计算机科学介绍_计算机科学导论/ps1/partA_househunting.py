#!/usr/bin/env python
# -*- encoding: utf-8 -*-
''' 
@File    :   partA_househunting.py
@Time    :   2022/10/30 09:23:36
'''


def house_hunting(annaul_salary,portion_saved,total_cost,/):
    portion_down_payment = total_cost / 4   # 首付款

    current_saving = 0  # 当前储蓄
    month_salary = annaul_salary / 12 * portion_saved     # 每月固定薪水

    number_of_months = 0    # 所需月份数
    
    while True:
        return_on_invest = current_saving * 0.04 / 12   # 每月投资收入
        current_saving += (month_salary + return_on_invest)
        number_of_months += 1

        if current_saving >= portion_down_payment:
            break

    print(f"Number of months: {number_of_months}")


def main():
    try:
        annaul_salary = int(input("Enter your annual salary: "))
        portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
        total_cost = int(input("Enter the cost of your dream home: "))
        
        house_hunting(annaul_salary,portion_saved,total_cost)
        
    except TypeError as e:
        print(f"{e} \n please enter a correct parameter!")
        
    finally:
        print("Please keep up the good work")


if __name__ == "__main__":
    main()
