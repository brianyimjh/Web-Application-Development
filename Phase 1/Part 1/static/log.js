function calculate_calories() 
{
    var date_time = document.getElementById("log-date-time").value;
    var weight = document.getElementById("log-weight").value;
    var walking_duration = document.getElementById("log-walking").value;
    var running_duration = document.getElementById("log-running").value;
    var swimming_duration = document.getElementById("log-swimming").value;
    var bicycling_duration = document.getElementById("log-bicycling").value;

    var walking_calorie_consumed = 0.084;
    var running_calorie_consumed = 0.21;
    var swimming_calorie_consumed = 0.13;
    var bicycling_calorie_consumed = 0.064;

    var total_calories_consumed = (walking_calorie_consumed*walking_duration + 
    running_calorie_consumed*running_duration + 
    swimming_calorie_consumed*swimming_duration + 
    bicycling_calorie_consumed*bicycling_duration) *
    weight;

    total_calories_consumed = Math.round(total_calories_consumed*100) / 100;

    var str = document.getElementById("log-output").innerHTML;
    var output_description = str.slice(0, str.indexOf(':')+1);

    document.getElementById("log-output").innerHTML = output_description + ' ' + total_calories_consumed;

    var date_only = date_time.slice(0, date_time.indexOf('T')+1);
    document.getElementById("log-date-time").value = date_only;
    document.getElementById("log-date-time").focus();

    document.getElementById("log-weight").value = "";
    document.getElementById("log-walking").value = "";
    document.getElementById("log-running").value = "";
    document.getElementById("log-swimming").value = "";
    document.getElementById("log-bicycling").value = "";
}

document.querySelector("#log-submit").addEventListener("click", calculate_calories);