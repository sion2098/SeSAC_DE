import requests
from bs4 import BeautifulSoup
from pprint import pprint

url = "https://www.scrapethissite.com/pages/forms/"
res = requests.get(url)
bs = BeautifulSoup(res.text)


teams = bs.select("table.table tr.team") #<tr class="team">으로 되어있는 row를 한꺼번에 가져옴
                                         #리스트 형태로 반환

team_list = []

for team_info in teams: #리스트에서 각 <tr> 태그를 한개씩 꺼내서 team_info에 담음

    # Team Name 가져오기
    t_name = team_info.select_one("td.name").get_text(strip=True)

    # Team Year 가져오기
    t_year = team_info.select_one("td.year").get_text(strip=True)

    # Team Wins 가져오기
    t_wins = team_info.select_one("td.wins").get_text(strip=True)

    # Team Losses 가져오기
    t_losses = team_info.select_one("td.losses").get_text(strip=True)

    # Team OT-Losses 가져오기
    t_ot_losses = team_info.select_one("td.ot-losses").get_text(strip=True)

    # Team Win% 가져오기
    #win success/danger 값 가져오기
    t_pct = team_info.select_one("td.pct")
    if "text-success" in t_pct["class"]:
        sd_pct = t_pct.get_text(strip=True) + '(success)'

    elif "text-danger" in t_pct["class"]:
        sd_pct = t_pct.get_text(strip=True) + '(danger)'

    # Team GF 가져오기
    t_gf = team_info.select_one("td.gf").get_text(strip=True)

    # Team GA 가져오기
    t_ga = team_info.select_one("td.ga").get_text(strip=True)

    # Team +/- 가져오기
    # +/- 값 가져오기
    t_diff = team_info.select_one("td.diff")
    if "text-success" in t_diff["class"]:
        sd_diff = t_diff.get_text(strip=True) + '(success)'
    elif "text-danger" in t_diff["class"]:
        sd_diff = t_diff.get_text(strip=True) + '(danger)'

    # print(f"Team Name : {t_name}")
    # print(f"Year : {t_year}")
    # print(f"Wins : {t_wins}")
    # print(f"Losses : {t_losses}")
    # print(f"OT Losses : {t_ot_losses}")
    # print(f"Win % : {t_pct}%")
    # print(f"Goals For : {t_gf}")
    # print(f"Goals Against : {t_ga}")
    # print(f"+ / - : {t_diff}")
    # print("===================================")


    # 리스트 형태로 출력하기
    team_list.append({
        "Team Name": t_name,
        "Year": t_year,
        "Wins": t_wins,
        "Losses": t_losses,
        "OT Losses": t_ot_losses,
        "Win %": sd_pct,
        "Goals For": t_gf,
        "Goals Against": t_ga,
        "+/-": sd_diff
    })

pprint(team_list)
print(len(team_list))



