#!/usr/bin/env python
# coding: utf-8

# # 1、Import Data

# In[1]:


import pandas as pd
import statsmodels.stats.api as sms
from termcolor import colored, cprint
import statsmodels.formula.api as smf
import numpy as np
import scipy.stats as stats


# In[2]:


## Import Dataset ##

# read excel
file_path = '/Users/sarah/Desktop/Aeon combine dataset.xlsx'
excel_file = pd.ExcelFile(file_path)

# create empty dataframe
combined_df = pd.DataFrame()

# read each sheet and combined to combined_df
for sheet_name in excel_file.sheet_names:
    # read each sheet first cell
    first_cell = pd.read_excel(excel_file, sheet_name=sheet_name, nrows=1, header=None).iloc[0, 0]
    
    # read "Non Salesday" and "非繁忙時段"
    sales_day = 'No' if 'Non Salesday' in str(first_cell) else 'Yes'
    peak = 'No' if '非繁忙時段' in str(first_cell) else 'Yes'
    
    # read sheet data from the second row
    df = pd.read_excel(excel_file, sheet_name=sheet_name, header=1)
    
    # add PEAK and SALES_DAY columns
    df['PEAK'] = peak
    df['SALES_DAY'] = sales_day
    
    # combined all datasets
    combined_df = pd.concat([combined_df, df], ignore_index=True)

# creat a new combined excel
output_file_path = 'Aeon combine dataset-2.xlsx'
combined_df.to_excel(output_file_path, index=False)


# In[3]:


## Adding Member & SALES column ##

# define member or non-member with a new column "MEMBER"
member = []
for i in range(len(combined_df)):
    if pd.isna(combined_df["會員ID (N)"][i]) == True:
        member.append("No")
    else:
        member.append("Yes")
        
combined_df["MEMBER"] = member

# calculating the sum of product sales for each transaction "SALES"
sales = []
for i in range(len(combined_df)):
    product_sales = combined_df['銷售價'][i]*combined_df['數量'][i]
    sales.append(product_sales)
    
combined_df["SALES"] = sales

# add PB column 
pb = []
for i in range(len(combined_df)):
    if combined_df['商品名稱'][i].startswith('TV') == True:
        pb.append("PB")
    else:
        pb.append("Non-PB")
combined_df["PB"] = pb

combined_df


# # 2、Sales Analysis

# In[4]:


# sales of PB and Non-PB goods
combined_df.groupby(["PB"])["SALES"].sum().to_frame().rename(index={"PB": "PB"})


# In[5]:


PBsales_ratio = round((combined_df.loc[combined_df["PB"]=="PB"]["SALES"].sum() / combined_df["SALES"].sum()) * 100, 2)
print(f"The sales percentage of PB is {PBsales_ratio}%.")


# ## 2.1 Sales analysis by stores

# In[6]:


# calculate PB and Non-PB Quantity
pivot_df = combined_df.groupby(["門店編碼", "PB"]).agg({"數量": "sum"})     .pivot_table(index="門店編碼", columns="PB", values="數量").rename_axis("QUANTITY", axis=1)

# calculate sales by stores
pivot_df['Total_Sales_Quantity'] = pivot_df.sum(axis=1)

# calculate % of PB in total sales by stores 
pivot_df['% of PB Sales Quantity to Total'] = (pivot_df['PB'] / pivot_df['Total_Sales_Quantity']) * 100

pivot_df = pivot_df[['Non-PB', 'PB', 'Total_Sales_Quantity', '% of PB Sales Quantity to Total']]
pivot_df


# In[7]:


# calculate PB and Non-PB Sales
pivot_df = combined_df.groupby(["門店編碼", "PB"]).agg({"SALES": "sum"})     .pivot_table(index="門店編碼", columns="PB", values="SALES").rename_axis("SALES", axis=1)

# calculate sales by stores
pivot_df['Total_Sales'] = pivot_df.sum(axis=1)

# calculate % of PB in total sales by stores 
pivot_df['% of PB Sales to Total'] = (pivot_df['PB'] / pivot_df['Total_Sales']) * 100

pivot_df = pivot_df[['Non-PB', 'PB', 'Total_Sales', '% of PB Sales to Total']]
pivot_df


# Store 3 has the highest % of PB sales quantity to total, and also to the sales. 

# ## 2.2 Sales analysis by department

# ### 2.2.1 General

# In[8]:


