import matplotlib.pyplot as plt
import numpy as np

def daily_events(Discharge, Dates, Concentration):
    
    percentage_discharge_change = ['event']
    for elements in range(1, len(Discharge)):
        y = Discharge[elements]
        change = y - Discharge[elements - 1]
        if Discharge[elements - 1 ] == 0:
            percentage_discharge_change.append('no flow')
        else:
            percent_change = (change/Discharge[elements - 1]) * 100
            percentage_discharge_change.append(percent_change)
        
    # print(f'''Discharge Percentage change
    # {percentage_discharge_change}''')
#     print(len(percentage_discharge_change))
#     print('\n')
    
#     this part of the code prints out the changes in the flow and the serial number
    for elements in range(0, len(percentage_discharge_change)):
        c = f'{elements + 1} - {percentage_discharge_change[elements]}'
#         print(c)
    high_compound_flow = []
    low_compound_flow = []
    combine_compound_flow = []
    events = []
    event_dates = []
    baseflow = []
    baseflow_dates = []
    event_endpoint = 0
    event_bunch = []
    catch_no = 0
    packer = 0
    caught_events = {}
    event_occuring = False
    switch = False
    winter = 0
    spring = 0
    summer  = 0
    fall = 0
    seasons = 0
    all_varient = []
    while seasons < 4:
        event_point = float(input('What is the value of the event start point: '))
        seasons += 1        
        if seasons == 1:
            winter = event_point
            all_varient.append(float(event_point))
        elif seasons == 2:
            spring = event_point
            all_varient.append(float(event_point))
        elif seasons == 3:
            summer = event_point
            all_varient.append(float(event_point))
        elif seasons == 4:
            fall = event_point
            all_varient.append(float(event_point))
    
    mean_jump = sum(all_varient)/len(all_varient)
#     print(mean_jump)
    
    season_delineation = input('''
There are two different seasonal delineation methods:
Method A
    1. Winter -  December - February
    2. Spring - March - May
    3. Summer - June - August
    4. Fall - September - November
                               
Method B
    1. Winter -  January - March
    2. Spring - April - June
    3. Summer - July - September
    4. Fall - October - December
                               
Please select the method you want to use by typing A or B: ''').upper()
    print('\n') 
    searching = True

    month = ''
    if season_delineation == 'A':
        # print(Dates[0])
        step = 0
        while searching == True:
            #This does not loop in any list it is to tell you what the starter is
            day = list(Dates[0])
#             print(day)
            member = day[step]
#             print(member)
            try:
                member = int(member)
                month +=  f'{member}'
                step += 1
            except:
                searching = False
                if float(month) == 12 or float(month) < 3:
                    event_point = winter
                    print('Analysis starting in Winter')
                elif float(month) > 2 and float(month) < 6:
                    event_point = spring
                    print('Analysis starting in spring')
                elif float(month) > 5 and float(month) < 9:
                    event_point = summer                    
                    print('Analysis starting in summer')
                elif float(month) > 8 and float(month) < 12:
                    event_point = fall                    
                    print('Analysis starting in fall')
    elif season_delineation == 'B':
        # print(Dates[0])
        step = 0
        while searching == True:
            day = list(Dates[0])
            member = day[step]
#             print(member)
            try:
                member = int(member)
                month +=  f'{member}'
                step += 1
            except:
                searching = False
                if float(month) < 4:
                    event_point = winter
                    print('Analysis starting in Winter')
                elif float(month) > 3 and float(month) < 7:
                    event_point = spring
                    print('Analysis starting in spring')
                elif float(month) > 6 and float(month) < 10:
                    event_point = summer                    
                    print('Analysis starting in summer')
                elif float(month) > 9:
                    event_point = fall                    
                    print('Analysis starting in fall')
    print('\n')
    
    if Discharge[0] > event_point:
        event_occuring = True
        ## this part supplies the whole data for the analysis
    event_ends = 0
    base_compound = 0
    high_compound = 0
    for elements in range(0, len(Discharge)):
        searching = True
        month = ''
        if season_delineation == 'A':
#             print(Dates[0])
            step = 0
            while searching == True:
                day = list(Dates[elements])
    #             print(day)
