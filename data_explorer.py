import pandas as pd
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

file_name = './data/DataScientist_completeCSV.csv'

df = pd.read_csv(file_name, header=0)

num_top_companies = 5


#******************************************************************
# Total Aggregates, Total YOE, Tot Comp
#******************************************************************

# tot_years_mean_df = df.groupby(['YOE Total']).agg(['mean', 'count', 'std'])

# print(tot_years_mean_df)

# fig = px.scatter()
# fig.add_trace(go.Scatter(
#                     name='Mean', 
#                     x=tot_years_mean_df.index, 
#                     y=tot_years_mean_df['Total Compensation']['mean'],
#                     error_y=dict(
#                         type='data', # value of error bar given in data coordinates
#                         array=1.96*tot_years_mean_df['Total Compensation']['std']/np.sqrt(tot_years_mean_df['Total Compensation']['count']),
#                         visible=True),
#                     mode='markers'
#                     ))



# fig.update_layout(showlegend=True)
# fig.show()


#******************************************************************
# Total Aggregates, Total YOE, Tot Comp
#******************************************************************

# tot_years_mean_df = df.groupby(['YOE At Company']).agg(['mean', 'count', 'std'])

# print(tot_years_mean_df)

# fig = px.scatter()
# fig.add_trace(go.Scatter(
#                     name='Mean', 
#                     x=tot_years_mean_df.index, 
#                     y=tot_years_mean_df['Total Compensation']['mean'],
#                     error_y=dict(
#                         type='data', # value of error bar given in data coordinates
#                         array=1.96*tot_years_mean_df['Total Compensation']['std']/np.sqrt(tot_years_mean_df['Total Compensation']['count']),
#                         visible=True),
#                     mode='markers'
#                     ))



# fig.update_layout(showlegend=True)
# fig.show()

#******************************************************************
# Total Aggregates, Total YOE, Base Comp
#******************************************************************

# tot_years_mean_df = df.groupby(['YOE Total']).agg(['mean', 'count', 'std'])

# print(tot_years_mean_df)

# fig = px.scatter()
# fig.add_trace(go.Scatter(
#                     name='Mean', 
#                     x=tot_years_mean_df.index, 
#                     y=tot_years_mean_df['Base Comp']['mean'],
#                     error_y=dict(
#                         type='data', # value of error bar given in data coordinates
#                         array=1.96*tot_years_mean_df['Base Comp']['std']/np.sqrt(tot_years_mean_df['Base Comp']['count']),
#                         visible=True),
#                     mode='markers'
#                     ))



# fig.update_layout(showlegend=True)
# fig.show()


#******************************************************************
# Top Companies, Total YOE, Tot Comp
#******************************************************************

# top_companies = df["Company"].value_counts()[:num_top_companies+1].index

# df_top = df[df["Company"].isin(top_companies)]
# df_top_grouped = df_top.groupby(['Company','YOE Total']).agg(['mean', 'count', 'std'])


# df_top_grouped.reset_index(inplace=True)



# fig = px.scatter()

# for company in top_companies:
#     company_grouped_df = df_top_grouped[df_top_grouped['Company'] == company]

#     fig.add_trace(go.Scatter(
#                         name='{}'.format(company), 
#                         x=company_grouped_df['YOE Total'], 
#                         y=company_grouped_df['Total Compensation']['mean'],
#                         error_y=dict(
#                         type='data', # value of error bar given in data coordinates
#                         array=1.96*company_grouped_df['Total Compensation']['std']/np.sqrt(company_grouped_df['Total Compensation']['count']),
#                         visible=False),
#                         mode='lines'
#                         ))

# fig.update_layout(showlegend=True)
# fig.show()

#******************************************************************
# Top Companies, YOE At Company, Tot Comp
#******************************************************************

# top_companies = df["Company"].value_counts()[:num_top_companies+1].index

# df_top = df[df["Company"].isin(top_companies)]
# df_top_grouped = df_top.groupby(['Company','YOE At Company']).agg(['mean', 'count', 'std'])

# df_top_grouped.reset_index(inplace=True)

# print(df_top_grouped)

# fig = px.scatter()
# for company in top_companies:
#     company_grouped_df = df_top_grouped[df_top_grouped['Company'] == company]

#     fig.add_trace(go.Scatter(
#                         name='{}'.format(company), 
#                         x=company_grouped_df['YOE At Company'], 
#                         y=company_grouped_df['Total Compensation']['mean'],
#                         error_y=dict(
#                         type='data', # value of error bar given in data coordinates
#                         array=1.96*company_grouped_df['Total Compensation']['std']/np.sqrt(company_grouped_df['Total Compensation']['count']),
#                         visible=False),
#                         mode='lines'
#                         ))

# fig.update_layout(showlegend=True)
# fig.show()


#******************************************************************
# Top Companies, Total YOE, Base Comp
#******************************************************************

top_companies = df["Company"].value_counts()[:num_top_companies+1].index

df_top = df[df["Company"].isin(top_companies)]
df_top_grouped = df_top.groupby(['Company','YOE Total']).agg(['mean', 'count', 'std'])


df_top_grouped.reset_index(inplace=True)


fig = px.scatter()

for company in top_companies:
    company_grouped_df = df_top_grouped[df_top_grouped['Company'] == company]

    fig.add_trace(go.Scatter(
                        name='{}'.format(company), 
                        x=company_grouped_df['YOE Total'], 
                        y=company_grouped_df['Base Comp']['mean'],
                        error_y=dict(
                        type='data', # value of error bar given in data coordinates
                        array=1.96*company_grouped_df['Base Comp']['std']/np.sqrt(company_grouped_df['Base Comp']['count']),
                        visible=True),
                        mode='lines'
                        ))

fig.update_layout(showlegend=True)
fig.show()