# calculate PB and Non-PB Quantity
pivot_df = combined_df.groupby(["DEPARTMENT名稱", "PB"]).agg({"數量": "sum"})     .pivot_table(index="DEPARTMENT名稱", columns="PB", values="數量").rename_axis("QUANTITY", axis=1)

# calculate sales by department 
pivot_df['Total_Sales_Quantity'] = pivot_df.sum(axis=1)

# calculate % of PB in total sales by department 
pivot_df['% of PB Sales Quantity to Total'] = (pivot_df['PB'] / pivot_df['Total_Sales_Quantity']) * 100

pivot_df = pivot_df[['Non-PB', 'PB', 'Total_Sales_Quantity', '% of PB Sales Quantity to Total']]
pivot_df


# In[9]:


# calculate PB and Non-PB Sales
pivot_df = combined_df.groupby(["DEPARTMENT名稱", "PB"]).agg({"SALES": "sum"})     .pivot_table(index="DEPARTMENT名稱", columns="PB", values="SALES").rename_axis("SALES", axis=1)

# calculate sales by stores
pivot_df['Total_Sales'] = pivot_df.sum(axis=1)

# calculate % of PB in total sales by stores 
pivot_df['% of PB Sales to Total'] = (pivot_df['PB'] / pivot_df['Total_Sales']) * 100

pivot_df = pivot_df[['Non-PB', 'PB', 'Total_Sales', '% of PB Sales to Total']]
pivot_df


# FASHION department has the highest % of PB Sales Quantity to Total, and the same as in sales.

# ### 2.2.2  HOUSEHOLD & EA

# #### 2.2.2.1 Quantity VS Sales

# In[10]:


# calculate PB and Non-PB Quantity
pivot_df = combined_df.loc[combined_df["DEPARTMENT名稱"] == "HOUSEHOLD & EA"].groupby(["SECTION名稱", "PB"]).agg({"數量": "sum"})     .pivot_table(index="SECTION名稱", columns="PB", values="數量").rename_axis("QUANTITY", axis=1)

# calculate sales by department 
pivot_df['Total_Sales_Quantity'] = pivot_df.sum(axis=1)

# calculate % of PB in total sales by department 
pivot_df['% of PB Sales Quantity to Total'] = (pivot_df['PB'] / pivot_df['Total_Sales_Quantity']) * 100

pivot_df = pivot_df[['Non-PB', 'PB', 'Total_Sales_Quantity', '% of PB Sales Quantity to Total']]
pivot_df


# In[11]:


# calculate PB and Non-PB Sales
pivot_df = combined_df.loc[combined_df["DEPARTMENT名稱"] == "HOUSEHOLD & EA"].groupby(["SECTION名稱", "PB"]).agg({"SALES": "sum"})     .pivot_table(index="SECTION名稱", columns="PB", values="SALES").rename_axis("SALES", axis=1)

# calculate sales by stores
pivot_df['Total_Sales'] = pivot_df.sum(axis=1)

# calculate % of PB in total sales by stores 
pivot_df['% of PB Sales to Total'] = (pivot_df['PB'] / pivot_df['Total_Sales']) * 100

pivot_df = pivot_df[['Non-PB', 'PB', 'Total_Sales', '% of PB Sales to Total']]
pivot_df


# In "HOUSEHOLD & EA" department, the ratio of PB sales quantity in FURNITURE & INTERIOR section is the highest, but HOUSEKEEPING section has the highest ratio of PB sales.

# #### 2.2.2.2 Top 10 products in  HOUSEHOLD & EA

# In[12]:


# Top 10 in general 
combined_df.loc[combined_df["DEPARTMENT名稱"] == "HOUSEHOLD & EA"].groupby(by="商品名稱").agg({"SECTION名稱": "first", "數量": "sum"}).sort_values(by="數量", ascending=False).head(10)


# In[13]:


# Top 10 in PB Brand 
combined_df[(combined_df["DEPARTMENT名稱"] == "HOUSEHOLD & EA") & (combined_df["PB"] == "PB")].groupby(by="商品名稱").agg({"SECTION名稱": "first", "數量": "sum"}).sort_values(by="數量", ascending=False).head(10)


# In[14]:


# Top 10 in non-PB Brand
combined_df[(combined_df["DEPARTMENT名稱"] == "HOUSEHOLD & EA") & (combined_df["PB"] == "Non-PB")].groupby(by="商品名稱").agg({"SECTION名稱": "first", "數量": "sum"}).sort_values(by="數量", ascending=False).head(10)