#                 print(step)
#                 print(member)
                member = day[step]
    #             print(member)
                try:
                    member = int(member)
                    month +=  f'{member}'
                    step += 1
                except:
                    searching = False
                    if float(month) == 12 or float(month) < 3:
                        event_point = winter
                    elif float(month) > 2 and float(month) < 6:
                        event_point = spring
                    elif float(month) > 5 and float(month) < 9:
                        event_point = summer                 
                    elif float(month) > 8 and float(month) < 12:
                        event_point = fall                 
        elif season_delineation == 'B':
            # print(Dates[0])
            step = 0
            while searching == True:
                day = list(Dates[elements])
    #             print(day)
                member = day[step]
    #             print(member)
                try:
                    member = int(member)
                    month +=  f'{member}'
                    step += 1
                except:
                    searching = False
                    if float(month) < 4:
                        event_point = winter
                    elif float(month) > 3 and float(month) < 7:
                        event_point = spring
                    elif float(month) > 6 and float(month) < 10:
                        event_point = summer
                    elif float(month) > 9:
                        event_point = fall
        
#         print(f'you have passed there emeka {event_point}')
        last_slope = -1
        if event_occuring and elements >= len(events):
            truncated_list = Discharge[elements:]
            section_dates = Dates[elements:]
            changing_flow = percentage_discharge_change[elements:]
            ## this part sections the whole data at event point and works on it until the event ends
            for elements1 in range(0, len(truncated_list)):
#                 the part logs the event
                if event_occuring:
                    if truncated_list[elements1] > event_point:
                        event_ends = 0
                        if elements1 > 0:
                            if changing_flow[elements1] == 'no flow':
                                changing_flow[elements1] = 0.0000000001
                            if changing_flow[elements1] < 0:
                                events.append(truncated_list[elements1])
                                event_dates.append(section_dates[elements1])
                                last_slope = changing_flow[elements1]
                                baseflow.append('')
                            else:
                                if last_slope < 0:
                                    high_compound += 1
                                    events.append(truncated_list[elements1])
                                    event_dates.append(section_dates[elements1])
                                    last_slope = changing_flow[elements1]
                                    baseflow.append('')
                                else:
                                    events.append(truncated_list[elements1])
                                    event_dates.append(section_dates[elements1])
                                    last_slope = changing_flow[elements1]
                                    baseflow.append('')
                        else:
                            event_ends = 0
                            events.append(truncated_list[elements1])
                            event_dates.append(section_dates[elements1])
                            baseflow.append('')
#                         the part chech if the event is ended and if base flow as begun
                    else:                        
                        event_ends += 1
                        if event_ends < 2:
                            events.append(truncated_list[elements1])
                            event_dates.append(section_dates[elements1])
                            drop_1 = truncated_list[elements1]
                            baseflow.append('')
                        #this part checks if a compount event begins after reaching baseflow treshold
                        else:
                            if truncated_list[elements1] <= drop_1:
                                baseflow.append(truncated_list[elements1])
                                baseflow_dates.append(section_dates[elements1])
                                event_occuring = False
                                switch = True
                                event_endpoint = elements1
                                events.append('')
                            else:
#                             This part check if it is a slight bump, is significant to creat compound event
                                if truncated_list[elements1] <= event_point:
                                    baseflow.append(truncated_list[elements1])
                                    baseflow_dates.append(section_dates[elements1])
                                    events.append('')
                                    event_occuring = False
                                    switch = True
                                    event_endpoint = elements1
                                else:
                                    base_compound += 1
                                    events.append(truncated_list[elements1])
                                    event_dates.append(section_dates[elements1])
                                    baseflow.append('')
        else:
            if len(events) > 0 and len(events) >= packer and switch == True:
                catch_no += 1
                event_bunch.append(events)
                packer = len(events)
                caught_events[f'{catch_no} event '] = f'{event_dates[0]} - {event_dates[-1]}'
                switch = False
                if high_compound > 1:
                    if base_compound > 1:
                        combine_compound_flow.append(f'{event_dates[0]} - {event_dates[-1]}')
                    else:
                        high_compound_flow.append(f'{event_dates[0]} - {event_dates[-1]}')
                elif base_compound > 1:
                    low_compound_flow.append(f'{event_dates[0]} - {event_dates[-1]}')
                    
            if elements >= len(events):
                if Discharge[elements] >= event_point:
                    event_ends = 0
                    event_dates = []
                    event_occuring = True
                    if event_occuring and elements >= len(events):
                        truncated_list = Discharge[elements:]
                        section_dates = Dates[elements:]
                        changing_flow = percentage_discharge_change[elements:]
                        ## this part sections the whole data at event point and works on it until the event ends
                        for elements1 in range(0, len(truncated_list)):
            #                 the part logs the event
                            if event_occuring:
                                if truncated_list[elements1] > event_point:
                                    event_ends = 0
                                    if elements1 > 0:
                                        if changing_flow[elements1] == 'no flow':
                                            changing_flow[elements1] = 0.0000000001
                                        if changing_flow[elements1] < 0:
                                            events.append(truncated_list[elements1])
                                            event_dates.append(section_dates[elements1])
                                            last_slope = changing_flow[elements1]
                                            baseflow.append('')
                                        else:
                                            if last_slope < 0:
                                                high_compound += 1
                                                events.append(truncated_list[elements1])
                                                event_dates.append(section_dates[elements1])
                                                last_slope = changing_flow[elements1]
                                                baseflow.append('')
                                            else:
                                                events.append(truncated_list[elements1])
                                                event_dates.append(section_dates[elements1])
                                                last_slope = changing_flow[elements1]
                                                baseflow.append('')
                                    else:
                                        event_ends = 0
                                        events.append(truncated_list[elements1])
                                        event_dates.append(section_dates[elements1])
                                        baseflow.append('')
            #                         the part chech if the event is ended and if base flow as begun
                                else:                           
                                    event_ends += 1
                                    if event_ends < 2:
                                        events.append(truncated_list[elements1])
                                        event_dates.append(section_dates[elements1])
                                        drop_1 = truncated_list[elements1]
                                        baseflow.append('')
                                    #this part checks if a compount event begins after reaching baseflow treshold
                                    else:
                                        if truncated_list[elements1] <= drop_1:
                                            baseflow.append(truncated_list[elements1])
                                            baseflow_dates.append(section_dates[elements1])
                                            event_occuring = False
                                            switch = True
                                            event_endpoint = elements1
                                            events.append('')
                                        else:
            #                             This part check if it is a slight bump, is significant to creat compound event
                                            if truncated_list[elements1] <= event_point:
                                                baseflow.append(truncated_list[elements1])
                                                baseflow_dates.append(section_dates[elements1])
                                                events.append('')
                                                event_occuring = False
                                                switch = True
                                                event_endpoint = elements1
                                            else:
                                                base_compound += 1
                                                events.append(truncated_list[elements1])
                                                event_dates.append(section_dates[elements1])
                                                baseflow.append('')
                    else:
                        if len(events) > 0 and len(events) >= packer and switch == True:
                            catch_no += 1
                            event_bunch.append(events)
                            packer = len(events)
                            caught_events[f'{catch_no} event '] = f'{event_dates[0]} - {event_dates[-1]}'
                            switch = False
                            if high_compound > 1:
                                if base_compound > 1:
                                    combine_compound_flow.append(f'{event_dates[0]} - {event_dates[-1]}')
                                else:
                                    high_compound_flow.append(f'{event_dates[0]} - {event_dates[-1]}')
                            elif base_compound > 1:
                                low_compound_flow.append(f'{event_dates[0]} - {event_dates[-1]}')
         
                else:
                    baseflow.append(Discharge[elements])
                    baseflow_dates.append(Dates[elements])
                    events.append('')                        
    
    # print(event_endpoint)            
    # print(f'''events -
    # {events}''')
    # print(len(events))
    # print('\n')
    
    # print(f'''event_dates -
    # {event_dates}''')
    # print(len(event_dates))
    # print('\n')
    
    # print(f'''Baseflow -
    # {baseflow}''')
    # print(len(baseflow))
    # print('\n')
    # print(f'''Baseflow Dates -
    # {baseflow_dates}''')
    # print(len(baseflow_dates))
    # print('\n')
    # print(f'''Event Bunch -
    # {event_bunch}''')
    # print(len(event_bunch))
    # print('\n')
    
    
#     print(f'''Caught_event -
#     {caught_events}''')
#     print(len(caught_events))
#     print('\n')
#     print(f'There are {len(caught_events)} events')
#     print('\n')
    
    
    # print(f'''Combine Compound Flows - 
    # {combine_compound_flow}''')
    # print(f'You have {len(combine_compound_flow)} combine compound flows')
    # print('\n')
    # print(f'''High Compound flows - 
    # {high_compound_flow}''')
    # print(f'You have {len(high_compound_flow)} high compound flows')
    # print('\n')
    # print(f'''Low Compound Flows -
    # {low_compound_flow}''')
    # print(f'You have {len(low_compound_flow)} low compound flows')
    # print('\n')

