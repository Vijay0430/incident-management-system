def send_alert(severity, component_id):

    if severity == "P0":

        print(
            f"EMAIL ALERT: Critical issue in {component_id}"
        )

    elif severity == "P1":

        print(
            f"SLACK ALERT: Warning in {component_id}"
        )

    else:

        print(
            f"LOG ALERT: Minor issue in {component_id}"
        )