# In "HOUSEHOLD & EA" department, 法國雙飛人 藥水 sold quantity most.

# #### 2.2.2.3 Top 5 products by section 

# In[28]:


# get data when DEPARTMENT = "HOUSEHOLD & EA"
household_df = combined_df[combined_df["DEPARTMENT名稱"] == "HOUSEHOLD & EA"]

# count by each section & item
grouped_df = household_df.groupby(['SECTION名稱', '商品名稱'])['數量'].sum().reset_index()

# get top 5 items by each section
top5_items_df = grouped_df.sort_values(['SECTION名稱', '數量'], ascending=[True, False])                           .groupby('SECTION名稱')                           .head(5)                           .reset_index(drop=True)

top5_items_df


# In[15]:


# get data when DEPARTMENT = "HOUSEHOLD & EA" and Non-PB products
household_df = combined_df[(combined_df["DEPARTMENT名稱"] == "HOUSEHOLD & EA") & (combined_df["PB"] == "Non-PB")]

# count by each section & item
grouped_df = household_df.groupby(['SECTION名稱', '商品名稱'])['數量'].sum().reset_index()

# get top 5 items by each section
top5_items_df = grouped_df.sort_values(['SECTION名稱', '數量'], ascending=[True, False])                           .groupby('SECTION名稱')                           .head(5)                           .reset_index(drop=True)

top5_items_df


# In[16]:


# get data when DEPARTMENT = "HOUSEHOLD & EA" and PB products
household_df = combined_df[(combined_df["DEPARTMENT名稱"] == "HOUSEHOLD & EA") & (combined_df["PB"] == "PB")]

# count by each section & item
grouped_df = household_df.groupby(['SECTION名稱', '商品名稱'])['數量'].sum().reset_index()

# get top 5 items by each section
top5_items_df = grouped_df.sort_values(['SECTION名稱', '數量'], ascending=[True, False])                           .groupby('SECTION名稱')                           .head(5)                           .reset_index(drop=True)

top5_items_df


# ### 2.2.3 FOOD & DELICA

# #### 2.2.3.1 Quantity VS Sales

# In[17]:


# calculate PB and Non-PB Quantity
pivot_df = combined_df.loc[combined_df["DEPARTMENT名稱"] == "FOOD & DELICA"].groupby(["SECTION名稱", "PB"]).agg({"數量": "sum"})     .pivot_table(index="SECTION名稱", columns="PB", values="數量").rename_axis("QUANTITY", axis=1)

# calculate sales by department 
pivot_df['Total_Sales_Quantity'] = pivot_df.sum(axis=1)

# calculate % of PB in total sales by department 
pivot_df['% of PB Sales Quantity to Total'] = (pivot_df['PB'] / pivot_df['Total_Sales_Quantity']) * 100

pivot_df = pivot_df[['Non-PB', 'PB', 'Total_Sales_Quantity', '% of PB Sales Quantity to Total']]
pivot_df


# In[18]:


# calculate PB and Non-PB Sales
pivot_df = combined_df.loc[combined_df["DEPARTMENT名稱"] == "FOOD & DELICA"].groupby(["SECTION名稱", "PB"]).agg({"SALES": "sum"})     .pivot_table(index="SECTION名稱", columns="PB", values="SALES").rename_axis("SALES", axis=1)

# calculate sales by stores
pivot_df['Total_Sales'] = pivot_df.sum(axis=1)

# calculate % of PB in total sales by stores 
pivot_df['% of PB Sales to Total'] = (pivot_df['PB'] / pivot_df['Total_Sales']) * 100

pivot_df = pivot_df[['Non-PB', 'PB', 'Total_Sales', '% of PB Sales to Total']]
pivot_df


# #### 2.2.3.2 Top 10 products in FOOD & DELICA

# In[19]:


# Top 10 in general 
combined_df.loc[combined_df["DEPARTMENT名稱"] == "FOOD & DELICA"].groupby(by="商品名稱").agg({"SECTION名稱": "first", "數量": "sum"}).sort_values(by="數量", ascending=False).head(10)


# In[21]:


# Top 10 in PB Brand 
combined_df[(combined_df["DEPARTMENT名稱"] == "FOOD & DELICA") & (combined_df["PB"] == "PB")].groupby(by="商品名稱").agg({"SECTION名稱": "first", "數量": "sum"}).sort_values(by="數量", ascending=False).head(10)


