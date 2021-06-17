import http from './api-config'

class DataService {
    getCandles(symbol, interval, isReal = true, predictionType, pageSize, page) {
        return http.get("candles", {
            params: {
                symbol: symbol,
                interval: interval,
                is_real: this.boolParam(isReal),
                prediction_type: predictionType,
                page_size: pageSize,
                page: page
            }
        })
    }

    boolParam(val) {
        return val ? 'True' : 'False'
    }
}

export default new DataService();