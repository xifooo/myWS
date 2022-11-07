#!/usr/bin/env python
# -*- encoding: utf-8 -*-
''' 
@File    :   partC_best_saving_rate.py
@Time    :   2022/10/30 11:04:35
'''

'''
36个月内攒够首付的钱(start_salary), 攒钱的过程中算上每半年的加薪与每月的投资收入
存款用来支付首付款, 两者差距不超过100刀
最后算出为一套100万美元的房子支付首付款的最佳储蓄率
'''

def best_saving_rate(start_salary):
    total_cost = 100_0000
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
    start_salary = int(input("Enter the starting salary: "))
    
    best_saving_rate(start_salary)
    # best_saveing_rate = int(input("Best saving rate: "))
    # start_salary = int(input("Enter the starting salary: "))
    ...


if __name__ == "__main__":
    main()