# In[22]:


# Top 10 in non-PB Brand
combined_df[(combined_df["DEPARTMENT名稱"] == "FOOD & DELICA") & (combined_df["PB"] == "Non-PB")].groupby(by="商品名稱").agg({"SECTION名稱": "first", "數量": "sum"}).sort_values(by="數量", ascending=False).head(10)


# #### 2.2.3.3 Top 5 products by section

# In[27]:


# get data when DEPARTMENT = "FOOD & DELICA"
household_df = combined_df[combined_df["DEPARTMENT名稱"] == "FOOD & DELICA"]

# count by each section & item
grouped_df = household_df.groupby(['SECTION名稱', '商品名稱'])['數量'].sum().reset_index()

# get top 5 items by each section
top5_items_df = grouped_df.sort_values(['SECTION名稱', '數量'], ascending=[True, False])                           .groupby('SECTION名稱')                           .head(5)                           .reset_index(drop=True)

top5_items_df


# In[24]:


# get data when DEPARTMENT = "FOOD & DELICA" and Non-PB products
household_df = combined_df[(combined_df["DEPARTMENT名稱"] == "FOOD & DELICA") & (combined_df["PB"] == "Non-PB")]

# count by each section & item
grouped_df = household_df.groupby(['SECTION名稱', '商品名稱'])['數量'].sum().reset_index()

# get top 5 items by each section
top5_items_df = grouped_df.sort_values(['SECTION名稱', '數量'], ascending=[True, False])                           .groupby('SECTION名稱')                           .head(5)                           .reset_index(drop=True)

top5_items_df


# In[25]:


# get data when DEPARTMENT = "FOOD & DELICA" and PB products
household_df = combined_df[(combined_df["DEPARTMENT名稱"] == "FOOD & DELICA") & (combined_df["PB"] == "PB")]

# count by each section & item
grouped_df = household_df.groupby(['SECTION名稱', '商品名稱'])['數量'].sum().reset_index()

# get top 5 items by each section
top5_items_df = grouped_df.sort_values(['SECTION名稱', '數量'], ascending=[True, False])                           .groupby('SECTION名稱')                           .head(5)                           .reset_index(drop=True)

top5_items_df


# ### 2.2.4 FASHION

# #### 2.2.4.1 Quantity VS Sales

# In[30]:


# calculate PB and Non-PB Quantity
pivot_df = combined_df.loc[combined_df["DEPARTMENT名稱"] == "FASHION"].groupby(["SECTION名稱", "PB"]).agg({"數量": "sum"})     .pivot_table(index="SECTION名稱", columns="PB", values="數量").rename_axis("QUANTITY", axis=1)

# calculate sales by department 
pivot_df['Total_Sales_Quantity'] = pivot_df.sum(axis=1)

# calculate % of PB in total sales by department 
pivot_df['% of PB Sales Quantity to Total'] = (pivot_df['PB'] / pivot_df['Total_Sales_Quantity']) * 100

pivot_df = pivot_df[['Non-PB', 'PB', 'Total_Sales_Quantity', '% of PB Sales Quantity to Total']]
pivot_df


# In[31]:


# calculate PB and Non-PB Sales
pivot_df = combined_df.loc[combined_df["DEPARTMENT名稱"] == "FASHION"].groupby(["SECTION名稱", "PB"]).agg({"SALES": "sum"})     .pivot_table(index="SECTION名稱", columns="PB", values="SALES").rename_axis("SALES", axis=1)

# calculate sales by stores
pivot_df['Total_Sales'] = pivot_df.sum(axis=1)

# calculate % of PB in total sales by stores 
pivot_df['% of PB Sales to Total'] = (pivot_df['PB'] / pivot_df['Total_Sales']) * 100

pivot_df = pivot_df[['Non-PB', 'PB', 'Total_Sales', '% of PB Sales to Total']]
pivot_df


# #### 2.2.4.2 Top 10 products in FASHION

# In[32]:


# Top 10 in general 
combined_df.loc[combined_df["DEPARTMENT名稱"] == "FASHION"].groupby(by="商品名稱").agg({"SECTION名稱": "first", "數量": "sum"}).sort_values(by="數量", ascending=False).head(10)


# In[33]:


