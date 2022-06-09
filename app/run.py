from flask import Flask, render_template
import requests, json
import collections

app = Flask(__name__)

@app.route("/")
def covid19_tracker():
    url = "https://api.covid19india.org/data.json"
    total_data = requests.get(url=url).json()
    url = "https://api.covid19india.org/state_district_wise.json"
    state_data = requests.get(url=url).json()
    total, change = get_total(total_data)
    daily = get_daily(total_data)
    stateinfo, districtinfo, infoforcount = get_state_info(total_data, state_data)
    key_map = map_key_name(stateinfo)
    max_ = int(stateinfo[0].get('confirmed'))
    return render_template('home.html', total=total, daily=daily, change=change,
                        stateinfo=stateinfo, districtinfo=districtinfo, key_map=key_map,
                        infoforcount=infoforcount, max_=max_)


def get_total(data):
    totalconfirmed = data.get('cases_time_series')[-1].get('totalconfirmed')
    changeconfiremd = int(totalconfirmed) - int(data.get('cases_time_series')[-2].get('totalconfirmed'))
    totalrecovered = data.get('cases_time_series')[-1].get('totalrecovered')
    changerecovered = int(totalrecovered) - int(data.get('cases_time_series')[-2].get('totalrecovered'))
    totaldeceased = data.get('cases_time_series')[-1].get('totaldeceased')
    changedeceased = int(totaldeceased) - int(data.get('cases_time_series')[-2].get('totaldeceased'))
    totalactive = str(int(totalconfirmed) - int(totalrecovered) - int(totaldeceased))
    change = [changeconfiremd, changerecovered, changedeceased]
    total = [totalconfirmed, totalrecovered, totalactive, totaldeceased]
    return total, change


def get_daily(data):
    daily_dic = collections.defaultdict(list)
    
    for daily in data.get('cases_time_series'):
        a = daily.get('dailyconfirmed')
        b = daily.get('dailyrecovered')
        c = daily.get('dailydeceased')
        daily_dic["confirmed"].append(a)
        daily_dic["recovered"].append(b)
        daily_dic["deceased"].append(c)
        daily_dic["_date"].append(daily.get('date'))
        d = int(a) - int(b) - int(c)
        if d<0:
            daily_dic["active"].append(0)
        else:
            daily_dic["active"].append(str(d))
    return daily_dic


def get_state_info(total_data, state_data):
    stateinfo = list()
    infoforcount = collections.defaultdict(list)
    districtinfo = collections.defaultdict(list)
    for state in total_data.get("statewise")[1:]:
        c = state.get("confirmed")
        d = state.get("deaths")
        r = state.get("recovered")
        a = state.get("active")

        # <FOR MAP>
        if state['state'] == 'Odisha':
                state_name = 'Orissa'
        elif state['state'] == 'Uttarakhand':
                state_name = 'Uttaranchal'
        else:
                state_name = state['state']
        infoforcount[state_name].append([c, r, a, d])
        # </FORMAP>

        if any([int(c), int(d), int(r), int(a)]):
            c = c if c!="0" else "-"
            r = r if r!="0" else "-"
            a = a if a!="0" else "-"
            d = d if d!="0" else "-"
            stateinfo.append({
                'state': state.get("state"),
                'confirmed': c,
                'deaths': d,
                'recovered': r,
                'active': a
            })
            for key, val in state_data.get(state.get("state")).items():
                if isinstance(val, dict):
                    for key1, val1 in val.items():
                        districtinfo[state.get("state")].append([key1, val1.get('confirmed')])
    for eachdist in districtinfo.items():
        a = sorted(eachdist[1],key=lambda v:v[1], reverse=True)
        districtinfo[eachdist[0]] = a
    return stateinfo, districtinfo, infoforcount


def map_key_name(data):
    key_name = []
    dict_ = {'Maharashtra':'in-mh', 'Tamil Nadu':'in-tn', 'Delhi':'in-dl', 'Rajasthan':'in-rj',
            'Kerala':'in-kl', 'Uttar Pradesh':'in-up', 'Andhra Pradesh':'in-ap', 'Madhya Pradesh':'in-mp',
            'Karnataka':'in-ka', 'Gujarat':'in-2984', 'Haryana':'in-hr', 'Jammu and Kashmir':'in-jk',
            'Punjab':'in-pb', 'West Bengal':'in-wb', 'Odisha':'in-or', 'Bihar':'in-br',
            'Uttarakhand':'in-ut', 'Assam':'in-as', 'Chandigarh':'in-ch', 'Himachal Pradesh':'in-hp',
            'Chhattisgarh':'in-ct', 'Goa':'in-ga', 'Jharkhand':'in-jh', 'Manipur':'in-mn',
            'Mizoram':'in-mz', 'Arunachal Pradesh':'in-ar', 'Dadra and Nagar Haveli':'in-dn',
            'Tripura':'in-tr', 'Puducherry':'in-py', 'Lakshadweep': 'in-ld', 'Sikkim': 'in-sk',
            'Nagaland': 'in-nl', 'Daman and Diu': 'in-3464', 'Meghalaya': 'in-ml'}
    for state in data:
        if dict_.get(state['state']):
            key_name.append([dict_[state['state']], int(state['confirmed'])])
    return key_name


if __name__ == "__main__":
    app.run(debug=True)
