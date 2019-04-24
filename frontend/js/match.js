var url_string = window.location.href
var url = new URL(url_string);

var process = url.searchParams.get("process");
var url1 = url.searchParams.get("url1");
var url2 = url.searchParams.get("url2");
var min_match_count = url.searchParams.get("min_match_count");
var sensibility = url.searchParams.get("sensibility");
var min_percent_match = url.searchParams.get("min_percent_match");

var input_process = document.getElementById("process")
input_process.value = process;

var input_url1 = document.getElementById("url1")
input_url1.value = url1;

var input_url2 = document.getElementById("url2")
input_url2.value = url2;

var input_min_match_count = document.getElementById("min-match-count")
input_min_match_count.value = min_match_count;

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
    urlMmatch += `&sensibility=${input_sensibility.value/100}`
    urlMmatch += `&min_percent_match=${input_min_percent_match.value}`


    // fetch(conf.urlBackend+'match?' + Math.random() + '=' + Math.random() + "&" + urlMmatch)
    fetch(conf.urlBackend+input_process.value+'?' + Math.random() + '=' + Math.random() + "&" + urlMmatch)
        .then((response) => response.json())
        .then((result) => {
            console.log(result)
            imgMatch.src = result+'?' + Math.random() + '=' + Math.random();
        }

        )

});

var firstTimeMatch  = () =>{
    submit.click()
}