# Top 10 in PB Brand 
combined_df[(combined_df["DEPARTMENT名稱"] == "FASHION") & (combined_df["PB"] == "PB")].groupby(by="商品名稱").agg({"SECTION名稱": "first", "數量": "sum"}).sort_values(by="數量", ascending=False).head(10)


# In[34]:


# Top 10 in Non-PB Brand 
combined_df[(combined_df["DEPARTMENT名稱"] == "FASHION") & (combined_df["PB"] == "Non-PB")].groupby(by="商品名稱").agg({"SECTION名稱": "first", "數量": "sum"}).sort_values(by="數量", ascending=False).head(10)


# #### 2.2.4.3 Top 5 products by section

# In[36]:


# get data when DEPARTMENT = "FASHION"
household_df = combined_df[combined_df["DEPARTMENT名稱"] == "FASHION"]

# count by each section & item
grouped_df = household_df.groupby(['SECTION名稱', '商品名稱'])['數量'].sum().reset_index()

# get top 5 items by each section
top5_items_df = grouped_df.sort_values(['SECTION名稱', '數量'], ascending=[True, False])                           .groupby('SECTION名稱')                           .head(5)                           .reset_index(drop=True)

top5_items_df


# In[37]:


# get data when DEPARTMENT = "FASHION" and Non-PB products
household_df = combined_df[(combined_df["DEPARTMENT名稱"] == "FASHION") & (combined_df["PB"] == "Non-PB")]

# count by each section & item
grouped_df = household_df.groupby(['SECTION名稱', '商品名稱'])['數量'].sum().reset_index()

# get top 5 items by each section
top5_items_df = grouped_df.sort_values(['SECTION名稱', '數量'], ascending=[True, False])                           .groupby('SECTION名稱')                           .head(5)                           .reset_index(drop=True)

top5_items_df


# In[38]:


# get data when DEPARTMENT = "FASHION" and PB products
household_df = combined_df[(combined_df["DEPARTMENT名稱"] == "FASHION") & (combined_df["PB"] == "PB")]

# count by each section & item
grouped_df = household_df.groupby(['SECTION名稱', '商品名稱'])['數量'].sum().reset_index()

# get top 5 items by each section
top5_items_df = grouped_df.sort_values(['SECTION名稱', '數量'], ascending=[True, False])                           .groupby('SECTION名稱')                           .head(5)                           .reset_index(drop=True)

top5_items_df


# ## 2.3 Membership Rate

# ### 2.3.1 General

# In[41]:


# Total - Members VS Non-Members 
total_mem = combined_df.loc[combined_df["會員ID (N)"].notnull(), "銷售單號(N)"].nunique()
total_nonmem = combined_df.loc[combined_df["會員ID (N)"].isnull(), "銷售單號(N)"].nunique()

# PB - Members VS Non-Members
pb_mem = combined_df.loc[(combined_df["PB"] == "PB") & (combined_df["會員ID (N)"].notnull()), "銷售單號(N)"].nunique()
pb_nonmem = combined_df.loc[(combined_df["PB"] == "PB") & (combined_df["會員ID (N)"].isnull()), "銷售單號(N)"].nunique()

# Non-PB - Members VS Non-Members
nonpb_mem = combined_df.loc[(combined_df["PB"] == "Non-PB") & (combined_df["會員ID (N)"].notnull()), "銷售單號(N)"].nunique()
nonpb_nonmem = combined_df.loc[(combined_df["PB"] == "Non-PB") & (combined_df["會員ID (N)"].isnull()), "銷售單號(N)"].nunique()

# Creat Dataframe 
result_df = pd.DataFrame({
    "Category": ["Total Member", "Total Non-member", "PB Member", "PB Non-member", "Non-PB Member", "Non-PB Non-member"],
    "Count": [total_mem, total_nonmem, pb_mem, pb_nonmem, nonpb_mem, nonpb_nonmem]
})


result_df


# In[44]:


# Total Membership Rate
num_members_total = combined_df.loc[combined_df["會員ID (N)"].notnull(), "銷售單號(N)"].nunique()
total_invoices_total = combined_df["銷售單號(N)"].nunique()
membership_rate_total = (num_members_total / total_invoices_total) * 100

# PB Membership Rate
num_members_pb = combined_df.loc[(combined_df["PB"] == "PB") & (combined_df["會員ID (N)"].notnull()), "銷售單號(N)"].nunique()
total_invoices_pb = combined_df.loc[combined_df["PB"] == "PB", "銷售單號(N)"].nunique()
membership_rate_pb = (num_members_pb / total_invoices_pb) * 100

