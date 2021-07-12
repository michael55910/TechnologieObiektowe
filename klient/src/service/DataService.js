import http from './api-config'

class DataService {
    getCandles(symbol, interval, isReal = true, pageSize, page) {
        return http.get("candles", {
            params: {
                symbol: symbol,
                interval: interval,
                is_real: this.boolParam(isReal),
                page_size: pageSize,
                page: page
            }
        })
    }

    getAllPairs(status = undefined) {
        return http.get("pairs", {
            params: {
                status: status
            }
        })
    }

    getIntervals() {
        return http.get("intervals")
    }

    getPredictionMethods() {
        return http.get("predictionmethods")
    }

    trainModel(symbol, interval, predictionMethod, windowSize, predictionSize) {
        return http.post("learn", {
            symbol: symbol,
            interval: interval,
            predictionMethod: predictionMethod,
            windowSize: windowSize * 1,
            predictionSize: predictionSize * 1
        }, /*Object.assign({}, http.defaults, {withCredentials: true})*/ {withCredentials: true})
    }

    getPredictionModels(symbol = undefined, interval = undefined) {
        return http.get("predictionmodels", {
            params: {
                symbol: symbol,
                interval: interval,
            }
        })
    }

    getLineValues(symbol, interval, isReal = true, pageSize, page) {
        return http.get("line", {
            params: {
                symbol: symbol,
                interval: interval,
                is_real: this.boolParam(isReal),
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