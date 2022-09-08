function post_register_details()
{
    var email = document.getElementById("reg-email").value;
    var password = document.getElementById("reg-password").value;
    var weight = document.getElementById("reg-weight").value;
    var gender = document.getElementById("reg-gender").value;

    $.ajax({
        url: "/register",
        type: "POST",
        data: {
            email: email,
            password: password,
            weight: weight,
            gender: gender
        },
        error: function() {
            alert('Register error');
        },
        success: function(data, status, xhr) {
            var email = data.email;
            var password = data.password;
            var weight = data.weight;
            var gender = data.gender;
            console.log("Email: " + email + "\nPassword: " + password + "\nWeight: " + weight + "\nGender: " + gender);

            document.getElementById("reg-email").value = "";
            document.getElementById("reg-email").focus();
            document.getElementById("reg-password").value = "";
            document.getElementById("reg-weight").value = "";
            document.getElementById("reg-gender").value = "";
        }
    })
}

function post_login_details()
{
    var email = document.getElementById("login-email").value;
    var password = document.getElementById("login-password").value;

    $.ajax({
        url: "/login",
        type: "POST",
        data: {
            email: email,
            password: password
        },
        error: function() {
            alert('Login error');
        },
        success: function(data, status, xhr) {
            var email = data.email;
            var password = data.password;
            console.log("Email: " + email + "\nPassword: " + password);

            document.getElementById("login-email").value = "";
            document.getElementById("login-email").focus();
            document.getElementById("login-password").value = "";
        }
    })
}

if (document.getElementById('login-submit')) {
    document.querySelector("#login-submit").addEventListener("click", post_login_details);
}
if (document.getElementById('reg-submit')) {
    document.querySelector("#reg-submit").addEventListener("click", post_register_details);
}

function calculate_calories() 
{
    var date_time = document.getElementById("log-date-time").value;
    var weight = document.getElementById("log-weight").value;
    var walking_duration = document.getElementById("log-walking").value;
    var running_duration = document.getElementById("log-running").value;
    var swimming_duration = document.getElementById("log-swimming").value;
    var bicycling_duration = document.getElementById("log-bicycling").value;

    $.ajax({
        url: "/log",
        type: "POST",
        data: {
            date_time: date_time,
            weight: weight,
            walking_duration: walking_duration,
            running_duration: running_duration,
            swimming_duration: swimming_duration,
            bicycling_duration: bicycling_duration
        },
        error: function() {
            alert('Log error');
        },
        success: function(data, status, xhr) {
            var total_calories_consumed = data.total_calories_consumed;
            console.log("Total calories: " + total_calories_consumed);

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
    })
}

if (document.getElementById('log-submit')) {
    document.querySelector("#log-submit").addEventListener("click", calculate_calories);
}

function upload_csv() 
{
    var file = document.getElementById('csv-file');

    if (window.FileReader) {
        var reader = new FileReader();
        reader.readAsText(file.files[0]);

        reader.onload = function(e) {
            var csv = event.target.result;
            var text_lines = csv.split(/\r\n|\n/);

            var headers = text_lines[0].split(',');

            for (var i=1; i<text_lines.length; i++) {
                var obj = {};
                var row = text_lines[i].split(',');
                
                for (var j=0; j<row.length; j++) {
                    obj[headers[j]] = row[j];
                }
    
                $.ajax({
                    url: "/upload",
                    type: "POST",
                    data: obj,
                    error: function() {
                        alert('Upload error');
                    },
                    success: function() {
                        $("#csv-file").replaceWith($("#csv-file").val('').clone(true));
                    }
                })
            }
        }

        reader.onerror = function(e) {
            if (event.target.error.name == 'NotReadableError') {
                alert('Cannot read file');
            }
        }

    } else {
        alert('FileReader is not supported in this browser');
    }
}

if (document.getElementById('upload-submit')) {
    document.querySelector("#upload-submit").addEventListener("click", upload_csv);
}