# Non-PB Membership Rate
num_members_nonpb = combined_df.loc[(combined_df["PB"] == "Non-PB") & (combined_df["會員ID (N)"].notnull()), "銷售單號(N)"].nunique()
total_invoices_nonpb = combined_df.loc[combined_df["PB"] == "Non-PB", "銷售單號(N)"].nunique()
membership_rate_nonpb = (num_members_nonpb / total_invoices_nonpb) * 100


Membership_rate_df = pd.DataFrame({
    "Category": ["Total", "PB", "Non-PB"],
    "Membership Rate (%)": [membership_rate_total, membership_rate_pb, membership_rate_nonpb]
})


Membership_rate_df


# In[45]:


# Total - Members VS Non-Members ave. Sales 
total_sales_mem = combined_df.loc[combined_df["會員ID (N)"].notnull(), "SALES"].sum()
num_mem = combined_df.loc[combined_df["會員ID (N)"].notnull(), "銷售單號(N)"].nunique()
avg_sales_mem = total_sales_mem / num_mem

total_sales_nonmem = combined_df.loc[combined_df["會員ID (N)"].isnull(), "SALES"].sum()
num_nonmem = combined_df.loc[combined_df["會員ID (N)"].isnull(), "銷售單號(N)"].nunique()
avg_sales_nonmem = total_sales_nonmem / num_nonmem

# PB - Members VS Non-Members ave. Sales 
pb_sales_mem = combined_df.loc[(combined_df["PB"] == "PB") & (combined_df["會員ID (N)"].notnull()), "SALES"].sum()
num_mem_pb = combined_df.loc[(combined_df["PB"] == "PB") & (combined_df["會員ID (N)"].notnull()), "銷售單號(N)"].nunique()
avg_sales_mem_pb = pb_sales_mem / num_mem_pb

pb_sales_nonmem = combined_df.loc[(combined_df["PB"] == "PB") & (combined_df["會員ID (N)"].isnull()), "SALES"].sum()
num_nonmem_pb = combined_df.loc[(combined_df["PB"] == "PB") & (combined_df["會員ID (N)"].isnull()), "銷售單號(N)"].nunique()
avg_sales_nonmem_pb = pb_sales_nonmem / num_nonmem_pb

# Non-PB Membership Rate ave. Sales
nonpb_sales_mem = combined_df.loc[(combined_df["PB"] == "Non-PB") & (combined_df["會員ID (N)"].notnull()), "SALES"].sum()
num_mem_nonpb = combined_df.loc[(combined_df["PB"] == "Non-PB") & (combined_df["會員ID (N)"].notnull()), "銷售單號(N)"].nunique()
avg_sales_mem_nonpb = nonpb_sales_mem / num_mem_nonpb

nonpb_sales_nonmem = combined_df.loc[(combined_df["PB"] == "Non-PB") & (combined_df["會員ID (N)"].isnull()), "SALES"].sum()
num_nonmem_nonpb = combined_df.loc[(combined_df["PB"] == "Non-PB") & (combined_df["會員ID (N)"].isnull()), "銷售單號(N)"].nunique()
avg_sales_nonpb = nonpb_sales_nonmem / num_nonmem_nonpb


ave_sales_df = pd.DataFrame({
    "Category": ["Total Member", "Total Non-member", "PB Member", "PB Non-member", "Non-PB Member", "Non-PB Non-member"],
    "Average Sales": [avg_sales_mem, avg_sales_nonmem, avg_sales_mem_pb, avg_sales_nonmem_pb, avg_sales_mem_nonpb, avg_sales_nonpb]
})

ave_sales_df


# In[47]:


# T-test
def t_test(group1, group2):
    t_stat, p_val = stats.ttest_ind(group1, group2, nan_policy='omit')
    return t_stat, p_val

# Total - Members VS Non-Members T-test 
total_mem_sales = combined_df.loc[combined_df["會員ID (N)"].notnull(), "SALES"]
total_nonmem_sales = combined_df.loc[combined_df["會員ID (N)"].isnull(), "SALES"]
t_stat_total, p_val_total = t_test(total_mem_sales, total_nonmem_sales)

