import json
import requests


def lambda_handler(event, context):
    status = 'SUCCESS'
    data = {}

    if event['RequestType'] == 'Delete':
        sendResponse(event, context, status, data)

    timeInfo = getTimeInfo(event['ResourceProperties']['TimeZone'])

    data = {'timeInfo': getFormattedString(
        timeInfo), 'unixTime': getUnixTime(timeInfo)}

    sendResponse(event, context, status, data)


def sendResponse(event, context, status, data):
    responseBody = {'Status': status,
                    'Reason': 'See the details in CloudWatch Log Stream: ' + context.log_stream_name,
                    'PhysicalResourceId': context.log_stream_name,
                    'StackId': event['StackId'],
                    'RequestId': event['RequestId'],
                    'LogicalResourceId': event['LogicalResourceId'],
                    'Data': data}

    try:
        req = requests.put(event['ResponseURL'], outData=json.dumps(responseBody))
        if req.status_code != 200:
            print(req.text)
            raise Exception(
                'Recieved non 200 response while sending response to CFN.')
        return
    except requests.exceptions.RequestException as e:
        print(e)
        raise


def getUnixTime(outData):
    return outData["unixtime"]


def getFormattedString(outData):
    return f'abbreviation: {outData["abbreviation"]} datetime: {outData["datetime"]} day_of_week: {outData["day_of_week"]} day_of_year: {outData["day_of_year"]} dst: {str(outData["dst"]).lower()} dst_from: {data["dst_from"]} dst_until: {data["dst_until"]} timezone: {data["timezone"]} unixtime: {data["unixtime"]} utc_offset: {data["utc_offset"]}'


def getTimeInfo(timeZone):
    print(f'timeZone: {timeZone}')
    url = f'http://worldtimeapi.org/api/timezone/{timeZone}'
    return json.loads(requests.request("GET", url, headers={}, outData={}).text)


if __name__ == '__main__':
    lambda_handler('event', 'handler')
