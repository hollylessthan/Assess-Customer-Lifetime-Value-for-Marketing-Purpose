
## Home Alarm CLV


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# %%
churn = pd.DataFrame(
    {
        "autopay": [0.032, 0.070, 0.097, 0.103, 0.095, 0.078, 0.069, 0.059, 0.053],
        "no_autopay": [0.084, 0.122, 0.162, 0.154, 0.134, 0.120, 0.111, 0.096, 0.086],
    }
)
churn


# ### Calculate CLV for autopay customers


# #### list your assumptions here
# Assume the revenue is received and calculated at the end of the year and the revenue for the first year is 480 dollars with an annual growth rate of 3 % for the following years.
# The assumption for the autopay customers is listed as the `auto_assum` table below.


auto_assum = pd.DataFrame({"Item": ["Annual discount rate", "Monthly discount rate", "Annual growth rate", "Annual revenue first Year", "Cost of service", "Annual direct marketing cost", "Installation cost"], "Number": [0.1, ((1+0.1)**(1/12)-1), 0.03, 480, 0.15, 0.05, 492-195]})
print(auto_assum)

auto_CLV = pd.DataFrame({"Item":["Revenues", "Product/Service Costs", "Marketing Costs", "Customer Profit", "Churn / Attrition rate", "Prob. of being active for the following year", "Profit expected on average", "Discount #", "Present value of Expected Profits", "CLV"]})
auto_CLV.set_index('Item')
#annual clv

auto_CLV["Start of LTV Calc."] = auto_CLV["Year1"] = auto_CLV["Year2"] = auto_CLV["Year3"] = auto_CLV["Year4"] = auto_CLV["Year5"] = auto_CLV["Year6"] = auto_CLV["Year7"] = auto_CLV["Year8"]= auto_CLV["Year9"]= [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
auto_CLV.iloc[0, 2:] = [480 * (1+ auto_assum.loc[2, "Number"])**i for i in range(len(auto_CLV)-1)]
auto_CLV.iloc[1, 2:] = auto_CLV.iloc[0, 2:] * auto_assum.loc[4, "Number"]
auto_CLV.iloc[2, 2:] = auto_CLV.iloc[0, 2:] * auto_assum.loc[5, "Number"]
auto_CLV.iloc[3, 2:] = auto_CLV.iloc[0, 2:]  - (auto_CLV.iloc[1, 2:] + auto_CLV.iloc[2, 2:])
auto_CLV.iloc[4, 2:] = churn["autopay"]
for i in range(len(auto_CLV)-1):
    i = i+ 2
    auto_CLV.iloc[5, i] = auto_CLV.iloc[5, i-1] * (1 - auto_CLV.iloc[4, i])
    auto_CLV.iloc[7, i] = auto_CLV.iloc[7, i-1] + 1
    auto_CLV.iloc[6, i] = auto_CLV.iloc[3, i] * auto_CLV.iloc[5, i-1]
    auto_CLV.iloc[8, i] = auto_CLV.iloc[6, i]/ ((1 + auto_assum.loc[0, "Number"])** auto_CLV.iloc[7, i])
    auto_CLV.iloc[9, i] = auto_CLV.iloc[9, i - 1] + auto_CLV.iloc[8, i]


auto_CLV


# ### Calculate CLV for non-autopay customers


# Assume the revenue is received and calculated at the end of the year and the revenue for the first year is 480 dollars with an annual growth rate of 3 % for the following years.
# The assumption for the non-autopay customers is listed as the `nonauto_assum` table below.
# The clv for the non-autopay customers is calculated and presented as the `nonauto_CLV` table.


nonauto_assum = pd.DataFrame({"Item": ["Annual discount rate", "Monthly discount rate", "Annual growth rate", "Annual revenue first Year", "Cost of service", "Annual direct marketing cost", "Installation cost"], "Number": [0.1, ((1+0.1)**(1/12)-1), 0.03, 480, 0.15, 0.05, 492-195]})
print(nonauto_assum)

nonauto_CLV = pd.DataFrame({"Item":["Revenues", "Product/Service Costs", "Marketing Costs", "Customer Profit", "Churn / Attrition rate", "Prob. of being active for the following year", "Profit expected on average", "Discount #", "Present value of Expected Profits", "CLV"]})
nonauto_CLV.set_index('Item')
#annual clv
nonauto_CLV["Start of LTV Calc."] = nonauto_CLV["Year1"] = nonauto_CLV["Year2"] = nonauto_CLV["Year3"] = nonauto_CLV["Year4"] = nonauto_CLV["Year5"] = nonauto_CLV["Year6"] = nonauto_CLV["Year7"] = nonauto_CLV["Year8"]= nonauto_CLV["Year9"]= [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
nonauto_CLV.iloc[0, 2:] = [480 * (1+ nonauto_assum.loc[2, "Number"])**i for i in range(len(nonauto_CLV)-1)]
nonauto_CLV.iloc[1, 2:] = nonauto_CLV.iloc[0, 2:] * nonauto_assum.loc[4, "Number"]
nonauto_CLV.iloc[2, 2:] = nonauto_CLV.iloc[0, 2:] * nonauto_assum.loc[5, "Number"]
nonauto_CLV.iloc[3, 2:] = nonauto_CLV.iloc[0, 2:]  - (nonauto_CLV.iloc[1, 2:] + nonauto_CLV.iloc[2, 2:])
nonauto_CLV.iloc[4, 2:] = churn["no_autopay"]
for i in range(len(nonauto_CLV)-1):
    i = i+ 2
    nonauto_CLV.iloc[5, i] = nonauto_CLV.iloc[5, i-1] * (1 - nonauto_CLV.iloc[4, i])
    nonauto_CLV.iloc[7, i] = nonauto_CLV.iloc[7, i-1] + 1
    nonauto_CLV.iloc[6, i] = nonauto_CLV.iloc[3, i] * nonauto_CLV.iloc[5, i-1]
    nonauto_CLV.iloc[8, i] = nonauto_CLV.iloc[6, i]/ ((1 + nonauto_assum.loc[0, "Number"])** nonauto_CLV.iloc[7, i])
    nonauto_CLV.iloc[9, i] = nonauto_CLV.iloc[9, i - 1] + nonauto_CLV.iloc[8, i]

nonauto_CLV



# ### Create a line graph of CLV for both autopay and non-autopay customer 

clv_compar = pd.DataFrame({"autoCLV": auto_CLV.iloc[9, 2:], "nonautoCLV": nonauto_CLV.iloc[9, 2:]})
clv_compar["autoCLV"] = clv_compar["autoCLV"].astype(float)
clv_compar["nonautoCLV"] = clv_compar["nonautoCLV"].astype(float)

sns.relplot(data=clv_compar, kind="line")
plt.show()


# ### Create a line graph of the retention rate for both autopay and non-autopay customer 

ret_compar = pd.DataFrame({"autoCLV": auto_CLV.iloc[5, 2:], "nonautoCLV": nonauto_CLV.iloc[5, 2:]})
ret_compar["autoCLV"] = ret_compar["autoCLV"].astype(float)
ret_compar["nonautoCLV"] = ret_compar["nonautoCLV"].astype(float)
ret_compar.info()




#ret_compar = pd.DataFrame({"auto_retention": 1 - churn["autopay"], "nonauto_retention": 1 - churn["no_autopay"]})

sns.relplot(data=ret_compar, kind="line")
plt.show()

# ### Calculate the maximum amount to spend on autopay incentives

max_pay = auto_CLV.iloc[9, -1] - nonauto_CLV.iloc[9, -1]# the difference of pv of clv in year 9 for nonauto and auto pay
#auto_assum.loc[6, "Number"]

# assume the installation cost has been charge for every exisiting customer

print(f"Maxium amount to spend on autopay incentives is {max_pay.round(2)}")


# ### Suggested marketing actions
#
# Suggest three marketing actions Home Alarm should consider to convert existing customers to autopay who are about to start their second year with Home Alarm.

# 1. provide the customers who continue using their service for the next year with Home Alarm discount coupons that can be used to buy other products of Home Alarm. The total value of the coupon should be no more than churn rate * per profit of that year.
# 2. provide customer survey to the first year customers for improvement suggestion. Use those suggestion to adjust their service model for the next year. Customers who provide the survey can receive a discount of 1% for the service of the next year.
# 3. use email marketing to promote their service with no more than churn rate * per profit of that year  on the marketing cost.
#