# PB - Members VS Non-Members T-test 
pb_mem_sales = combined_df.loc[(combined_df["PB"] == "PB") & (combined_df["會員ID (N)"].notnull()), "SALES"]
pb_nonmem_sales = combined_df.loc[(combined_df["PB"] == "PB") & (combined_df["會員ID (N)"].isnull()), "SALES"]
t_stat_pb, p_val_pb = t_test(pb_mem_sales, pb_nonmem_sales)

# Non-PB - Members VS Non-Members T-test 
nonpb_mem_sales = combined_df.loc[(combined_df["PB"] == "Non-PB") & (combined_df["會員ID (N)"].notnull()), "SALES"]
nonpb_nonmem_sales = combined_df.loc[(combined_df["PB"] == "Non-PB") & (combined_df["會員ID (N)"].isnull()), "SALES"]
t_stat_nonpb, p_val_nonpb = t_test(nonpb_mem_sales, nonpb_nonmem_sales)


t_test_df = pd.DataFrame({
    "Category": ["Total", "PB", "Non-PB"],
    "T-Statistic": [t_stat_total, t_stat_pb, t_stat_nonpb],
    "P-Value": [p_val_total, p_val_pb, p_val_nonpb]
})


t_test_df


# ### 2.3.2 Membership rate and sales across stores

# In[49]:


def calculate_membership_rate(df):
    total_sales_count = df["銷售單號(N)"].nunique()
    member_sales_count = df.loc[df["會員ID (N)"].notnull(), "銷售單號(N)"].nunique()
    membership_rate = (member_sales_count / total_sales_count) * 100 if total_sales_count > 0 else 0
    return membership_rate

# membership rate by Stores 
store_groups = combined_df.groupby('門店編碼')

membership_rates = []

for store, group in store_groups:
    total_rate = calculate_membership_rate(group)
    pb_rate = calculate_membership_rate(group[group['PB'] == 'PB'])
    nonpb_rate = calculate_membership_rate(group[group['PB'] == 'Non-PB'])
    
    membership_rates.append({
        "門店編碼": store,
        "Total Membership Rate": total_rate,
        "PB Membership Rate": pb_rate,
        "Non-PB Membership Rate": nonpb_rate
    })

membership_rate_df = pd.DataFrame(membership_rates)

membership_rate_df


# In[68]:


# recognize Member VS Non-Member
combined_df['會員身份'] = combined_df['會員ID (N)'].notnull().map({True: 'Member', False: 'Non-member'})

# calculate average sales
def calculate_avg_sales(group):
    return group['SALES'].sum() / group['銷售單號(N)'].nunique() if group['銷售單號(N)'].nunique() > 0 else 0

# calculate by store 
result = combined_df.groupby(['門店編碼', '會員身份', 'PB']).apply(calculate_avg_sales).reset_index(name='平均銷售額')

# create pivot table
dept_avg_sale_table = result.pivot_table(index='門店編碼', columns=['會員身份', 'PB'], values='平均銷售額').reset_index()

dept_avg_sale_table


# In[59]:


## T-test


# ### 2.3.3 Membership rate and sales across departments

# In[60]:


# membership Rate by Departments 
dept_groups = combined_df.groupby('DEPARTMENT名稱')

membership_rates = []

for store, group in dept_groups:
    total_rate = calculate_membership_rate(group)
    pb_rate = calculate_membership_rate(group[group['PB'] == 'PB'])
    nonpb_rate = calculate_membership_rate(group[group['PB'] == 'Non-PB'])
    
    membership_rates.append({
        "DEPARTMENT名稱": store,
        "Total Membership Rate": total_rate,
        "PB Membership Rate": pb_rate,
        "Non-PB Membership Rate": nonpb_rate
    })

membership_rate_df = pd.DataFrame(membership_rates)

membership_rate_df


# In[69]:


# sales by Department 
result = combined_df.groupby(['DEPARTMENT名稱', '會員身份', 'PB']).apply(calculate_avg_sales).reset_index(name='平均銷售額')

# create pivot table
dept_avg_sale_table = result.pivot_table(index='DEPARTMENT名稱', columns=['會員身份', 'PB'], values='平均銷售額').reset_index()

dept_avg_sale_table


# In[ ]:


## T-test


# ### 2.3.4 Top section in HOUSEHOLD & EA for Member & Non-Member

# In[72]:


# calculate quantity by SECTION、PB、Membership
grouped_data = household_data.groupby(['SECTION名稱', 'PB', 'MEMBER']).agg({'數量': 'sum'}).reset_index()
grouped_data = grouped_data.sort_values(by=['PB', 'MEMBER', '數量'], ascending=[True, False, False])

# select top 10 under PB and Membership
top_sections = grouped_data.groupby(['PB', 'MEMBER']).head(10)

# rename PB and Membership
top_sections['MEMBER'] = top_sections['MEMBER'].replace({'Yes': '會員', 'No': '非會員'})
top_sections['PB'] = top_sections['PB'].replace({'Yes': 'PB', 'No': '非PB'})

top_sections


# ## 2.4 Sales day vs. Non-sales day

# ### 2.4.1 General

# In[73]:


# sales by sales-day
combined_df.groupby(["SALES_DAY"]).agg({"SALES": "sum"})


# In[74]:


# sales by sales-day & PB
combined_df.groupby(["SALES_DAY", "PB"]).agg({"SALES": "sum"}).reset_index()


# In[88]:


# ave. sales by sales-day 
result = combined_df.groupby(['SALES_DAY','PB']).apply(calculate_avg_sales).reset_index(name='平均銷售額')

sale_day_avg_sale_table = result.pivot_table(index='SALES_DAY', columns=['PB'], values='平均銷售額')
sale_day_avg_sale_table


# In[99]:


# ratio 
print('The Non-PB ratio is',233.674855/147.422203 )
print('The PB ratio is',116.158940/64.567215 )


# ### 2.4.2 Sales ratio by store

# #### 2.4.2.1 Peak Period

# In[110]:


# Peak period - Sales Day VS. Non-Sale Day - ave sales 
peak_df = combined_df[combined_df['PEAK'] == 'Yes']

# sales by Department 
result = peak_df.groupby(['SALES_DAY', '門店編碼','會員身份', 'PB']).apply(calculate_avg_sales).reset_index(name='平均銷售額')

# create pivot table
store_avg_sale_table = result.pivot_table(index='門店編碼', columns=['SALES_DAY','會員身份', 'PB'], values='平均銷售額')

store_avg_sale_table


# In[107]:


import matplotlib.pyplot as plt
import seaborn as sns

# create heatmap 
plt.figure(figsize=(12, 8))
sns.heatmap(store_avg_sale_table, cmap='YlGnBu', annot=True, fmt=".2f", linewidths=.5)

plt.title('Peak period - Sales Day VS. Non-Sale Day - Average Sales by Store')
plt.xlabel('Sales Day, Membership, PB')
plt.ylabel('Store Code')

plt.show()


# In[113]:


# Peak period - Sales Day VS. Non-Sale Day - PB VS Non-PB

def calculate_total_sales(df):
    return df['SALES'].sum()

# Sales by 'SALES_DAY', '門店編碼', 'PB' 
result = peak_df.groupby(['SALES_DAY', '門店編碼', 'PB']).apply(calculate_total_sales).reset_index(name='SALES')
store_sales_table = result.pivot_table(index='門店編碼', columns=['SALES_DAY', 'PB'], values='SALES')

store_sales_table


# In[115]:


plt.figure(figsize=(12, 8))
sns.heatmap(store_sales_table, cmap='YlGnBu', annot=True, fmt=".2f", linewidths=.5)

plt.title('Peak period - Sales Day VS. Non-Sale Day - PB VS Non-PB')
plt.xlabel('Sales Day, PB')
plt.ylabel('Store Code')

plt.show()


# #### 2.4.2.2 Non-Peak Period

# In[116]:


# Non-Peak period - Sales Day VS. Non-Sale Day - ave sales 
nonpeak_df = combined_df[combined_df['PEAK'] == 'No']

# Sales by 'SALES_DAY', '門店編碼', 'PB' 
result = nonpeak_df.groupby(['SALES_DAY', '門店編碼', 'PB']).apply(calculate_total_sales).reset_index(name='SALES')
store_sales_table = result.pivot_table(index='門店編碼', columns=['SALES_DAY', 'PB'], values='SALES')

store_sales_table


# In[117]:


plt.figure(figsize=(12, 8))
sns.heatmap(store_sales_table, cmap='YlGnBu', annot=True, fmt=".2f", linewidths=.5)

plt.title('Peak period - Sales Day VS. Non-Sale Day - PB VS Non-PB')
plt.xlabel('Sales Day, PB')
plt.ylabel('Store Code')

plt.show()


# In[ ]:




