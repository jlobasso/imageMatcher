var url_string = window.location.href
var url = new URL(url_string);

var url1 = url.searchParams.get("url1");
var url2 = url.searchParams.get("url2");
var min_match_count = url.searchParams.get("min_match_count");
var scale = url.searchParams.get("scale");
var sensibility = url.searchParams.get("sensibility");
var min_percent_match = url.searchParams.get("min_percent_match");

var input_url1 = document.getElementById("url1")
input_url1.value = url1;
var input_url2 = document.getElementById("url2")
input_url2.value = url2;
var input_min_match_count = document.getElementById("min-match-count")
input_min_match_count.value = min_match_count;
var input_scale = document.getElementById("scale")
input_scale.value = scale;
var input_sensibility = document.getElementById("sensibility")
input_sensibility.value = sensibility * 100;
var input_min_percent_match = document.getElementById("min-percent-match")
input_min_percent_match.value = min_percent_match;


const submit = document.getElementById("submit")

var imgMatch = document.getElementById("img-match")

submit.addEventListener("click", async () => {
    
    
    var urlMmatch = `url1=${input_url1.value}`
    urlMmatch += `&url2=${input_url2.value}`
    urlMmatch += `&min_match_count=${input_min_match_count.value}`
    urlMmatch += `&scale=${input_scale.value}`
    urlMmatch += `&sensibility=${input_sensibility.value/100}`
    urlMmatch += `&min_percent_match=${input_min_percent_match.value}`

    fetch('http://localhost:5000/match?' + Math.random() + '=' + Math.random() + "&" + urlMmatch)
        .then((response) => response.json())
        .then((result) => {
            result = result.replace(/\.\.\/frontend/g,"")
            imgMatch.src = 'http://localhost:8080'+result+'?' + Math.random() + '=' + Math.random();
        }

        )

});

var firstTimeMatch  = () =>{
    submit.click()
}