#     print('EVENTS')
#     for elements in events:
#         print(elements)
#     print('end')
    
    valid_drop = mean_jump 
    pack = 0
    blocks = 0
    pairs = 1
    event_kickout = []
    for elements in range(0,len(events)):
        if type(events[elements]) == float:
            pack += 1
        elif elements > pack - 1 and pack > 0 and pack < 3:
            look_max = []
            blocks += 1
            reductions = 0
            for members in range (0, pack):
                look_max.append(events[elements - pack])
                pairs += 1
#             print(look_max)
            max_look = max(look_max)
#             print(max_look)
#             print(look_max)
#             print(type(max_look))
            if max_look < 1.25 * event_point:
                event_kickout.append(f'{blocks} event ')
                for kit in range (0, pack):
                    events[elements - 1 - pack + reductions] = ''
                    reductions += 1
            pack = 0
        else:
            if pack > 0:
                blocks += 1
            pack = 0
            
    print(f'blocks (representing the amount of events left) = {blocks}')
#     print(f'These are the event kickout - {event_kickout}')
    for elements in range(0, len(event_kickout)):
        del caught_events[event_kickout[elements]]
    
    print('\n')
    print('These are the modified events')
    print(caught_events)
    print(len(caught_events))
    print('\n')
    print(f'There are {len(caught_events)} events')
    print('\n')
    
    for elements in range (0, len(events)):
        if type(events[elements]) == float:
            if elements > 0 and events[elements] > valid_drop:
                events[elements - 1] = Discharge[elements - 1]
                
    file_name = "Daily_flow_event_data.txt"
        # Write to file (small predicted data)
    with open(file_name, "w") as file:
        for number in events:
            file.write(f"{number}\n")
    print(f"Numbers successfully written to {file_name}")
    # print('BaseFlow')
    # for elements in baseflow:
    #     if elements == 0.0:
    #         print('')
    #     else:
    #         print(elements)
#     print('end')
    
    
    y2 = events
    y1 = Discharge
    
    x = []
    for elements in range(0, len(y1)):
        x.append(Dates[elements])

    # Convert empty strings to np.nan and the rest to float for y2
    y2_clean = [float(val) if val != '' else np.nan for val in y2]

    # Create stacked subplots with shared x-axis
    fig, axs = plt.subplots(2, 1, figsize=(6, 6), sharex=True)

    # First plot (y1)
    axs[0].plot(x, y1, marker='', color='green')
    axs[0].set_title('Plot of Discharge Data')
    axs[0].set_ylabel('Drainage (cm3/day)')
    axs[0].grid(False)

    # Second plot (y2 with missing)
    axs[1].plot(x, y2_clean, marker='', linestyle='-', color='blue')
    axs[1].set_title('Plot of Events')
    axs[1].set_xlabel('Dates')
    axs[1].set_ylabel('Drainage (cm3/day)')
    axs[1].grid(False)
    points = 30
    if len(x) < points:
        points = len(x)
    axs[1].xaxis.set_major_locator(plt.MaxNLocator(nbins=points))
    fig.autofmt_xdate(rotation=45)

    # Optional: Set same y-axis limits (uncomment if needed)
    y_min = min(min(y1, default=np.nan), min(y2_clean, default=np.nan))
    y_max = max(max(y1, default=np.nan), max(y2_clean, default=np.nan))
    if not np.isnan(y_min) and not np.isnan(y_max):
        axs[0].set_ylim(y_min, y_max)
        axs[1].set_ylim(y_min, y_max)

    # Adjust layout and show
    plt.tight_layout()
    plt.show()
    
#     print(Discharge)
#     print(events)
    
    
    for elements in range(0, len(Discharge)):
        if type(events[elements]) == float and type(baseflow[elements]) == float:
            baseflow[elements] = ''
        elif type(events[elements]) == str and type(baseflow[elements]) == str and Discharge[elements] > 0:
            baseflow[elements] = Discharge[elements]
    
    file_name = "Daily_flow_base_data.txt"
        # Write to file (small predicted data)
    with open(file_name, "w") as file:
        for number in baseflow:
            file.write(f"{number}\n")
    print(f"Numbers successfully written to {file_name}")
    
    print('\n Flow weighted Concentration for event\n')
    
    start_date = False
    end_date = False
    hit = 0
    full_hit = 0
    flow_weighted_concentration = []
    label = 0
    
    for key in caught_events:
        label += 1
        good_break_point = False
