from django.shortcuts import render
import requests
import json

# Source: https://rapidapi.com/api-sports/api/covid-193/
url = "https://covid-193.p.rapidapi.com/statistics"

headers = {
    'x-rapidapi-host': "covid-193.p.rapidapi.com",
    'x-rapidapi-key': "4cfc067686mshbbe01f961376f54p1bf59fjsnd0b2f6961912"
    }

response = requests.request("GET", url, headers=headers).json()

# Create your views here.
def webview(request):
    num_results = int(response["results"])
    country_list = []

    for i in range(num_results):
        country = response["response"][i]["country"]
        country_list.append(country)

    # In case of POST request, perform this
    if request.method=="POST":
        selected_country = request.POST["selectedCountry"]
        print(selected_country)

        for i in range(num_results):
            if selected_country == response["response"][i]["country"]:
                new = response["response"][i]["cases"]["new"]
                active = response["response"][i]["cases"]["active"]
                critical = response["response"][i]["cases"]["critical"]
                recovered = response["response"][i]["cases"]["recovered"]
                total = response["response"][i]["cases"]["total"]
                deaths = int(total) - int(active) - int(recovered)

        context = {"selectedCountry": selected_country, "country_list": country_list, "new": new, "active": active, "critical": critical, 
                    "recovered": recovered, "deaths": deaths, "total": total}
        return render(request, "webview.html", context)

    # Default performance
    context = {"country_list": country_list}
    return render(request, "webview.html", context)
