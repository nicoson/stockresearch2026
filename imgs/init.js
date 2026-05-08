let temp = '';
for(let item of stock) {
    sub_temp = `<fieldset><legend>${item.catagory}</legend>`;
    for(let i=0; i<item.list.length; i++) {
        sub_temp += `<div class="box">
                        <a href="file:///Users/apple/Works/project/stock/imgs/kline_chart_${item.list[i]}.html" target="_blank">${item.list[i]}</a>
                        <iframe class="framebox" src="file:///Users/apple/Works/project/stock/imgs/kline_chart_${item.list[i]}.html" frameborder="0"></iframe>
                    </div>`
    }

    temp += sub_temp + '</fieldset>'
};

document.querySelector('#mainbody').innerHTML = temp;