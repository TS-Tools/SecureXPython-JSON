"""
Crunches the Data from the SecureX Get in JSON > Output formattin - Tim Snow
https://github.com/TS-Tools/SecureXPython-JSON

"""
import json
import jmespath

with open(f"SecureX.json", "r") as read_file:
    res = json.load(read_file)


combined_module_values = []
combined_judgements_values = []
combined_judgements_str_values = []
combined_sightings_values = []
combined_sightings_str_values = []

flatten_list = (
    lambda y: [x for a in y for x in flatten_list(a)] if type(y) is list else [y]
)

for block in res["data"]:
    for key in block:
        if key == "module":
            module = block["module"]
            to_search = block["data"]
            verdicts = []
            judgements = []
            indicators = []
            sightings = []
            for i in to_search:
                if i == "verdicts":
                    # disposition, disposition_name, severity
                    verdicts = jmespath.search(
                        "verdicts.docs[*][disposition, disposition_name, severity]",
                        to_search,
                    )
                elif i == "judgements":
                    # disposition, disposition_name, reason, source, severity, priority, tlp
                    judgements = jmespath.search(
                        "judgements.docs[*][disposition, disposition_name, reason, source, severity, priority, tlp]",
                        to_search,
                    )
                    # print(judgements)

            values = [
                module,
                flatten_list(verdicts),
                flatten_list(judgements),
                flatten_list(indicators),
                flatten_list(sightings),
            ]
            combined_module_values.append(values)

       



out = lambda x, y: x[y] if any(x) is True else ""


def out_j(x, y):

    if y <= len(x) - 1:
        output = x[y]
    else:
        output = ""
    return output


with open(f"output.txt", "a") as f:
    f.write("\nCisco SecureX Lookup\n")
    for i in combined_module_values:

        module_str = f"""
Module : {i[0]}
	Verdicts
		Disposition      => {out(i[1], 0)}
		Disposition Name => {out(i[1], 1)}
		Severity         => {out(i[1], 2)}
    Judgements
		Disposition      => {out(i[2], 0)}
		Disposition Name => {out(i[2], 1)}
		Reason           => {out(i[2], 2)}
		Source           => {out(i[2], 3)}
		Severity         => {out(i[2], 4)}
		Priority         => {out(i[2], 5)}
		TLP              => {out(i[2], 6)}
	Indicators
		Short Description=> {out(i[3], 0)}
		TLP              => {out(i[3], 1)}
	Sightings
		Description      => {out(i[4], 0)}
		Confidence       => {out(i[4], 1)}
        """
        if any(i[1:4]) != False:     #Only show the modules with date, mute the rest
            f.write(module_str)
        #f.write(module_str)

