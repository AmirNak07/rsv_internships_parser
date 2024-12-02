import json


def extract_internship_data(json_data, regions, all_skils):
    data = json.loads(json_data)

    result = []
    for i in range(len(data["data"])):
        try:
            payment_amount = data["data"][i]["paymentAmount"]
        except KeyError:
            payment_amount = "-"

        try:
            skils = ", ".join(map(lambda x: all_skils[x], data["data"][i]["skillIds"]))
        except KeyError:
            skils = "-"

        result.append([
            # Title
            data["data"][i]["name"],
            # Institute Name
            data["data"][i]["instituteName"],
            # Region
            ", ".join(map(lambda x: regions[x], data["data"][i]["region_ids"])),
            # Industry Name
            data["data"][i]["industryName"],
            # Skills
            skils,
            # Duration
            data["data"][i]["duration"],
            # Work Format
            data["data"][i]["participationFormatName"],
            # Payment Amount
            payment_amount
        ])
    return result
