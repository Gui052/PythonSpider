import requests
formate = {
	"operationName": "null",
	"variables": "{}",
	"query": "query ($first: Int, $after: String, $last: Int, $before: String) {  oneStatisticHistory {    oneDailyStatistics(first: $first, after: $after, last: $last, before: $before) {      edges {        cursor        node {          ...OneDailyStatistic          __typename        }        __typename      }      pageInfo {        endCursor        startCursor        hasNextPage        hasPreviousPage        __typename      }      __typename    }    __typename  }}fragment OneDailyStatistic on OneDailyStatistic {  revenue100w  oneAvgBtcPrice  platformIncomeBtcAmount  referralMiningBtcAmount  statisticalDate  tradeMiningBtcAmount  unfrozenOneAmount  unlockedOneAmount  totalFee  __typename}"
}
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "content-type":"application/json",
    "accept":"*/*"
                        })


te = session.post('https://b1.run/api/graphql', data=formate).text

print(te)