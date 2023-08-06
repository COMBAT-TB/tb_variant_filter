# Copyright (C) 2019  Peter van Heusden <pvh@sanbi.ac.za>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from .. import Location, doc_inherit
from io import StringIO
import pandas as pd
from neo4j import GraphDatabase
import requests

from ..region_list import RegionList


class UVPRegions(RegionList):
    url = "https://raw.githubusercontent.com/CPTR-ReSeqTB/UVP/master/bin/excluded_loci.txt"
    name = "UVP"
    description = "UVP excluded loci list"
    project_url = "https://github.com/CPTR-ReSeqTB/UVP"
    regions = [
        Location(locus="Rv0031", start=33582, end=33794, strand=1),
        Location(locus="Rv0094c", start=103710, end=104663, strand=-1),
        Location(locus="Rv0095c", start=104805, end=105215, strand=-1),
        Location(locus="Rv0257", start=309699, end=310073, strand=1),
        Location(locus="Rv0277c", start=332708, end=333136, strand=-1),
        Location(locus="Rv0336", start=400192, end=401703, strand=1),
        Location(locus="Rv0353", start=423639, end=424019, strand=1),
        Location(locus="Rv0393", start=472781, end=474106, strand=1),
        Location(locus="Rv0397", start=475816, end=476184, strand=1),
        Location(locus="Rv0487", start=576787, end=577338, strand=1),
        Location(locus="Rv0490", start=579349, end=580581, strand=1),
        Location(locus="Rv0515", start=606551, end=608062, strand=1),
        Location(locus="Rv0538", start=630040, end=631686, strand=1),
        Location(locus="Rv0605", start=701406, end=702014, strand=1),
        Location(locus="Rv0605", start=701406, end=702014, strand=1),
        Location(locus="Rv0740", start=831776, end=832303, strand=1),
        Location(locus="Rv0741", start=832534, end=832848, strand=1),
        Location(locus="Rv0750", start=842033, end=842278, strand=1),
        Location(locus="Rv0755A", start=850342, end=850527, strand=-1),
        Location(locus="Rv0795", start=889072, end=889398, strand=1),
        Location(locus="Rv0796", start=889347, end=890333, strand=1),
        Location(locus="Rv0797", start=890388, end=891482, strand=1),
        Location(locus="Rv0814c", start=908181, end=908483, strand=-1),
        Location(locus="Rv0823c", start=916477, end=917646, strand=-1),
        Location(locus="Rv0829", start=921575, end=921865, strand=1),
        Location(locus="Rv0850", start=947312, end=947644, strand=1),
        Location(locus="Rv0867c", start=964312, end=965535, strand=-1),
        Location(locus="Rv0920c", start=1025497, end=1026816, strand=-1),
        Location(locus="Rv0921", start=1027104, end=1027685, strand=1),
        Location(locus="Rv0922", start=1027685, end=1029337, strand=1),
        Location(locus="Rv1034c", start=1158918, end=1159307, strand=-1),
        Location(locus="Rv1035c", start=1159375, end=1160061, strand=-1),
        Location(locus="Rv1036c", start=1160095, end=1160433, strand=-1),
        Location(locus="Rv1037c", start=1160544, end=1160828, strand=-1),
        Location(locus="Rv1038c", start=1160855, end=1161151, strand=-1),
        Location(locus="Rv1041c", start=1164572, end=1165435, strand=-1),
        Location(locus="Rv1042c", start=1165092, end=1165499, strand=-1),
        Location(locus="Rv1047", start=1169423, end=1170670, strand=1),
        Location(locus="Rv1128c", start=1251617, end=1252972, strand=-1),
        Location(locus="Rv1148c", start=1276300, end=1277748, strand=-1),
        Location(locus="Rv1149", start=1277893, end=1278300, strand=1),
        Location(locus="Rv1150", start=1278269, end=1278820, strand=1),
        Location(locus="Rv1197", start=1340659, end=1340955, strand=1),
        Location(locus="Rv1198", start=1341006, end=1341290, strand=1),
        Location(locus="Rv1199c", start=1341358, end=1342605, strand=-1),
        Location(locus="Rv1288", start=1441348, end=1442718, strand=1),
        Location(locus="Rv1295", start=1450697, end=1451779, strand=1),
        Location(locus="Rv1313c", start=1468171, end=1469505, strand=-1),
        Location(locus="Rv1318c", start=1479199, end=1480824, strand=-1),
        Location(locus="Rv1319c", start=1480894, end=1482501, strand=-1),
        Location(locus="Rv1369c", start=1541994, end=1542980, strand=-1),
        Location(locus="Rv1370c", start=1542929, end=1543255, strand=-1),
        Location(locus="Rv1458c", start=1643319, end=1644260, strand=-1),
        Location(locus="Rv1489A", start=1678942, end=1679172, strand=1),
        Location(locus="Rv1493", start=1684005, end=1686257, strand=1),
        Location(locus="Rv1557", start=1761744, end=1762937, strand=1),
        Location(locus="Rv1558", start=1762947, end=1763393, strand=1),
        Location(locus="Rv1572c", start=1779194, end=1779298, strand=-1),
        Location(locus="Rv1574", start=1779930, end=1780241, strand=1),
        Location(locus="Rv1575", start=1780199, end=1780699, strand=1),
        Location(locus="Rv1573", start=1779314, end=1779724, strand=1),
        Location(locus="Rv1574", start=1779930, end=1780241, strand=1),
        Location(locus="Rv1575", start=1780199, end=1780699, strand=1),
        Location(locus="Rv1576c", start=1780643, end=1782064, strand=-1),
        Location(locus="Rv1577c", start=1782072, end=1782584, strand=-1),
        Location(locus="Rv1578c", start=1782758, end=1783228, strand=-1),
        Location(locus="Rv1579c", start=1783309, end=1783623, strand=-1),
        Location(locus="Rv1580c", start=1783620, end=1783892, strand=-1),
        Location(locus="Rv1581c", start=1783906, end=1784301, strand=-1),
        Location(locus="Rv1582c", start=1784497, end=1785912, strand=-1),
        Location(locus="Rv1583c", start=1785912, end=1786310, strand=-1),
        Location(locus="Rv1584c", start=1786307, end=1786528, strand=-1),
        Location(locus="Rv1585c", start=1786584, end=1787099, strand=-1),
        Location(locus="Rv1586c", start=1787096, end=1788505, strand=-1),
        Location(locus="Rv1587c", start=1788162, end=1789163, strand=-1),
        Location(locus="Rv1588c", start=1789168, end=1789836, strand=-1),
        Location(locus="Rv1702c", start=1927211, end=1928575, strand=-1),
        Location(locus="Rv1756c", start=1987745, end=1988731, strand=-1),
        Location(locus="Rv1757c", start=1988680, end=1989006, strand=-1),
        Location(locus="Rv1758", start=1989042, end=1989566, strand=1),
        Location(locus="Rv1763", start=1996152, end=1996478, strand=1),
        Location(locus="Rv1764", start=1996427, end=1997413, strand=1),
        Location(locus="Rv1765A", start=1999142, end=1999357, strand=-1),
        Location(locus="Rv1765c", start=1997418, end=1998515, strand=-1),
        Location(locus="Rv1793", start=2030694, end=2030978, strand=1),
        Location(locus="Rv1829", start=2073943, end=2074437, strand=1),
        Location(locus="Rv1910c", start=2156706, end=2157299, strand=-1),
        Location(locus="Rv1911c", start=2157382, end=2157987, strand=-1),
        Location(locus="Rv1945", start=2195989, end=2197353, strand=1),
        Location(locus="Rv2013", start=2260665, end=2261144, strand=1),
        Location(locus="Rv2014", start=2261098, end=2261688, strand=1),
        Location(locus="Rv2015c", start=2261816, end=2263072, strand=-1),
        Location(locus="Rv2048c", start=2294531, end=2306986, strand=-1),
        Location(locus="Rv2082", start=2338709, end=2340874, strand=1),
        Location(locus="Rv2085", start=2343027, end=2343332, strand=1),
        Location(locus="Rv2090", start=2347373, end=2348554, strand=1),
        Location(locus="Rv2105", start=2365465, end=2365791, strand=1),
        Location(locus="Rv2106", start=2365740, end=2366726, strand=1),
        Location(locus="Rv2112c", start=2370905, end=2372569, strand=-1),
        Location(locus="Rv2167c", start=2430159, end=2431145, strand=-1),
        Location(locus="Rv2168c", start=2431094, end=2431420, strand=-1),
        Location(locus="Rv2177c", start=2439282, end=2439947, strand=-1),
        Location(locus="Rv2196", start=2459678, end=2461327, strand=1),
        Location(locus="Rv2258c", start=2530836, end=2531897, strand=-1),
        Location(locus="Rv2277c", start=2549124, end=2550029, strand=-1),
        Location(locus="Rv2278", start=2550065, end=2550391, strand=1),
        Location(locus="Rv2279", start=2550340, end=2551326, strand=1),
        Location(locus="Rv2346c", start=2625888, end=2626172, strand=-1),
        Location(locus="Rv2347c", start=2626223, end=2626519, strand=-1),
        Location(locus="Rv2354", start=2635628, end=2635954, strand=1),
        Location(locus="Rv2355", start=2635903, end=2636889, strand=1),
        Location(locus="Rv2424c", start=2720776, end=2721777, strand=-1),
        Location(locus="Rv2460c", start=2762531, end=2763175, strand=-1),
        Location(locus="Rv2461c", start=2763172, end=2763774, strand=-1),
        Location(locus="Rv2479c", start=2784657, end=2785643, strand=-1),
        Location(locus="Rv2480c", start=2785592, end=2785918, strand=-1),
        Location(locus="Rv2489c", start=2800846, end=2801145, strand=-1),
        Location(locus="Rv2512c", start=2828556, end=2829803, strand=-1),
        Location(locus="Rv2543", start=2866468, end=2867127, strand=1),
        Location(locus="Rv2544", start=2867124, end=2867786, strand=1),
        Location(locus="Rv2648", start=2972160, end=2972486, strand=1),
        Location(locus="Rv2649", start=2972435, end=2973421, strand=1),
        Location(locus="Rv2650c", start=2973795, end=2975234, strand=-1),
        Location(locus="Rv2651c", start=2975242, end=2975775, strand=-1),
        Location(locus="Rv2652c", start=2975928, end=2976554, strand=-1),
        Location(locus="Rv2653c", start=2976586, end=2976909, strand=-1),
        Location(locus="Rv2654c", start=2976989, end=2977234, strand=-1),
        Location(locus="Rv2655c", start=2977231, end=2978658, strand=-1),
        Location(locus="Rv2656c", start=2978660, end=2979052, strand=-1),
        Location(locus="Rv2657c", start=2979049, end=2979309, strand=-1),
        Location(locus="Rv2659c", start=2979691, end=2980818, strand=-1),
        Location(locus="Rv2665", start=2982699, end=2982980, strand=1),
        Location(locus="Rv2666", start=2983071, end=2983874, strand=1),
        Location(locus="Rv2673", start=2989291, end=2990592, strand=1),
        Location(locus="Rv2680", start=2996105, end=2996737, strand=1),
        Location(locus="Rv2689c", start=3005845, end=3007062, strand=-1),
        Location(locus="Rv2690c", start=3007236, end=3009209, strand=-1),
        Location(locus="Rv2774c", start=3082352, end=3082756, strand=-1),
        Location(locus="Rv2791c", start=3100202, end=3101581, strand=-1),
        Location(locus="Rv2792c", start=3101581, end=3102162, strand=-1),
        Location(locus="Rv2805", start=3112867, end=3113271, strand=1),
        Location(locus="Rv2807", start=3113658, end=3114812, strand=1),
        Location(locus="Rv2810c", start=3115741, end=3116142, strand=-1),
        Location(locus="Rv2812", start=3116818, end=3118227, strand=1),
        Location(locus="Rv2814c", start=3120566, end=3121552, strand=-1),
        Location(locus="Rv2815c", start=3121501, end=3121827, strand=-1),
        Location(locus="Rv2825c", start=3132892, end=3133539, strand=-1),
        Location(locus="Rv2828c", start=3135788, end=3136333, strand=-1),
        Location(locus="Rv2859c", start=3170720, end=3171646, strand=-1),
        Location(locus="Rv2882c", start=3191644, end=3192201, strand=-1),
        Location(locus="Rv2885c", start=3194166, end=3195548, strand=-1),
        Location(locus="Rv2886c", start=3195545, end=3196432, strand=-1),
        Location(locus="Rv2931", start=3245445, end=3251075, strand=1),
        Location(locus="Rv2932", start=3251072, end=3255688, strand=1),
        Location(locus="Rv2943", start=3288464, end=3289705, strand=1),
        Location(locus="Rv2943A", start=3289705, end=3290235, strand=1),
        Location(locus="Rv2944", start=3289790, end=3290506, strand=1),
        Location(locus="Rv2961", start=3313283, end=3313672, strand=1),
        Location(locus="Rv2977c", start=3332787, end=3333788, strand=-1),
        Location(locus="Rv2978c", start=3333785, end=3335164, strand=-1),
        Location(locus="Rv2979c", start=3335164, end=3335748, strand=-1),
        Location(locus="Rv2980", start=3335960, end=3336505, strand=1),
        Location(locus="Rv3023c", start=3381375, end=3382622, strand=-1),
        Location(locus="Rv3115", start=3481451, end=3482698, strand=1),
        Location(locus="Rv3184", start=3551281, end=3551607, strand=1),
        Location(locus="Rv3185", start=3551556, end=3552542, strand=1),
        Location(locus="Rv3186", start=3552764, end=3553090, strand=1),
        Location(locus="Rv3187", start=3553039, end=3554025, strand=1),
        Location(locus="Rv3191c", start=3557311, end=3558345, strand=-1),
        Location(locus="Rv3281", start=3663689, end=3664222, strand=1),
        Location(locus="Rv3325", start=3710433, end=3710759, strand=1),
        Location(locus="Rv3326", start=3710708, end=3711694, strand=1),
        Location(locus="Rv3327", start=3711749, end=3713461, strand=1),
        Location(locus="Rv3346c", start=3743198, end=3743455, strand=-1),
        Location(locus="Rv3348", start=3753765, end=3754256, strand=1),
        Location(locus="Rv3349c", start=3754293, end=3755033, strand=-1),
        Location(locus="Rv3355c", start=3769514, end=3769807, strand=-1),
        Location(locus="Rv3380c", start=3795100, end=3796086, strand=-1),
        Location(locus="Rv3381c", start=3796035, end=3796361, strand=-1),
        Location(locus="Rv3386", start=3800092, end=3800796, strand=1),
        Location(locus="Rv3387", start=3800786, end=3801463, strand=1),
        Location(locus="Rv3424c", start=3841714, end=3842076, strand=-1),
        Location(locus="Rv3427c", start=3843885, end=3844640, strand=-1),
        Location(locus="Rv3428c", start=3844738, end=3845970, strand=-1),
        Location(locus="Rv3430c", start=3847642, end=3848805, strand=-1),
        Location(locus="Rv3431c", start=3849294, end=3850139, strand=-1),
        Location(locus="Rv3466", start=3883525, end=3884193, strand=1),
        Location(locus="Rv3467", start=3883964, end=3884917, strand=1),
        Location(locus="Rv3474", start=3890830, end=3891156, strand=1),
        Location(locus="Rv3475", start=3891105, end=3892091, strand=1),
        Location(locus="Rv3513c", start=3945092, end=3945748, strand=-1),
        Location(locus="Rv3515c", start=3950824, end=3952470, strand=-1),
        Location(locus="Rv3611", start=4052950, end=4053603, strand=1),
        Location(locus="Rv3619c", start=4059984, end=4060268, strand=-1),
        Location(locus="Rv3620c", start=4060295, end=4060591, strand=-1),
        Location(locus="Rv3636", start=4075752, end=4076099, strand=1),
        Location(locus="Rv3637", start=4076484, end=4076984, strand=1),
        Location(locus="Rv3638", start=4076984, end=4077730, strand=1),
        Location(locus="Rv3639c", start=4077884, end=4078450, strand=-1),
        Location(locus="Rv3640c", start=4078520, end=4079749, strand=-1),
        Location(locus="Rv3680", start=4119795, end=4120955, strand=1),
        Location(locus="Rv3710", start=4153740, end=4155674, strand=1),
        Location(locus="Rv3798", start=4252993, end=4254327, strand=1),
        Location(locus="Rv3826", start=4299812, end=4301566, strand=1),
        Location(locus="Rv3827c", start=4301563, end=4302789, strand=-1),
        Location(locus="Rv3828c", start=4302786, end=4303397, strand=-1),
        Location(locus="Rv3844", start=4318775, end=4319266, strand=1),
        Location(locus="Rv3876", start=4353010, end=4355010, strand=1),
        Location(locus="IG1195_Rv1174c-Rv1175c", start=1306002, end=1306201, strand=1),
        Location(locus="IG127_Rv0126-Rv0127", start=154130, end=154231, strand=1),
        Location(locus="IG1711_Rv1682-Rv1683", start=1907321, end=1907593, strand=1),
        Location(locus="IG18_Rv0018c-Rv0019c", start=23182, end=23269, strand=1),
        Location(locus="IG3012_Rv2965c-Rv2966c", start=3318816, end=3318900, strand=1),
        Location(locus="IG3013_Rv2966c-Rv2967c", start=3319468, end=3319662, strand=1),
        Location(locus="IG533_Rv0525-Rv0526", start=616832, end=616845, strand=1),
        Location(locus="IG559_Rv0551c-Rv0552", start=642812, end=642888, strand=1),
        Location(locus="IG622_Rv0612-Rv0613c", start=706930, end=706947, strand=1),
        Location(locus="IG71_Rv0071-Rv0072", start=80194, end=80623, strand=1),
        Location(locus="IG784_Rv0769-Rv0770", start=863159, end=863255, strand=1),
        Location(locus="IG877_Rv0861c-Rv0862c", start=960152, end=960341, strand=1),
    ]

    @doc_inherit
    def load_from_web_and_db(self, bolt_url: str):
        response = requests.get(self.url)
        if response.status_code == 200:
            uvp_df = pd.read_csv(StringIO(response.text), delimiter="\t")
            uvp_df_loci_df = uvp_df[
                ~uvp_df.astype(str)["Comment"].str.contains("family protein")
                & ~uvp_df["Comment"].isna()  # noqa: W503
            ]

            graph = GraphDatabase.driver(uri=bolt_url)
            self.regions = RegionList.locus_list_to_locations(
                graph, uvp_df_loci_df, "locus tag"
            )
            graph.close()
 
            # add the intergenic regions
            for i, row in uvp_df[uvp_df["Comment"].isna()].iterrows():
                self.regions.append(
                    Location(row["locus tag"], row["chromStart"], row["chromEnd"], 1)
                )
