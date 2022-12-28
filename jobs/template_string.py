def make_template_string(data: dict) -> str:
    return f'''
        <!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title></title>
</head>

<body style="background-color: aliceblue; color: #787878;">

    <h2>State name with highest number of success count</h2>
    <table border="2" style="width: 40%;">
        <tr>
            <th><b>State</b></th>
            <th><b>Success count</b></th>
        </tr>

        <tr>
            <th>{data['state-q1']}</th>
            <th>{data['count']}</th>
        </tr>
    </table>

    <br><br>

    <h2>State with highest average amount of transaction for successful transactions</h2>
    <table border="2" style="width: 40%;">
        <tr>
            <th><b>State</b></th>
            <th><b>Average amount</b></th>
        </tr>

        <tr>
            <th>{data['state-q2']}</th>
            <th>{data['average']}</th>
        </tr>
    </table>


</body>

</html>
    '''