#         print(list(caught_events[key]))
        matcher = list(caught_events[key])
        for elementss in range(0, len(Dates)):
#             print(elementss)
            if good_break_point == True:
                break
            if start_date == False:
                mini_conc = []
                mini_flow = []
                starter = list(Dates[elementss])
                hit = 0
                for elements in range(0, len(starter)):
                    if starter[elements] == matcher[elements]:
                        hit += 1
                    if hit == len(starter):
                        start_date = True
                        starter.append(' ')
                        starter.append('-')
                        starter.append(' ')
                        half_band = starter
                        mini_conc.append(concentration[elementss])
                        mini_flow.append(events[elementss])
            else:
                full_band_unsure = []
                for elemennt in (half_band):
                    full_band_unsure.append(elemennt)
#                 print('This is the static half band')
#                 print(half_band)
                ender = list(Dates[elementss])
                hit = 0
                for elements in ender:
                    full_band_unsure.append(elements)
                for elements in range(0, len(full_band_unsure)):
                    if full_band_unsure[elements] == matcher[elements]:
                        hit += 1
                    if hit == len(full_band_unsure):
#                         print('I got the full hit')
#                         print(full_band_unsure)
                        full_hit += 1
                        start_date = False
                        good_break_point = True
                mini_conc.append(concentration[elementss])
                mini_flow.append(events[elementss])
                if start_date == False:
                    conc_flow_sum = 0
                    flow_sum = 0
                    for elements in range(0, len(mini_conc)):
                        try:
                            y = float(mini_conc[elements])
                            if y > 0:
                                conc_flow_sum += (float(mini_conc[elements] * float(mini_flow[elements])))
                                flow_sum += float(mini_flow[elements])
                        except:
                            toool = 'not usable becuase is it a string'
                    F_W_C = conc_flow_sum / flow_sum    
                    flow_weighted_concentration.append(f'{label}_event - {F_W_C}')
                    print(flow_weighted_concentration)

#     print(full_hit)
    print('\n')
    print('The flow weighted concentration for the events are: ')
    print(flow_weighted_concentration)
    print(len(flow_weighted_concentration))
    
#     print(full_hit)
#     print('\n')
#     print('These are your base flow')
#     print(baseflow)
    
#################################################################################################################################################################################################################################
Discharge = 'Daily_Discharge_Data.txt'
Dates = 'Daily_Dates.txt'
Concentration = 'Daily_Concentration_Data.txt'

a = open(Discharge, 'r')
a1 = open(Dates, 'r')
a2 = open(Concentration, 'r')
# you can put event data (actual dates copies from excel) or numbers in the event date txt file
b = []
b1 = []
b2 = []
for lines in a:
    #c = we strip the lines with c, making every line an item
    c = lines.strip()
    d = lines.split()
    b.append(d)
a.close()

for lines in a1:
    #c = we strip the lines with c, making every line an item
    c = lines.strip()
    d = lines.split()
    b1.append(d)
a1.close()

for lines in a2:
    #c = we strip the lines with c, making every line an item
    c = lines.strip()
    d = lines.split()
    b2.append(d)
a2.close()

#     print(b)
#     print(len(b))
#     print('\n')
#     print(b1)
#     print(len(b1))
#     print('\n')

Discharge = []
Dates = []
concentration = []
for elements in b:
    if len(elements) < 1:
        elements = '0'
        Discharge.append(float(elements))
    else:
        Discharge.append(float(elements[0]))

for elements in b1:
    Dates.append((elements[0]))

for elements in b2:
    if len(elements) < 1:
        elements = '0' 
        concentration.append(float(elements))
    else:
#             print(elements)
        concentration.append(float(elements[0]))
        
print('\n')        
#     print(f'''Discharge:
# {Discharge}''')
#     print(len(Discharge))
#     print('\n')
#     print(f'''Dates:
# {Dates}''')
#     print(len(Dates))
#     print('\n')
#     print(f'''Concentration:
# {concentration}''')
#     print(len(concentration))
#     print('\n')



# daily_events(Discharge, Dates, Concentration)


