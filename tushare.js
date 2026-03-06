let header = new Headers();
header.append('Content-Type', 'application/json');
header.append('x-jwt-token', 'UHo4VTRmSFlldFVsRTA1QTRFM082azJNQkxyeURTNGpjTDEyZWJsb2F0WkJzVUR0TVQrSWZPSDFLUW5wcEtPU2VCaVBVWk0yakFNUlNOSjZaYXZhVlVRLzg4ZEdEZlRpMk5TQno1Nmg3eEJjSWMySGhBTjVCbUxoK2VPdFBFdlROZzNHdVpRbjM0ZkZrYlhOV1BoaTdnPT0=');
let options = {
    method: 'POST',
    headers: header,
    body:{}
}

let url = 'http://api.tushare.pro';
options.body = JSON.stringify({
    "api_name": "daily",
    "token": "bc3439516f386aa5dade311bbd1b0d2c3e1109fa98648bcab1801803",
    "params": {
        "ts_code":"688981.SH",
        // "start_date":"20180901",
        // "end_date":"20251231"
    }
});

var data=[];
fetch(url, options).then(res => res.json()).then(res => {
    data = res;
    console.log(data);
})